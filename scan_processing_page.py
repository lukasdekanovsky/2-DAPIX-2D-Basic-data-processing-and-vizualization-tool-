from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from pandastable import Table, TableModel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image, ImageTk
import imageio


class ScanDataProcessing():

    def __init__(self, number_of_gifs):
        self.number_of_gifs = number_of_gifs
    

    def show_table(self, window, file_box, data_folder):
        selected_file = file_box.get(file_box.curselection())
        
        # Read the selected file into a pandas DataFrame
        file_path = os.path.join(data_folder, selected_file)
        df = pd.read_csv(file_path, delimiter=' ')  # Assuming the file is in CSV format and comma-separated
        
        # Create a tkinter window
        table_window = tk.Toplevel(window)
        table_window.title("Data Visualization")
        
        # Create a PandasTable widget and display the DataFrame
        table = Table(table_window, dataframe=df, showtoolbar=True, showstatusbar=True)
        table.show()

    def show_2D_image(self, window, file_box, data_folder):
        
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

    def show_gif_data(self, window):
        gif_window = tk.Toplevel(window)
        gif_window.title("GIF Viewer")
        gif_window.geometry("400x300")
        

        # Get the file names from the gif folder
        data_folder = "./gif"
        data_files = os.listdir(data_folder)

        gif_results_folder = "./results"
        gif_result_files = os.listdir(gif_results_folder)

        #

        # Create a listbox to display the gif source files
        gif_scrollbar = tk.Scrollbar(gif_window)
        gif_listbox = tk.Listbox(gif_window, yscrollcommand=gif_scrollbar.set)
        gif_scrollbar.config(command=gif_listbox.yview)
        gif_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        gif_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        gif_listbox.pack()

        for data_file in data_files:
            gif_listbox.insert(tk.END, data_file)

        # Create a listbox to display the gif final files
        second_scrollbar = tk.Scrollbar(gif_window)
        second_listbox = tk.Listbox(gif_window, yscrollcommand=second_scrollbar.set)
        second_scrollbar.config(command=second_listbox.yview)
        second_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        second_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        second_listbox.pack()

        for gif_result in gif_result_files:
            second_listbox.insert(tk.END, gif_result)

        # Create a button to play the selected gif
        play_button = tk.Button(gif_window, text="Investigate data", command=lambda: self.investigate_data(data_folder, gif_window, gif_listbox, second_listbox))
        play_button.pack()
        play_button = tk.Button(gif_window, text="Create GIF", command=lambda: self.create_gif(gif_window, gif_listbox, second_listbox))
        play_button.pack()
        play_button = tk.Button(gif_window, text="Show GIF", command=lambda: self.show_gif(gif_window,gif_listbox, second_listbox, gif_results_folder))
        play_button.pack()
        play_button = tk.Button(gif_window, text="Delete all .txt files", command=lambda: self.destroy_txt_files(gif_window, gif_listbox, second_listbox))
        play_button.pack()
        play_button = tk.Button(gif_window, text="Delete all GIF files", command=lambda: self.destroy_gif_files(gif_window, gif_listbox, second_listbox, data_folder="./results"))
        play_button.pack()


    def destroy_txt_files(self, gif_window, gif_listbox, second_listbox, data_folder="./gif"):
        # Delete all files from the ./gif folder
        file_list = os.listdir(data_folder)
        for file_name in file_list:
            file_path = os.path.join(data_folder, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        self.update_window(gif_window, gif_listbox, second_listbox)

    def destroy_gif_files(self, gif_window, gif_listbox, second_listbox, data_folder="./results"):
        # Delete all files from the ./results folder
        file_list = os.listdir(data_folder)
        for file_name in file_list:
            file_path = os.path.join(data_folder, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        self.update_window(gif_window, gif_listbox, second_listbox)

    def investigate_data(self, data_folder, gif_window, gif_listbox, second_listbox):
        selected_file = gif_listbox.get(gif_listbox.curselection())
        file_path = os.path.join(data_folder, selected_file)
        
        # Read the selected file into a pandas DataFrame
        df = pd.read_csv(file_path, delimiter=' ')  # Assuming the file is in CSV format and comma-separated
    
        # Create a tkinter window
        table_window = tk.Toplevel(gif_window)
        table_window.title("Data Visualization")
        
        # Create a PandasTable widget and display the DataFrame
        table = Table(table_window, dataframe=df, showtoolbar=True, showstatusbar=True)
        table.show()

        self.update_window(gif_window, gif_listbox, second_listbox)


    def create_gif(self, gif_window, gif_listbox, second_listbox):
        # Get the file names from the gif folder
        data_folder = "./gif"
        gif_files = os.listdir(data_folder)

        # Create a list to store the frames
        frames = []

        # Loop through each file in the gif folder
        for gif_file in gif_files:
            # Check if the file is a .txt file
            if gif_file.endswith(".txt"):
                # Read the pixel values from the .txt file
                file_path = os.path.join(data_folder, gif_file)
                pixel_values = np.loadtxt(file_path)

                # Create an image from the pixel values
                img = Image.fromarray(pixel_values)

                # Append the image to the frames list
                frames.append(img)

        # Save the frames as a gif file
        gif_path = f"./results/animated{self.number_of_gifs}.gif"
        imageio.mimsave(gif_path, frames, duration=0.5)
        self.number_of_gifs += 1

        self.update_window(gif_window, gif_listbox, second_listbox)

        # Show a message box with the path to the created gif file
        messagebox.showinfo("GIF Created", f"The GIF file has been created and saved to:\n{gif_path}")


    def show_gif(self,gif_window, gif_listbox, second_listbox, gif_results_folder):
        selected_gif = second_listbox.get(second_listbox.curselection())
        gif_path = os.path.join(gif_results_folder, selected_gif)

            # Open the GIF file
        gif = Image.open(gif_path)

        # Create a new window
        window = tk.Toplevel(gif_window)

        # Create a label to display the GIF
        label = tk.Label(window)
        label.pack()

        # Function to update the label's image
        def update(index=0):
            # Get the GIF's frame at the current index
            gif.seek(index)
            frame = ImageTk.PhotoImage(gif)

            # Update the label's image
            label.config(image=frame)
            label.image = frame  # Store the PhotoImage object as an attribute of the label

            # Schedule the next update
            window.after(100, update, (index + 1) % gif.n_frames)

        # Start the animation
        update()

        self.update_window(gif_window, gif_listbox, second_listbox)




    def update_window(self, gif_window, gif_listbox, second_listbox):
            # Clear the listboxes
            gif_listbox.delete(0, tk.END)
            second_listbox.delete(0, tk.END)

            # Get the updated file names from the gif folder
            data_folder = "./gif"
            data_files = os.listdir(data_folder)

            gif_results_folder = "./results"
            gif_result_files = os.listdir(gif_results_folder)

            # Update the gif source files listbox
            for data_file in data_files:
                gif_listbox.insert(tk.END, data_file)

            # Update the gif final files listbox
            for gif_result in gif_result_files:
                second_listbox.insert(tk.END, gif_result)