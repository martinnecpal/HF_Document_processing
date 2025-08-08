import gradio as gr
import os
from PIL import Image, ImageEnhance
import uuid
import tempfile
import cv2
import numpy as np

def process_image(file):
    image = cv2.imread(file.name)  # file is a tempfile._TemporaryFileWrapper
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "bw_image.png")
    cv2.imwrite(file_path, gray)
    return image, file_path

def adjust_brightness_and_display(image_file):
    if image_file is None:
        return "No image uploaded", None, None, None
    
    try:
        # Open the uploaded image
        img = Image.open(image_file.name)
        
        # Adjust brightness with default factor of 1.5
        brightness_factor = 1.5
        enhancer = ImageEnhance.Brightness(img)
        brightened_img = enhancer.enhance(brightness_factor)
        
        # Create a temporary file for the processed image
        session_id = str(uuid.uuid4())
        temp_dir = tempfile.gettempdir()
        output_filename = f"brightness_adjusted_{session_id}.jpg"
        output_path = os.path.join(temp_dir, output_filename)
        
        # Save the processed image
        brightened_img.save(output_path, "JPEG", quality=95)
        
        
        return img, brightened_img, output_path
        
    except Exception as e:
        return f"Error processing image: {str(e)}", None, None, None

with gr.Blocks() as demo:
    gr.Markdown("## Upload an image, adjust brightness, and download the result")
    
    with gr.Row():
        with gr.Column():
            file_input = gr.File(
                label="Upload Image", 
                file_types=[".jpg", ".jpeg", ".png", ".bmp", ".tiff"], 
                file_count="single"
            )
            process_button = gr.Button("Adjust Brightness", variant="primary")
            cv_adjust = gr.Button('cv', variant="primary")
    
    with gr.Row():
        with gr.Column():
            original_image = gr.Image(label="Original Image", width=300, height=300)
        with gr.Column():
            result_image = gr.Image(label="Processed Image (Brightness +50%)", width=300, height=300)
    
    with gr.Row():
        download_output = gr.File(label="Download Processed Image")

    with gr.Row():
        cv_file_input = gr.File(label="Upload an image")
        cv_image_output = gr.Image(type="numpy", width=300, height=300)   
        fileoutput = gr.File(label="Dovnlosad processed file") 

    cv_adjust.click(
        fn = process_image,
        inputs = cv_file_input,
        outputs = [cv_image_output, fileoutput]
    )

    process_button.click(
        fn=adjust_brightness_and_display,
        inputs=file_input,
        outputs=[original_image, result_image, download_output]
    )

if __name__ == "__main__":
    demo.launch()