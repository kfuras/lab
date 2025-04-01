from PIL import Image, ImageDraw, ImageFont
import csv, os

# --- Config ---
WIDTH, HEIGHT = 1200, 628
FONT_PATH = "Roboto[wdth,wght].ttf"  # Replace with your actual font path
FONT_SIZE = 50
SMALL_FONT_SIZE = 24
TEXT_COLOR = "white"
SHADOW_COLOR = "black"
OUTPUT_DIR = "generated_images"
BACKGROUND_DIR = "backgrounds"

# --- Setup ---
os.makedirs(OUTPUT_DIR, exist_ok=True)
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
small_font = ImageFont.truetype(FONT_PATH, SMALL_FONT_SIZE)

# --- Process CSV ---
with open("titles.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        title = row.get("title", "").strip()
        category = row.get("category", "").strip()
        if not title or not category:
            continue

        # Background selection
        category_slug = category.lower().replace(" ", "_")
        background_path = os.path.join(BACKGROUND_DIR, f"{category_slug}.png")
        if not os.path.isfile(background_path):
            print(f"⚠️ Background not found for category: {category}")
            continue

        # Load background and add overlay
        bg = Image.open(background_path).resize((WIDTH, HEIGHT)).convert("RGBA")
        overlay = Image.new("RGBA", bg.size, (0, 0, 0, 100))
        img = Image.alpha_composite(bg, overlay)
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

        # Draw lines with shadow
        y_start = (HEIGHT - len(lines) * FONT_SIZE) // 2
        for i, l in enumerate(lines):
            text_width = draw.textlength(l, font=font)
            x = (WIDTH - text_width) // 2
            y = y_start + i * FONT_SIZE
            draw.text((x + 2, y + 2), l, font=font, fill=SHADOW_COLOR)
            draw.text((x, y), l, font=font, fill=TEXT_COLOR)

        # Save output
        safe_name = title.lower().replace(" ", "_").replace("/", "-")
        output_path = os.path.join(OUTPUT_DIR, f"{safe_name}.png")
        img.convert("RGB").save(output_path)
        print(f"✅ Created: {output_path}")
