import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

class ImageProcessor:
    def __init__(self, img):
        self.img = img

    def calculate_histogram(self):
        hist = cv2.calcHist([self.img], [0], None, [256], [0, 256])
        plt.plot(hist)
        plt.title("Histogram")
        plt.show()

    def thresholding(self):
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        tresh_choice = simpledialog.askstring("Thresholding", "1. Thresholding\n2. Adaptive Thresholding\nEnter your choice:")
        if tresh_choice == "1":
            value = simpledialog.askstring("Thresholding", "Enter Thresholding value:")
            ret, thresh1 = cv2.threshold(img_gray, int(value), 255, cv2.THRESH_BINARY)
            ret, thresh2 = cv2.threshold(img_gray, int(value), 255, cv2.THRESH_BINARY_INV)
            cv2.imshow('Binary Threshold', thresh1)
            cv2.imshow('Binary Threshold Inverted', thresh2)
            cv2.waitKey(0)
        elif tresh_choice == "2":
            print("Adaptive Thresholding")
            thresh1 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 4)
            thresh2 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 4)
            cv2.imshow('Adaptive Thresholding Binary', thresh2)
            cv2.imshow('Adaptive Thresholding Binary Inverted', thresh1)
            cv2.waitKey(0)
        else:
            print("Not found")

    def resize(self, scale_percent):
        width = int(self.img.shape[1] * int(scale_percent) / 100)
        height = int(self.img.shape[0] * int(scale_percent) / 100)
        dim = (width, height)
        img_resized = cv2.resize(self.img, dim, interpolation=cv2.INTER_NEAREST)
        self.img = img_resized
        self.display_image()

    def blurring(self, blur_choice, k1=None, k2=None):
        if blur_choice == "1":
            img_blurred = cv2.blur(self.img, (int(k1), int(k2)))
        elif blur_choice == "2":
            img_blurred = cv2.medianBlur(self.img, int(k1))
        elif blur_choice == "3":
            img_blurred = cv2.GaussianBlur(self.img, (5, 5), 0)
        else:
            print("Not found")
            return

        cv2.imshow("Blurred Image", img_blurred)
        cv2.waitKey(0)

    def color_conversion(self, color_choice):
        if color_choice == "1":
            img_converted = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        elif color_choice == "2":
            img_converted = cv2.cvtColor(self.img, cv2.COLOR_BGR2LAB)
        elif color_choice == "3":
            img_converted = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        else:
            print("Not found")
            return

        cv2.imshow("Converted Image", img_converted)
        cv2.waitKey(0)

    def contours(self, contours_choice, thresh_min=None, thresh_max=None):
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        if contours_choice == "1":
            img_contours = cv2.Canny(img_gray, int(thresh_min), int(thresh_max))
        elif contours_choice == "2":
            ret, thresh_img = cv2.threshold(img_gray, int(thresh_min), 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            img_contours = np.zeros(self.img.shape)
            img_contours = cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3)
        else:
            print("Not found")
            return

        cv2.imshow("Contours Image", img_contours)
        cv2.waitKey(0)

    def display_image(self):
        img_display = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        img_display = Image.fromarray(img_display)
        img_display = ImageTk.PhotoImage(img_display)
        image_label.config(image=img_display)
        image_label.image = img_display

def main():
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    img = cv2.imread(image_path)

    if img is None:
        print("Image not loaded.")
        return

    image_processor = ImageProcessor(img)

    root = tk.Tk()
    root.title("Advanced Image Processing App")
    root.geometry("800x600")

    image_label = tk.Label(root)
    image_label.pack(pady=10)

    operations_label = tk.Label(root, text="Choose an operation:")
    operations_label.pack()

    operations_var = tk.StringVar()
    operations_var.set("1")  # Default to the Calculate Histogram operation
    operations_menu = tk.OptionMenu(root, operations_var, "1", "2", "3", "4", "5", "6", "7")
    operations_menu.pack(pady=10)

    execute_button = tk.Button(root, text="Execute Operation", command=lambda: execute_operation(image_processor, operations_var.get()))
    execute_button.pack(pady=10)

    quit_button = tk.Button(root, text="Quit", command=root.destroy)
    quit_button.pack(pady=10)

    image_processor.display_image()

    root.mainloop()

def execute_operation(image_processor, operation_choice):
    if operation_choice == "1":
        image_processor.calculate_histogram()
    elif operation_choice == "2":
        image_processor.thresholding()
    elif operation_choice == "3":
        scale_percent = simpledialog.askstring("Resize", "Enter Scale Percent:")
        image_processor.resize(scale_percent)
    elif operation_choice == "4":
        blur_choice = simpledialog.askstring("Blurring", "1. Blur\n2. Median Blur\n3. Gaussian Blur\nEnter your choice:")
        if blur_choice in ["1", "2", "3"]:
            k1 = simpledialog.askstring("Kernel Size 1", "Enter Kernel Size 1:")
            k2 = simpledialog.askstring("Kernel Size 2", "Enter Kernel Size 2 (for Blur operation):") if blur_choice == "1" else None
            image_processor.blurring(blur_choice, k1, k2)
    elif operation_choice == "5":
        color_choice = simpledialog.askstring("Color Conversion", "1. Gray\n2. LAB\n3. HSV\nEnter your choice:")
        image_processor.color_conversion(color_choice)
    elif operation_choice == "6":
        contours_choice = simpledialog.askstring("Contours", "1. Canny\n2. Find Contours and Draw\nEnter your choice:")
        if contours_choice in ["1", "2"]:
            thresh_min = simpledialog.askstring("Threshold Min", "Enter Threshold Min:")
            thresh_max = simpledialog.askstring("Threshold Max", "Enter Threshold Max (for Canny):") if contours_choice == "1" else None
            image_processor.contours(contours_choice, thresh_min, thresh_max)
    elif operation_choice == "7":
        print("Additional operation can be added here.")
    else:
        print("Operation not found.")

if __name__ == "__main__":
    main()
