from PIL import Image, ImageDraw, ImageFont
import csv
import os

# Settings
WIDTH, HEIGHT = 1200, 628
FONT_PATH = "Arial Bold.ttf"  # Make sure this font file is in your folder
FONT_SIZE = 48
OUTPUT_DIR = "generated_images"
BACKGROUND_COLOR = "#111827"
TEXT_COLOR = "white"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load font
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

# Read blog titles from CSV
with open("titles.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        title = row["title"]

        # Create image
        img = Image.new("RGB", (WIDTH, HEIGHT), color=BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        # Text wrapping (basic)
        lines = []
        words = title.split(" ")
        line = ""
        for word in words:
            test_line = line + word + " "
            if draw.textlength(test_line, font=font) < WIDTH - 100:
                line = test_line
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)

        # Vertical positioning
        total_text_height = len(lines) * FONT_SIZE
        y_start = (HEIGHT - total_text_height) // 2

        # Draw each line
        for i, line in enumerate(lines):
            text_width = draw.textlength(line, font=font)
            x = (WIDTH - text_width) // 2
            y = y_start + i * FONT_SIZE
            draw.text((x, y), line.strip(), font=font, fill=TEXT_COLOR)

        # Save image
        safe_name = title.lower().replace(" ", "_").replace("/", "-")
        img.save(os.path.join(OUTPUT_DIR, f"{safe_name}.png"))

print("✅ Images created in /generated_images")

