import tkinter as tk
import os
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Listbox
import matplotlib.cm
import matplotlib

from file_manager import FileManager
from data_visualization_manager import DataVisualizationManager


# ---------------- CONSTANTS -------------------------- #
WINDOW_BACKGROUND = "#F0FFFF"
BUTTON_BACKGROUND_OPENFILE = "#7FFFD4"
FONT_NAME = "Courier"

# ------------------ FUNCTIONS ------------------------ #
def open_file(window, file_manager):
    file_manager.open_and_save_file()
    window.destroy()
    main()

def app_reload(window): # Reload the application
    print("Application reload selected")
    window.destroy()
    main()

def delete_file(window, file_manager, file_box, data_folder):
    print("Delete selected")
    file_manager.delete_file(file_box, data_folder)
    window.destroy()
    main()

def data_check(window, data_manager, file_box, data_folder):
    print("Show table selected")
    data_manager.show_table(window, file_box, data_folder)

def plot_2D_image(window, data_manager, file_box, data_folder):
    print("Plot 2D Image")
    data_manager.plot_2D_image(window, file_box, data_folder)

def download_report():
    print("Downloading report")

# ------------------ UI SETUP + MAIN ------------------ #
def main():

    # WINDOW + CANVAS initialization
    window = tk.Tk()
    canvas = tk.Canvas(width=430, height=250, bg=WINDOW_BACKGROUND, highlightthickness=0)
    title_img = tk.PhotoImage(file="./images/title.png")

    # --------------- MENU ----------------- #
    menu = Menu(window)

    # MENU menu
    data_menu = Menu(menu, tearoff=0)
    data_menu.add_command(label="Reports", command=download_report)
    data_menu.add_command(label="Reinitialize", command=lambda: app_reload(window))
    menu.add_cascade(label="Menu", menu=data_menu)

    # PROCESSING menu
    processing_menu = Menu(menu, tearoff=0)
    processing_menu.add_command(label="Proces data")
    menu.add_cascade(label="Processing", menu=processing_menu)

    # Canvas
    window.config(padx=10, pady=10, bg=WINDOW_BACKGROUND, menu=menu)
    window.title("DA-pix v1.10")
    canvas.itemconfig(title_img, tags="transparent")
    canvas.create_image(350, 10, image=title_img, anchor="center")
    canvas.create_text(120, 160, text="DA-pix", font=(FONT_NAME, 44, "bold"), fill="white", anchor="center")
    canvas.create_text(360,200, text="@LukasDekanovsky", font=(FONT_NAME, 10, "bold"), fill="black", anchor="center")
    canvas.grid(row=0, column=1)

    # -------------------- MANAGERS ------------------- #
    file_manager = FileManager()
    data_manager = DataVisualizationManager()

    # LABELS ----------------- #
    open_file_button_label = tk.Label(text="Select a source\ndata file:",font=(FONT_NAME, 10, "bold"), bg=WINDOW_BACKGROUND)
    open_file_button_label.grid(column=0, row=1, sticky="w")

    data_processing_label = tk.Label(text="Data processing:", font=(FONT_NAME, 10, "bold"), bg=WINDOW_BACKGROUND)
    data_processing_label.grid(column=0, row=2, sticky="w")

    # BUTTONS ---------------- #
    open_file_button = tk.Button(text="Open file", bg=BUTTON_BACKGROUND_OPENFILE, command=lambda: open_file(window, file_manager))
    open_file_button.grid(column=1, row=1, sticky="w", padx=5)  

    # FILEBOX ---------------- #
    file_box = Listbox(window, width=20, height=5, font=(FONT_NAME, 10))
    file_box.grid(column=1, row=1, columnspan=2, pady=2, sticky="e")

    # Populate file box with file names
    data_folder = "./data"
    file_names = file_manager.get_file_names(data_folder)

    # This FOR loop will allow us to select only individual file and create a 2D plot
    for file_name in file_names:
        file_box.insert(tk.END, file_name)

        # Create delete button for each file
        display_button = tk.Button(text="Show",activebackground='#7FFFD4',activeforeground='white', height=2, width=5, command=lambda: data_check(window, data_manager, file_box, data_folder))
        display_button.grid(column=3, row=1, padx=5, sticky="n")

        delete_button = tk.Button(text="Delete", background="#EE3B3B",  activebackground='#FFEFDB',activeforeground='white', height=2, width=5, command=lambda: delete_file(window, file_manager, file_box, data_folder))
        delete_button.grid(column=3, row=1, padx=5, sticky="s")

        plot_button = tk.Button(text="Plot 2D Image", bg="#7FFFD4", height=2, width=15, command=lambda: plot_2D_image(window, data_manager, file_box, data_folder))
        plot_button.grid(column=1, row=2, padx=5, sticky="w")








    window.mainloop()

if __name__ == "__main__":
    main()