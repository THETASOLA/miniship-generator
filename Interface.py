import tkinter as tk
from tkinter import filedialog
from generator import ImageResizer
import os
from PIL import Image, ImageTk, ImageOps
from tkinter import messagebox
import tkinter as tk

class ImageResizerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Miniship Generator")
        self.resizer = ImageResizer

        # Variables
        self.selected_image = None

        # Create labels and entry widgets for input and output paths
        self.input_label = tk.Label(master, text="Input Image:")
        self.input_label.grid(row=0, column=0, padx=10, pady=5)
        self.input_entry = tk.Entry(master, width=30, state="readonly")
        self.input_entry.grid(row=0, column=1, padx=10, pady=5)
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_input)
        self.browse_button.grid(row=0, column=2, padx=10, pady=5)

        self.output_label = tk.Label(master, text="Output Path:")
        self.output_label.grid(row=1, column=0, padx=10, pady=5)
        self.output_entry = tk.Entry(master, width=30, state="readonly")
        self.output_entry.grid(row=1, column=1, padx=10, pady=5)
        self.save_button = tk.Button(master, text="Save As", command=self.browse_output)
        self.save_button.grid(row=1, column=2, padx=10, pady=5)

        # Create canvas for image display
        self.canvas = tk.Canvas(master, width=200, height=200)
        self.canvas.grid(row=2, column=3, rowspan=3, padx=10, pady=5)
        
        # Create listbox for icons with previews
        self.icons_listbox = tk.Listbox(master, selectmode=tk.SINGLE, width=30, height=10)
        self.icons_listbox.grid(row=3, column=0, padx=10, pady=5, rowspan=3, columnspan=2, sticky="nsew")
        self.icons_listbox.bind("<<ListboxSelect>>", self.load_selected_icon)
        
        # Create a button to permanently add icon
        self.save_icon = tk.Button(master, text="add", command=self.add_icon)
        self.save_icon.grid(row=3, column=2, padx=10, pady=5)

        # Create canvas for icon display
        self.icon_canvas_mini = tk.Canvas(master, width=100, height=100)
        self.icon_canvas_mini.grid(row=3, column=3, rowspan=3, padx=10, pady=5)
        
        # Create canvas for icon display
        self.icon_canvas = tk.Canvas(master, width=100, height=100)
        self.icon_canvas.grid(row=3, column=1, rowspan=3, padx=10, pady=5)

        # Populate the icons listbox
        self.populate_icons_listbox()

    def browse_input(self):
        self.selected_image = filedialog.askopenfilename(title="Select Image")
        self.resizer = ImageResizer(self.selected_image, "")
        generate = self.resizer.resize_image()
        self.miniship = generate
        generate = self.miniship.copy()
        self.resizer.setup_add_icon(generate)
        self.display_miniship(generate)

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(title="Save As", defaultextension=".png", filetypes=[("PNG files", "*.png")])
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, file_path)

    def display_image(self, image):
        # Resize image to fit the canvas
        resized_image = ImageOps.fit(image, (200, 200), method=0, bleed=0.0, centering=(0.5, 0.5))
        photo = ImageTk.PhotoImage(resized_image)
        self.canvas.config(width=photo.width(), height=photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo 

    def populate_icons_listbox(self):
        icons_directory = "customizeUI/icons/"
        icon_files = [f for f in os.listdir(icons_directory) if f.lower().endswith(".png")]

        for icon_file in icon_files:
            self.icons_listbox.insert(tk.END, icon_file)
            
    def add_icon(self):
        icon_path = os.path.join("customizeUI/icons/", self.icons_listbox.get(self.icons_listbox.curselection()))
        self.resizer.addIcon.append(icon_path)
        generate = self.miniship.copy()
        self.resizer.setup_add_icon(generate)
        self.display_miniship(generate)
        self.display_icon(icon_path)
    
    def load_selected_icon(self, event):
        selected_index = self.icons_listbox.curselection()
        if selected_index:
            selected_icon_name = self.icons_listbox.get(selected_index)
            icon_path = os.path.join("customizeUI/icons/", selected_icon_name)
            generate = self.miniship.copy()
            self.resizer.setup_add_icon_temp(generate, icon_path)
            self.display_miniship(generate)
            self.display_icon(icon_path)
    
    def display_miniship(self, image):
        icon_image = image
        resized_icon = ImageOps.fit(icon_image, (icon_image.width , icon_image.height), method=0, bleed=0.0, centering=(0.5, 0.5))
        photo = ImageTk.PhotoImage(resized_icon)
        self.icon_canvas_mini.config(width=photo.width(), height=photo.height())
        self.icon_canvas_mini.create_image(0, 0, anchor=tk.NW, image=photo)
        self.icon_canvas_mini.image = photo

    def display_icon(self, icon_path):
        icon_image = Image.open(icon_path)
        resized_icon = ImageOps.fit(icon_image, (100, 100), method=0, bleed=0.0, centering=(0.5, 0.5))
        photo = ImageTk.PhotoImage(resized_icon)
        self.icon_canvas.config(width=photo.width(), height=photo.height())
        self.icon_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.icon_canvas.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerGUI(root)
    root.mainloop()
