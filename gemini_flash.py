import json
import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")


def generate_outline(user_prompt: str) -> list:
    """
    Generates a 5-panel comic layout based on the user's story idea
    using Gemini Flash.
    """
    prompt = f"""
    You are a professional AI comic planner.
    Your task is to generate a strictly formatted JSON array containing
    5 panel descriptions for a comic based on the story idea below:
    STORY: "{user_prompt}"
    Each JSON object must include:
    - "panel" (integer)
    - "title" (string)
    - "scene_description" (string)
    - "image_prompt" (string)
    Respond ONLY in this valid JSON format, without any explanations or
    markdown:
    [
    {{
    "panel": 1,
    "title": "Title here",
    "scene_description": "Scene description here",
    "image_prompt": "Image prompt for Stable Diffusion"
    }}
    ]
    """
    try:
        response = model.generate_content(prompt)
        output_text = response.text.strip()

        if output_text.startswith("```json"):
            output_text = output_text.replace("```json", "").replace("```", "").strip()
        elif output_text.startswith("```"):
            output_text = output_text.replace("```", "").strip()

        panel_data = json.loads(output_text)
        if not isinstance(panel_data, list):
            raise ValueError("Gemini response is not a list.")

        for panel in panel_data:
            if not isinstance(panel, dict) or not all(
                key in panel for key in ("panel", "title", "scene_description", "image_prompt")
            ):
                raise ValueError(f"Invalid panel format or missing keys: {panel}")

        return panel_data
    except json.JSONDecodeError as e:
        print("X JSON Decode Error:", e)
        print("X Full Text Received:\n", output_text)
        return [{"error": f"JSON parsing failed: {str(e)}"}]
    except Exception as e:
        print("X Unexpected Error:", e)
        return [{"error": f"Generation failed: {str(e)}"}]
