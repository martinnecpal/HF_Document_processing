---
title: Document Processing - Brightness Adjuster
emoji: 🌟
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.41.1
app_file: app.py
pinned: false
license: mit
---

# Document Processing - Brightness Adjuster

A simple Gradio app that automatically reformat image.

## Features
- Upload images in various formats (JPG, JPEG, PNG, BMP, TIFF)
- Automatic brightness increase by 50%
- Side-by-side comparison view
- Download processed images

## Usage
1. Upload an image using the file input
2. Click "Adjust Brightness" 
3. View the original and processed images side by side
4. Download the enhanced image

## Technical Details
- Built with Gradio and PIL (Pillow)
- Brightness enhancement factor: 1.5x
- Supports multiple image formats
- Responsive web interface