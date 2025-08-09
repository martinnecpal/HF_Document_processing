import gradio as gr
import os
import tempfile
import cv2
import numpy as np

# function that calculate lower boun level 
# it was defined experimentaly and means when M as a mean walue of gryscale is 180 then lower bound walue is 130
# when mean walue of gry scale pixels is 90 then lower baund value is 70
def calculate_LowerBound(M):
    # Define the slope (m) and intercept (b)
    m = 2 / 3
    b = 10

    # Calculate B based on M
    B = m * M + b
    return B

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

def change_image(image,lower_bound = 100):

    # Assuming 'image' is your RGB image (shape = (2777, 1903, 3))
    # For example, using a dummy image for demonstration
    # image = np.random.randint(0, 256, (2777, 1903, 3), dtype=np.uint8)

    # Define the range of values for the R, G, or B channels
    upper_bound = 255

    # Create a condition where any channel (R, G, or B) is in the range [50, 255]
    condition = (image[:, :, 0] >= lower_bound) & (image[:, :, 0] <= upper_bound) | \
               (image[:, :, 1] >= lower_bound) & (image[:, :, 1] <= upper_bound) | \
               (image[:, :, 2] >= lower_bound) & (image[:, :, 2] <= upper_bound)

    # Set the RGB value to white where the condition is true
    image[condition] = [255, 255, 255]

    # Now, 'image' has white pixels where any of the R, G, or B channels were in the range [50, 255]
    return image


def process_image(file):
    image = cv2.imread(file.name)  # file is a tempfile._TemporaryFileWrapper
    
    block_images = process_image_in_blocks(image=image) # vrati roylo6ene obraykz na bloky
        
    ch_blocks = [] # will be list of changed blocks 
    for part_image in block_images:
        ll = calculate_LowerBound(np.mean(part_image)) # calculate lower bound od picel which pixels will be removed from image is obtain experimentaly
        changed = change_image(part_image,lower_bound=ll) # remove pixel of lower boud 
        ch_blocks.append(changed) # create new list 

    # Assuming 'ch_blocks' is a list of 25 blocks (e.g., 5x5 grid)
    # Concatenate the blocks horizontally in each row, and then concatenate the rows vertically

    # List to store the rows
    rows = []
    # Loop to concatenate blocks in each row
    for i in range(0, 25, 5):  # Step size of 5 to group the blocks into rows
        row = np.concatenate(ch_blocks[i:i+5], axis=1)  # Concatenate blocks horizontally (axis=1)
        rows.append(row)
    # Concatenate the rows vertically to form the final image
    cc = np.concatenate(rows, axis=0)  # Concatenate along the vertical axis (axis=0)    
    
    image = cc # test to be image OK

    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "bw_image.png")
    cv2.imwrite(file_path, image)
    return image, file_path

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("Home"):
            gr.Markdown("## Welcome to the Home Page")
        with gr.Tab("Settings"):
            gr.Markdown("## Adjust your settings here")
        with gr.Tab("My getting started"):
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