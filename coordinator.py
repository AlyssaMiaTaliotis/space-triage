"""
Coordinator that orchestrates the ultrasound triage workflow.
Connects to all MCP servers and coordinates the processing pipeline.
"""
import asyncio
import logging
from typing import Dict

from mcp import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Coordinator:
    def __init__(self):
        self.ingest_client = Client("ultrasound-ingest")
        self.segmentation_client = Client("segmentation")
        self.diagnostic_client = Client("diagnostic")
        self.tts_client = Client("voice-tts")
        
        self.guidance_text = "Please adjust the probe position to improve image quality."

    async def process_frame(self):
        """Process a single frame through the entire pipeline."""
        # Get next frame from ingest server
        frame_data = await self.ingest_client.request("nextFrame", {})
        logger.info("Received new frame")

        # Segment the image
        seg_result = await self.segmentation_client.request(
            "segment",
            {"image": frame_data["image"]}
        )
        logger.info(f"Segmentation score: {seg_result['score']}")

        # Check segmentation score
        if seg_result["score"] < 0.5:
            logger.info("Low segmentation score, requesting probe adjustment")
            await self.tts_client.request(
                "speak",
                {"text": self.guidance_text}
            )
            return

        # Process with diagnostic server
        diag_result = await self.diagnostic_client.request(
            "assess",
            {
                "image": frame_data["image"],
                "mask": seg_result["mask"]
            }
        )
        
        # Build result sentence
        result_text = (
            f"Image quality is {diag_result['image_quality']:.0%}. "
            f"Identified {', '.join(diag_result['landmarks'])}. "
            f"{diag_result['diagnosis']}."
        )
        
        # Speak result
        await self.tts_client.request(
            "speak",
            {"text": result_text}
        )
        logger.info(f"Spoke result: {result_text}")

    async def run(self):
        """Run the coordinator in an infinite loop."""
        while True:
            try:
                await self.process_frame()
                # Throttle to 1 Hz
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error in processing loop: {e}")
                await asyncio.sleep(1)

if __name__ == "__main__":
    coordinator = Coordinator()
    asyncio.run(coordinator.run())
