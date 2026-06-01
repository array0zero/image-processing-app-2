# image-processing-app-2

A simple Streamlit/OpenCV app for trying basic image processing operations.

## Overview

`image-processing-app-2` is a personal portfolio project for practicing how to build a small image processing application with clear input, processing, and output steps.

This app lets users upload an image, choose a basic image processing operation, adjust parameters, compare the original and processed images, and download the result.

## Purpose

This repository is intended for a job-hunting portfolio. Instead of publishing research code directly, this project demonstrates related image processing skills in a public and easy-to-explain application.

The project focuses on:

- Organizing input, processing, and output steps
- Separating application code and image processing functions
- Building a usable Streamlit app
- Keeping the structure easy to extend later
- Writing a README that explains the purpose, setup, and usage clearly

## Features

Current MVP features:

- Upload PNG/JPG images
- Select an image processing operation
- Adjust parameters from the sidebar
- Display original and processed images side by side
- Download the processed image as a PNG file

Supported image processing operations:

- Resize
- Grayscale
- Gaussian Blur
- Thresholding
- Canny Edge Detection
- Contour Detection

## Tech Stack

- Python
- OpenCV
- NumPy
- Pillow
- Streamlit
- Git / GitHub

## Directory Structure

```text
image-processing-app-2/
├── README.md
├── app.py
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── processing.py
│   └── utils.py
├── samples/
│   ├── input/
│   └── output/
└── assets/
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/image-processing-app-2.git
cd image-processing-app-2
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## How to Run

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal.

## Basic Usage

1. Upload a PNG or JPG image.
2. Select an image processing operation from the sidebar.
3. Adjust the parameters.
4. Compare the original and processed images.
5. Download the processed image if needed.

## Processing Flow

```text
Uploaded image
    ↓
Convert to OpenCV image
    ↓
Select processing method
    ↓
Apply image processing function
    ↓
Display result in Streamlit
    ↓
Download processed image
```

## Implementation Notes

- `app.py` handles the Streamlit user interface.
- `src/processing.py` contains image processing functions.
- `src/utils.py` contains helper functions for image loading, display conversion, encoding, and filenames.
- OpenCV uses BGR color order, so images are converted to RGB before display in Streamlit.
- Processing functions are separated from the UI to make the project easier to test and extend.

## Future Improvements

Planned improvements:

- Add sample input/output images
- Add screenshots to this README
- Add histogram visualization
- Add contour area and perimeter analysis
- Add batch processing for multiple images
- Add ZIP download for multiple processed images
- Add unit tests for processing functions
- Add optional machine learning features with PyTorch