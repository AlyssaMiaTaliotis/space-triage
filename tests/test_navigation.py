import sys
import os
import asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import base64

from navigation_server import NavigationServer

async def test_navigation():
    server = NavigationServer()
    # Use a real or dummy image in base64
    with open("sample_images/masked_output.png", "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")
    response = await server.navigate({
        "image": image_b64,
        "target_organ": "heart"
    })
    print("Navigation response:", response)

if __name__ == "__main__":
    asyncio.run(test_navigation())