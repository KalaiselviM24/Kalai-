import os
import re

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

pipe = None


def get_pipeline():
    global pipe
    if pipe is None:
        model_id = "runwayml/stable-diffusion-v1-5"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=dtype)
        pipe = pipe.to(device)
    return pipe


def sanitize_filename(prompt: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9]", "_", prompt[:30])
    return f"{clean}.png"


def generate_image(prompt: str, filename: str = None) -> str:
    """
    Generates a comic illustration using Stable Diffusion and saves it
    locally.
    """
    if not filename:
        filename = sanitize_filename(prompt)

    out_dir = "static/panels"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)

    try:
        pipeline = get_pipeline()
        image = pipeline(prompt).images[0]
        image.save(path)
    except Exception as e:
        print(f"Image generation fallback triggered: {e}")
        # Fallback image generation if GPU/model memory is unavailable
        img = Image.new("RGB", (512, 512), color=(73, 109, 137))
        img.save(path)
    return path
