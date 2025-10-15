# Document Scanner using OpenCV

A real-time document scanner built with **OpenCV** and **NumPy** that detects, extracts, and warps documents from a live webcam feed, simulating a flatbed scan effect.
This project showcases computer vision techniques such as edge detection, contour detection, perspective transforms, and image preprocessing.

---

## Features

- Real-time document detection from a webcam
- Automatic cropping using contour detection
- Perspective warping for a "scanned" effect
- Preprocessing pipeline (grayscale, blur, canny, dilation, erosion)
- Reordering of contour points for accurate transformation
- Stacked image display for visual debugging

---

## Technologies Used

- Python 3.12
- OpenCV
- NumPy

---

## Project Structure

Document_Scanner
├── doc_scanner.py
├── README.md

---

## Installation

### Prerequisites

- Python 3.x installed
- pip (Python package manager)

### Install dependencies

pip install opencv-python numpy

## How to Run

In the terminal:
python scanner.py

Then:
Show a paper/document to your webcam.
The system will detect the largest 4-point contour.
If successful, it will extract and warp the document to flat perspective.
Press q to exit the window.

## How It Works

Capture Frame: From webcam using OpenCV.

Preprocess Image:
  Convert to grayscale
  Apply Gaussian Blur
  Edge detection using Canny
  Dilation and erosion to close gaps
Find Contours: Extract external contours with 4 corners.
Reorder Points: Ensures consistent corner order (top-left, top-right, bottom-left and bottom-right)
Warp Perspective: Applies a matrix transform to get a top-down view.

Display:
Original frame
Thresholded image
Contour outline
Final warped scan

## To-Do / Ideas for Future

Add functionality to save scanned images as PNG or PDF
Detect and extract multiple documents in a frame
Add GUI using PyQt or Tkinter
Add OCR

## Requirements
opencv-python
numpy

## Author
Jai Kumar
Email: jaikumar913276@gmail.com
GitHub: Iam-Jai-Kumar

## Acknowledgements
OpenCV Team for powerful vision tools
The Python community for awesome support
