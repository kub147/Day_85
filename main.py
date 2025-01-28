import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App")

        # Initialize variables
        self.image = None
        self.watermarked_image = None

        # Create UI elements
        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=5)

        self.canvas = tk.Canvas(root, width=1000, height=800, bg="gray")
        self.canvas.pack()

        self.watermark_text_label = tk.Label(root, text="Watermark Text:")
        self.watermark_text_label.pack(pady=5)

        self.watermark_text_entry = tk.Entry(root, width=30)
        self.watermark_text_entry.pack(pady=5)

        self.add_watermark_button = tk.Button(root, text="Add Watermark", command=self.add_watermark)
        self.add_watermark_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack(pady=5)

    def load_image(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select an image file",
                filetypes=[("Image Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")]
            )
            if not file_path:
                return

            self.image = Image.open(file_path)
            self.display_image(self.image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")
            print(f"Error details: {e}")  # Log error details for debugging

    def display_image(self, image):
        # Resize image to fit canvas
        image.thumbnail((1000, 800))
        self.tk_image = ImageTk.PhotoImage(image)

        # Calculate position to center the image
        x = (self.canvas.winfo_width() - self.tk_image.width()) // 2
        y = (self.canvas.winfo_height() - self.tk_image.height()) // 2

        # Create the image on the canvas centered
        self.canvas.create_image(x, y, image=self.tk_image, anchor="nw")

    def add_watermark(self):
        if not self.image:
            messagebox.showerror("Error", "Please load an image first!")
            return

        watermark_text = self.watermark_text_entry.get()
        if not watermark_text:
            messagebox.showerror("Error", "Please enter watermark text!")
            return

        # Create a copy of the image to add watermark
        self.watermarked_image = self.image.copy()
        draw = ImageDraw.Draw(self.watermarked_image)

        # Use a fallback font if Helvetica.ttc is not available
        try:
            font = ImageFont.truetype("/Users/kuba/Downloads/Indie_Flower/IndieFlower-Regular.ttf", 46)
        except IOError:
            font = ImageFont.load_default()

        # Obliczanie rozmiaru tekstu
        bbox = draw.textbbox((0, 0), watermark_text, font)
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # Wyśrodkowanie tekstu
        x = (self.image.width - width) // 2  # Wyśrodkowanie poziome
        y = (self.image.height - height) - 20  # Wyśrodkowanie pionowe

        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))  # White text with transparency

        self.display_image(self.watermarked_image)

    def save_image(self):
        if not self.watermarked_image:
            messagebox.showerror("Error", "No watermarked image to save!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"),
                                                            ("All Files", "*.*")])
        if file_path:
            self.watermarked_image.save(file_path)
            messagebox.showinfo("Success", "Image saved successfully!")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
