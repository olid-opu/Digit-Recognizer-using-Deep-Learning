import base64
import io
import numpy as np
from PIL import Image, ImageOps


def _center_and_resize_digit(image: Image.Image) -> Image.Image:
    image_array = np.array(image)
    mask = image_array > 20

    if not np.any(mask):
        return Image.new("L", (28, 28), 0)

    ys, xs = np.where(mask)
    top, bottom = ys.min(), ys.max()
    left, right = xs.min(), xs.max()
    cropped = image.crop((left, top, right + 1, bottom + 1))

    width, height = cropped.size
    side = max(width, height)
    square = Image.new("L", (side, side), 0)
    offset = ((side - width) // 2, (side - height) // 2)
    square.paste(cropped, offset)

    resized = square.resize((20, 20), Image.Resampling.LANCZOS)
    canvas = Image.new("L", (28, 28), 0)
    canvas.paste(resized, (4, 4))
    return canvas


def preprocess_base64_image(base64_string: str) -> np.ndarray:
    # Remove header like: data:image/png;base64,...
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]

    image_data = base64.b64decode(base64_string, validate=True)
    image = Image.open(io.BytesIO(image_data)).convert("L")

    # Auto-invert only when background is light; black-canvas drawings should stay as-is.
    border_pixels = np.concatenate(
        [
            np.array(image)[0, :],
            np.array(image)[-1, :],
            np.array(image)[:, 0],
            np.array(image)[:, -1],
        ]
    )
    if border_pixels.mean() > 127:
        image = ImageOps.invert(image)

    image = _center_and_resize_digit(image)

    # Convert to numpy
    image_array = np.array(image, dtype=np.float32)

    # Normalize to 0-1
    image_array = image_array / 255.0

    # Reshape to (1, 1, 28, 28)
    image_array = image_array.reshape(1, 1, 28, 28)

    return image_array