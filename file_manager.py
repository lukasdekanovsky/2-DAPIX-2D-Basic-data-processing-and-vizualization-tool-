from tkinter import filedialog
import shutil
import os

class FileManager():

    def __init__(self):
        self.file_path = ""
        self.data_folder_path = "./data/"

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


    def get_file_names(self, data_folder):
        file_names = []
        for file in os.listdir(data_folder):
            if os.path.isfile(os.path.join(data_folder, file)):
                file_names.append(file)
        return file_names
    

    def delete_file(self, file_box, data_folder):
        # Get selected file name
        selected_file = file_box.get(file_box.curselection())
        
        # Delete the file from the filesystem
        os.remove(os.path.join(data_folder, selected_file))

        # Delete the file from the listbox
        file_box.delete(file_box.curselection())