import tkinter as tk
from tkinter import filedialog
from generator import ImageResizer
import os
from PIL import Image, ImageTk, ImageOps
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

class ImageResizerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Miniship Generator")
        self.resizer = ImageResizer
        self.miniship = None
        self.current_icon_elevation = 0
        self.sharpen = 4.0

        # Variables
        self.selected_image = None

        # Create labels and entry widgets for input and output paths
        self.browse_button = tk.Button(master, text="Load Ship Sprite", command=self.browse_input)
        self.browse_button.grid(row=0, column=1, padx=10, pady=5)

        self.save_button = tk.Button(master, text="Save Miniship", command=self.browse_output)
        self.save_button.grid(row=1, column=1, padx=10, pady=5)

        # Create canvas for image display
        self.canvas = tk.Canvas(master, width=200, height=200)
        self.canvas.grid(row=2, column=3, rowspan=3, padx=10, pady=5)

        # Create treeview for icons with previews
        self.icons_treeview = ttk.Treeview(master, selectmode="browse", columns=("Icon",))
        self.icons_treeview.grid(row=4, column=0, padx=10, pady=5, rowspan=3, columnspan=2, sticky="nsew")
        self.icons_treeview.bind("<ButtonRelease-1>", self.load_selected_icon)

        # Set up treeview columns
        self.icons_treeview.heading("#0", text="Icons")
        self.icons_treeview.column("#0", width=150, anchor="w")

        # Create a docker for the icons and the buttons
        self.icons_docker = tk.Frame(master, border=1, relief="sunken", width=50, background="black")
        self.icons_docker.grid(row=3, column=3, padx=10, pady=5, rowspan=3, sticky="nsew")
        
        # Create a button to permanently add icon
        self.save_icon = tk.Button(self.icons_docker, text="add", command=self.add_icon)
        self.save_icon.grid(row=3, column=2, padx=10, pady=5)

        # Create a button to permanently remove icon
        self.delete_icon = tk.Button(self.icons_docker, text="del", command=self.del_icon)
        self.delete_icon.grid(row=4, column=2, padx=10, pady=5)

        # Create a button to nudge up the icon
        self.upping_icon = tk.Button(self.icons_docker, text="up", command=self.up_icon)
        self.upping_icon.grid(row=5, column=2, padx=10, pady=5)

        # Create a button to nudge down the icon
        self.downing_icon = tk.Button(self.icons_docker, text="down", command=self.down_icon)
        self.downing_icon.grid(row=6, column=2, padx=10, pady=5)

        # Create canvas for icon display
        self.icon_canvas_mini = tk.Canvas(self.icons_docker, width=100, height=100, background="#0a1621")
        self.icon_canvas_mini.grid(row=3, column=4, rowspan=3, padx=10, pady=5)

        # Slider from 0 to 10
        self.slider_label = tk.Label(master, text="Sharpness")
        self.slider_label.grid(row=0, column=2, padx=10, pady=5, columnspan=2, sticky="nsew")
        self.slider_var = tk.DoubleVar()
        self.slider = tk.Scale(master, from_=0, to=10, variable=self.slider_var, orient=tk.HORIZONTAL, command=self.slider_changed)
        self.slider.grid(row=1, column=2, padx=10, pady=5, columnspan=2, sticky="nsew")

        # Populate the icons listbox
        self.populate_icons_treeview()
    
    def slider_changed(self, event):
        generate = self.miniship.copy()
        generate = self.resizer.sharpen(generate, self.slider_var.get())
        self.sharpen = self.slider_var.get()
        self.resizer.setup_add_icon(generate)
        self.display_miniship(generate)
    
    def up_icon(self):
        self.current_icon_elevation += -1
        selected_item_id = self.icons_treeview.selection()
        if selected_item_id:
            selected_icon_name = self.icons_treeview.item(selected_item_id, "text")
            icon_path = os.path.join("customizeUI/icons/", selected_icon_name)
            if self.miniship:
                generate = self.miniship.copy()
                generate = self.resizer.sharpen(generate, 4.0)
                self.resizer.setup_add_icon_temp(generate, icon_path, self.current_icon_elevation)
                self.display_miniship(generate)
    
    def down_icon(self):
        self.current_icon_elevation += 1
        selected_item_id = self.icons_treeview.selection()
        if selected_item_id:
            selected_icon_name = self.icons_treeview.item(selected_item_id, "text")
            icon_path = os.path.join("customizeUI/icons/", selected_icon_name)
            if self.miniship:
                generate = self.miniship.copy()
                generate = self.resizer.sharpen(generate, 4.0)
                self.resizer.setup_add_icon_temp(generate, icon_path, self.current_icon_elevation)
                self.display_miniship(generate)


    def populate_icons_treeview(self):
        icons_directory = "customizeUI/icons/"
        icon_files = [f for f in os.listdir(icons_directory) if f.lower().endswith(".png")]

        for icon_file in icon_files:
            icon_path = os.path.join(icons_directory, icon_file)
            icon_image = Image.open(icon_path)
            photo = ImageTk.PhotoImage(icon_image)
            self.icons_treeview.insert("", "end", text=icon_file , image= photo)

    def browse_input(self):
        self.selected_image = filedialog.askopenfilename(title="Select Image", defaultextension=".png" , filetypes=[("PNG files", "*.png")])
        self.resizer = ImageResizer(self.selected_image, "")
        generate = self.resizer.resize_image()
        self.miniship = generate
        generate = self.miniship.copy()
        generate = self.resizer.sharpen(generate, 4.0)
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
            
    def add_icon(self):
        icon_path = os.path.join("customizeUI/icons/", self.icons_treeview.item(self.icons_treeview.selection(), "text"))
        #we make a copy of the current elevation

        elevation = self.current_icon_elevation
        self.resizer.addIcon.append([icon_path, elevation])
        generate = self.miniship.copy()
        generate = self.resizer.sharpen(generate, self.sharpen)
        self.resizer.setup_add_icon(generate)
        self.display_miniship(generate)

    def del_icon(self):
        if self.resizer.addIcon and self.resizer.addIcon[-1]:
            self.resizer.addIcon.remove(self.resizer.addIcon[-1])
            generate = self.miniship.copy()
            generate = self.resizer.sharpen(generate, self.sharpen)
            self.resizer.setup_add_icon(generate)
            self.display_miniship(generate)

    
    def load_selected_icon(self, event):
        self.current_icon_elevation = 0
        selected_item_id = self.icons_treeview.selection()
        if selected_item_id:
            selected_icon_name = self.icons_treeview.item(selected_item_id, "text")
            icon_path = os.path.join("customizeUI/icons/", selected_icon_name)
            if self.miniship:
                generate = self.miniship.copy()
                generate = self.resizer.sharpen(generate, self.sharpen)
                self.resizer.setup_add_icon_temp(generate, icon_path)
                self.display_miniship(generate)

    
    def display_miniship(self, image):
        icon_image = image
        resized_icon = ImageOps.fit(icon_image, (icon_image.width , icon_image.height), method=0, bleed=0.0, centering=(0.5, 0.5))
        photo = ImageTk.PhotoImage(resized_icon)
        self.icon_canvas_mini.config(width=photo.width(), height=photo.height())
        self.icon_canvas_mini.create_image(0, 0, anchor=tk.NW, image=photo)
        self.icon_canvas_mini.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerGUI(root)
    root.mainloop()
