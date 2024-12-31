items = {}
import tkinter as tk
from tkinter import ttk
from functools import partial
import atexit
import os


# Callback function for checkbox state change
def on_checkbutton_click(item, var):
    items[item] = var.get()

def on_exit():
    curr_path = os.path.realpath(__file__)
    
    with open(curr_path, 'r', encoding = 'utf8') as f:
        lines = f.readlines()
        lines[0] = "items = " + str(items) + "\n"

    with open(curr_path, 'w', encoding = 'utf8') as f:
        f.writelines(lines)

def add_item(entry, entry_var, checkbox_frame, canvas, vars):
    new_item_name = entry_var.get().strip()
    if new_item_name:
        items[new_item_name] = False  # Assuming new items start with a default state of True
        
        var = tk.BooleanVar(value=False)
        vars.append(var)
        checkbox = ttk.Checkbutton(checkbox_frame, text=new_item_name, variable=var,
                                   command=partial(on_checkbutton_click, new_item_name, var))
        checkbox.pack(anchor='w', padx=5, pady=5)
        
        # Update the canvas and scrollbar
        checkbox_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Clear the entry after adding
        entry_var.set("")

    #let canvas show the newly added element
    canvas.yview_moveto(1)


def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Todo List")

    # Set the size of the window to fullscreen
    root.state('zoomed')
    
    # Create a frame to hold the Listbox and scrollbar
    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create a canvas to allow scrolling
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar to the canvas
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Create a frame inside the canvas to hold the checkboxes
    checkbox_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=checkbox_frame, anchor="nw")
    
    # Variables to store the state of checkboxes
    vars = []

    # Create a checkbox for each item
    for item in items:
        var = tk.BooleanVar(value=items[item])
        vars.append(var)
        checkbox = ttk.Checkbutton(checkbox_frame, text=item, variable=var, command=partial(on_checkbutton_click, item, var))
        checkbox.pack(anchor='w', padx=5, pady=5)

    # Configure the canvas and scrollbar
    checkbox_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.config(yscrollcommand=scrollbar.set)

    entry_var = tk.StringVar()
    entry = ttk.Entry(root, textvariable=entry_var)
    entry.pack(pady=5, padx=10, fill=tk.X)

    add_button = ttk.Button(root, text="Add", command=lambda: add_item(entry, entry_var, checkbox_frame, canvas, vars))
    add_button.pack(pady=5)

    checkbox_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.yview_moveto(1)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    finally:
        on_exit()

