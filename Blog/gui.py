import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import base64

class ImageToBase64Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Base64 Converter")

        self.selected_image_path = tk.StringVar()
        self.base64_output = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Entry for displaying the selected image path
        self.path_entry = tk.Entry(self.root, textvariable=self.selected_image_path, state="readonly", width=40)
        self.path_entry.grid(row=0, column=0, padx=10, pady=10)

        # Browse button to select an image
        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_image)
        self.browse_button.grid(row=0, column=1, padx=10, pady=10)

        # Convert button to convert the image to base64
        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_to_base64)
        self.convert_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Text area for displaying base64 output
        self.output_text = tk.Text(self.root, height=10, width=40)
        self.output_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def browse_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("All files", "*.*")])
        if file_path:
            self.selected_image_path.set(file_path)

            # Display the selected image
            self.display_image(file_path)

    def convert_to_base64(self):
        image_path = self.selected_image_path.get()
        if image_path:
            try:
                with open(image_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    base64_data = encoded_string.decode('utf-8')
                    self.base64_output.set(base64_data)

                    # Display the base64 output in the text area
                    self.output_text.delete("1.0", tk.END)
                    self.output_text.insert(tk.END, base64_data)
            except Exception as e:
                print(f"Error: {e}")

    def display_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((200, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        # Display the image on the GUI
        image_label = tk.Label(self.root, image=img)
        image_label.image = img
        image_label.grid(row=3, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToBase64Converter(root)
    root.mainloop()
