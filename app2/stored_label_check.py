import os
from PIL import Image, ImageDraw, ImageFont

# Define the path to the dataset, labels, and labelcheck folders
script_directory = os.path.dirname(__file__)
dataset_folder = os.path.join(script_directory, "dataset")
labels_folder = os.path.join(script_directory, "labels")
labelcheck_folder = os.path.join(script_directory, "labelcheck")

# Create the labelcheck folder if it doesn't exist
os.makedirs(labelcheck_folder, exist_ok=True)

# Load the font for displaying labels (optional, customize the font path as needed)
font_path = os.path.join(script_directory, "arial.ttf")  # Specify the path to a font file
font = ImageFont.truetype(font_path, size=16) if os.path.exists(font_path) else None

# Process each image in the dataset folder
for filename in os.listdir(dataset_folder):
    # Only process image files
    if filename.endswith(('jpg', 'jpeg', 'png')):
        # Load the image
        image_path = os.path.join(dataset_folder, filename)
        image = Image.open(image_path)

        # Load the label file
        label_file = os.path.join(labels_folder, os.path.splitext(filename)[0] + ".txt")
        if os.path.exists(label_file):
            with open(label_file, "r") as file:
                # Read the bounding box data
                draw = ImageDraw.Draw(image)
                for line in file:
                    # Parse the label and bounding box data
                    parts = line.strip().split()
                    label = parts[0]
                    x_center = float(parts[1])
                    y_center = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])

                    # Calculate the coordinates of the bounding box
                    img_width, img_height = image.size
                    xmin = (x_center - width / 2) * img_width
                    ymin = (y_center - height / 2) * img_height
                    xmax = (x_center + width / 2) * img_width
                    ymax = (y_center + height / 2) * img_height

                    # Draw the bounding box
                    draw.rectangle([(xmin, ymin), (xmax, ymax)], outline="red", width=2)

                    # Draw the label above the bounding box
                    label_position = (xmin, ymin - 20)  # Adjust the position as needed
                    draw.text(label_position, label, fill="red", font=font)

            # Save the image with bounding boxes and labels in the labelcheck folder
            output_path = os.path.join(labelcheck_folder, filename)
            image.save(output_path)

print("DONE: Processed images saved to 'labelcheck' folder.")
