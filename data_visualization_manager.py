from tkinter import filedialog
import tkinter as tk
from pandastable import Table, TableModel
import numpy as np
import pandas as pd
import shutil
import matplotlib.pyplot as plt
import numpy as np
import os

class DataVisualizationManager():

    def __init__(self):
        ...
    

    def show_table(self, window, file_box, data_folder):
        selected_file = file_box.get(file_box.curselection())
        
        # Read the selected file into a pandas DataFrame
        file_path = os.path.join(data_folder, selected_file)
        df = pd.read_csv(file_path)  # Assuming the file is in CSV format
        
        # Create a tkinter window
        table_window = tk.Toplevel(window)
        table_window.title("Data Visualization")
        
        # Create a PandasTable widget and display the DataFrame
        table = Table(table_window, dataframe=df, showtoolbar=True, showstatusbar=True)
        table.show()

    def plot_2D_image(self, window, file_box, data_folder):
        
        selected_file = file_box.get(file_box.curselection())
        file_path = os.path.join(data_folder, selected_file)
        
        # Read the pixel values from the .txt file
        pixel_values = np.loadtxt(file_path)
        # Create a figure and axis
        fig, ax = plt.subplots()
        # Display the pixel values as an image
        img = ax.imshow(pixel_values, cmap='viridis')
        # Add a colorbar for reference
        cbar = fig.colorbar(img)

        # Adjust the visual properties
        ax.set_title('Pixel Values')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        cbar.set_label('Intensity')

        # Show the plot
        plt.show()