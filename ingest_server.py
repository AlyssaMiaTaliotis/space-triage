"""
Simulated Ultrasound-2 image source.
Runs an MCP server exposing `nextFrame -> {image, settings, timestamp}`.
Reads PNG/JPEG files that the user drops into `sample_images/` and serves
them round-robin; no hardware required.
"""
import asyncio
import base64
import glob
import json
import logging
import os
import time
from pathlib import Path
from typing import Dict, List

from mcp_local import App
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UltrasoundIngestServer:
    def __init__(self):
        self.app = App("ultrasound-ingest")
        self.images: List[str] = []
        self.current_idx = 0
        self.metadata = {"depth": 70, "gain": 35}

    async def load_images(self):
        """Load all images from sample_images directory."""
        image_dir = Path("sample_images")
        if not image_dir.exists():
            image_dir.mkdir(exist_ok=True)
            logger.info("Created sample_images directory")
        
        self.images = []
        for ext in ('*.png', '*.jpg', '*.jpeg'):
            self.images.extend(glob.glob(str(image_dir / ext)))
        logger.info(f"Loaded {len(self.images)} images from sample_images/")

    async def next_frame(self, _) -> Dict:
        """Return next image in round-robin fashion with metadata."""
        if not self.images:
            await self.load_images()
            if not self.images:
                raise RuntimeError("No images found in sample_images/")

        image_path = self.images[self.current_idx]
        self.current_idx = (self.current_idx + 1) % len(self.images)

        # Load and encode image
        with Image.open(image_path) as img:
            # Convert to bytes
            img_byte_arr = img.convert('RGB')
            img_bytes = img_byte_arr.tobytes()
            # Encode as base64 for JSON serialization
            img_b64 = base64.b64encode(img_bytes).decode('utf-8')

        response = {
            "image": img_b64,
            "settings": self.metadata,
            "timestamp": int(time.time())
        }
        
        logger.info(f"Serving frame from {image_path}")
        return response

    def run(self):
        """Start the MCP server."""
        self.app.register_request("nextFrame", self.next_frame)
        self.app.run(
            os.sys.stdin.buffer,
            os.sys.stdout.buffer,
            self.app.create_initialization_options()
        )

if __name__ == "__main__":
    server = UltrasoundIngestServer()
    server.run()
