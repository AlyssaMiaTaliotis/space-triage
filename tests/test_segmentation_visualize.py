import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import io
from PIL import Image
from segmentation_server import SegmentationServer

# Load a test image (replace with your own image path if desired)
TEST_IMAGE_PATH = "sample_images/masked_output.png"  # Change if needed
OUTPUT_OVERLAY_PATH = "tests/output_overlay.png"

# Load image as bytes
with open(TEST_IMAGE_PATH, "rb") as f:
    image_bytes = f.read()

async def test_segment_and_visualize():
    server = SegmentationServer()
    request = {"image": image_bytes}
    response = await server.segment(request)
    # Save overlay image
    overlay_bytes = response["overlay"]
    overlay_img = Image.open(io.BytesIO(overlay_bytes))
    overlay_img.save(OUTPUT_OVERLAY_PATH)
    print(f"Overlay image saved to {OUTPUT_OVERLAY_PATH}")
    # Optionally, display the image (uncomment below if running locally with GUI)
    # overlay_img.show()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_segment_and_visualize())
