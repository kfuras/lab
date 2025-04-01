from PIL import Image, ImageDraw, ImageFont
import csv
import os

# === CONFIGURATION ===
WIDTH, HEIGHT = 1200, 628
BACKGROUND_IMAGE = "TechBackground.png"  # Replace with your own background
FONT_PATH = "Arial Bold.ttf"        # Make sure this .ttf is in your folder
FONT_SIZE = 50
SMALL_FONT_SIZE = 24
OUTPUT_DIR = "generated_images"
TEXT_COLOR = "white"
CATEGORY_LABEL = "Automation"        # You can change this dynamically if needed

# === SETUP ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load fonts
try:
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    small_font = ImageFont.truetype(FONT_PATH, SMALL_FONT_SIZE)
except Exception as e:
    print("⚠️ Font loading failed:", e)
    exit(1)

# Read blog titles from CSV
try:
    with open("titles.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row.get("title", "").strip()
            if not title:
                print("⚠️ Skipping empty row")
                continue

            print(f"🖼️ Generating image for: {title}")

            # Load and resize background image
            bg = Image.open(BACKGROUND_IMAGE).resize((WIDTH, HEIGHT))
            img = bg.convert("RGB")
            draw = ImageDraw.Draw(img)

            # Draw category label (top-left corner)
            draw.text((40, 30), CATEGORY_LABEL, font=small_font, fill="#94a3b8")  # Slate-400 color

            # Text wrapping logic
            words = title.split(" ")
            lines = []
            line = ""
            for word in words:
                test = f"{line} {word}".strip()
                if draw.textlength(test, font=font) < WIDTH - 100:
                    line = test
                else:
                    lines.append(line)
                    line = word
            lines.append(line)

            # Center title text vertically
            y_start = (HEIGHT - len(lines) * FONT_SIZE) // 2

            for i, line in enumerate(lines):
                line_width = draw.textlength(line, font=font)
                x = (WIDTH - line_width) // 2
                y = y_start + i * FONT_SIZE
                draw.text((x, y), line, font=font, fill=TEXT_COLOR)

            # Save image
            safe_name = title.lower().replace(" ", "_").replace("/", "-").replace("?", "")
            filename = os.path.join(OUTPUT_DIR, f"{safe_name}.png")
            img.save(filename)
            print(f"✅ Saved: {filename}")

except Exception as e:
    print("🚨 Error:", e)

