from tkinter import filedialog
from generator import ImageResizer
import os
from PIL import ImageTk, ImageOps
import tkinter as tk
from tkinter import ttk
import customizeUI

class ImageResizerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Miniship Generator")
        self.resizer = ImageResizer
        self.miniship = None
        self.current_icon_elevation = 0
        self.sharpen = 4.0
        self.outline = 1
        self.selected_image = None

        # Create labels and entry widgets for input and output paths
        self.browse_button = tk.Button(master, text="Load Ship Sprite", command=self.browse_input)
        self.browse_button.grid(row=0, column=0, padx=10, pady=5)

        self.save_button = tk.Button(master, text="Save Miniship", command=self.browse_output)
        self.save_button.grid(row=0, column=1, padx=10, pady=5)

        # Create canvas for image display
        self.canvas = tk.Canvas(master, width=200, height=200)
        self.canvas.grid(row=2, column=3, rowspan=3, padx=10, pady=5)

        # Create treeview for icons with previews
        self.icons_treeview = ttk.Treeview(master, selectmode="browse", columns=("Icon",), height=12)
        self.icons_treeview.grid(row=4, column=0, padx=10, pady=5, rowspan=3, columnspan=2, sticky="nsew")
        self.icons_treeview.bind("<ButtonRelease-1>", self.load_selected_icon)

        # Set up treeview columns
        self.icons_treeview.heading("#0", text="Icons")
        self.icons_treeview.column("#0",width=150, anchor="w")

        # Create a docker for the icons and the buttons
        self.icons_docker = tk.Frame(master, border=1, relief="sunken", width=50, height=5, background="black")
        self.icons_docker.grid(row=4, column=3, padx=10, pady=5, rowspan=3, sticky="nsew")
        
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
        
        # Create a drop down list for the bottom icons
        self.bottom_icon_label = tk.Label(self.icons_docker, text="Bottom Left Icon")
        self.bottom_icon_label.grid(row=6, column=4, padx=10, pady=5, sticky="nsew")
        self.bottom_icon_var = tk.StringVar()
        self.bottom_icon_var.set("None")
        self.bottom_icon = ttk.Combobox(self.icons_docker, textvariable=self.bottom_icon_var, values=["None"])
        self.bottom_icon.grid(row=7, column=4, padx=10, pady=5, sticky="nsew")
        self.bottom_icon.bind("<<ComboboxSelected>>", self.bottom_icon_changed)
        
        # Create a drop down list for the bottom right icons
        self.bottom_right_icon_label = tk.Label(self.icons_docker, text="Bottom Right Icon")
        self.bottom_right_icon_label.grid(row=8, column=4, padx=10, pady=5, sticky="nsew")
        self.bottom_right_icon_var = tk.StringVar()
        self.bottom_right_icon_var.set("None")
        self.bottom_right_icon = ttk.Combobox(self.icons_docker, textvariable=self.bottom_right_icon_var, values=["None"])
        self.bottom_right_icon.grid(row=9, column=4, padx=10, pady=5, sticky="nsew")
        self.bottom_right_icon.bind("<<ComboboxSelected>>", self.bottom_right_icon_changed)
        
        # Slider from 0 to 10
        self.slider_sharp_label = tk.Label(master, text="Sharpness")
        self.slider_sharp_label.grid(row=0, column=2, padx=10, pady=5, columnspan=2, sticky="nsew")
        self.slider_sharp_var = tk.DoubleVar()
        self.slider_sharp = tk.Scale(master, from_=0, to=10, variable=self.slider_sharp_var, orient=tk.HORIZONTAL, command=self.slider_sharp_changed)
        self.slider_sharp.grid(row=1, column=2, padx=10, pady=5, columnspan=2, sticky="nsew")

        # Slider from 0 to 5
        self.slider_outline_label = tk.Label(master, text="Outline")
        self.slider_outline_label.grid(row=2, column=2, padx=10, pady=5, columnspan=2, sticky="nsew")
        self.slider_outline_var = tk.DoubleVar()
        self.slider_outline = tk.Scale(master, from_=0, to=4, variable=self.slider_outline_var, orient=tk.HORIZONTAL, command=self.slider_outline_changed)
        self.slider_outline.grid(row=3, column=2, padx=10, pady=5, columnspan=2, sticky="nsew")

        # Create a search bar entry widget
        self.search_entry_label = tk.Label(master, text="Search Icons")
        self.search_entry_label.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        self.search_entry = tk.Entry(master)
        self.search_entry.grid(row=3, column=1, padx=10, pady=5)
        self.search_entry.bind('<KeyRelease>', self.filter_icons)

        # Populate the icons listbox
        self.populate_icons_treeview()
        self.populate_bottom_icon_dropdown()
        self.populate_bottom_right_icon_dropdown()
        
    def populate_bottom_icon_dropdown(self, path="customizeUI\\bbox\\"):
        file_list = os.listdir(path)

        image_extensions = [".png", ".jpg", ".jpeg", ".gif"]
        file_list = [file for file in file_list if any(file.lower().endswith(ext) for ext in image_extensions)]
        file_list.insert(0, "None")

        self.bottom_icon["values"] = file_list
        self.bottom_icon.current(0)
    
    def populate_bottom_right_icon_dropdown(self, path="customizeUI\\elite\\"):
        file_list = os.listdir(path)

        image_extensions = [".png", ".jpg", ".jpeg", ".gif"]
        file_list = [file for file in file_list if any(file.lower().endswith(ext) for ext in image_extensions)]
        file_list.insert(0, "None")

        self.bottom_right_icon["values"] = file_list
        self.bottom_right_icon.current(0)

    def filter_icons(self, event):
        search_term = self.search_entry.get().lower()
        
        # Clear existing items from the treeview
        for item_id in self.icons_treeview.get_children():
            self.icons_treeview.delete(item_id)

        for icon_file in self.icon_files:
            if search_term in icon_file.lower():
                self.icons_treeview.insert("", "end", text=icon_file)
    
    def bottom_icon_changed(self, event):
        if self.miniship:
            self.resizer.addIcon_bottom = self.bottom_icon_var.get()
            generate = self.miniship.copy()
            generate = self.resizer.sharpen(generate, self.slider_sharp_var.get())
            self.resizer.upsize_black_lines(self.selected_image, generate, self.outline)
            self.resizer.setup_add_icon(generate)
            self.display_miniship(generate)
            
    def bottom_right_icon_changed(self, event):
        if self.miniship:
            self.resizer.addIcon_bottom_right = self.bottom_right_icon_var.get()
            generate = self.miniship.copy()
            generate = self.resizer.sharpen(generate, self.slider_sharp_var.get())
            self.resizer.upsize_black_lines(self.selected_image, generate, self.outline)
            self.resizer.setup_add_icon(generate)
            self.display_miniship(generate)
    
    def slider_sharp_changed(self, event):
        generate = self.miniship.copy()
        generate = self.resizer.sharpen(generate, self.slider_sharp_var.get())
        self.resizer.upsize_black_lines(self.selected_image, generate, self.outline)
        self.sharpen = self.slider_sharp_var.get()
        self.resizer.setup_add_icon(generate)
        self.display_miniship(generate)

    def slider_outline_changed(self, event):
        generate = self.miniship.copy()
        self.outline = int(self.slider_outline_var.get() + 1)
        generate = self.resizer.sharpen(generate, self.sharpen)
        self.resizer.upsize_black_lines(self.selected_image, generate, self.outline)
        self.resizer.setup_add_icon(generate)
        self.display_miniship(generate)
    
    def up_icon(self):
        self.current_icon_elevation += -1
        selected_item_id = self.icons_treeview.selection()
        if selected_item_id:
            selected_icon_name = self.icons_treeview.item(selected_item_id, "text")
            icon_path = os.path.join("customizeUI/", selected_icon_name)
            if self.miniship:
                generate = self.miniship.copy()
                generate = self.resizer.sharpen(generate, self.sharpen)
                self.resizer.upsize_black_lines(self.selected_image, generate, self.outline)
                self.resizer.setup_add_icon_temp(generate, icon_path, self.current_icon_elevation)
                self.display_miniship(generate)
    
    def down_icon(self):
        self.current_icon_elevation += 1
        selected_item_id = self.icons_treeview.selection()
        if selected_item_id:
            selected_icon_name = self.icons_treeview.item(selected_item_id, "text")
            icon_path = os.path.join("customizeUI/", selected_icon_name)
            if self.miniship:
                generate = self.miniship.copy()
                generate = self.resizer.sharpen(generate, self.sharpen)
                self.resizer.upsize_black_lines(self.selected_image, generate, self.outline)
                self.resizer.setup_add_icon_temp(generate, icon_path, self.current_icon_elevation)
                self.display_miniship(generate)

    def populate_icons_treeview(self):
        icons_directory = "customizeUI/"
        self.icon_files = [f for f in os.listdir(icons_directory) if f.lower().endswith(".png")]

        for icon_file in self.icon_files:
            self.icons_treeview.insert("", "end", text=icon_file)

    def browse_input(self):
        self.selected_image = filedialog.askopenfilename(title="Select Image", defaultextension=".png" , filetypes=[("PNG files", "*.png")])
        self.resizer = ImageResizer(self.selected_image, "")
        generate = self.resizer.resize_image()
        self.resizer.cache_black_lines(self.selected_image)
        self.miniship = generate
        generate = self.miniship.copy()
        generate = self.resizer.sharpen(generate, self.sharpen)
        self.resizer.upsize_black_lines(self.selected_image, generate, self.outline)
        self.resizer.setup_add_icon(generate)
        self.display_miniship(generate)

    def browse_output(self):
        if self.miniship:

            file_path = filedialog.asksaveasfilename(initialfile = "miniship_" + os.path.basename(self.selected_image).replace("_base", ""),title="Save As", defaultextension=".png", filetypes=[("PNG files", "*.png")])
            generate = self.miniship.copy()
            generate = self.resizer.sharpen(generate, self.sharpen)
            self.resizer.upsize_black_lines(self.selected_image, generate, self.outline)
            self.resizer.save_image(generate ,file_path.replace(".png", "_base.png"))
            self.resizer.setup_add_icon(generate)
            self.resizer.save_image(generate ,file_path)

    def display_image(self, image):

        resized_image = ImageOps.fit(image, (200, 200), method=0, bleed=0.0, centering=(0.5, 0.5))
        photo = ImageTk.PhotoImage(resized_image)
        self.canvas.config(width=photo.width(), height=photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo 

    def add_icon(self):
        icon_path = os.path.join("customizeUI/", self.icons_treeview.item(self.icons_treeview.selection(), "text"))
        elevation = self.current_icon_elevation
        self.resizer.addIcon.append([icon_path, elevation])
        generate = self.miniship.copy()
        generate = self.resizer.sharpen(generate, self.sharpen)
        self.resizer.upsize_black_lines(self.selected_image, generate, self.outline)
        self.resizer.setup_add_icon(generate)
        self.display_miniship(generate)

    def del_icon(self):
        if self.resizer.addIcon and self.resizer.addIcon[-1]:
            self.resizer.addIcon.remove(self.resizer.addIcon[-1])
            generate = self.miniship.copy()
            generate = self.resizer.sharpen(generate, self.sharpen)
            self.resizer.upsize_black_lines(self.selected_image, generate, self.outline)
            self.resizer.setup_add_icon(generate)
            self.display_miniship(generate)

    
    def load_selected_icon(self, event):
        self.current_icon_elevation = 0
        selected_item_id = self.icons_treeview.selection()
        if selected_item_id:
            selected_icon_name = self.icons_treeview.item(selected_item_id, "text")
            icon_path = os.path.join("customizeUI/", selected_icon_name)
            if self.miniship:
                generate = self.miniship.copy()
                generate = self.resizer.sharpen(generate, self.sharpen)
                self.resizer.upsize_black_lines(self.selected_image, generate, self.outline)
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
