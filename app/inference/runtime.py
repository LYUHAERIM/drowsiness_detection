from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Optional

from app.config import YOLO_CHECKPOINT_PATH
from app.inference.live_engine import LiveInferenceResult, LiveZoomEngine, SlotInfo

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(name)s: %(message)s")
LOGGER = logging.getLogger(__name__)

ENGINE = LiveZoomEngine(checkpoint_path=YOLO_CHECKPOINT_PATH, fps=5.0)
WARMUP_SECONDS = 2.0


@dataclass(frozen=True)
class RuntimeSnapshot:
    status: str
    alert: str
    report: str
    debug_text: str
    reason: str
    frame_received: bool
    frame_index: int
    running: bool
    is_warming_up: bool = False
    warmup_until: float = 0.0
    pipeline_ready: bool = False
    slots: list[SlotInfo] = field(default_factory=list)


class LiveInferenceRuntime:
    def __init__(self):
        self._lock = threading.Lock()
        self._running = False
        self._last_snapshot = RuntimeSnapshot(
            status="NORMAL",
            alert="카메라가 꺼져 있습니다.",
            report="Start 버튼을 눌러 데모를 시작하세요.",
            debug_text="running=False frame_received=False",
            reason="idle",
            frame_received=False,
            frame_index=0,
            running=False,
            is_warming_up=False,
            warmup_until=0.0,
            pipeline_ready=False,
            slots=[],
        )
        self._warmup_until = 0.0

    def _build_warmup_snapshot(
        self, result: LiveInferenceResult, *, frame_received: bool
    ) -> RuntimeSnapshot:
        remaining = max(0.0, self._warmup_until - time.time())
        debug_text = (
            f"warmup=True remaining={remaining:.2f}s "
            f"frame_received={frame_received} frame_index={result.frame_index} "
            f"{result.debug_text}"
        )
        return RuntimeSnapshot(
            status="INIT",
            alert="",
            report="",
            debug_text=debug_text,
            reason="warmup",
            frame_received=frame_received,
            frame_index=result.frame_index,
            running=True,
            is_warming_up=True,
            warmup_until=self._warmup_until,
            pipeline_ready=False,
            slots=[],
        )

    def start(self) -> RuntimeSnapshot:
        with self._lock:
            LOGGER.info("Live inference started")
            ENGINE.reset()
            self._running = True
            self._warmup_until = time.time() + WARMUP_SECONDS
            self._last_snapshot = RuntimeSnapshot(
                status="INIT",
                alert="",
                report="",
                debug_text=(
                    "running=True frame_received=False reason=warmup "
                    f"warmup_until={self._warmup_until:.3f}"
                ),
                reason="warmup",
                frame_received=False,
                frame_index=0,
                running=True,
                is_warming_up=True,
                warmup_until=self._warmup_until,
                pipeline_ready=False,
                slots=[],
            )
            return self._last_snapshot

    def stop(self) -> RuntimeSnapshot:
        with self._lock:
            LOGGER.info("Live inference stopped after %s frames", ENGINE.frame_count)
            self._running = False
            self._warmup_until = 0.0
            self._last_snapshot = RuntimeSnapshot(
                status=self._last_snapshot.status,
                alert="카메라가 중지되었습니다.",
                report=self._last_snapshot.report,
                debug_text=(
                    f"running=False frame_received={self._last_snapshot.frame_received} "
                    f"last_reason={self._last_snapshot.reason} frame_index={self._last_snapshot.frame_index}"
                ),
                reason=self._last_snapshot.reason,
                frame_received=self._last_snapshot.frame_received,
                frame_index=self._last_snapshot.frame_index,
                running=False,
                is_warming_up=False,
                warmup_until=0.0,
                pipeline_ready=False,
                slots=self._last_snapshot.slots,
            )
            return self._last_snapshot

    def snapshot(self) -> RuntimeSnapshot:
        with self._lock:
            return self._last_snapshot

    def process_frame(self, data_url: str) -> tuple[RuntimeSnapshot, Optional[object]]:
        """
        Returns:
            (snapshot, annotated_frame_bgr)
            annotated_frame_bgr: np.ndarray or None
        """
        with self._lock:
            if not self._running:
                return self._last_snapshot, None

            try:
                is_warming_up = time.time() < self._warmup_until
                result: LiveInferenceResult = ENGINE.analyze_data_url(
                    data_url,
                    warming_up=is_warming_up,
                )
                if is_warming_up:
                    self._last_snapshot = self._build_warmup_snapshot(
                        result,
                        frame_received=result.frame_received,
                    )
                    return self._last_snapshot, result.annotated_frame

                debug_text = (
                    f"frame_received={result.frame_received} "
                    f"frame_index={result.frame_index} "
                    f"{result.debug_text}"
                )
                self._last_snapshot = RuntimeSnapshot(
                    status=result.status,
                    alert=result.alert,
                    report=result.report,
                    debug_text=debug_text,
                    reason="live",
                    frame_received=result.frame_received,
                    frame_index=result.frame_index,
                    running=True,
                    is_warming_up=False,
                    warmup_until=self._warmup_until,
                    pipeline_ready=True,
                    slots=result.slots,
                )
                return self._last_snapshot, result.annotated_frame
            except Exception:
                LOGGER.exception("Live inference failed")
                self._last_snapshot = RuntimeSnapshot(
                    status="NORMAL",
                    alert="추론 중 오류가 발생했습니다.",
                    report=self._last_snapshot.report,
                    debug_text="runtime_error=check_python_logs",
                    reason="runtime_error",
                    frame_received=bool(data_url),
                    frame_index=ENGINE.frame_count,
                    running=True,
                    is_warming_up=False,
                    warmup_until=self._warmup_until,
                    pipeline_ready=False,
                    slots=[],
                )
                return self._last_snapshot, None


RUNTIME = LiveInferenceRuntime()
