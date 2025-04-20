import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from mcp import Client

async def test_tts():
    tts_client = Client("voice-tts")
    text = "Hello astronaut, your scan is complete. Please proceed to the next step."
    result = await tts_client.request("speak", {"text": text})
    if "audio" in result:
        with open("tests/output_tts.mp3", "wb") as f:
            f.write(result["audio"])
        print("TTS audio saved to tests/output_tts.mp3")
    else:
        print(f"TTS error: {result}")

if __name__ == "__main__":
    asyncio.run(test_tts())
