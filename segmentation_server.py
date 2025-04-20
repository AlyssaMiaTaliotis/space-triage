"""
Stub PyTorch "model" that draws a central circle mask on the input image and
returns confidence 0.8. Exposes one MCP request: `segment(image: bytes)`.
"""
import asyncio
import io
import json
import logging
import os
from typing import Dict

import numpy as np
from mcp_local import App
from PIL import Image, ImageDraw

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SegmentationServer:
    def __init__(self):
        self.app = App("segmentation")
        self.confidence = 0.8

    def create_circular_mask(self, image: Image.Image) -> Image.Image:
        """Create a circular mask in the center of the image."""
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        
        # Calculate circle parameters
        width, height = image.size
        center = (width // 2, height // 2)
        radius = min(width, height) // 4
        
        # Draw circle
        draw.ellipse(
            [
                center[0] - radius,
                center[1] - radius,
                center[0] + radius,
                center[1] + radius
            ],
            fill=255
        )
        
        return mask

    def overlay_mask_on_image(self, image: Image.Image, mask: Image.Image, color=(255, 0, 0), alpha=1.0) -> Image.Image:
        """Overlay the mask on the image with the given color and high visibility (fully opaque)."""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
        mask_rgb = Image.new('RGBA', image.size, color + (0,))
        mask_alpha = mask.point(lambda p: 255 if p > 0 else 0)  # Fully opaque where mask > 0
        overlay = Image.composite(mask_rgb, overlay, mask_alpha)
        return Image.alpha_composite(image, overlay)

    async def segment(self, request: Dict) -> Dict:
        """Process image and return mask with bbox, confidence score, and overlay."""
        logger.info("Processing segmentation request")
        
        # Convert bytes to image
        image_bytes = request.get("image")
        if not image_bytes:
            raise ValueError("No image data provided")
            
        image = Image.open(io.BytesIO(image_bytes))
        
        # Create mask
        mask = self.create_circular_mask(image)
        
        # Get bounding box
        bbox = mask.getbbox()
        
        # Convert mask to PNG bytes
        mask_bytes = io.BytesIO()
        mask.save(mask_bytes, format='PNG')
        
        # Create overlay image
        overlay_img = self.overlay_mask_on_image(image, mask)
        overlay_bytes = io.BytesIO()
        overlay_img.save(overlay_bytes, format='PNG')
        
        response = {
            "mask": mask_bytes.getvalue(),
            "bbox": list(bbox),
            "score": self.confidence,
            "overlay": overlay_bytes.getvalue()
        }
        
        logger.info(f"Segmentation complete with score {self.confidence}")
        return response

    def run(self):
        """Start the MCP server."""
        self.app.register_request("segment", self.segment)
        self.app.run(
            os.sys.stdin.buffer,
            os.sys.stdout.buffer,
            self.app.create_initialization_options()
        )

if __name__ == "__main__":
    server = SegmentationServer()
    server.run()
