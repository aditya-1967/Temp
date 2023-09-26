import tkinter as tk
from tkinter import messagebox
import json
import os
import qrcode
from PIL import Image

def submit_form():
    name = entry_name.get()
    age = entry_age.get()
    gender = gender_var.get()
    medical_history = text_medical_history.get('1.0', 'end-1c')

    if not name or not age or not gender:
        messagebox.showerror('Error', 'Please fill in all required fields')
        return

    registration_data = {
        "Name": name, 
        "Age": age, 
        "Gender": gender,
        "Medical History": medical_history
    }

    with open("registration.json", 'a') as file:
        json.dump(registration_data, file, indent = 4)

    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size = 10,
        border = 4,
    )

    qr.add_data(json.dumps(registration_data))
    qr.make(fit = True)
    qr_img = qr.make_image(fill_color = "black", back_color = "white")

    patient_folder = os.path.join('patient_qrcodes', name)
    os.makedirs(patient_folder, exist_ok = True)
    qr_img.save(os.path.join(patient_folder, "registration_qr.png"))

    messagebox.showinfo('Success', 'Registration Successful!')


root = tk.Tk()
root.title('Hospital Registration Form')

label_name = tk.Label(root, text = 'Name:')
label_name.pack()
entry_name = tk.Entry(root)
entry_name.pack()

label_age = tk.Label(root, text = 'Age:')
label_age.pack()
entry_age = tk.Entry(root)
entry_age.pack()

label_gender = tk.Label(root, text = 'Gender:')
label_name.pack()
gender_var = tk.StringVar()
gender_var.set('Male')
gender_radio_male = tk.Radiobutton(root, text = "Male", variable = gender_var, value = "Male")
gender_radio_female = tk.Radiobutton(root, text = "Female", variable = gender_var, value = "Female")
gender_radio_male.pack()
gender_radio_female.pack()

label_medical_history = tk.Label(root, text = "Medical History:")
label_medical_history.pack()
text_medical_history = tk.Text(root, height = 5, width = 30)
text_medical_history.pack()

submit_button = tk.Button(root, text = "Submit", command = submit_form)
submit_button.pack()

root.mainloop()