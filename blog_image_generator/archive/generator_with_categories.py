from PIL import Image, ImageDraw, ImageFont
import csv, os

# Config
WIDTH, HEIGHT = 1200, 628
FONT_PATH = "Roboto[wdth,wght].ttf"
FONT_SIZE = 50
SMALL_FONT_SIZE = 24
OUTPUT_DIR = "generated_images"
TEXT_COLOR = "white"
BACKGROUND_DIR = "backgrounds"  # Folder containing category images

# Prepare output
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load fonts
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
small_font = ImageFont.truetype(FONT_PATH, SMALL_FONT_SIZE)

# Read CSV and generate images
with open("titles.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        title = row.get("title", "").strip()
        category = row.get("category", "").strip()
        if not title or not category:
            continue

        # Convert category to safe lowercase filename (e.g. "Azure Cloud" → "azure_cloud.jpg")
        category_slug = category.lower().replace(" ", "_")
        background_path = os.path.join(BACKGROUND_DIR, f"{category_slug}.png")

        if not os.path.isfile(background_path):
            print(f"⚠️ Background for category '{category}' not found: {background_path}")
            continue

        # Load background
        bg = Image.open(background_path).resize((WIDTH, HEIGHT))
        img = bg.convert("RGB")
        draw = ImageDraw.Draw(img)

        # Draw category label
        draw.text((40, 30), category, font=small_font, fill="#94a3b8")

        # Word wrap title
        words = title.split()
        lines, line = [], ""
        for word in words:
            test = f"{line} {word}".strip()
            if draw.textlength(test, font=font) < WIDTH - 100:
                line = test
            else:
                lines.append(line)
                line = word
        lines.append(line)

        # Vertically center
        y_start = (HEIGHT - len(lines) * FONT_SIZE) // 2
        for i, l in enumerate(lines):
            text_width = draw.textlength(l, font=font)
            x = (WIDTH - text_width) // 2
            y = y_start + i * FONT_SIZE
            draw.text((x, y), l, font=font, fill=TEXT_COLOR)

        # Save image
        safe_name = title.lower().replace(" ", "_").replace("/", "-")
        output_file = os.path.join(OUTPUT_DIR, f"{safe_name}.png")
        img.save(output_file)
        print(f"✅ Created: {output_file}")

