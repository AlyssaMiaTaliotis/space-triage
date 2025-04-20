import os
import sys
import asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from voice_tts_server import VoiceTTSServer

async def test_direct_tts():
    server = VoiceTTSServer()
    # Directly call the speak method without MCP
    text = "This is a direct test of the voice TTS server without MCP."
    result = await server.speak({"text": text})
    if "audio" in result:
        out_path = os.path.join(os.path.dirname(__file__), "output_tts_direct.mp3")
        with open(out_path, "wb") as f:
            f.write(result["audio"])
        print(f"Audio saved to {out_path}")
    else:
        print(f"TTS error: {result}")

if __name__ == "__main__":
    asyncio.run(test_direct_tts())
