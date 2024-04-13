import tkinter
from tkinter import filedialog
import os
import webbrowser

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def openHelp():
    webbrowser.open("Help.html")

def subfolder_required():
    if cb_create_subfolder_var.get():
        tb_custom_subfolder.config(state='normal')
        lb_custom_subfolder.config(state='normal')
        lb_subfolder.config(state='normal')
        for checkbox in checkboxes:
            checkbox.config(state='normal')
    else:
        tb_custom_subfolder.config(state='disabled')
        lb_custom_subfolder.config(state='disabled')
        lb_subfolder.config(state='disabled')
        for checkbox in checkboxes:
            checkbox.config(state='disabled')

def create_folders():
    # Getting folder path and folder names
    folder_path = tf_location.get()
    folder_list = tf_folder_main.get().upper().split(',')

    # Create main folders
    for folder in folder_list:
        new_folder_path = os.path.join(folder_path,folder)
        os.makedirs(new_folder_path,exist_ok=True)

        # Create subfolders from checkbox
        if cb_create_subfolder_var.get():
            for i in range(len(checkboxes)):
                if checkbox_vars[i].get():
                    subfolder = checkboxes[i].cget('text')
                    new_subfolder_path = os.path.join(new_folder_path,subfolder)
                    os.makedirs(new_subfolder_path,exist_ok=True)
            # Create custom subfolders
            custom_subfolders = tb_custom_subfolder.get("1.0","end").split('\n')
            for subfolder in custom_subfolders:
                if subfolder:
                    new_subfolder_path = os.path.join(new_folder_path,subfolder)
                    os.makedirs(new_subfolder_path,exist_ok=True)   

# Browse to select the location to create folders
def browse():
    folder_path = tkinter.filedialog.askdirectory()
    tf_location.delete(0,tkinter.END)
    tf_location.insert(0,folder_path)

# Read subfolders from file
with open('subfolders.txt') as file:
    text = file.read().split('\n')

# GUI creation
root = tkinter.Tk()
root.title("Folder Manager")
root.geometry("450x450")
center_window(root)

# Widgets
# Folder
lb_folder_main  = tkinter.Label(root,text="Folders",font=("Arial",13,'bold'))
tf_folder_main = tkinter.Entry(root,width=30,font=("Arial",11,))

# Location
lb_location = tkinter.Label(root,text="Location",font=("Arial",13,'bold'))
tf_location = tkinter.Entry(root,width=21,font=("Arial",11))

# Browse button
btn_location = tkinter.Button(root,width=7,text="Browse",font=("Arial",10),command=browse)

# Create subfolder
lb_create_subfolder = tkinter.Label(root,text="Create subfolders",font=("Arial",11,'bold'))
cb_create_subfolder_var = tkinter.IntVar()
cb_create_subfolder = tkinter.Checkbutton(root,variable=cb_create_subfolder_var,command=subfolder_required)

# Subfolders
lb_subfolder = tkinter.Label(root,text="Subfolders",font=("Arial",11,'bold'))
lb_custom_subfolder = tkinter.Label(root,text="Custom folders",font=("Arial",11,'bold'))
tb_custom_subfolder = tkinter.Text(root,height=8,width=27,font=("Arial",11,))

# Buttons
btn_help = tkinter.Button(root,text="Help",font=("Arial",11,'bold'),command=openHelp)
btn_create = tkinter.Button(root,text="Create",font=("Arial",11,'bold'),command=create_folders)

# Layout
# Main folder
lb_folder_main.grid(row=0,column=0,padx=15,pady=15,sticky="E")
tf_folder_main.grid(row=0,column=1,sticky="w",columnspan=2)

# Location
lb_location.grid(row=1,column=0,padx=10,pady=5,sticky="E")
tf_location.grid(row=1,column=1,sticky="W")
btn_location.grid(row=1,column=2,columnspan=2,sticky="W")

# Create subfolder
lb_create_subfolder.grid(row=2,column=0,padx=10,pady=15,sticky="E")
cb_create_subfolder.grid(row=2,column=1,sticky="W")

# Subfolder label
lb_subfolder.grid(row=3,column=0,padx=10,pady=15,sticky="W")
lb_subfolder.config(state='disabled')

#Subfolder checkboxes
checkbox_vars = [tkinter.IntVar(value=1) for i in text]
checkboxes = []
for i in range(len(text)):
    cb = tkinter.Checkbutton(root,text=text[i], variable=checkbox_vars[i])
    cb.grid(row=4+i,column=0,padx=15,sticky="W")
    cb.config(state='disabled')
    checkboxes.append(cb)
# Custom subfolder
lb_custom_subfolder.grid(row=3,column=1,padx=10,pady=15,sticky="E")
lb_custom_subfolder.config(state='disabled')
tb_custom_subfolder.grid(row=4,column=1,columnspan=2,rowspan=len(text)+1,padx=10,pady=15,sticky="W")
tb_custom_subfolder.config(state='disabled')

# Buttons
btn_help.grid(row=5+len(text),column=0,padx=5,pady=20,sticky="E")
btn_create.grid(row=5+len(text),column=1,padx=5,pady=20,sticky="E")
root.mainloop()