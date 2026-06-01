"""Image processing functions used by the Streamlit app.

All functions receive an OpenCV image represented as a NumPy array.
Color images are assumed to be in BGR order, which is OpenCV's default.
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class ContourSummary:
    """Simple summary for detected contours."""

    count: int
    min_area: float
    max_area: float
    mean_area: float


def _to_grayscale(image: np.ndarray) -> np.ndarray:
    """Return a grayscale version of a BGR or grayscale image."""
    if image.ndim == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def _ensure_odd(value: int) -> int:
    """OpenCV Gaussian kernels must be odd and greater than zero."""
    value = max(1, int(value))
    return value if value % 2 == 1 else value + 1


def resize_image(image: np.ndarray, scale_percent: int) -> np.ndarray:
    """Resize an image by percentage while keeping the aspect ratio."""
    scale = max(1, int(scale_percent)) / 100
    height, width = image.shape[:2]
    new_size = (max(1, int(width * scale)), max(1, int(height * scale)))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert a color image to grayscale."""
    return _to_grayscale(image)


def apply_gaussian_blur(
    image: np.ndarray,
    kernel_size: int = 5,
    sigma: float = 0,
) -> np.ndarray:
    """Apply Gaussian blur to reduce noise or soften an image."""
    kernel = _ensure_odd(kernel_size)
    return cv2.GaussianBlur(image, (kernel, kernel), sigmaX=sigma)


def apply_threshold(
    image: np.ndarray,
    threshold_value: int = 127,
    max_value: int = 255,
) -> np.ndarray:
    """Apply binary thresholding to a grayscale version of the image."""
    gray = _to_grayscale(image)
    _, thresholded = cv2.threshold(gray, threshold_value, max_value, cv2.THRESH_BINARY)
    return thresholded


def detect_edges(
    image: np.ndarray,
    threshold1: int = 100,
    threshold2: int = 200,
) -> np.ndarray:
    """Detect edges using the Canny edge detector."""
    gray = _to_grayscale(image)
    return cv2.Canny(gray, threshold1, threshold2)


def detect_contours(
    image: np.ndarray,
    threshold_value: int = 127,
    min_area: float = 0,
) -> tuple[np.ndarray, ContourSummary]:
    """Detect contours and draw them on a copy of the original image.

    Returns:
        A tuple of ``(drawn_image, summary)``.
    """
    gray = _to_grayscale(image)
    _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = [c for c in contours if cv2.contourArea(c) >= min_area]
    output = image.copy() if image.ndim == 3 else cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(output, filtered_contours, contourIdx=-1, color=(0, 255, 0), thickness=2)

    areas = [float(cv2.contourArea(c)) for c in filtered_contours]
    if areas:
        summary = ContourSummary(
            count=len(areas),
            min_area=min(areas),
            max_area=max(areas),
            mean_area=sum(areas) / len(areas),
        )
    else:
        summary = ContourSummary(count=0, min_area=0.0, max_area=0.0, mean_area=0.0)

    return output, summary
