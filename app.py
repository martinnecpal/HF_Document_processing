import gradio as gr
import os
from PIL import Image, ImageEnhance
import uuid
import tempfile

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
    
    with gr.Row():
        with gr.Column():
            original_image = gr.Image(label="Original Image", width=300, height=300)
        with gr.Column():
            result_image = gr.Image(label="Processed Image (Brightness +50%)", width=300, height=300)
    
    with gr.Row():
        download_output = gr.File(label="Download Processed Image")

    process_button.click(
        fn=adjust_brightness_and_display,
        inputs=[file_input],
        outputs=[original_image, result_image, download_output]
    )

if __name__ == "__main__":
    demo.launch()