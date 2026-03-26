from __future__ import annotations

import logging
import threading
from dataclasses import dataclass
from typing import Optional

from app.inference.live_engine import LiveDrowsinessEngine

ENGINE = LiveDrowsinessEngine(fps=5.0)
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(name)s: %(message)s")
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class RuntimeSnapshot:
    status: str
    alert: str
    report: str
    debug_text: str
    reason: str
    frame_received: bool
    frame_index: int
    students: list[dict]
    overlay_data_url: str
    running: bool


class LiveInferenceRuntime:
    """
    프론트의 프레임 제출과 백엔드 추론을 분리하는 런타임.

    - 브라우저는 최신 frame만 제출합니다.
    - 백엔드 worker thread가 최신 pending frame 하나만 가져가 추론합니다.
    - 프론트 요청은 추론 완료를 기다리지 않고 즉시 최신 snapshot을 반환합니다.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._running = False
        self._shutdown = False
        self._pending_frame: Optional[str] = None
        self._submitted_frames = 0
        self._processed_frames = 0
        self._replaced_frames = 0

        self._last_snapshot = RuntimeSnapshot(
            status="NORMAL",
            alert="카메라가 꺼져 있습니다.",
            report="Start 버튼을 눌러 데모를 시작하세요.",
            debug_text="running=False frame_received=False",
            reason="idle",
            frame_received=False,
            frame_index=0,
            students=[],
            overlay_data_url="",
            running=False,
        )

        self._worker = threading.Thread(
            target=self._worker_loop,
            name="live-inference-worker",
            daemon=True,
        )
        self._worker.start()

    def start(self) -> RuntimeSnapshot:
        with self._condition:
            LOGGER.info("Live inference started")
            ENGINE.reset()
            self._running = True
            self._pending_frame = None
            self._submitted_frames = 0
            self._processed_frames = 0
            self._replaced_frames = 0
            self._last_snapshot = RuntimeSnapshot(
                status="NORMAL",
                alert="실시간 분석을 시작했습니다.",
                report="카메라가 시작되었습니다.\n첫 프레임을 기다리는 중입니다.",
                debug_text="running=True frame_received=False reason=waiting_first_frame",
                reason="waiting_first_frame",
                frame_received=False,
                frame_index=0,
                students=[],
                overlay_data_url="",
                running=True,
            )
            self._condition.notify_all()
            return self._last_snapshot

    def stop(self) -> RuntimeSnapshot:
        with self._condition:
            LOGGER.info("Live inference stopped after %s processed frames", self._processed_frames)
            self._running = False
            self._pending_frame = None
            self._last_snapshot = RuntimeSnapshot(
                status=self._last_snapshot.status,
                alert="카메라가 중지되었습니다.",
                report=self._last_snapshot.report,
                debug_text=(
                    f"running=False frame_received={self._last_snapshot.frame_received} "
                    f"last_reason={self._last_snapshot.reason} frame_index={self._last_snapshot.frame_index} "
                    f"submitted={self._submitted_frames} processed={self._processed_frames} "
                    f"replaced={self._replaced_frames}"
                ),
                reason=self._last_snapshot.reason,
                frame_received=self._last_snapshot.frame_received,
                frame_index=self._last_snapshot.frame_index,
                students=self._last_snapshot.students,
                overlay_data_url=self._last_snapshot.overlay_data_url,
                running=False,
            )
            self._condition.notify_all()
            return self._last_snapshot

    def snapshot(self) -> RuntimeSnapshot:
        with self._lock:
            return self._last_snapshot

    def process_frame(self, data_url: str) -> RuntimeSnapshot:
        """
        프론트 요청은 최신 frame만 제출하고 곧바로 snapshot을 돌려줍니다.

        추론 자체는 worker thread가 비동기로 처리합니다.
        """
        with self._condition:
            if not self._running:
                return self._last_snapshot

            if data_url:
                self._submitted_frames += 1
                if self._pending_frame:
                    self._replaced_frames += 1
                self._pending_frame = data_url
                self._condition.notify()

            return self._decorate_snapshot_locked(self._last_snapshot)

    def _worker_loop(self) -> None:
        while True:
            with self._condition:
                while not self._shutdown and (not self._running or not self._pending_frame):
                    self._condition.wait()

                if self._shutdown:
                    return

                data_url = self._pending_frame
                self._pending_frame = None

            try:
                result = ENGINE.analyze_data_url(data_url)
                debug_text = (
                    f"frame_received={result.frame_received} "
                    f"frame_index={result.frame_index} "
                    f"reason={result.reason} "
                    f"{result.debug_text}"
                )
                with self._condition:
                    self._processed_frames += 1
                    self._last_snapshot = RuntimeSnapshot(
                        status=result.status,
                        alert=result.alert,
                        report=result.report,
                        debug_text=debug_text,
                        reason=result.reason,
                        frame_received=result.frame_received,
                        frame_index=result.frame_index,
                        students=result.students,
                        overlay_data_url=result.overlay_data_url,
                        running=self._running,
                    )
            except Exception:
                LOGGER.exception("Live inference failed in worker")
                with self._condition:
                    self._last_snapshot = RuntimeSnapshot(
                        status="NORMAL",
                        alert="추론 중 오류가 발생했습니다.",
                        report=self._last_snapshot.report,
                        debug_text="runtime_error=check_python_logs",
                        reason="runtime_error",
                        frame_received=bool(data_url),
                        frame_index=ENGINE.frame_count,
                        students=self._last_snapshot.students,
                        overlay_data_url=self._last_snapshot.overlay_data_url,
                        running=self._running,
                    )

    def _decorate_snapshot_locked(self, snapshot: RuntimeSnapshot) -> RuntimeSnapshot:
        queue_debug = (
            f"{snapshot.debug_text}\n"
            f"submitted={self._submitted_frames} "
            f"processed={self._processed_frames} "
            f"replaced={self._replaced_frames} "
            f"pending={1 if self._pending_frame else 0}"
        )
        return RuntimeSnapshot(
            status=snapshot.status,
            alert=snapshot.alert,
            report=snapshot.report,
            debug_text=queue_debug,
            reason=snapshot.reason,
            frame_received=snapshot.frame_received,
            frame_index=snapshot.frame_index,
            students=snapshot.students,
            overlay_data_url=snapshot.overlay_data_url,
            running=snapshot.running,
        )


RUNTIME = LiveInferenceRuntime()
