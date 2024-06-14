import tkinter as tk
from tkinter.ttk import Labelframe
import os
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Listbox, Checkbutton
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkthemes import ThemedStyle
import matplotlib

from main_page import MainPage
from scan_processing_page import ScanDataProcessing


# ---------------- CONSTANTS -------------------------- #
WINDOW_BACKGROUND = "#E0EEEE"
BUTTON_BACKGROUND_OPENFILE = "#98F5FF"
FONT_NAME = 'Helvetica'

GIF_FOLDER = "./gif"
GIF_RESULTS_FOLDER = "./results"

# ------------------ FUNCTIONS ------------------------ #
def open_file(window, homepage):
    homepage.open_and_save_file()
    window.destroy()
    main()

def app_reload(window): # Reload the application
    print("Application reload selected")
    window.destroy()
    main()

def delete_file(window, homepage, file_box, data_folder):
    print("Delete selected")
    homepage.delete_file(file_box, data_folder)
    window.destroy()
    main()

def data_check(window, scan_data_page, file_box, data_folder):
    print("Show table selected")
    scan_data_page.show_table(window, file_box, data_folder)

def plot_2D_image(window, scan_data_page, file_box, data_folder):
    print("Plot 2D Image")
    scan_data_page.show_2D_image(window, file_box, data_folder)

def plot_gif(window, scan_data_page):
    scan_data_page.show_gif_data(window)

def open_files(window, homepage):
    homepage.open_and_save_files()
    window.destroy()
    main()

def download_report():
    print("Downloading report")

# ------------------ UI SETUP + MAIN ------------------ #
def main():

    # WINDOW + CANVAS initialization
    window = tk.Tk()
    style = ttk.Style()
    canvas = tk.Canvas(width=430, height=250, bg=WINDOW_BACKGROUND, highlightthickness=0)
    title_img = tk.PhotoImage(file="./images/title.png")

    # Configure the style
    style.configure("Custom.TButton",
                foreground="black",
                background="white",
                font=(FONT_NAME, 10, "bold"),
                padding=2)

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
    homepage = MainPage()
    scan_data_page = ScanDataProcessing(number_of_gifs=len(os.listdir(GIF_RESULTS_FOLDER)))

    # LABELS ----------------- #
    data_processing2D_label = ttk.Label(text="2D Data processing", style="TLabel", font=(FONT_NAME, 15, "bold"), background=WINDOW_BACKGROUND)
    data_processing2D_label.grid(column=0, row=1, sticky="ew", padx=50)

    open_file_button_label = ttk.Label(text="Select a source\ndata file", style="TLabel", font=(FONT_NAME, 10, "bold"), background=WINDOW_BACKGROUND)
    open_file_button_label.grid(column=0, row=2, sticky="w")

    data_processing_label = ttk.Label(text="Data processing", font=(FONT_NAME, 10, "bold"), background=WINDOW_BACKGROUND)
    data_processing_label.grid(column=0, row=3, sticky="w")

    data_processingCT_label = ttk.Label(text="Energy scanning", font=(FONT_NAME, 15, "bold"), background=WINDOW_BACKGROUND)
    data_processingCT_label.grid(column=0, row=4, sticky="ew", padx=50, pady=10)

    open_files_button_label = ttk.Label(text="Select files for\ngif creation",font=(FONT_NAME, 10, "bold"), background=WINDOW_BACKGROUND)
    open_files_button_label.grid(column=0, row=5, sticky="w")

    create_gif_button_label = ttk.Label(text="Create a .gif file",font=(FONT_NAME, 10, "bold"), background=WINDOW_BACKGROUND)
    create_gif_button_label.grid(column=0, row=6, sticky="w")

    # BUTTONS ---------------- 
    open_file_button = ttk.Button(style="Custom.TButton", text="Open file", command=lambda: open_file(window, homepage))
    open_file_button.grid(column=0, row=2, sticky="e", padx=10)  

    open_files_button = ttk.Button(style="Custom.TButton", text="Open files", command=lambda: open_files(window, homepage))
    open_files_button.grid(column=0, row=5, sticky="e", padx=10)

    reset_gif_folder = ttk.Button(style="Custom.TButton", text="Reset gif data", command=lambda: homepage.reset_gif_folder(GIF_FOLDER))
    reset_gif_folder.grid(column=1, row=5, sticky="w", padx=150)

    gif_button = ttk.Button(style="Custom.TButton", text="Process GIF secv.", command=lambda: plot_gif(window, scan_data_page))
    gif_button.grid(column=0, row=6, padx=10, sticky="e", pady=7)

    # FILEBOX ---------------- #
    file_box = Listbox(window, width=30, height=3, font=(FONT_NAME, 10))
    file_box.grid(column=1, row=2, columnspan=2, padx=5, sticky="ew")

    # CHECKBOX ----------------- # 
    gif_folder_full_check = tk.Checkbutton(window, text='Data loaded', variable=1, onvalue=1, offvalue=0, state='disabled')
    gif_folder_full_check.grid(column=1, row=5, sticky="w")
    # Check if data exists in the gif folder
    if os.listdir(GIF_FOLDER):
        gif_folder_full_check.select()
    


    # Populate file box with file names
    data_folder = "./data"
    file_names = homepage.get_file_names(data_folder)

    # This FOR loop will allow us to select only individual file and create a 2D plot
    for file_name in file_names:
        file_box.insert(tk.END, file_name)

        # Create delete button for each file
        display_button = ttk.Button(style="Custom.TButton", text="Show", command=lambda: data_check(window, scan_data_page, file_box, data_folder))
        display_button.grid(column=3, row=2, padx=5, sticky="n")

        delete_button = ttk.Button(style="Custom.TButton", text="Delete", command=lambda: delete_file(window, homepage, file_box, data_folder))
        delete_button.grid(column=3, row=3, padx=5, sticky="s")

        plot_button = ttk.Button(style="Custom.TButton", text="Show 2D Image", command=lambda: plot_2D_image(window, scan_data_page, file_box, data_folder))
        plot_button.grid(column=0, row=3, padx=10, sticky="e")








    window.mainloop()

if __name__ == "__main__":
    main()