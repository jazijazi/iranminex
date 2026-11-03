# services/captcha_service.py
import random
import string
from PIL import Image, ImageDraw, ImageFont , ImageFilter
import io
import math
import base64
from django.conf import settings
import os

class CaptchaGenerator:
    def __init__(self):
        self.width = 220
        self.height = 80
        self.length = 5
        self.chars = 'A2B9C4D8E6F7G8H6J3K5L5M4N7P39R2S3TUVW4X2YZA'
        self.font_paths = [
            os.path.join(settings.BASE_DIR, "fonts", "dejavu-sans.bold.ttf"),
            os.path.join(settings.BASE_DIR, "fonts", "tomnr.ttf"),
            os.path.join(settings.BASE_DIR, "fonts", "ARIAL.TTF"),
        ]

    def generate_text(self):
        """Generate random text for CAPTCHA"""
        return ''.join(random.choice(self.chars) for _ in range(self.length))

    def _load_font(self, size):
        for path in self.font_paths:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    def generate_image(self, text) -> Image:
        """Generate an easy-to-read CAPTCHA image"""
        image = Image.new('RGB', (self.width, self.height), color='white')
        draw = ImageDraw.Draw(image)
        font = self._load_font(36)  # same font for every character, no mixing

        # very light background noise, just enough to deter trivial OCR
        for _ in range(40):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            draw.point((x, y), fill=(
                random.randint(195, 230),
                random.randint(195, 230),
                random.randint(195, 230)
            ))

        box = 50  # canvas per character, sized so rotation never clips the glyph
        spacing = 40  # > box width minus overlap margin, prevents adjacent chars touching

        for i, char in enumerate(text):
            char_img = Image.new('RGBA', (box, box), (255, 255, 255, 0))
            char_draw = ImageDraw.Draw(char_img)
            color = (random.randint(0, 60), random.randint(0, 60), random.randint(0, 60))

            # center manually via textbbox instead of anchor= (works for default
            # bitmap font too, which doesn't support most anchor modes)
            bbox = char_draw.textbbox((0, 0), char, font=font, stroke_width=1)
            cw, ch = bbox[2] - bbox[0], bbox[3] - bbox[1]
            tx, ty = (box - cw) // 2 - bbox[0], (box - ch) // 2 - bbox[1]
            char_draw.text((tx, ty), char, font=font, fill=color, stroke_width=1, stroke_fill=color)

            angle = random.randint(-8, 8)  # gentle tilt only
            rotated_char = char_img.rotate(angle, expand=0, resample=Image.BICUBIC)

            x = 10 + i * spacing
            y = (self.height - box) // 2 + random.randint(-3, 3)
            image.paste(rotated_char, (x, y), rotated_char)

        # one faint line — minimal anti-bot measure without hurting legibility
        draw.line(
            [(random.randint(0, self.width), random.randint(0, self.height)),
             (random.randint(0, self.width), random.randint(0, self.height))],
            fill=(205, 205, 205), width=1
        )

        return image

    def image_to_base64(self, image: Image) -> str:
        """Convert PIL image to base64 string"""
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        return base64.b64encode(buffer.getvalue()).decode()