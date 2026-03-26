from __future__ import annotations

import logging
import threading
from dataclasses import dataclass, field
from typing import Optional

from app.config import YOLO_CHECKPOINT_PATH
from app.inference.device import get_device_summary
from app.inference.live_engine import LiveInferenceResult, LiveZoomEngine, SlotInfo

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
    running: bool
    slots: list[SlotInfo] = field(default_factory=list)


class LiveInferenceRuntime:
    def __init__(self):
        self._lock = threading.Lock()
        self._running = False
        self._engine: Optional[LiveZoomEngine] = None
        self._last_snapshot = RuntimeSnapshot(
            status="NORMAL",
            alert="카메라가 꺼져 있습니다.",
            report="Start 버튼을 눌러 데모를 시작하세요.",
            debug_text="running=False frame_received=False",
            reason="idle",
            frame_received=False,
            frame_index=0,
            running=False,
            slots=[],
        )

    def _get_engine(self) -> LiveZoomEngine:
        if self._engine is None:
            LOGGER.info("Initializing live engine on %s", get_device_summary())
            self._engine = LiveZoomEngine(checkpoint_path=YOLO_CHECKPOINT_PATH, fps=5.0)
        return self._engine

    def start(self) -> RuntimeSnapshot:
        with self._lock:
            try:
                engine = self._get_engine()
                LOGGER.info("Live inference started on %s", get_device_summary(engine.device))
                engine.reset()
            except FileNotFoundError:
                LOGGER.exception("Checkpoint file not found")
                self._running = False
                self._last_snapshot = RuntimeSnapshot(
                    status="NORMAL",
                    alert="모델 파일을 찾을 수 없습니다.",
                    report=(
                        f"체크포인트 파일이 없습니다.\n"
                        f"확인 경로: {YOLO_CHECKPOINT_PATH}\n"
                        "Windows에서는 프로젝트 루트 기준 상대경로를 그대로 사용하면 됩니다."
                    ),
                    debug_text=f"startup_error=missing_checkpoint path={YOLO_CHECKPOINT_PATH}",
                    reason="startup_error",
                    frame_received=False,
                    frame_index=0,
                    running=False,
                    slots=[],
                )
                return self._last_snapshot
            except Exception as exc:
                LOGGER.exception("Live inference startup failed")
                self._running = False
                self._last_snapshot = RuntimeSnapshot(
                    status="NORMAL",
                    alert="실시간 추론 엔진 시작에 실패했습니다.",
                    report=(
                        "앱 초기화 중 오류가 발생했습니다.\n"
                        "CUDA가 불안정하면 CPU로 다시 시도해 보세요.\n"
                        f"오류 요약: {exc}"
                    ),
                    debug_text=f"startup_error={exc}",
                    reason="startup_error",
                    frame_received=False,
                    frame_index=0,
                    running=False,
                    slots=[],
                )
                return self._last_snapshot

            self._running = True
            self._last_snapshot = RuntimeSnapshot(
                status="NORMAL",
                alert=f"실시간 분석을 시작했습니다. 현재 device: {get_device_summary(engine.device)}",
                report="카메라가 시작되었습니다.\n첫 프레임을 기다리는 중입니다.",
                debug_text=(
                    "running=True frame_received=False "
                    f"reason=waiting_first_frame device={engine.device}"
                ),
                reason="waiting_first_frame",
                frame_received=False,
                frame_index=0,
                running=True,
                slots=[],
            )
            return self._last_snapshot

    def stop(self) -> RuntimeSnapshot:
        with self._lock:
            frame_count = self._engine.frame_count if self._engine is not None else 0
            LOGGER.info("Live inference stopped after %s frames", frame_count)
            self._running = False
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
                engine = self._get_engine()
                result: LiveInferenceResult = engine.analyze_data_url(data_url)
                debug_text = (
                    f"frame_received={result.frame_received} "
                    f"frame_index={result.frame_index} "
                    f"device={engine.device} "
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
                    slots=result.slots,
                )
                return self._last_snapshot, result.annotated_frame
            except Exception as exc:
                LOGGER.exception("Live inference failed")
                self._last_snapshot = RuntimeSnapshot(
                    status="NORMAL",
                    alert="추론 중 오류가 발생했습니다. CPU fallback 또는 CUDA 설정을 확인해 주세요.",
                    report=(
                        f"{self._last_snapshot.report}\n"
                        "Windows 사용자는 `python check_cuda.py`로 CUDA 인식 상태를 먼저 확인해 보세요."
                    ),
                    debug_text=f"runtime_error={exc}",
                    reason="runtime_error",
                    frame_received=bool(data_url),
                    frame_index=self._engine.frame_count if self._engine is not None else 0,
                    running=True,
                    slots=[],
                )
                return self._last_snapshot, None


RUNTIME = LiveInferenceRuntime()
