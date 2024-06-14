from tkinter import filedialog
import shutil
import os

class MainPage():

    def __init__(self):
        self.file_path = ""
        self.data_folder_path = "./data/"
        self.gif_data_folder_path = "./gif/"

    def open_and_save_file(self):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        
        # We are checking if the file was selected
        if file_path:
            destination_path = self.data_folder_path
            # we are saving the path of the original file 
            self.file_path = file_path 
            file_name = self.file_path.split("/")[-1]

            # we are copying the file to the project folder
            shutil.copy(self.file_path, destination_path + file_name)

    def open_and_save_files(self):
        file_paths = filedialog.askopenfilenames(initialdir="/", title="Select files", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        
        # We are checking if files were selected
        if file_paths:
            destination_path = self.gif_data_folder_path
            for file_path in file_paths:
                file_name = file_path.split("/")[-1]
                # we are copying each file to the gif folder
                shutil.copy(file_path, destination_path + file_name)

    def get_file_names(self, data_folder):
        file_names = []
        for file in os.listdir(data_folder):
            if os.path.isfile(os.path.join(data_folder, file)):
                file_names.append(file)
        return file_names
    
    def reset_gif_folder(self, gif_folder):
        for file in os.listdir(gif_folder):
            file_path = os.path.join(gif_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    

    def delete_file(self, file_box, data_folder):
        # Get selected file name
        selected_file = file_box.get(file_box.curselection())
        
        # Delete the file from the filesystem
        os.remove(os.path.join(data_folder, selected_file))

        # Delete the file from the listbox
        file_box.delete(file_box.curselection())

   
       