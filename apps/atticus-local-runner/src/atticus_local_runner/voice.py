"""Explicitly activated local voice session (DRL-013).

Capture begins only after an explicit arm/push-to-talk action. Processing is
local by default, raw audio is not retained unless requested, turns are
deletable, and offline mode never opens a network path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from drl_ai_core import canonical_digest, redact_text


class CaptureState(StrEnum):
    """Visible capture/processing state for UI and audit."""

    IDLE = "idle"
    ARMED = "armed"
    CAPTURING = "capturing"
    PROCESSING = "processing"
    READY = "ready"


@dataclass(frozen=True, slots=True)
class VoiceTurn:
    """One local voice turn after optional transcription."""

    turn_id: str
    transcript: str | None
    audio_retained: bool
    processed_locally: bool
    offline: bool
    capture_visible: bool
    created_at: datetime
    audio_bytes: int = 0


@dataclass
class LocalVoiceSession:
    """Push-to-talk local voice prototype with deletion and offline defaults."""

    offline: bool = True
    retain_raw_audio: bool = False
    allow_cloud_processing: bool = False
    _state: CaptureState = field(default=CaptureState.IDLE, init=False)
    _buffer: bytearray = field(default_factory=bytearray, init=False)
    _turns: dict[str, VoiceTurn] = field(default_factory=dict, init=False)
    _raw_audio: dict[str, bytes] = field(default_factory=dict, init=False)
    _seq: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if self.allow_cloud_processing and self.offline:
            raise ValueError("offline sessions cannot enable cloud processing")
        if self.allow_cloud_processing:
            raise ValueError(
                "cloud voice processing is out of scope for the local-default prototype"
            )

    @property
    def capture_state(self) -> CaptureState:
        return self._state

    @property
    def capture_visible(self) -> bool:
        return self._state in {
            CaptureState.ARMED,
            CaptureState.CAPTURING,
            CaptureState.PROCESSING,
        }

    def arm(self) -> None:
        """Explicit user activation (push-to-talk arming)."""

        if self._state not in {CaptureState.IDLE, CaptureState.READY}:
            raise RuntimeError(f"cannot arm from state {self._state.value}")
        self._state = CaptureState.ARMED

    def start_capture(self) -> None:
        if self._state is not CaptureState.ARMED:
            raise PermissionError("voice capture requires explicit activation")
        self._buffer.clear()
        self._state = CaptureState.CAPTURING

    def ingest_pcm_fixture(self, pcm: bytes) -> None:
        """Ingest synthetic PCM for tests; never opens a microphone device."""

        if self._state is not CaptureState.CAPTURING:
            raise RuntimeError("ingest requires an active capture")
        if not pcm:
            raise ValueError("empty audio frame")
        self._buffer.extend(pcm)

    def stop_and_transcribe(self, *, now: datetime | None = None) -> VoiceTurn:
        if self._state is not CaptureState.CAPTURING:
            raise RuntimeError("stop_and_transcribe requires active capture")
        self._state = CaptureState.PROCESSING
        pcm = bytes(self._buffer)
        self._buffer.clear()
        # Deterministic local mock STT; never leaves the process.
        transcript = redact_text(f"local-transcript:{len(pcm)}:{canonical_digest(pcm)[:12]}")
        self._seq += 1
        turn_id = f"voice-turn-{self._seq:04d}"
        stamped = now or datetime.now(UTC)
        retained = bool(self.retain_raw_audio)
        if retained:
            self._raw_audio[turn_id] = pcm
        turn = VoiceTurn(
            turn_id=turn_id,
            transcript=transcript,
            audio_retained=retained,
            processed_locally=True,
            offline=self.offline,
            capture_visible=True,
            created_at=stamped,
            audio_bytes=len(pcm),
        )
        self._turns[turn_id] = turn
        self._state = CaptureState.READY
        return turn

    def delete_turn(self, turn_id: str) -> None:
        if turn_id not in self._turns:
            raise KeyError(f"unknown turn {turn_id!r}")
        del self._turns[turn_id]
        self._raw_audio.pop(turn_id, None)
        if not self._turns and self._state is CaptureState.READY:
            self._state = CaptureState.IDLE

    def delete_all(self) -> None:
        self._turns.clear()
        self._raw_audio.clear()
        self._buffer.clear()
        self._state = CaptureState.IDLE

    def list_turns(self) -> list[VoiceTurn]:
        return [self._turns[key] for key in sorted(self._turns)]

    def raw_audio_for(self, turn_id: str) -> bytes | None:
        return self._raw_audio.get(turn_id)

    def status(self) -> dict[str, Any]:
        return {
            "capture_state": self._state.value,
            "capture_visible": self.capture_visible,
            "offline": self.offline,
            "retain_raw_audio": self.retain_raw_audio,
            "turn_count": len(self._turns),
            "buffered_bytes": len(self._buffer),
        }
