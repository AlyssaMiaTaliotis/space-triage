"""
Thin wrapper that starts the official elevenlabs-mcp server as a subprocess
so that it looks like a local MCP server named 'voice-tts'.
"""
import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
from mcp_local import App
try:
    from elevenlabs import generate, save, set_api_key
except ImportError:
    generate = save = set_api_key = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class VoiceTTSServer:
    def __init__(self):
        self.app = App("voice-tts")
        self.api_key = os.environ.get("ELEVEN_API_KEY")
        if not self.api_key:
            logger.error("ELEVEN_API_KEY environment variable not set")
            raise RuntimeError("ELEVEN_API_KEY not set")
        if set_api_key:
            set_api_key(self.api_key)

    async def speak(self, request):
        """Request: {"text": str}. Returns: {"audio": bytes (mp3)}"""
        text = request.get("text")
        if not text:
            return {"error": "No text provided"}
        logger.info(f"Synthesizing speech for: {text[:100]}")
        if generate is None:
            return {"error": "elevenlabs package not installed"}
        try:
            audio = generate(text=text, voice="Adam", model="eleven_multilingual_v2")
            # audio is bytes (mp3)
            return {"audio": audio}
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return {"error": str(e)}

    def run(self):
        self.app.register_request("speak", self.speak)
        self.app.run(
            os.sys.stdin.buffer,
            os.sys.stdout.buffer,
            self.app.create_initialization_options()
        )

if __name__ == "__main__":
    server = VoiceTTSServer()
    server.run()
