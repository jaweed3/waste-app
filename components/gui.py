import tkinter as tk
from tkinter import Label, filedialog, Frame
from PIL import Image, ImageTk
import requests
import os

class WasteClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Waste Classifier")
        self.root.geometry("560x600")
        
        # Main Frame
        main_frame = Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = Label(main_frame, text="Waste Classification System", font=('Times New Roman', 18))
        title_label.pack(pady=10)

        # Try to load logo if exists
        try:
            img = Image.open('logo.jpeg')
            img = img.resize((200, 100), Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(img)
            logo_label = Label(main_frame, image=logo_img)
            logo_label.image = logo_img
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Could Not load logo: {e}")

        # Image display Frame
        self.image_frame = Frame(main_frame, width=250, height=250, bg="#f0f0f0", bd=2, relief=tk.GROOVE)
        self.image_frame.pack(pady=10)
        self.image_frame.pack_propagate(False)

        # Image Display Label
        self.image_label = Label(self.image_frame, text="No Image Selected", bg="#f0f0f0")
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # Result Label
        self.result_label = Label(main_frame, text="", font=("Times New Roman", 14), bg='#f0f0f0', bd=1, relief=tk.GROOVE)
        self.result_label.pack(fill=tk.X, pady=10, ipady=10)

        # Button Frame
        button_frame = Frame(main_frame)
        button_frame.pack(pady=10)

        # Upload Button
        upload_button = tk.Button(
            button_frame,
            text="Select Image",
            command=self.image_uploader,
            bg="#4CAF50",
            fg="white",
            font=("Times New Roman", 12),
            padx=20,
            pady=5
        )
        upload_button.pack(side=tk.LEFT, padx=10)

        # Status Button
        self.status_label = Label(root, text="ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def image_uploader(self):
        file_types = [("All Image Files", "*.png *.jpg *.jpeg")]
        path = filedialog.askopenfilename(filetypes=file_types)
        full_path = os.path.basename(path)

        # If a file is selected
        if path:
            self.status_label.config(text=f"Selected: {full_path}")

            # Display the Image
            img = Image.open(path)
            img = img.resize((230, 230), Image.LANCZOS)
            pic = ImageTk.PhotoImage(img)

            self.image_label.config(image=pic, text="")
            self.image_label.image = pic

            # Send the image to Flask API
            self.predict_image(path)
        
        else:
            self.status_label.config(text="No Image Selected")

    def predict_image(self, image_path):
        try:
            self.result_label.config(text="Processing...")
            self.root.update()

            # Prepare the file for upload
            with open(image_path, 'rb') as img_file:
                files = {'image': (os.path.basename(image_path), img_file, 'image/jpeg')}

                # Send to Flask API
                response = requests.post('http://localhost:5000/predict', files=files)

                if response.status_code == 200:
                    result = response.json()
                    class_name = result['class_name']
                    confidence = result['result'] * 100

                    self.result_label.config(
                        text=f"Prediction: {class_name}\nConfidence: {confidence:.2f}%"
                    )
                    self.status_label.config(text=f"Successfully Classified as {class_name}")
                
                else:
                    error_msg = response.json().get('error', 'unknown error')
                    self.result_label.config(text=f"Error Message : {error_msg}")
                    self.status_label.config(text=f"Error During Classification")

        except Exception as e:
            self.result_label.config(text=f"Error in Sending API to Flask : {e}")
            self.status_label.config(text="Error During Classification")

def main():
    root = tk.Tk()
    app = WasteClassifierApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()