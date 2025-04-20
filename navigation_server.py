"""
Navigation Agent MCP server for ultrasound guidance.
Given an ultrasound image and target organ, determines if the organ is present.
If not, uses Claude LLM to generate step-by-step navigation instructions.
"""
import os
from dotenv import load_dotenv
load_dotenv()

import asyncio
import base64
import logging
import sys
from typing import Dict

from mcp_local import App
from PIL import Image
import io
import httpx
import anthropic

# Import classification logic and prompt engineering
sys.path.append(os.path.join(os.path.dirname(__file__), 'sam'))
from classification import identify_entity_in_image
from prompts import create_navigation_prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Real Claude API call using Anthropic SDK
async def call_claude_llm(prompt: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set in your environment or .env file!")
    client = anthropic.AsyncAnthropic(api_key=api_key)
    response = await client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=128,
        messages=[{"role": "user", "content": prompt}]
    )
    # The SDK returns message.content as a list of dicts, join if needed
    if isinstance(response.content, list):
        return " ".join([c["text"] if isinstance(c, dict) and "text" in c else str(c) for c in response.content])
    return str(response.content)

class NavigationServer:
    def __init__(self):
        self.app = App("navigation")

    async def navigate(self, request: Dict) -> Dict:
        """
        Given a base64 image and target organ, determines if the organ is present.
        If not, generates navigation instructions using Claude.
        """
        image_b64 = request.get("image")
        target_organ = request.get("target_organ")
        if not image_b64 or not target_organ:
            return {"error": "Missing image or target_organ in request."}
        # Decode image
        image_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        # Use classification logic
        found = identify_entity_in_image(image, target_organ)
        if found:
            return {
                "found": True,
                "message": f"The {target_organ} is visible in the scan. Proceed with evaluation."
            }
        # If not found, generate navigation instructions
        navigation_prompt = create_navigation_prompt(target_organ)
        instructions = await call_claude_llm(navigation_prompt)
        return {
            "found": False,
            "message": instructions
        }

    def run(self):
        self.app.register_request("navigate", self.navigate)
        self.app.run(
            os.sys.stdin.buffer,
            os.sys.stdout.buffer,
            self.app.create_initialization_options()
        )

if __name__ == "__main__":
    server = NavigationServer()
    server.run()
