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
    page_title="画像処理アプリ",
    page_icon="🖼️",
    layout="wide",
)

st.title("画像処理アプリ")
st.write(
    "画像をアップロードし、基本的な画像処理を選択して実行できます。"
    "元画像と処理後の画像を比較し、結果画像をダウンロードできます。"
)

uploaded_file = st.file_uploader(
    "画像をアップロードしてください",
    type=["png", "jpg", "jpeg"],
)

operation = st.sidebar.selectbox(
    "画像処理を選択",
    [
        "リサイズ（Resize）",
        "グレースケール（Grayscale）",
        "ガウシアンブラー（Gaussian Blur）",
        "しきい値処理（Thresholding）",
        "エッジ検出（Canny Edge Detection）",
        "輪郭検出（Contour Detection）",
    ],
)

st.sidebar.header("パラメータ設定")

if uploaded_file is None:
    st.info("PNG または JPG 画像をアップロードしてください。")
    st.stop()

try:
    original_image = load_image_from_upload(uploaded_file)
except ValueError as error:
    st.error(str(error))
    st.stop()

processed_image = original_image.copy()
contour_summary = None

if operation == "リサイズ（Resize）":
    scale_percent = st.sidebar.slider(
        "拡大・縮小率（%）",
        min_value=10,
        max_value=200,
        value=100,
        step=10,
    )
    processed_image = resize_image(original_image, scale_percent)

elif operation == "グレースケール（Grayscale）":
    processed_image = convert_to_grayscale(original_image)

elif operation == "ガウシアンブラー（Gaussian Blur）":
    kernel_size = st.sidebar.slider(
        "カーネルサイズ",
        min_value=1,
        max_value=31,
        value=5,
        step=2,
    )
    sigma = st.sidebar.slider(
        "ぼかしの強さ（Sigma）",
        min_value=0.0,
        max_value=10.0,
        value=0.0,
        step=0.5,
    )
    processed_image = apply_gaussian_blur(
        original_image,
        kernel_size=kernel_size,
        sigma=sigma,
    )

elif operation == "しきい値処理（Thresholding）":
    threshold_value = st.sidebar.slider(
        "しきい値",
        min_value=0,
        max_value=255,
        value=127,
    )
    processed_image = apply_threshold(
        original_image,
        threshold_value=threshold_value,
    )

elif operation == "エッジ検出（Canny Edge Detection）":
    threshold1 = st.sidebar.slider(
        "しきい値1",
        min_value=0,
        max_value=255,
        value=100,
    )
    threshold2 = st.sidebar.slider(
        "しきい値2",
        min_value=0,
        max_value=255,
        value=200,
    )
    processed_image = detect_edges(
        original_image,
        threshold1=threshold1,
        threshold2=threshold2,
    )

elif operation == "輪郭検出（Contour Detection）":
    threshold_value = st.sidebar.slider(
        "しきい値",
        min_value=0,
        max_value=255,
        value=127,
    )
    min_area = st.sidebar.slider(
        "最小輪郭面積",
        min_value=0,
        max_value=10000,
        value=100,
        step=50,
    )
    processed_image, contour_summary = detect_contours(
        original_image,
        threshold_value=threshold_value,
        min_area=float(min_area),
    )

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("元画像")
    st.image(image_for_display(original_image), use_container_width=True)
    st.caption(f"画像サイズ: {original_image.shape}")

with right_col:
    st.subheader("処理後の画像")
    st.image(image_for_display(processed_image), use_container_width=True)
    st.caption(f"画像サイズ: {processed_image.shape}")

if contour_summary is not None:
    st.subheader("輪郭検出の結果")
    metric_cols = st.columns(4)
    metric_cols[0].metric("輪郭数", contour_summary.count)
    metric_cols[1].metric("最小面積", f"{contour_summary.min_area:.1f}")
    metric_cols[2].metric("最大面積", f"{contour_summary.max_area:.1f}")
    metric_cols[3].metric("平均面積", f"{contour_summary.mean_area:.1f}")

st.divider()

output_filename = make_output_filename(uploaded_file.name, operation)
st.download_button(
    label="処理後の画像をダウンロード",
    data=encode_png(processed_image),
    file_name=output_filename,
    mime="image/png",
)