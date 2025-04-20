# Space Triage - Ultrasound Workflow System

A CPU-based ultrasound triage workflow system using MCP servers for image processing, segmentation, diagnostics, and voice feedback.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up ElevenLabs API key:
```bash
export ELEVEN_API_KEY=sk_01403a7fb1688de2d91de74cbef48378ad6ae55fdfc7ea1b
```

3. Create a `sample_images` directory and add some ultrasound images (PNG/JPEG).

## Running the System

Open separate terminal tabs and run each server:

```bash
# Tab 1: Start the ingest server
python ingest_server.py

# Tab 2: Start the segmentation server
python segmentation_server.py

# Tab 3: Start the diagnostic server
python diagnostic_server.py

# Tab 4: Start the voice TTS server
python voice_tts_server.py

# Tab 5: Start the coordinator
python coordinator.py
```

## Testing

Run the test suite:
```bash
pytest tests/
```

## Components

- `ingest_server.py`: Simulates ultrasound image source
- `segmentation_server.py`: Performs image segmentation
- `diagnostic_server.py`: Analyzes images and provides diagnostic feedback
- `voice_tts_server.py`: Text-to-speech service using ElevenLabs
- `coordinator.py`: Orchestrates the workflow

## Architecture

The system uses MCP (Message Communication Protocol) servers for all components. The coordinator orchestrates the workflow:

1. Get next frame from ingest server
2. Perform segmentation
3. If segmentation score is low, request probe adjustment
4. Otherwise, perform diagnostic analysis
5. Convert results to speech using TTS

All processing is CPU-based and runs at 1Hz for testing purposes.

## Features

- **Voice-Activated Area Specification:**  
  Astronauts can use voice commands to specify the anatomical area they want to analyze (e.g., "Analyze the heart" or "Check the liver").

- **Ultrasound Image Input:**  
  The system accepts ultrasound images from the NASA Ultrasound-2 probe, captured in a microgravity environment.

- **Image Segmentation and Analysis:**  
  A trained segmentation model evaluates the input image to determine if the target anatomical area is visible.
  
- **Diagnostic Assessment:**  
  If the correct area is imaged, Space Triage provides an initial diagnostic assessment and details on image quality, tissue textures, and anatomical landmarks.

- **Guided Transition Assistance:**  
  If the target area is not captured, the system outputs voice instructions guiding the astronaut to adjust the probe’s position and settings to capture the desired anatomical view.

## How It Works

1. **Area Specification:**  
   The astronaut specifies the anatomical area for analysis by speaking a simple command.

2. **Image Capture and Input:**  
   An ultrasound image is captured using the NASA Ultrasound-2 system and is then fed into Space Triage.

3. **Segmentation Analysis:**  
   The segmentation model processes the image to verify whether the specified anatomical area is present.  
   - **If the target area is found:**  
     The system provides a detailed diagnostic assessment.
   - **If the target area is missing:**  
     Voice-guided instructions are generated to help transition the probe to the correct position.

4. **Voice Guidance and Feedback:**  
   The system’s voice agent produces a transcript that can be read aloud, instructing the astronaut on necessary adjustments. This includes:
   - Verification of the current image.
   - Step-by-step movements and probe positioning.
   - Optimization of machine settings (depth, gain, frequency).
   - Final confirmation when the correct view is achieved.

## Example Workflow

1. **Astronaut Command:** "Heart."
2. **Image Capture:** An ultrasound image is taken and fed into the segmentation model.
3. **Segmentation Outcome:**
   - **If the Heart is Visible:**  
     The system says:  
     "The heart is visible. The image displays clear cardiac landmarks including chamber walls and valve motion. Proceed with the cardiac evaluation."
   - **If the Heart is Not Visible:**  
     The system says:  
     "The current image does not show the heart. Please slide the probe upward and adjust the angle slightly toward the chest. Once repositioned, recapture the image."
