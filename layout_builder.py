def build_comic_layout(image_paths: list, full_story: str, outline: list) -> list:
    """
    Organizes panel content into a unified layout dataset.
    """
    raw_story_panels = full_story.split("**Panel ")
    story_panels = [f"**Panel {panel}" for panel in raw_story_panels if panel.strip()]
    layout = []

    for idx, (image, panel_info) in enumerate(zip(image_paths, outline), start=1):
        text_content = ""
        if idx - 1 < len(story_panels):
            raw_text = story_panels[idx - 1]
            lines = raw_text.strip().splitlines()
            text_content = "\n".join(lines[1:]).strip() if len(lines) > 1 else raw_text

        layout.append(
            {
                "panel": idx,
                "title": panel_info.get("title", f"Panel {idx}"),
                "image_path": image,
                "text": text_content,
                "scene_description": panel_info.get("scene_description", ""),
                "image_prompt": panel_info.get("image_prompt", ""),
            }
        )

    return layout
