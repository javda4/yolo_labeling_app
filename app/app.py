import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import os

# Class definition
class ImageBoundingBoxApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Bounding Box app")

        # Frame for the main window
        frame = tk.Frame(master)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Side panel frame
        self.side_panel = tk.Frame(master)
        self.side_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Button to select a folder
        self.select_folder_btn = tk.Button(frame, text="Select Folder", command=self.select_folder)
        self.select_folder_btn.pack()

        # Create canvas to display images
        self.canvas = tk.Canvas(frame, width=800, height=600)
        self.canvas.pack()

        # Initialize variables
        self.image_files = []
        self.current_index = 0
        self.current_image = None
        self.bounding_boxes = {}  # Dictionary to hold bounding box coordinates and labels for each image
        self.selected_bbox = None  # Track the currently selected bounding box

        # Create buttons to navigate images
        self.prev_btn = tk.Button(frame, text="Previous", command=self.prev_image)
        self.prev_btn.pack(side=tk.LEFT)

        self.next_btn = tk.Button(frame, text="Next", command=self.next_image)
        self.next_btn.pack(side=tk.LEFT)

        # Add a button to delete the selected bounding box
        self.delete_btn = tk.Button(frame, text="Delete Bounding Box", command=self.delete_selected_bbox)
        self.delete_btn.pack(side=tk.LEFT)

        # Add the "DONE" button to create dataset and labels folders
        self.done_btn = tk.Button(frame, text="DONE", command=self.on_done)
        self.done_btn.pack(side=tk.RIGHT)

        # Add a listbox to the side panel to display bounding box information
        self.bbox_listbox = tk.Listbox(self.side_panel)
        self.bbox_listbox.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events to draw and select bounding boxes
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        # Bind listbox selection event
        self.bbox_listbox.bind("<<ListboxSelect>>", self.on_bbox_listbox_select)

        # Initial state
        self.drawing = False
        self.bbox_start = None

        # Add a message widget to display status messages
        self.status_message = tk.Message(frame, text="", width=200)
        self.status_message.pack(side=tk.BOTTOM)

    def select_folder(self):
        # Open file dialog to select a folder
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('jpg', 'jpeg', 'png'))]
            self.current_index = 0
            self.load_image()

    def load_image(self):
        # Clear existing bounding boxes from the canvas
        self.canvas.delete("bbox")

        if self.image_files:
            image_path = self.image_files[self.current_index]
            self.current_image = Image.open(image_path)
            self.photo_image = ImageTk.PhotoImage(self.current_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

            # Draw existing bounding boxes and labels for the current image
            if image_path in self.bounding_boxes:
                for bbox in self.bounding_boxes[image_path]:
                    # Draw bounding box
                    self.canvas.create_rectangle(bbox["coords"][0], bbox["coords"][1], bbox["coords"][2], bbox["coords"][3], outline="red", tag="bbox")
                    # Display label near the bounding box
                    self.canvas.create_text(bbox["coords"][0], bbox["coords"][1] - 10, text=bbox["label"], fill="red", anchor=tk.SW, tag="bbox_label")

            # Update the bounding box list in the listbox
            self.update_bounding_box_list()

    def update_bounding_box_list(self):
        # Update the bounding box list in the listbox
        self.bbox_listbox.delete(0, tk.END)
        image_path = self.image_files[self.current_index]
        if image_path in self.bounding_boxes:
            for idx, bbox in enumerate(self.bounding_boxes[image_path]):
                label = bbox["label"]
                coords = bbox["coords"]
                dimensions = f"({coords[0]}, {coords[1]}) to ({coords[2]}, {coords[3]})"
                self.bbox_listbox.insert(tk.END, f"Bounding Box {idx + 1}: Label='{label}', Dimensions={dimensions}")

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_image()

    def next_image(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.load_image()

    def redraw_bounding_boxes(self):
        image_path = self.image_files[self.current_index]
        if image_path in self.bounding_boxes:
            for bbox in self.bounding_boxes[image_path]:
                # Draw bounding box
                self.canvas.create_rectangle(
                    bbox["coords"][0],
                    bbox["coords"][1],
                    bbox["coords"][2],
                    bbox["coords"][3],
                    outline="red",
                    tag="bbox"
                )
                # Display label near the bounding box
                self.canvas.create_text(
                    bbox["coords"][0],
                    bbox["coords"][1] - 10,
                    text=bbox["label"],
                    fill="red",
                    anchor=tk.SW,
                    tag="bbox_label"
                    )

    def on_mouse_down(self, event):
        image_path = self.image_files[self.current_index]
        # Check if the click is within an existing bounding box
        for idx, bbox in enumerate(self.bounding_boxes.get(image_path, [])):
            coords = bbox["coords"]
            if coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3]:
                # Select the bounding box
                self.selected_bbox = bbox
                # Change the color of the selected bounding box for visibility
                self.canvas.delete("bbox")
                self.load_image()  # Redraw bounding boxes
                self.canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], outline="blue", width=2, tag="bbox")  # Highlight with blue
                # Highlight the selected bounding box in the listbox
                self.bbox_listbox.select_set(idx)
                return

        # If not within an existing bounding box, start drawing a new bounding box
        self.drawing = True
        self.bbox_start = (event.x, event.y)

    def on_mouse_drag(self, event):
        # Update the current bounding box
        if self.drawing:
            self.canvas.delete("bbox")
            # Redraw all bounding boxes and labels to avoid losing them
            image_path = self.image_files[self.current_index]
            if image_path in self.bounding_boxes:
                for bbox in self.bounding_boxes[image_path]:
                    # Draw bounding box
                    self.canvas.create_rectangle(bbox["coords"][0], bbox["coords"][1], bbox["coords"][2], bbox["coords"][3], outline="red", tag="bbox")
                    # Display label near the bounding box
                    self.canvas.create_text(bbox["coords"][0], bbox["coords"][1] - 10, text=bbox["label"], fill="red", anchor=tk.SW, tag="bbox_label")

            # Draw the new bounding box being created
            self.canvas.create_rectangle(self.bbox_start[0], self.bbox_start[1], event.x, event.y, outline="red", tag="bbox")

    def on_mouse_up(self, event):
        if self.drawing:
            self.drawing = False
            bbox_end = (event.x, event.y)
            # Prompt user for label
            label = simpledialog.askstring("Label", "Enter label for bounding box:", parent=self.master)

            if label is None or label.strip() == "":
                # If the user cancels the input or provides an empty label, remove the temporary bounding box and redraw existing ones
                self.canvas.delete("bbox")
                self.redraw_bounding_boxes()
                return

            # Add bounding box and label if the user provided a label
            image_path = self.image_files[self.current_index]
            if image_path not in self.bounding_boxes:
                self.bounding_boxes[image_path] = []

            self.bounding_boxes[image_path].append({
                "coords": (self.bbox_start[0], self.bbox_start[1], bbox_end[0], bbox_end[1]),
                "label": label
            })

            # Draw the bounding box and label on the canvas
            self.canvas.create_rectangle(self.bbox_start[0], self.bbox_start[1], bbox_end[0], bbox_end[1], outline="red", tag="bbox")
            self.canvas.create_text(self.bbox_start[0], self.bbox_start[1] - 10, text=label, fill="red", anchor=tk.SW, tag="bbox_label")

            # Update the bounding box list in the listbox
            self.update_bounding_box_list()

    def on_bbox_listbox_select(self, event):
        # Retrieve the index of the selected bounding box from the listbox
        selection = self.bbox_listbox.curselection()
        if selection:
            index = selection[0]  # There should only be one item selected

            # Get the image path
            image_path = self.image_files[self.current_index]

            # Select the corresponding bounding box
            if image_path in self.bounding_boxes:
                # Retrieve the selected bounding box
                self.selected_bbox = self.bounding_boxes[image_path][index]

                # Highlight the selected bounding box on the canvas
                coords = self.selected_bbox["coords"]
                self.canvas.delete("bbox")
                self.load_image()  # Redraw bounding boxes
                self.canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], outline="blue", width=2, tag="bbox")  # Highlight with blue

    def delete_selected_bbox(self):
        # Delete the selected bounding box
        if self.selected_bbox:
            # Remove the selected bounding box from the dictionary
            image_path = self.image_files[self.current_index]
            if image_path in self.bounding_boxes:
                self.bounding_boxes[image_path].remove(self.selected_bbox)
                self.selected_bbox = None

                # Update the bounding box list in the listbox
                self.update_bounding_box_list()

                # Redraw all bounding boxes
                self.redraw_bounding_boxes()

    def on_done(self):
        # Get the directory where the script is located
        script_directory = os.path.dirname(__file__)

        # Create the dataset and labels folders in the script's directory
        dataset_folder = os.path.join(script_directory, "dataset")
        labels_folder = os.path.join(script_directory, "labels")
        os.makedirs(dataset_folder, exist_ok=True)
        os.makedirs(labels_folder, exist_ok=True)

        # Initialize a set to store unique class names
        class_names = set()

        # Save images and bounding box data
        for image_path in self.image_files:
            # Check if the current image has bounding boxes
            if image_path in self.bounding_boxes and self.bounding_boxes[image_path]:
                # Save the current image to the dataset folder
                filename = os.path.basename(image_path)
                dataset_path = os.path.join(dataset_folder, filename)
                current_image = Image.open(image_path)
                current_image.save(dataset_path)

                # Save bounding box data in YOLO format
                label_path = os.path.join(labels_folder, os.path.splitext(filename)[0] + ".txt")
                with open(label_path, "w") as f:
                    for bbox in self.bounding_boxes[image_path]:
                        label = bbox["label"]
                        coords = bbox["coords"]
                        class_names.add(label)
                        # Convert bounding box coordinates to YOLO format
                        img_width, img_height = current_image.size
                        x_center = (coords[0] + coords[2]) / 2 / img_width
                        y_center = (coords[1] + coords[3]) / 2 / img_height
                        width = abs(coords[2] - coords[0]) / img_width
                        height = abs(coords[3] - coords[1]) / img_height
                        # Write bounding box data to the file in YOLO format
                        f.write(f"{label} {x_center} {y_center} {width} {height}\n")

        # Create data.yaml file
        class_names = sorted(class_names)  # Sort class names
        data_yaml_path = os.path.join(script_directory, "data.yaml")
        with open(data_yaml_path, "w") as yaml_file:
            yaml_file.write("# Define the paths to the training, validation, and test data\n")
            yaml_file.write("train: /path/to/train/images  # Path to training images\n")
            yaml_file.write("val: /path/to/val/images      # Path to validation images\n")
            yaml_file.write("test: /path/to/test/images    # Path to test images (optional)\n\n")
            yaml_file.write("# Define the names and indices of the classes (labels)\n")
            yaml_file.write("names:\n")
            for idx, class_name in enumerate(class_names):
                yaml_file.write(f"  {idx}: \"{class_name}\"\n")
            yaml_file.write("\n# Define the number of classes\n")
            yaml_file.write(
                f"nc: {len(class_names)}  # Number of classes (update this according to your dataset)\n")

        self.status_message.config(text="Dataset and labels have been made.")

        # Print a message indicating that the task is complete
        print("DONE: Images and bounding box data saved successfully.")


# Main function
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageBoundingBoxApp(root)
    root.mainloop()
