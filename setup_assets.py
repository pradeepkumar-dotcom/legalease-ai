"""
Setup script to generate brand logos (Logo.png and inverseLogo.png) for LegalEase
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def generate_logos():
    image_dir = Path(__file__).resolve().parent / "Image"
    image_dir.mkdir(parents=True, exist_ok=True)
    
    logo_path = image_dir / "Logo.png"
    inverse_logo_path = image_dir / "inverseLogo.png"
    
    # Dimensions
    width, height = 800, 240
    
    # Helper to draw legal icon (Scales of Justice & Shield motif)
    def draw_legal_symbol(draw, x_offset, y_offset, primary_color, accent_color):
        # Base pillar / stand
        draw.line([(x_offset + 50, y_offset + 30), (x_offset + 50, y_offset + 130)], fill=primary_color, width=6)
        draw.polygon([(x_offset + 30, y_offset + 130), (x_offset + 70, y_offset + 130), (x_offset + 80, y_offset + 145), (x_offset + 20, y_offset + 145)], fill=accent_color)
        
        # Horizontal beam
        draw.line([(x_offset + 10, y_offset + 45), (x_offset + 90, y_offset + 45)], fill=accent_color, width=5)
        
        # Left scale pan
        draw.line([(x_offset + 10, y_offset + 45), (x_offset + 5, y_offset + 75)], fill=primary_color, width=2)
        draw.line([(x_offset + 10, y_offset + 45), (x_offset + 25, y_offset + 75)], fill=primary_color, width=2)
        draw.arc([x_offset - 2, y_offset + 70, x_offset + 32, y_offset + 90], 0, 180, fill=accent_color, width=4)
        
        # Right scale pan
        draw.line([(x_offset + 90, y_offset + 45), (x_offset + 75, y_offset + 75)], fill=primary_color, width=2)
        draw.line([(x_offset + 90, y_offset + 45), (x_offset + 95, y_offset + 75)], fill=primary_color, width=2)
        draw.arc([x_offset + 68, y_offset + 70, x_offset + 102, y_offset + 90], 0, 180, fill=accent_color, width=4)
        
        # Top finial
        draw.ellipse([x_offset + 44, y_offset + 20, x_offset + 56, y_offset + 32], fill=accent_color)

    # 1. Generate Light Logo (Dark Navy & Gold on Clean White)
    img_light = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw_light = ImageDraw.Draw(img_light)
    
    # Colors
    navy = (15, 23, 42, 255)       # #0F172A
    gold = (217, 119, 6, 255)      # #D97706
    slate = (100, 116, 139, 255)   # #64748B
    
    draw_legal_symbol(draw_light, 40, 45, navy, gold)
    
    # Text
    draw_light.text((170, 50), "LegalEase", fill=navy, font=None) # Default fallback bitmap/truetype
    # Add geometric stylized typography fallback with text drawing
    try:
        # Try loading default system font if available
        font_large = ImageFont.truetype("arial.ttf", 64)
        font_sub = ImageFont.truetype("arial.ttf", 22)
    except IOError:
        font_large = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    draw_light.text((170, 55), "LegalEase", fill=navy, font=font_large)
    draw_light.text((172, 130), "AI-POWERED LEGAL DOCUMENT GENERATION", fill=gold, font=font_sub)
    draw_light.text((172, 160), "Enterprise-Grade Contracts • Instant Compliance • Accurate Drafting", fill=slate, font=font_sub)
    img_light.save(logo_path, "PNG")
    print(f"[+] Saved Light Logo to {logo_path}")

    # 2. Generate Inverted Logo (White & Vivid Amber on Midnight Slate)
    img_dark = Image.new("RGBA", (width, height), (15, 23, 42, 255)) # #0F172A
    draw_dark = ImageDraw.Draw(img_dark)
    
    white = (248, 250, 252, 255)
    amber = (251, 191, 36, 255)
    muted_slate = (148, 163, 184, 255)
    
    draw_legal_symbol(draw_dark, 40, 45, white, amber)
    draw_dark.text((170, 55), "LegalEase", fill=white, font=font_large)
    draw_dark.text((172, 130), "AI-POWERED LEGAL DOCUMENT GENERATION", fill=amber, font=font_sub)
    draw_dark.text((172, 160), "Enterprise-Grade Contracts • Instant Compliance • Accurate Drafting", fill=muted_slate, font=font_sub)
    img_dark.save(inverse_logo_path, "PNG")
    print(f"[+] Saved Inverse Logo to {inverse_logo_path}")

if __name__ == "__main__":
    generate_logos()
