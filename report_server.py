import os
import logging
import anthropic
from dotenv import load_dotenv
from prompts import create_report_prompt

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportServer:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set in your environment or .env file!")
        self.client = anthropic.AsyncAnthropic(api_key=api_key)

    async def generate_report(self, report_data: dict) -> str:
        """
        Generate a human-readable report using Claude LLM.
        report_data should include keys: astronaut, organ, navigation, segmentation, diagnosis, image_quality, landmarks, timestamp, etc.
        """
        prompt = create_report_prompt(report_data)
        try:
            response = await self.client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=256,
                messages=[{"role": "user", "content": prompt}]
            )
            report = response.content
            if isinstance(report, list):
                report = " ".join([c["text"] if isinstance(c, dict) and "text" in c else str(c) for c in report])
        except Exception as e:
            logger.error(f"Error in Claude API call: {str(e)}")
            report = "Unable to generate report at this time."
        return report

if __name__ == "__main__":
    import asyncio
    server = ReportServer()
    # Example usage with dummy data
    dummy_data = {
        "astronaut": "John Doe",
        "organ": "liver",
        "navigation": "Probe moved to right upper quadrant.",
        "segmentation": "Central region segmented successfully.",
        "diagnosis": "Liver appears healthy.",
        "image_quality": 0.85,
        "landmarks": ["liver"],
        "timestamp": "2025-04-19T22:09:00Z"
    }
    async def test():
        report = await server.generate_report(dummy_data)
        print("Generated Report:\n", report)
    asyncio.run(test())
