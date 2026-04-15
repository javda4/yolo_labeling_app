# YOLO Labeling App

THIS PROJECT IS STILL IN DEVELOPMENT


A lightweight GUI tool for quickly labeling images in **YOLO format** and automatically generating the required dataset structure for training object detection models.

This project is designed to simplify the dataset creation process by allowing users to select a folder of images, label objects through an intuitive interface, and automatically generate the necessary annotation files and configuration for YOLO training.

---

## Features

- Simple graphical interface for image labeling
- Select a folder containing images to begin labeling
- Draw bounding boxes around objects
- Automatically generate YOLO `.txt` annotation files
- Automatically generate a `data.yaml` configuration file
- Organizes dataset structure for training
- Lightweight and easy to run locally

---

## Dataset Output Structure


Each labeled image produces a corresponding `.txt` file containing bounding box annotations in YOLO format.

Example label file:

```

0 0.52 0.48 0.32 0.41

```

Format:

```

<class_id> <x_center> <y_center> <width> <height>

````

All values are **normalized between 0 and 1** relative to the image dimensions.

---

## data.yaml Example

The application automatically generates the dataset configuration file required for training.

```yaml
train: dataset/images/train
val: dataset/images/train

nc: 1

names: ["object"]
````

This file can be directly used when training a YOLO model.

---

## Installation

Clone the repository:

```
git clone https://github.com/javda4/yolo_labeling_app.git
cd yolo_labeling_app
```

Install dependencies (if applicable):

```
pip install -r requirements.txt
```

Run the application:

```
python main.py
```

---

## Usage

1. Launch the application
2. Select a folder containing images
3. Navigate through images in the dataset
4. Draw bounding boxes around objects of interest
5. Assign the appropriate class label
6. Save annotations

The program will automatically:

* Generate YOLO `.txt` annotation files
* Organize images and labels into the correct dataset structure
* Create the `data.yaml` file for training

---

## Goal of the Project

The goal of this project is to provide a **minimal and efficient labeling workflow** for building YOLO training datasets without the overhead of large annotation platforms.

It is intended for:

* Rapid dataset creation
* Computer vision experimentation
* Small research projects
* Custom object detection pipelines

---

## Future Improvements

Planned features include:

* Multi-class labeling support
* Dataset splitting (train / validation)
* Keyboard shortcuts for faster labeling
* Bounding box editing
* Export improvements
* Image navigation tools
* Dataset statistics preview

---

## Contributing

Contributions are welcome. Feel free to submit issues, feature requests, or pull requests.

---

## License

This project is open source and available under the MIT License.

---

## Author

Created by **Javda**

GitHub:
https://github.com/javda4

```
```
