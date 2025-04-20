"""Tests for the ultrasound ingest server."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from ingest_server import UltrasoundIngestServer

async def test_next_frame():
    server = UltrasoundIngestServer()
    await server.load_images()
    response = await server.next_frame(None)
    print("Test next_frame response:")
    print({k: (v[:60] + '...') if k == 'image' else v for k, v in response.items()})

if __name__ == "__main__":
    asyncio.run(test_next_frame())