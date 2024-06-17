import tkinter as tk
from tkinter import filedialog, simpledialog, ttk
from PIL import Image, ImageTk
import os


class ImageBoundingBoxApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Bounding Box Tool")

        # Style the application
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'))

        # Toolbar frame
        self.toolbar = tk.Frame(self.master, bg="gray")
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Add buttons to toolbar
        self.add_toolbar_buttons()

        # Main frame
        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Side panel frame
        self.side_panel = tk.Frame(master)
        self.side_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create canvas to display images
        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create a scrollable listbox in the side panel
        self.bbox_listbox = tk.Listbox(self.side_panel)
        self.scrollbar = tk.Scrollbar(self.side_panel, orient=tk.VERTICAL)
        self.bbox_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.bbox_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.bbox_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Initialize variables
        self.image_files = []
        self.current_index = 0
        self.current_image = None
        self.bounding_boxes = {}  # Dictionary to hold bounding box coordinates and labels for each image
        self.selected_bbox = None

        # Bind mouse events to draw and select bounding boxes
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        # Bind listbox selection event
        self.bbox_listbox.bind("<<ListboxSelect>>", self.on_bbox_listbox_select)

        # Initial state
        self.drawing = False
        self.bbox_start = None

        # Status bar
        self.status_bar = tk.Label(self.master, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def add_toolbar_buttons(self):
        buttons = [
            ("Open Folder", self.select_folder, "Open a folder containing images."),
            ("Prev Image", self.prev_image, "Go to the previous image."),
            ("Next Image", self.next_image, "Go to the next image."),
            ("Delete BBox", self.delete_selected_bbox, "Delete the selected bounding box."),
            ("Save Data", self.on_done, "Save bounding box data."),
        ]

        for text, command, tooltip in buttons:
            button = ttk.Button(self.toolbar, text=text, command=command)
            button.pack(side=tk.LEFT, padx=5, pady=5)
            button.bind("<Enter>", lambda event, tip=tooltip: self.show_tooltip(event, tip))
            button.bind("<Leave>", self.hide_tooltip)

        # Tooltip label
        self.tooltip_label = tk.Label(self.master, text="", bg="yellow", bd=1, relief=tk.SUNKEN)

    def show_tooltip(self, event, tip):
        x = event.widget.winfo_x() + event.widget.winfo_width() / 2
        y = event.widget.winfo_y() + event.widget.winfo_height() + 10
        self.tooltip_label.config(text=tip)
        self.tooltip_label.place(x=x, y=y)

    def hide_tooltip(self, event):
        self.tooltip_label.place_forget()

    # Implement the rest of the methods for handling images, drawing bounding boxes,
    # updating the bounding box list, saving data, and other necessary features.

    def select_folder(self):
        # Method for selecting a folder containing images
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                                f.endswith(('jpg', 'jpeg', 'png'))]
            self.current_index = 0
            self.load_image()
            self.status_bar.config(text="Folder loaded")

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
                    self.canvas.create_rectangle(bbox["coords"][0], bbox["coords"][1], bbox["coords"][2],
                                                 bbox["coords"][3], outline="red", tag="bbox")
                    # Display label near the bounding box
                    self.canvas.create_text(bbox["coords"][0], bbox["coords"][1] - 10, text=bbox["label"], fill="red",
                                            anchor=tk.SW, tag="bbox_label")

            # Update the bounding box list in the listbox
            self.update_bounding_box_list()

            # Update the status bar
            self.status_bar.config(text=f"Viewing: {image_path}")

    def update_bounding_box_list(self):
        # Method for updating the bounding box list in the listbox
        self.bbox_listbox.delete(0, tk.END)
        image_path = self.image_files[self.current_index]
        if image_path in self.bounding_boxes:
            for idx, bbox in enumerate(self.bounding_boxes[image_path]):
                label = bbox["label"]
                coords = bbox["coords"]
                dimensions = f"({coords[0]}, {coords[1]}) to ({coords[2]}, {coords[3]})"
                self.bbox_listbox.insert(tk.END, f"Bounding Box {idx + 1}: Label='{label}', Dimensions={dimensions}")

    def prev_image(self):
        # Method for navigating to the previous image
        if self.current_index > 0:
            self.current_index -= 1
            self.load_image()
            self.status_bar.config(text=f"Viewing: {self.image_files[self.current_index]}")

    def next_image(self):
        # Method for navigating to the next image
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.load_image()
            self.status_bar.config(text=f"Viewing: {self.image_files[self.current_index]}")

    def redraw_bounding_boxes(self):
        # Method for redrawing bounding boxes
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
        # Method to handle mouse down event
        image_path = self.image_files[self.current_index]
        # Check if the click is within an existing bounding box
        for idx, bbox in enumerate(self.bounding_boxes.get(image_path, [])):
            x1, y1, x2, y2 = bbox["coords"]
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.selected_bbox = idx
                break
        else:
            # Start drawing a new bounding box
            self.drawing = True
            self.bbox_start = (event.x, event.y)

    def on_mouse_drag(self, event):
        # Method to handle mouse drag event
        if self.drawing:
            # Clear previous preview rectangle
            self.canvas.delete("preview")

            # Draw preview rectangle
            self.canvas.create_rectangle(
                self.bbox_start[0], self.bbox_start[1],
                event.x, event.y,
                outline="blue", tag="preview"
            )

    def on_mouse_up(self, event):
        # Method to handle mouse up event
        if self.drawing:
            self.drawing = False
            self.canvas.delete("preview")

            # Add the completed bounding box to the list
            image_path = self.image_files[self.current_index]
            if image_path not in self.bounding_boxes:
                self.bounding_boxes[image_path] = []

            x1, y1 = self.bbox_start
            x2, y2 = event.x, event.y

            # Ask for a label for the new bounding box
            label = simpledialog.askstring("Label", "Enter label for bounding box:")
            if label:
                bbox = {
                    "coords": (x1, y1, x2, y2),
                    "label": label
                }
                self.bounding_boxes[image_path].append(bbox)

                # Redraw all bounding boxes
                self.redraw_bounding_boxes()

                # Update the bounding box list
                self.update_bounding_box_list()

                # Update the status bar
                self.status_bar.config(text="Bounding box added")

    def delete_selected_bbox(self):
        # Method for deleting the selected bounding box
        image_path = self.image_files[self.current_index]
        if image_path in self.bounding_boxes and self.selected_bbox is not None:
            # Remove the selected bounding box from the list
            del self.bounding_boxes[image_path][self.selected_bbox]

            # Clear selection
            self.selected_bbox = None

            # Clear the highlight of the bounding box
            self.canvas.delete("highlight")

            # Clear all existing bounding boxes and labels from the canvas
            self.canvas.delete("bbox")
            self.canvas.delete("bbox_label")

            # Redraw all remaining bounding boxes
            self.redraw_bounding_boxes()

            # Update the bounding box list
            self.update_bounding_box_list()

            # Update the status bar
            self.status_bar.config(text="Bounding box deleted")

    def on_bbox_listbox_select(self, event):
        # Method for handling selection of bounding boxes from the listbox
        selection = event.widget.curselection()
        if selection:
            # Get the index of the selected bounding box
            self.selected_bbox = selection[0]

            # Highlight the selected bounding box in the canvas
            self.canvas.delete("highlight")
            image_path = self.image_files[self.current_index]
            if image_path in self.bounding_boxes:
                bbox = self.bounding_boxes[image_path][self.selected_bbox]
                self.canvas.create_rectangle(
                    bbox["coords"][0],
                    bbox["coords"][1],
                    bbox["coords"][2],
                    bbox["coords"][3],
                    outline="green",
                    tag="highlight"
                )

    def on_done(self):
        # Get the directory where the script is located
        script_directory = os.path.dirname(__file__)

        # Create the dataset and labels folders in the script's directory
        dataset_folder = os.path.join(script_directory, "dataset")
        labels_folder = os.path.join(script_directory, "labels")
        os.makedirs(dataset_folder, exist_ok=True)
        os.makedirs(labels_folder, exist_ok=True)

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
                        # Convert bounding box coordinates to YOLO format
                        img_width, img_height = current_image.size
                        x_center = (coords[0] + coords[2]) / 2 / img_width
                        y_center = (coords[1] + coords[3]) / 2 / img_height
                        width = abs(coords[2] - coords[0]) / img_width
                        height = abs(coords[3] - coords[1]) / img_height
                        # Write bounding box data to the file in YOLO format
                        f.write(f"{label} {x_center} {y_center} {width} {height}\n")

        # Print a message indicating that the task is complete
        self.status_bar.config(text="DONE: Images and bounding box data saved successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageBoundingBoxApp(root)
    root.mainloop()
