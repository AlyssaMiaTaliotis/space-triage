def create_health_assessment_prompt(target_organ, ultrasound_image_data):
    prompt = (
        f"You are an astronaut assistant providing ultrasound image analysis for the {target_organ}. "
        f"The astronaut has successfully located and imaged the {target_organ}. "
        "Analyze the current ultrasound image and provide a concise health assessment.\n\n"
    )

    # Add the ultrasound image data for analysis
    prompt += (
        "Current ultrasound image data:\n"
        f"{ultrasound_image_data}\n\n"
    )

    prompt += (
        "Your response should:\n"
        "1. Begin with a clear sentence stating whether the organ looks healthy or abnormal.\n"
        "2. Include 2-3 short bullet points describing what you see, using simple, non-technical language.\n"
        "3. If the organ appears abnormal, provide a brief follow-up recommendation suitable for a non-medical astronaut in space.\n"
        "4. If the organ appears healthy, no recommendation is needed.\n\n"
        
        "Do not include labels like 'ASSESSMENT' or 'RECOMMENDATION'. Just write a natural, helpful response that follows the above structure."
    )

    return prompt

def create_navigation_prompt(target_organ, current_image_data=None):
    prompt = (
        "You are an astronaut assistant providing real-time ultrasound guidance to a non-medical expert. "
        f"The astronaut is trying to locate and image the {target_organ}. "
        "Based on the current ultrasound image, provide step-by-step instructions "
        "on how to reposition the probe to better visualize the target organ.\n\n"
    )

    # Add information about the current image if available
    if current_image_data:
        prompt += (
            "Current image analysis:\n"
            f"{current_image_data}\n\n"
        )

    prompt += (
        "Your instructions should be:\n"
        "1. Clear and concise for audio delivery\n"
        "2. Specific about direction and distance\n"
        "3. Include anatomical landmarks to look for\n"
        "4. When you introduce a new area say \"Remember the {area} is {where the area is}\"\n"
        "5. Adaptable to microgravity environment\n"
        "6. In laymen terms\n\n"
        "Format your response as sequential steps numbered 1-5 that can be directly "
        "converted to speech. Each step should be a single sentence."
    )

    return prompt

def create_navigation_prompt(target_organ, current_organ=None):
    prompt = (
        "You are an astronaut assistant providing real-time, voice-based navigation for ultrasound imaging in space. "
        "Your user is a non-expert astronaut operating the NASA Ultrasound-2 system in microgravity.\n\n"
    )
    if current_organ:
        prompt += (
            f"The astronaut is currently imaging the {current_organ}. "
            f"The goal is to transition to imaging the {target_organ}.\n\n"
        )
    else:
        prompt += (
            f"The astronaut needs to adjust the probe to image the {target_organ}.\n\n"
        )
    prompt += (
        "Give clear, step-by-step instructions on how to move or angle the probe to find the target organ. "
        "Use simple, non-technical language. Only give one or two steps at a time. "
        "Pause for confirmation after each step. If the astronaut is not successful, suggest a different adjustment. "
        "Keep instructions concise and positive.\n\n"
        "Respond only with the next navigation step."
    )
    return prompt

def create_report_prompt(report_data):
    """
    Create a prompt for Claude to generate a structured, human-readable ultrasound report.
    report_data should be a dict with keys like astronaut, organ, navigation, segmentation, diagnosis, image_quality, landmarks, timestamp, etc.
    """
    astronaut = report_data.get("astronaut", "the astronaut")
    organ = report_data.get("organ", "target organ")
    navigation = report_data.get("navigation", "N/A")
    segmentation = report_data.get("segmentation", "N/A")
    diagnosis = report_data.get("diagnosis", "N/A")
    image_quality = report_data.get("image_quality", None)
    landmarks = report_data.get("landmarks", [])
    timestamp = report_data.get("timestamp", "N/A")
    
    prompt = (
        f"You are an astronaut medical assistant. Generate a concise, structured ultrasound report for the following case.\n"
        f"Astronaut: {astronaut}\n"
        f"Organ: {organ}\n"
        f"Timestamp: {timestamp}\n"
        f"\nNavigation summary:\n{navigation}\n"
        f"\nSegmentation summary:\n{segmentation}\n"
        f"\nDiagnostic summary:\n{diagnosis}\n"
    )
    if image_quality is not None:
        prompt += f"\nImage quality score: {image_quality:.2f}\n"
    if landmarks:
        prompt += f"\nDetected landmarks: {', '.join(str(l) for l in landmarks)}\n"
    prompt += (
        "\nPlease write a natural-language report suitable for a flight surgeon or astronaut, summarizing the findings, any recommendations, and next steps if needed. "
        "Be concise, clear, and use lay language."
    )
    return prompt