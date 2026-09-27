import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-pro")


def generate_story(outline: list) -> str:
    """
    Generates a detailed comic story with narration and character dialogue
    from a list of comic panel outlines using Gemini 1.5 Pro.
    """
    formatted_outline = "\n".join(
        [
            f"Panel {item.get('panel', i + 1)}: {item.get('title', '')} - {item.get('scene_description', '')}"
            for i, item in enumerate(outline)
        ]
    )
    prompt = f"""
    You are a comic book writer.
    Given the following panel breakdown, write a comic-style story with
    engaging narration and character dialogues for each panel.
    Panel Outline:
    {formatted_outline}
    Guidelines:
    - Use a fun and engaging tone, like an actual comic book.
    - Format each panel heading strictly as *Panel 1: Title*, **Panel 2: Title**, etc.
    - Include narration (*NARRATION:*) and clearly marked character lines (*CAPTION:* or character name).
    - Keep each panel self-contained but part of a cohesive story.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating story: {str(e)}"
