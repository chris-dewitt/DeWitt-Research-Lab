"""Tests for explicitly activated local voice (DRL-013)."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from atticus_local_runner import CaptureState, LocalVoiceSession


def test_capture_requires_explicit_activation_and_is_visible() -> None:
    session = LocalVoiceSession(offline=True)
    assert session.capture_state is CaptureState.IDLE
    assert session.capture_visible is False
    with pytest.raises(PermissionError, match="explicit activation"):
        session.start_capture()
    session.arm()
    assert session.capture_state is CaptureState.ARMED
    assert session.capture_visible is True
    session.start_capture()
    assert session.capture_state is CaptureState.CAPTURING
    assert session.status()["capture_visible"] is True


def test_local_default_processing_and_offline_behavior() -> None:
    session = LocalVoiceSession(offline=True, retain_raw_audio=False)
    session.arm()
    session.start_capture()
    session.ingest_pcm_fixture(b"\x00\x01\x02\x03")
    turn = session.stop_and_transcribe(now=datetime(2026, 7, 29, tzinfo=UTC))
    assert turn.processed_locally is True
    assert turn.offline is True
    assert turn.audio_retained is False
    assert session.raw_audio_for(turn.turn_id) is None
    assert turn.transcript is not None
    assert turn.transcript.startswith("local-transcript:")


def test_voice_turn_deletion() -> None:
    session = LocalVoiceSession(retain_raw_audio=True)
    session.arm()
    session.start_capture()
    session.ingest_pcm_fixture(b"abcd")
    turn = session.stop_and_transcribe()
    assert session.raw_audio_for(turn.turn_id) == b"abcd"
    session.delete_turn(turn.turn_id)
    assert session.list_turns() == []
    assert session.raw_audio_for(turn.turn_id) is None
    assert session.capture_state is CaptureState.IDLE


def test_delete_all_clears_buffer_and_state() -> None:
    session = LocalVoiceSession()
    session.arm()
    session.start_capture()
    session.ingest_pcm_fixture(b"xyz")
    session.stop_and_transcribe()
    session.delete_all()
    assert session.list_turns() == []
    assert session.status()["buffered_bytes"] == 0
    assert session.capture_state is CaptureState.IDLE


def test_cloud_processing_rejected_for_local_prototype() -> None:
    with pytest.raises(ValueError, match="cloud voice processing"):
        LocalVoiceSession(offline=False, allow_cloud_processing=True)
    with pytest.raises(ValueError, match="offline sessions cannot enable cloud"):
        LocalVoiceSession(offline=True, allow_cloud_processing=True)
