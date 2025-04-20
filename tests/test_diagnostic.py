import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
import base64
from diagnostic_server import DiagnosticServer

# Dummy image and mask data for testing
dummy_image = "dummy-ultrasound-image-data"
dummy_mask = "dummy-mask-data"
target_organ = "liver"

async def test_diagnostic():
    server = DiagnosticServer()
    request = {
        "image": dummy_image,
        "mask": dummy_mask,
        "target_organ": target_organ
    }
    response = await server.assess(request)
    print("Diagnostic response:", response)
    assert "diagnosis" in response
    assert isinstance(response["diagnosis"], str)
    assert target_organ in response["landmarks"]

if __name__ == "__main__":
    asyncio.run(test_diagnostic())
