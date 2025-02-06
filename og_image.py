#!/usr/bin/env python3
import json
from PIL import Image, ImageDraw, ImageFont


def load_ephemeris(filename):
    with open(filename, "r") as f:
        return json.load(f)


def get_text_size(draw, text, font):
    try:
        return draw.textsize(text, font=font)
    except AttributeError:
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return (width, height)


def generate_og_image(ephemeris, output_file="og_threat_assessment.png"):
    # OG recommended dimensions: 1200 x 630 px
    img_width, img_height = 1200, 630
    bg_color = (0, 0, 0)  # Black background
    title_color = (255, 0, 0)  # Red title
    text_color = (0, 255, 0)  # Neon green for other lines
    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    # Use fonts 2x bigger (80px)
    try:
        title_font = ImageFont.truetype("VT323-Regular.ttf", 80)
        text_font = ImageFont.truetype("VT323-Regular.ttf", 80)
    except IOError:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Extract threat info.
    impact_risk = ephemeris.get("impact_risk", {})
    torino_scale = impact_risk.get("torino_scale", {}).get("maximum", "N/A")
    impact_probability = impact_risk.get("impact_probability", 0)
    impact_velocity = impact_risk.get("impact_velocity", {})
    velocity_value = impact_velocity.get("value", "N/A")
    velocity_unit = impact_velocity.get("unit", "")
    potential_impacts = impact_risk.get("potential_impacts", {})
    impact_count = potential_impacts.get("count", "N/A")
    last_update = impact_risk.get("last_updated", "N/A")

    # Convert probability to percentage.
    impact_prob_percent = impact_probability * 100

    # Get asteroid name.
    asteroid_name = ephemeris.get("name", "Unknown Asteroid")

    # Prepare text lines.
    lines = [
        f"ASTEROID THREAT ASSESSMENT: {asteroid_name}",
        "",  # blank line
        f"Torino Scale: {torino_scale}",
        f"Impact Probability: {impact_prob_percent:.2f}%",
        f"Impact Velocity: {velocity_value} {velocity_unit}",
        f"Detected Scenarios: {impact_count}",
        f"Last Update: {last_update}",
    ]

    # Calculate total text height to center the block vertically.
    total_height = 0
    sizes = []
    for i, line in enumerate(lines):
        font = title_font if i == 0 else text_font
        size = get_text_size(draw, line, font)
        sizes.append((size, font))
        total_height += size[1]
    total_height += (len(lines) - 1) * 10  # add 10px spacing between lines

    current_y = (img_height - total_height) // 2

    # Draw each line centered.
    for i, line in enumerate(lines):
        (text_width, text_height), font = sizes[i]
        x = (img_width - text_width) // 2
        fill_color = title_color if i == 0 else text_color
        draw.text((x, current_y), line, fill=fill_color, font=font)
        current_y += text_height + 10

    img.save(output_file)
    print(f"Open Graph image saved to {output_file}")


if __name__ == "__main__":
    ephemeris = load_ephemeris("ephemeris.json")
    generate_og_image(ephemeris)
