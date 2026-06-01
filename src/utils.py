"""Helper functions for file conversion, display, and downloads."""

from __future__ import annotations

import re
from pathlib import Path

import cv2
import numpy as np


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def load_image_from_upload(uploaded_file) -> np.ndarray:
    """Convert a Streamlit UploadedFile into an OpenCV BGR image."""
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not read the uploaded image. Please upload a PNG or JPG file.")
    return image


def image_for_display(image: np.ndarray) -> np.ndarray:
    """Convert an OpenCV image into a format suitable for st.image."""
    if image.ndim == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def encode_png(image: np.ndarray) -> bytes:
    """Encode a grayscale or BGR OpenCV image as PNG bytes."""
    success, buffer = cv2.imencode(".png", image)
    if not success:
        raise ValueError("Failed to encode image as PNG.")
    return buffer.tobytes()


def make_output_filename(original_filename: str, operation_name: str) -> str:
    """Create a safe output filename for a processed image."""
    stem = Path(original_filename).stem
    safe_stem = re.sub(r"[^A-Za-z0-9_-]+", "_", stem).strip("_") or "image"
    safe_operation = re.sub(r"[^A-Za-z0-9_-]+", "_", operation_name.lower()).strip("_")
    return f"{safe_stem}_{safe_operation}.png"
