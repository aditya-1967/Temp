import tkinter as tk
from tkinter import messagebox
import json
import os
import qrcode
from PIL import Image

def clear_form():
    entry_name.delete(0, 'end')
    entry_age.delete(0, 'end')
    gender_var.set('Male')
    text_medical_history.delete('1.0', 'end')
    entry_aadhar.delete(0, 'end')

def submit_form():
    name = entry_name.get()
    age = entry_age.get()
    gender = gender_var.get()
    medical_history = text_medical_history.get('1.0', 'end-1c')
    aadhar_number = entry_aadhar.get()

    if not name or not age or not gender or not aadhar_number:
        messagebox.showerror('Error', 'Please fill in all required fields')
        return

    # registration_data = {
    #     "Name": name, 
    #     "Age": age, 
    #     "Gender": gender,
    #     "Medical History": medical_history
    # }

    # with open("registration.json", 'a') as file:
    #     json.dump(registration_data, file, indent = 4)

    # if os.path.exists('registration.json'):
    #     with open('registration.json', 'r') as file:
    #         data = json.load(file)
    #         if aadhar_number in data:
    #             data[aadhar_number].update({
    #                 "Name": name, 
    #                 "Age": age, 
    #                 "Gender": gender,
    #                 "Medical History": medical_history
    #             })
    #         else:
    #             data[aadhar_number]({
    #                 "Name": name, 
    #                 "Age": age, 
    #                 "Gender": gender,
    #                 "Medical History": medical_history
    #             })
    # else:
    #     data = {
    #         aadhar_number: {
    #             "Name": name, 
    #             "Age": age, 
    #             "Gender": gender,
    #             "Medical History": medical_history
    #         }}

    data = {}

    if os.path.exists('registration.json'):
        with open('registration.json', 'r') as file:
            try: 
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}

    if aadhar_number in data:
        data[aadhar_number].update({
            "Name": name, 
            "Age": age,
            "Gender": gender,
            "Medical History": medical_history
        })
    else:
        data[aadhar_number] = {
            "Name": name, 
            "Age": age, 
            "Gender": gender,
            "Medical History": medical_history
        }
    
    with open('registration.json', 'w') as file:
        json.dump(data, file, indent=4)

    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size = 10,
        border = 4,
    )

    qr.add_data(json.dumps(data[aadhar_number]))
    qr.make(fit = True)
    qr_img = qr.make_image(fill_color = "black", back_color = "white")

    patient_folder = os.path.join('patient_qrcodes', name)
    os.makedirs(patient_folder, exist_ok = True)
    qr_img.save(os.path.join(patient_folder, "registration_qr.png"))

    messagebox.showinfo('Success', 'Registration Successful!')
    clear_form()

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

label_aadhar = tk.Label(root, text='Aadhar Number:')
label_aadhar.pack()
entry_aadhar = tk.Entry(root)
entry_aadhar.pack()

submit_button = tk.Button(root, text = "Submit", command = submit_form)
submit_button.pack()

root.mainloop()