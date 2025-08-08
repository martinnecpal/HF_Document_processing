import gradio as gr
import os
from PIL import Image, ImageEnhance
import uuid
import tempfile
import cv2
import numpy as np

# Function to process the image by dividing it into blocks and returns 25 blocks of image
def process_image_in_blocks(image, rows=5, cols=5):
    blocks = []
    height, width = image.shape[:2]

    # Calculate the size of each block
    block_height = height // rows
    block_width = width // cols

    # Create an empty array to store the processed image
    processed_image = np.zeros_like(image)

    for i in range(rows):
        for j in range(cols):
            # Extract each block from the image
            y_start = i * block_height
            y_end = (i + 1) * block_height if i != rows - 1 else height
            x_start = j * block_width
            x_end = (j + 1) * block_width if j != cols - 1 else width

            block = image[y_start:y_end, x_start:x_end]
            blocks.append(block)
            #cv2.imwrite(f'block.png{i},{j}.png', block) ## prepare to save image to see it
    return blocks

def process_image(file):
    image = cv2.imread(file.name)  # file is a tempfile._TemporaryFileWrapper
    
    blosks_images = process_image_in_blocks(image=image) # vrati roylo6ene obraykz na bloky
    image = blosks_images[5] # test ci vrati len blok a da do image
    
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "bw_image.png")
    cv2.imwrite(file_path, image)
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