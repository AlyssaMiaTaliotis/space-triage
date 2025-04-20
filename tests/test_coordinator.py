"""Tests for the coordinator."""
import asyncio
import pytest
from unittest.mock import patch, MagicMock

from coordinator import Coordinator

@pytest.mark.asyncio
async def test_coordinator_loop():
    """Test two iterations of the coordinator loop with mocked TTS."""
    coordinator = Coordinator()
    
    # Mock the TTS client to avoid actual speech synthesis
    coordinator.tts_client.request = MagicMock()
    coordinator.tts_client.request.return_value = asyncio.Future()
    coordinator.tts_client.request.return_value.set_result({})
    
    # Run two iterations
    iterations = 0
    
    async def mock_run():
        nonlocal iterations
        while iterations < 2:
            await coordinator.process_frame()
            iterations += 1
    
    try:
        await asyncio.wait_for(mock_run(), timeout=5)
    except asyncio.TimeoutError:
        pytest.fail("Coordinator failed to complete two iterations")
