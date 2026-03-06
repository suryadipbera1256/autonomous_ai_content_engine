import os
import textwrap
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw, ImageFont

load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

STANDARD_FONT = "C:\\Windows\\Fonts\\arial.ttf"
BOLD_FONT = "C:\\Windows\\Fonts\\ariblk.ttf"

def process_and_add_text_overlay(image_path, overlay_text):
    print("Processing image and adding professional text overlay...")
    try:
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size

        # CRITICAL FIX: Removed the emoji that Windows Arial can't render
        highlights = ["KEY INSIGHT:", f"{overlay_text}"]

        # Box dimensions
        box_width = int(width * 0.45)
        box_height = int(height * 0.22) # Slightly slimmer box
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        margin = 35
        box_x = width - box_width - margin
        box_y = margin
        draw.rounded_rectangle(
            [box_x, box_y, box_x + box_width, box_y + box_height],
            radius=20,
            fill=(0, 0, 0, 200), # Slightly darker for better text contrast
            outline=(100, 255, 218, 180),
            width=3
        )

        try:
            h_font = ImageFont.truetype(BOLD_FONT, 34)
            t_font = ImageFont.truetype(STANDARD_FONT, 28)
        except:
            print("Warning: Custom fonts not found. Using default.")
            h_font = ImageFont.load_default()
            t_font = ImageFont.load_default()

        # Draw Title
        draw.text((box_x + 30, box_y + 30), highlights[0], font=h_font, fill=(100, 255, 218, 255))
        
        # Draw wrapped text
        wrapped_text = textwrap.fill(highlights[1], width=32)
        draw.text((box_x + 30, box_y + 85), wrapped_text, font=t_font, fill=(255, 255, 255, 250))

        combined = Image.alpha_composite(img, overlay)
        combined.convert("RGB").save(image_path, "PNG")
        print("✅ Image processing complete.")
        
    except Exception as e:
        print(f"❌ Error adding text overlay: {e}")

def generate_image(prompt, overlay_text):
    print(f"Waking up the Image Creator...\nPrompt: '{prompt}'")
    
    try:
        client = InferenceClient(token=HF_API_KEY)
        image = client.text_to_image(
            prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0"
        )
        
        filename = "generated_post_image.png"
        image.save(filename)
        
        process_and_add_text_overlay(filename, overlay_text)
        return filename
            
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

if __name__ == "__main__":
    test_prompt = "Macro close-up, complex technical blueprint diagram of a neural network layer, neon lines on dark background"
    test_text = "Strategic upskilling is vital today."
    generate_image(test_prompt, test_text)