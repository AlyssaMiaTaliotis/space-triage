"""Tests for the segmentation server."""
import io
import pytest
from PIL import Image
import numpy as np

from mcp import Client

@pytest.fixture
def dummy_image():
    """Create a 256x256 dummy image."""
    img = Image.fromarray(np.zeros((256, 256), dtype=np.uint8))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    return img_bytes.getvalue()

@pytest.mark.asyncio
async def test_segmentation(dummy_image):
    """Test segmentation with a dummy image."""
    client = Client("segmentation")
    
    response = await client.request("segment", {"image": dummy_image})
    
    # Verify mask
    assert "mask" in response
    mask_bytes = response["mask"]
    mask = Image.open(io.BytesIO(mask_bytes))
    assert mask.size == (256, 256)
    
    # Verify bbox
    assert "bbox" in response
    bbox = response["bbox"]
    assert len(bbox) == 4
    assert all(isinstance(x, int) for x in bbox)
    
    # Verify score
    assert "score" in response
    assert response["score"] == 0.8
