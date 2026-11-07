import os
import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def compress_image(
    image_field,
    max_size=(400, 400),
    quality=50
) -> InMemoryUploadedFile:
    
    img = Image.open(image_field)
    img_format = (img.format or "JPEG").upper()

    # Resize in place, keeping aspect ratio
    img.thumbnail(max_size, Image.LANCZOS)

    # JPEG doesn't support alpha channel — flatten if needed
    if img_format == "JPEG" and img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    buffer = BytesIO()
    img.save(buffer, format=img_format, quality=quality, optimize=True)
    buffer.seek(0)

    original_name = os.path.splitext(image_field.name)[0]
    ext = img_format.lower()

    return InMemoryUploadedFile(
        buffer,
        "ImageField",
        f"{original_name}.{ext}",
        f"image/{ext}",
        sys.getsizeof(buffer),
        None,
    )