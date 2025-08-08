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

with gr.Blocks() as demo:
    gr.Markdown("## Upload an image, adjust brightness, and download the result")
    
    with gr.Row():
            cv_adjust = gr.Button('cv', variant="primary")

    with gr.Row():
        cv_file_input = gr.File(label="Upload an image")
        cv_image_output = gr.Image(type="numpy", width=300, height=300)   
        fileoutput = gr.File(label="Dovnlosad processed file") 

    cv_adjust.click(
        fn = process_image,
        inputs = cv_file_input,
        outputs = [cv_image_output, fileoutput]
    )

if __name__ == "__main__":
    demo.launch()