from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder():
    # Create a 400x400 image with a dark blue background
    img = Image.new('RGB', (400, 400), color=(30, 41, 59))
    d = ImageDraw.Draw(img)
    
    # Draw a circle
    d.ellipse([20, 20, 380, 380], outline=(99, 102, 241), width=10)
    
    # Add text "Portfolio"
    # trying to load a default font, otherwise default to simple
    try:
        # This path is common on Windows, but might vary
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()

    # Draw text in the middle (approximate centering)
    d.text((200, 200), "ME", fill=(248, 250, 252), anchor="mm", font=font)
    
    output_path = os.path.join(os.path.dirname(__file__), "..", "app", "static", "profile_placeholder.png")
    output_path = os.path.abspath(output_path)
    
    img.save(output_path)
    print(f"Placeholder image saved to {output_path}")

if __name__ == "__main__":
    create_placeholder()
