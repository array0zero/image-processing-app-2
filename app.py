"""Streamlit app for trying basic image processing operations."""

from __future__ import annotations

import streamlit as st

from src.processing import (
    apply_gaussian_blur,
    apply_threshold,
    convert_to_grayscale,
    detect_contours,
    detect_edges,
    resize_image,
)
from src.utils import encode_png, image_for_display, load_image_from_upload, make_output_filename


st.set_page_config(
    page_title="Image Processing App 2",
    page_icon="🖼️",
    layout="wide",
)

st.title("Image Processing App 2")
st.write(
    "Upload an image, choose a basic image processing operation, "
    "adjust parameters, and compare the result with the original image."
)

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"],
)

operation = st.sidebar.selectbox(
    "Select processing operation",
    [
        "Resize",
        "Grayscale",
        "Gaussian Blur",
        "Thresholding",
        "Canny Edge Detection",
        "Contour Detection",
    ],
)

st.sidebar.header("Parameters")

if uploaded_file is None:
    st.info("Please upload a PNG or JPG image to start.")
    st.stop()

try:
    original_image = load_image_from_upload(uploaded_file)
except ValueError as error:
    st.error(str(error))
    st.stop()

processed_image = original_image.copy()
contour_summary = None

if operation == "Resize":
    scale_percent = st.sidebar.slider("Scale (%)", min_value=10, max_value=200, value=100, step=10)
    processed_image = resize_image(original_image, scale_percent)

elif operation == "Grayscale":
    processed_image = convert_to_grayscale(original_image)

elif operation == "Gaussian Blur":
    kernel_size = st.sidebar.slider("Kernel size", min_value=1, max_value=31, value=5, step=2)
    sigma = st.sidebar.slider("Sigma", min_value=0.0, max_value=10.0, value=0.0, step=0.5)
    processed_image = apply_gaussian_blur(original_image, kernel_size=kernel_size, sigma=sigma)

elif operation == "Thresholding":
    threshold_value = st.sidebar.slider("Threshold value", min_value=0, max_value=255, value=127)
    processed_image = apply_threshold(original_image, threshold_value=threshold_value)

elif operation == "Canny Edge Detection":
    threshold1 = st.sidebar.slider("Threshold 1", min_value=0, max_value=255, value=100)
    threshold2 = st.sidebar.slider("Threshold 2", min_value=0, max_value=255, value=200)
    processed_image = detect_edges(original_image, threshold1=threshold1, threshold2=threshold2)

elif operation == "Contour Detection":
    threshold_value = st.sidebar.slider("Threshold value", min_value=0, max_value=255, value=127)
    min_area = st.sidebar.slider("Minimum contour area", min_value=0, max_value=10000, value=100, step=50)
    processed_image, contour_summary = detect_contours(
        original_image,
        threshold_value=threshold_value,
        min_area=float(min_area),
    )

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Original image")
    st.image(image_for_display(original_image), use_container_width=True)
    st.caption(f"Shape: {original_image.shape}")

with right_col:
    st.subheader("Processed image")
    st.image(image_for_display(processed_image), use_container_width=True)
    st.caption(f"Shape: {processed_image.shape}")

if contour_summary is not None:
    st.subheader("Contour summary")
    metric_cols = st.columns(4)
    metric_cols[0].metric("Count", contour_summary.count)
    metric_cols[1].metric("Min area", f"{contour_summary.min_area:.1f}")
    metric_cols[2].metric("Max area", f"{contour_summary.max_area:.1f}")
    metric_cols[3].metric("Mean area", f"{contour_summary.mean_area:.1f}")

st.divider()

output_filename = make_output_filename(uploaded_file.name, operation)
st.download_button(
    label="Download processed image",
    data=encode_png(processed_image),
    file_name=output_filename,
    mime="image/png",
)
