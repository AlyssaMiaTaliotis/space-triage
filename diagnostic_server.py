"""
Dummy diagnostic agent. Accepts `{image, mask}` and always returns:
{diagnosis: "No abnormal findings",
 image_quality: 0.72,
 landmarks: ["liver", "kidney"]}
"""
import asyncio
import logging
import os
from typing import Dict
import anthropic
from dotenv import load_dotenv
from prompts import create_health_assessment_prompt

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiagnosticServer:
    def __init__(self):
        self.default_response = {
            "diagnosis": "No abnormal findings",
            "image_quality": 0.72,
            "landmarks": ["liver", "kidney"]
        }
        self.app = App()

    async def assess(self, request: Dict) -> Dict:
        """Process image and mask, return diagnostic information."""
        logger.info("Processing diagnostic request")
        
        # Verify input contains required fields
        if not all(k in request for k in ["image", "mask", "target_organ"]):
            raise ValueError("Request must include 'image', 'mask', and 'target_organ'")

        # Extract fields
        image = request["image"]
        mask = request["mask"]
        target_organ = request["target_organ"]

        # Compose prompt for Claude
        prompt = create_health_assessment_prompt(target_organ, image)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set in your environment or .env file!")
        client = anthropic.AsyncAnthropic(api_key=api_key)
        try:
            response = await client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=128,
                messages=[{"role": "user", "content": prompt}]
            )
            assessment = response.content
            if isinstance(assessment, list):
                assessment = " ".join([c["text"] if isinstance(c, dict) and "text" in c else str(c) for c in assessment])
        except Exception as e:
            logger.error(f"Error in Claude API call: {str(e)}")
            assessment = "Unable to complete health assessment at this time."

        # Dummy image quality and landmarks for now
        return {
            "diagnosis": assessment,
            "image_quality": 0.72,
            "landmarks": [target_organ]
        }

    def run(self):
        """Start the MCP server."""
        self.app.register_request("assess", self.assess)
        self.app.run(
            os.sys.stdin.buffer,
            os.sys.stdout.buffer,
            self.app.create_initialization_options()
        )

if __name__ == "__main__":
    from mcp_local import App
    server = DiagnosticServer()
    server.run()
