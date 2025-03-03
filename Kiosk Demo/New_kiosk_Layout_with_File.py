import tkinter as tk
from tkinter import ttk,messagebox
import cv2
from PIL import Image, ImageTk, ImageDraw
import requests
import subprocess
import threading
import customtkinter as ctk
from tkinter import PhotoImage
from tkinter import font
import pygame
import serial
import adafruit_fingerprint
import os
import time
import re
import vlc

# Initialize the main application window
root = tk.Tk()
root.title("Support System with Camera")
root.geometry("1920x1200")  # Set the window size
#root.attributes('-fullscreen', True)

# Set desired camera resolution (e.g., 640x480 or 800x600)
#CAMERA_WIDTH = 5640
#CAMERA_HEIGHT = 5420

CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

video_path = "/home/steve/Downloads/video_4.mp4"  # Default video path for playback
camera_cap = None
video_cap = None
stop_video_thread = False
video_thread = None
video_lock = threading.Lock()

UserId = None

# Create frames for organization
top_frame = tk.Frame(root, height=150, bg="lightgray")
middle_frame = tk.Frame(root, height=250)
bottom_frame = tk.Frame(root, height=200, bg="lightgray")

# Pack the frames
top_frame.pack(fill="x", padx=10, pady=10)
middle_frame.pack(fill="x", padx=10, pady=10)
bottom_frame.pack(fill="x", padx=10, pady=10)

# Create a label to display the camera feed
#camera_label = tk.Label(top_frame, bg="white", width=CAMERA_WIDTH // 15, height=CAMERA_HEIGHT // 20)
#camera_label.pack(side="left", padx=20)


def update_camera():
    """Function to display the live camera feed."""
    global camera_cap
    camera_cap = cv2.VideoCapture(0)  # Open default camera
    while True:
        ret, frame = camera_cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (CAMERA_WIDTH, CAMERA_HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        camera_label.config(image=img)
        camera_label.image = img
        camera_label.update()
    camera_cap.release()

# def update_video():
#     """Function to play the video."""
#     global video_cap, stop_video_thread, video_path
#     with video_lock:
#         video_cap = cv2.VideoCapture(video_path)
#         while not stop_video_thread:
#             ret, frame = video_cap.read()
#             if not ret:
#                 break  # Stop when the video ends
#             frame = cv2.resize(frame, (CAMERA_WIDTH, CAMERA_HEIGHT))
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             img = ImageTk.PhotoImage(Image.fromarray(frame))
#             video_label.config(image=img)
#             video_label.image = img
#             video_label.update()
#         video_cap.release()

# def change_video(new_video):
#     global video_path, stop_video_thread, video_thread
# 
#     # Stop the current video thread
#     stop_video_thread = True
#     if video_thread and video_thread.is_alive():
#         video_thread.join()  # Wait for the current thread to finish
# 
#     # Update the video path and restart the video thread
#     video_path = new_video
#     stop_video_thread = False
#     video_thread = threading.Thread(target=update_video, daemon=True)
#     video_thread.start()


# def on_closing():
#     global stop_video_thread
#     stop_video_thread = True
#     if video_cap:
#         video_cap.release()
#     if camera_cap:
#         camera_cap.release()
#     root.destroy()

# Initialize the camera
# video_Source1 = 0
# cap = cv2.VideoCapture(video_Source1,cv2.CAP_V4L) 
# 
# 
# # Function to update the camera feed in the Tkinter label
# def update_frame():
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     if ret:
#         # Convert the image from BGR (OpenCV) to RGB (Tkinter)
#         cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         img = Image.fromarray(cv2image)
#         imgtk = ImageTk.PhotoImage(image=img)
#         
#         # Update the camera label with the new frame
#         camera_label.imgtk = imgtk
#         camera_label.configure(image=imgtk)
#     
#     # Call this function again after 10 milliseconds
#     camera_label.after(10, update_frame)

def run_videocall():
    camera_cap.release()
    camera_label.after_cancel(update_camera)
    try:
        subprocess.Popen(["python3", "VideoCall_With_support.py"])  # Adjust to "python" if using Python 2
    except Exception as e:
        print(f"Error starting videocall: {e}")  

# Start the camera update loop
camera_label = tk.Label(top_frame, text="Camera Feed", bg="black", width=CAMERA_WIDTH, height=CAMERA_HEIGHT)
camera_label.pack(side="left", padx=10)

# video_CAMERA_WIDTH = 640
# video_CAMERA_HEIGHT = 360
# video_label = tk.Label(bottom_frame, text="Video Player", bg="white", width=video_CAMERA_WIDTH, height=video_CAMERA_HEIGHT)
# video_label.pack(fill="both", padx=10, pady=10)
display_label = tk.Label(bottom_frame, text="This is the display that shows the information as customer enters", bg="white", height=10)
display_label.pack(fill="both", padx=50, pady=10)

def Login_popup():
    popup = tk.Toplevel()
    popup.title("Login Popup")
    popup.geometry("500x350")
    popup.configure(bg="#e0ebeb")
#     W_popup.protocol("WM_DELETE_WINDOW", lambda: None)

#     tk.Label(popup, text="Enter Email Address:", font=("Arial", 12)).pack(pady=10)

    username_label = tk.Label(popup, text="Phone Number:", fg="black", bg="#e0ebeb",font=("Arial", 16))
    username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")    
    # CTkEntry for Name
    username_entry = ctk.CTkEntry(popup, font=('bookman old style', 20), height=40, width=280)
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    email_label = tk.Label(popup, text="Email:", fg="black", bg="#e0ebeb",font=("Arial", 16))
    email_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")    
    # CTkEntry for Name
    email_entry = ctk.CTkEntry(popup, font=('bookman old style', 20), height=40, width=280)
    email_entry.grid(row=0, column=1, padx=10, pady=10)
      
    # Entry box inside the rounded rectangle
    # entry = tk.Entry(popup, font=("Arial", 10), bg="white", borderwidth=0, justify="center")
    #entry.place(x=50, y=85, width=200, height=25)  # Adjust placement

    popup.transient(root)
    
    # Submit button
    def submit_email():
        email = email_entry.get()
        username = username_entry.get()
        url = "https://truckovernight.azurewebsites.net/api/ProducerAPI/StoreUserLogin"
        print(url)
        # Define the JSON payload
        payload = {
                   "Username": username,
                   "email": email,
                  }
        response = requests.post(url, json=payload)
        print("---------------",response)
        if response.status_code == 200:
             print("Response:", response.json())
             if not (f"{response.json()}") == "0":
                print(f"Slot status updated! Booking ID: {response.json()}")
                second_popup = tk.Toplevel()
                second_popup.title("Second Popup")
                second_popup.geometry("550x350")
                second_popup.configure(bg="#e0ebeb")
                
                #tk.Label(second_popup, text="Welcome Shradha, you have access :", font=("Arial", 14)).pack(pady=10)
                # Welcome Label
                welcome_label = tk.Label(
                    second_popup, text="Welcome Shradha, you have access:",
                    font=("Arial", 20), bg="lightblue", fg="black"
                )
                welcome_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="e")
                                     
                selected_unit = tk.StringVar(value="Select Unit")  # Default value
                units = ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5", "Unit 6", "Unit 7", "Unit 8","Unit 9","Unit 10","Unit 11","Unit 12","Unit 13","Unit 14","Unit 15","Unit 16"]
                
                def update_invoice(*args):
                    if selected_unit.get() != "Select Unit":
                        invoice_label.grid(row=3, column=1, pady=5, sticky="e")
                        invoice_details.grid(row=4, column=1, pady=5, sticky="e")
                    else:
                        invoice_label.grid_remove()
                        invoice_details.grid_remove()
                    

                # Bind the dropdown selection to update_invoice function
                selected_unit.trace_add("write", update_invoice)
                
                style = ttk.Style()
                style.configure("TCombobox", font=("Arial", 44))
                style.configure("TCombobox.dropdown", font=("Arial", 34))
                dropdown = ttk.Combobox(second_popup, textvariable=selected_unit, values=units, state="readonly", style="TCombobox")

                dropdown = tk.OptionMenu(second_popup, selected_unit, *units)
                dropdown.config(font=("Arial", 19),width=13)
                dropdown.grid(row=1, column=0, columnspan=2, pady=10)
    #             dropdown = tk.OptionMenu(second_popup, selected_unit, *units)
    #             dropdown.config(font=("Arial", 19), width=15)
    #             dropdown.pack(pady=10)
                
                 # Invoice details
                invoice_label = tk.Label(
                    second_popup, text="Invoice Bill:",
                    font=("Arial", 18, "bold"), bg="#e0ebeb", fg="black"
                )

                invoice_details = tk.Label(
                    second_popup, text="$5.89\n$8.00",  # Default invoice details
                    font=("Arial", 18), bg="#e0ebeb", fg="black"
                )

                def Rent_of_Unit():
                    selected = selected_unit.get()
                    if selected == "":
                        #stripe integration
                        messagebox.showwarning("Error", "Please select a unit!")
                    else:
                        messagebox.showinfo("Action", f"Selected Unit: {selected}")
                    
                #tk.Button(second_popup, text="Payment", command=Rent_of_Unit).pack(pady=20)
                payment_button = tk.Button(
                    second_popup, text="Payment",
                    command=Rent_of_Unit,
                    font=("Arial", 16, "bold"), bg="green", fg="white", width=15, height=2
                )
                payment_button.grid(row=5, column=0, columnspan=2, pady=20)
                second_popup.transient(root)
             else:
                messagebox.showwarning("Error", "Email cannot be empty!")
                                            
        else:
           print(f"Request failed with status code: {response.status_code}")
           print("Response content:", response.text)

#         if email:
#             #messagebox.showinfo("Success", "Login successfully")
#             second_popup = tk.Toplevel()
#             second_popup.title("Second Popup")
#             second_popup.geometry("550x350")
#             second_popup.configure(bg="#e0ebeb")
#             
#             #tk.Label(second_popup, text="Welcome Shradha, you have access :", font=("Arial", 14)).pack(pady=10)
#             # Welcome Label
#             welcome_label = tk.Label(
#                 second_popup, text="Welcome Shradha, you have access:",
#                 font=("Arial", 20), bg="lightblue", fg="black"
#             )
#             welcome_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="e")
#                                  
#             selected_unit = tk.StringVar(value="Select Unit")  # Default value
#             units = ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5", "Unit 6", "Unit 7", "Unit 8","Unit 9","Unit 10","Unit 11","Unit 12","Unit 13","Unit 14","Unit 15","Unit 16"]
#             
#             def update_invoice(*args):
#                 if selected_unit.get() != "Select Unit":
#                     invoice_label.grid(row=3, column=1, pady=5, sticky="e")
#                     invoice_details.grid(row=4, column=1, pady=5, sticky="e")
#                 else:
#                     invoice_label.grid_remove()
#                     invoice_details.grid_remove()
#                 
# 
#             # Bind the dropdown selection to update_invoice function
#             selected_unit.trace_add("write", update_invoice)
#             
#             style = ttk.Style()
#             style.configure("TCombobox", font=("Arial", 44))
#             style.configure("TCombobox.dropdown", font=("Arial", 34))
#             dropdown = ttk.Combobox(second_popup, textvariable=selected_unit, values=units, state="readonly", style="TCombobox")
# 
#             dropdown = tk.OptionMenu(second_popup, selected_unit, *units)
#             dropdown.config(font=("Arial", 19),width=13)
#             dropdown.grid(row=1, column=0, columnspan=2, pady=10)
# #             dropdown = tk.OptionMenu(second_popup, selected_unit, *units)
# #             dropdown.config(font=("Arial", 19), width=15)
# #             dropdown.pack(pady=10)
#             
#              # Invoice details
#             invoice_label = tk.Label(
#                 second_popup, text="Invoice Bill:",
#                 font=("Arial", 18, "bold"), bg="#e0ebeb", fg="black"
#             )
# 
#             invoice_details = tk.Label(
#                 second_popup, text="$5.89\n$8.00",  # Default invoice details
#                 font=("Arial", 18), bg="#e0ebeb", fg="black"
#             )
# 
#             def Rent_of_Unit():
#                 selected = selected_unit.get()
#                 if selected == "":
#                     #stripe integration
#                     messagebox.showwarning("Error", "Please select a unit!")
#                 else:
#                     messagebox.showinfo("Action", f"Selected Unit: {selected}")
#                 
#             #tk.Button(second_popup, text="Payment", command=Rent_of_Unit).pack(pady=20)
#             payment_button = tk.Button(
#                 second_popup, text="Payment",
#                 command=Rent_of_Unit,
#                 font=("Arial", 16, "bold"), bg="green", fg="white", width=15, height=2
#             )
#             payment_button.grid(row=5, column=0, columnspan=2, pady=20)
#         
# #             payment_button = ctk.CTkButton(
# #                 second_popup, 
# #                 text="Payment", 
# #                 command= Rent_of_Unit,
# #                 font=("Arial", 16),  # Increased font size
# #                 height=2,  # Set button height
# #                 width=30,  # Set button width
# #                 bg="#009999",  # Background color
# #                 fg="white",  # Text color
# #                 relief="raised"  # Raised border style (optional)        
# #                 )
# #             payment_button.grid(row=1, column=0, columnspan=2, pady=20)
#             second_popup.transient(root)
#         else:
#             messagebox.showwarning("Error", "Email cannot be empty!")
    
    #tk.Button(popup, text="Submit", command=submit_email).pack(pady=10)
    
        
    submit_button = tk.Button(
            popup, 
            text="Submit", 
            command= submit_email,
            font=("Arial", 16),  # Increased font size
            height=2,  # Set button height
            width=35,  # Set button width
            bg="#009999",  # Background color
            fg="white",  # Text color
            relief="raised"  # Raised border style (optional)        
        )
    submit_button.grid(row=5, column=0, columnspan=2, pady=20,sticky="e")
    Login_fp_button = tk.Button(
            popup, 
            text="Finger print", 
            command= Login_Fp_submit,
            font=("Arial", 16),  # Increased font size
            height=2,  # Set button height
            width=35,  # Set button width
            bg="#009999",  # Background color
            fg="white",  # Text color
            relief="raised"  # Raised border style (optional)        
        )
    Login_fp_button.grid(row=6, column=0, columnspan=2, pady=20,sticky="e")


def open_fingerprint_popup():
    # Create a new popup window
    Fp_popup = tk.Toplevel()
    Fp_popup.title("Fingerprint Registration")
    Fp_popup.geometry("400x320")
    Fp_popup.configure(bg="white")

    # Add the "place your fingerprint" label
    label = tk.Label(Fp_popup, text="Place your fingerprint", font=("Arial", 16), bg="white")
    label.pack(pady=20)
    
    message_label = tk.Label(Fp_popup, text="Initializing...", font=("Arial", 14), bg="white", fg="green")
    message_label.pack(pady=20)

    # Load the fingerprint image
    try:
        fingerprint_image = Image.open("/home/pi/Downloads/fingerprint.png")  # Replace with your image path
        fingerprint_image = fingerprint_image.resize((50, 50),Image.Resampling.LANCZOS)
        fingerprint_photo = ImageTk.PhotoImage(fingerprint_image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {str(e)}")
        return

    # Add the fingerprint button
    fingerprint_button = tk.Button(Fp_popup, image=fingerprint_photo,command=lambda: submit_fingerprint(message_label,Fp_popup))# command=submit_fingerprint)
    fingerprint_button.image = fingerprint_photo  # Keep a reference to avoid garbage collection
    fingerprint_button.pack(pady=10)
    Fp_popup.after(500, submit_fingerprint(message_label,Fp_popup))    
    Fp_popup.focus_force()
    Fp_popup.transient(root)

otp = None
u_name = None
def send_otp():
    """Function to hide phone number field and show OTP field"""
    global otp
    phone = phone_entry.get().strip()
    print("-----------------phone",phone)
    
    url = "https://truckovernight.azurewebsites.net/api/MobileBookingAPI/SendOtpAsync"
    print(url)
    # Define the JSON payload
    payload = {
                "phone": phone            
              }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
         print("Response:", response.json())
         if not (f"{response.json()}") == "0":
               print(f"S: {response.json()}")
               response_data = response.json()                   
               otp = response_data
               
               print(f"OTP is --------: {otp}")
               u_name = otp['Username']
               print("----------------------FP_Username is", u_name)
               
    else:
       print(f"Request failed with status code: {response.status_code}")
       print("Response content:", response.text)

    
    # Hide phone number label, entry, and submit button
    phone_label.pack_forget()  
    phone_entry.pack_forget()  
    submit_SendOtp_button.pack_forget()  
    
    # Show OTP label, entry, and verify button
    Otp_label.pack(padx=10, pady=10,side=tk.LEFT)
    Otp_entry.pack(padx=10, pady=10,side=tk.LEFT)
    verify_button.pack(pady=10)  # Show verify button

def Verify_send_otp():
    global otp,u_name
    print("----------------------- u_name",u_name)
    Otp = Otp_entry.get().strip()
    otp = Otp

    if Otp == otp:       
        popup = tk.Toplevel()
        popup.title("Welcome")
        popup.geometry("300x150")
        popup.configure(bg="white")
        
        # Add a welcome label
        welcome_label = tk.Label(
            popup,
            text=f"Welcome Your Store{u_name}",
            font=("Arial", 16),
            bg="white",
            fg="Green"
        )
        welcome_label.pack(pady=40)
        popup.transient(root)
        print("Successfully Varify Otp")

def open_Login_Fp_popup():
    global phone_label, phone_entry, Otp_label, Otp_entry, submit_SendOtp_button, verify_button
    # Create a new popup window
    Fp_popup = tk.Toplevel()
    Fp_popup.title("Authentication")
    Fp_popup.geometry("400x320")
    Fp_popup.configure(bg="white")
    
    # Add the "place your fingerprint" label
    label = tk.Label(Fp_popup, text="Place your fingerprint", font=("Arial", 16), bg="white")
    label.pack(pady=20)

    # Load the fingerprint image
    try:
        fingerprint_image = Image.open("/home/steve/Downloads/fingerprint.png")  # Replace with your image path
        fingerprint_image = fingerprint_image.resize((50, 50),Image.Resampling.LANCZOS)
        fingerprint_photo = ImageTk.PhotoImage(fingerprint_image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {str(e)}")
        return
    
    # Add the fingerprint button
    fingerprint_button = tk.Button(Fp_popup, image=fingerprint_photo, command=Login_Fp_submit)
    fingerprint_button.image = fingerprint_photo  # Keep a reference to avoid garbage collection
    fingerprint_button.pack(pady=10)
    
    # Main Frame to hold everything (Ensures proper layout)
    frame = tk.Frame(Fp_popup, bg="white")
    frame.pack(pady=10)
    
    # Phone Number Label & Entry (Initially Visible)
    phone_label = tk.Label(frame, text="Phone Number:", fg="black", bg="white", font=("Arial", 16))
    phone_label.pack(side=tk.LEFT, pady=10, padx=10)

    phone_entry = ctk.CTkEntry(frame, font=('bookman old style', 20), height=40, width=280)
    phone_entry.pack(side=tk.LEFT, pady=10, padx=10)

    # Submit Button to Enter Phone Number
    submit_SendOtp_button = tk.Button(
        Fp_popup,
        text="Submit",
        command=send_otp,  # Show OTP field when clicked
        font=("Arial", 16),
        height=2,
        width=35,
        bg="#009999",
        fg="white",
        relief="raised"
    )
    submit_SendOtp_button.pack(pady=10, padx=10)
    
    # OTP Label & Entry (Initially Hidden)
    Otp_label = tk.Label(frame, text="OTP:", fg="black", bg="white", font=("Arial", 16))
    Otp_entry = ctk.CTkEntry(frame, font=('bookman old style', 20), height=40, width=280)

    # Verify Button (Initially Hidden)
    verify_button = tk.Button(
        Fp_popup,
        command=Verify_send_otp,
        text="Verify OTP",
        font=("Arial", 16),
        height=2,
        width=30,
        bg="#009999",
        fg="white",
        relief="raised"
    )
    
    #Fp_popup.after(500, Login_Fp_submit)    
    #Fp_popup.focus_force()
    Fp_popup.transient(root)
    #Login_Fp_submit()


def Login_welcome_popup(u_name):
    # Create a popup window to show the welcome message
    popup = tk.Toplevel()
    popup.title("Welcome")
    popup.geometry("300x150")
    popup.configure(bg="white")
    
    # Add a welcome label
    welcome_label = tk.Label(
        popup,
        text=f"Welcome {u_name}",
        font=("Arial", 16),
        bg="white",
        fg="Green"
    )
    welcome_label.pack(pady=40)
    popup.transient(root)


def FP_Login_Construct_url(matched_FpId):
    FingerprintId = matched_FpId
    fingerid = FingerprintId
    print("-------------------------------------------------------------",FingerprintId)

    templet_url = "https://truckovernight.azurewebsites.net/api/ProducerAPI/getUserByFingerprintId?fingerid={}&fingerD1=null&fingerD2=null&fingerD3=null"   
    return templet_url.format(FingerprintId)

def FP_Login_get_and_parse_json(url):
    try:
        #print(url)
        response = requests.get(url)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            print("----------------------",data)
            
            extracted_data = []
            
            for row in data:
                extracted_data.append(row)
                
            total = len(extracted_data)
            return extracted_data
        else:
            print("Request failed with status code:", response.status_code)
            return None, None
    except Exception as e:
        print("An error occurred:", e)
        return None, None

def open_register_popup():
    popup= tk.Toplevel()
    popup.title("Registation")
    popup.geometry("500x360")
    popup.configure(bg="#e0ebeb")
    
     
    # Name Label
    name_label = tk.Label(popup, text="Name:", fg="black", bg="#e0ebeb",font=("Arial", 16))
    name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")    
    # CTkEntry for Name
    name_entry = ctk.CTkEntry(popup, font=('bookman old style', 20), height=40, width=280)
    name_entry.grid(row=0, column=1, padx=10, pady=10)
    

    email_label = tk.Label(popup, text="Email:", fg="black", bg="#e0ebeb",font=("Arial", 16))
    email_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")    
    # CTkEntry for Name
    email_entry = ctk.CTkEntry(popup, font=('bookman old style', 20), height=40, width=280)
    email_entry.grid(row=2, column=1, padx=10, pady=10)
    
 
    phone_label = tk.Label(popup, text="Phone Number:", fg="black", bg="#e0ebeb",font=("Arial", 16))
    phone_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")    
    # CTkEntry for Name
    phone_entry = ctk.CTkEntry(popup, font=('bookman old style', 20), height=40, width=280)
    phone_entry.grid(row=3, column=1, padx=10, pady=10)
    
       
    popup.transient(root)

    # Submit button
    def submit_registration():
        global UserId
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()
        
         # Name validation
        if not name:
            messagebox.showerror("Invalid Input", "Please enter your name.")
            return False
        
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            messagebox.showerror("Invalid Input", "Please enter a valid email address.")
            return False
        
        phone_pattern = r"^\d{10}$"
        if not re.match(phone_pattern, phone):
            messagebox.showerror("Invalid Input", "Please enter a valid 10-digit phone number.")
            return False
        

#         if name and email and phone:
#            # messagebox.showinfo("Success", f"Registration Successful!\nName: {name}\nEmail: {email}\nPhone: {phone}\n")
#             open_fingerprint_popup()
#             success_label.config(text="User successfully registered!", fg="green")
#             #popup.destroy()
#         else:
#             success_label.config(text="Failed to register fingerprint.", fg="red")
           # messagebox.showwarning("Error", "All fields are required!")
           
        if name and email and phone:
            url = "https://truckovernight.azurewebsites.net/api/ProducerAPI/StoreChamberUserRegistration"
            print(url)
            # Define the JSON payload
            payload = {
                        "Username": name,
                        "Email": email,
                        "Phone": phone,
                        #"Address": address,
                        "Fingerprint":"A",
                        "FingerprintId":"null",
                        "FingerData1":"null",
                        "FingerData2":"null",
                        "FingerData3":"null"
                     }
            response = requests.post(url, json=payload)
           # print("------------------",response)
            if response.status_code == 200:
                 print("Response:", response.json())
                 if not (f"{response.json()}") == "0":
                       print(f"S: {response.json()}")
                       response_data = response.json()
                        # Check if the response is an integer or a dictionary
                       if isinstance(response_data, int):                    
                            UserId = response_data
                       elif isinstance(response_data, dict):                       
                            UserId = response_data.get("UserId")  # Adjust the key based on your API response                        
                       else:
                            raise ValueError("Unexpected response format")
                         
                       print(f"User ID -----: {UserId}")
                       open_fingerprint_popup()
                       success_label.config(text="User successfully registered!", fg="green")
            else:
               print(f"Request failed with status code: {response.status_code}")
               print("Response content:", response.text)
               success_label.config(text="Failed to register fingerprint.", fg="red")


    #tk.Button(popup, text="Submit", command=submit_registration).pack(pady=20)
    submit_button = tk.Button(
        popup, 
        text="Submit", 
        command=submit_registration ,
        font=("Arial", 16),  # Increased font size
        height=2,  # Set button height
        width=35,  # Set button width
        bg="#009999",  # Background color
        fg="white",  # Text color
        relief="raised"  # Raised border style (optional)
        
    )
    submit_button.grid(row=5, column=0, columnspan=2, pady=20,sticky="e")
    
    fp_link = tk.Label(popup, text="Are you an existing User?", fg="blue", bg="#e0ebeb", font=("Arial", 12), cursor="hand2")
    fp_link.grid(row=6, column=0, columnspan=2, pady=10)
    fp_link.bind("<Button-1>", lambda e: open_Login_Fp_popup())
    
    success_label = tk.Label(popup, text="", font=("Arial", 10))
    success_label.grid(row=7, column=0, columnspan=2, pady=10)

#Old find Fingerpring code with API
def Login_Fp_submit():
    uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
    finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
    
    FINGERPRINT_FOLDER = "save_fingerprint/"
    print("Waiting for fingerprint...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Processing image...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Error processing image.")
        return False
    print("Searching for matches in the template folder...", end="")
    """  ##########################################################################  """
    found_match = False
    matched_filename = None
    for filename in os.listdir(FINGERPRINT_FOLDER):
        if filename.endswith(".dat"):
            file_path = os.path.join(FINGERPRINT_FOLDER, filename)
            with open(file_path, "rb") as file:
                data = file.read()
                print("FINGERPRINT_FOLDER filename...",file_path)
            finger.send_fpdata(list(data), "char", 2)
            if finger.compare_templates() == adafruit_fingerprint.OK:
                matched_filename =  filename
               # print("****************************************",matched_filename)
                found_match = True
                break
    if found_match:
        ######## you can make changes here to what to do when the finger authenticated ##########
        #print(f"Fingerprint matches the template in the file {matched_filename}!")
        matched_FpId = matched_filename
        print("----------------------- FingerprintId is ",matched_FpId)
        url = FP_Login_Construct_url(matched_FpId)
        print(url)
        
        response = requests.get(url)
        if response.status_code == 200:
             print("Response:", response.json())
             if not (f"{response.json()}") == "0":
                 data = response.json()
                 u_name = data['Username']
                 print("----------------------FP_Username is", u_name)
                 Login_welcome_popup(u_name)                           
        else:
           print(f"Request failed with status code: {response.status_code}")
           print("Response content:", response.text)
                 
    else:
        print("No match found.")
    """ ############################################################################### """
    # The above marked location code can be changed to work with your custom API to read data
    return found_match


#Old enrole finger print Code
def submit_fingerprint(message_label,Fp_popup):    
        global UserId
        uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
        finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
        
        def update_label(text,color="green"):
            """Update the message label text."""
            message_label.config(text=text,fg=color)
            message_label.update_idletasks()
        
        FINGERPRINT_FOLDER = "save_fingerprint/"
        MAX_RETRIES = 3
        for attempt in range(MAX_RETRIES):
            print(f"Enrollment attempt {attempt + 1} of {MAX_RETRIES}")
            update_label(f"Enrollment attempt {attempt + 1} of {MAX_RETRIES}", "green")
            for fingerimg in range(1, 3):
                if fingerimg == 1:
                    print("Place finger on sensor...", end="")
                    update_label("Place your finger on the sensor...", "green")
                else:
                    print("Place same finger again...", end="")
                    update_label("Place the same finger again...", "green")

                while True:
                    i = finger.get_image()
                    if i == adafruit_fingerprint.OK:
                        print("Image taken")
                        update_label("Image taken successfully.")
                        break
                    if i == adafruit_fingerprint.NOFINGER:
                        print(".", end="")
                        update_label("Waiting for finger...")
                    elif i == adafruit_fingerprint.IMAGEFAIL:
                        print("Imaging error")
                        update_label("Imaging error. Please try again.", "red")
                        return False
                    else:
                        print("Other error")
                        return False
                    
                print("Templating...", end="")
                i = finger.image_2_tz(fingerimg)
                if i == adafruit_fingerprint.OK:
                    print("Templated")
                else:
                    if i == adafruit_fingerprint.IMAGEMESS:
                        print("Image too messy")
                    elif i == adafruit_fingerprint.FEATUREFAIL:
                        print("Could not identify features")
                        update_label("Could not identify features. Try again.")
                    elif i == adafruit_fingerprint.INVALIDIMAGE:
                        print("Image invalid")
                        update_label("Invalid image. Try again.", "red")
                    else:
                        print("Other error")
                    return False
                    
                if fingerimg == 1:
                    print("Remove finger")
                    update_label("Finger removed. Ready for the next scan.", "blue")
                    time.sleep(1)
                    while i != adafruit_fingerprint.NOFINGER:
                        i = finger.get_image()

            print("Creating model...", end="")
            i = finger.create_model()
            if i == adafruit_fingerprint.OK:
                print("Created")
            else:
                if i == adafruit_fingerprint.ENROLLMISMATCH:
                    print("Prints did not match")
                    update_label("Fingerprints did not match. Try again.")
                else:
                    print("Other error")
                    update_label("Error creating model. Try again.")
                return False
            print("Storing template...")
            """ ############################################################################## """
            filename = f"template_{int(time.time())}.dat"
            data = finger.get_fpdata("char", 1)
            filename_with_path = os.path.join(FINGERPRINT_FOLDER, f"template_{int(time.time())}.dat")
            with open(filename_with_path, "wb") as file:
                file.write(bytearray(data))
            """ ############################################################################### """
            
            
            Fp_id = filename #FpId.get()
            print("------------------------- Fp_id is ",Fp_id)  
            UId = UserId
            print("------------------------- UId_id is ",UId)
            url = "https://truckovernight.azurewebsites.net/api/ProducerAPI/UpdateStoreChamberUser"
            print(url)
            # Define the JSON payload
            payload = {
                        "Id":UId,
                        "FingerprintId": Fp_id 
                        #"FingerData1":Fp_img
                     }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                 print("Response:", response.json())
                 if not (f"{response.json()}") == "0":
                       print(f"fingerprint: {response.json()}")
                       Fp_popup.destroy()
                                                
            else:
               print(f"Request failed with status code: {response.status_code}")
               print("Response content:", response.text)
               Fp_popup.destroy()
                
                # The above marked location code can be changed to work with your custom API to write data
            print(f"Template saved to {filename}")
            return True




# register_button = tk.Button(
#     middle_frame,
#     text="Register User",
#     width=25,
#     height=2,
#     bg="#f0f5f5",  # Background color
#     fg="black",    # Text color
#     command=open_register_popup
# )
# register_button.pack(anchor="e", padx=10, pady=10)
# #register_button.place(x=1350, y=450)
# 
# Login_button = tk.Button(
#     middle_frame,
#     text="Login User",
#     width=25,
#     height=2,
#     bg="#f0f5f5",  # Background color
#     fg="black",    # Text color
#     #relief="flat", # Flat style
#     command=Login_popup
# )
# Login_button.pack(anchor="e", padx=10, pady=10)
#Login_button.place(x=680, y=450)
    
info_frame = tk.Frame(middle_frame)
info_frame.pack(anchor="w", pady=10)

green_label = tk.Label(info_frame, text="●", font=("Arial", 21), fg="green")
green_label.grid(row=0, column=0, padx=5,sticky="w")
green_text = tk.Label(info_frame, text="- Available to Rent", font=("Arial", 15))
green_text.grid(row=0, column=1, padx=5,sticky="w")

red_label = tk.Label(info_frame, text="●", font=("Arial", 21), fg="red")
red_label.grid(row=1, column=0, padx=5,sticky="w")
red_text = tk.Label(info_frame, text="- Already Rented", font=("Arial", 15))
red_text.grid(row=1, column=1, padx=5,sticky="w")

gray_label = tk.Label(info_frame, text="●", font=("Arial", 21), fg="gray")
gray_label.grid(row=2, column=0, padx=5,sticky="w")
gray_text = tk.Label(info_frame, text="- Reserved", font=("Arial", 15))
gray_text.grid(row=2, column=1, padx=5,sticky="w")

def fullscreen():
    root.attributes('-fullscreen', True)


fullscreen_button = tk.Button(
    middle_frame,
    text="FullScreen",
    width=25,
    height=2,
    bg="#f0f5f5",  # Background color
    fg="black",    # Text color
    command=fullscreen
)
fullscreen_button.pack(anchor="e", padx=10, pady=10)


# def extract_audio(video_path, audio_path):
#     """Extract audio from video using ffmpeg."""
#     subprocess.run(['ffmpeg', '-i', video_path, '-q:a', '0', '-map', 'a', audio_path])
# Initialize pygame mixer for audio playback
#pygame.mixer.init()

def open_video_popup():
    popup = tk.Toplevel(root)
    popup.title("Video Player")
    popup.geometry("870x500")

    # VLC Instance
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new("/home/pi/Downloads/welcome-video_RzrvDBH9 (online-video-cutter.com).mp4")
    player.set_media(media)

    # Embedding VLC in Tkinter window
    video_frame = tk.Frame(popup, width=870, height=500)
    video_frame.pack(expand=True, fill="both")
    popup.update_idletasks()  # Ensures winfo_id() is available
    player.set_xwindow(video_frame.winfo_id())

    player.play()
    
    # Initialize button list and state tracking
    buttons = []
    buttons_hidden = False
    custom_font = font.Font(family="Helvetica", size=12, weight="bold")

    def hide_buttons():
        """Hide all buttons and prevent them from reappearing."""
        nonlocal buttons_hidden
        for button in buttons:
            button.place_forget()
        popup.update_idletasks()  # Force UI update
        buttons_hidden = True  # Mark buttons as hidden

    def goto_video(seconds):
        """Jump to a specific timestamp in the video and hide all buttons."""
        player.set_time(seconds * 1000)  # VLC time is in milliseconds
        hide_buttons()  # Hide buttons after clicking

    def check_time():
        """Check the current video time and update button positions after 53 seconds."""
        nonlocal buttons_hidden
        current_time = player.get_time() // 1000  # Convert ms to seconds

        if current_time >= 53 and not buttons_hidden:
            btn1.place(relx=0.35, rely=0.50, anchor="w")
            btn2.place(relx=0.65, rely=0.50, anchor="w")
            btn3.place(relx=0.35, rely=0.93, anchor="w")
            btn4.place(relx=0.65, rely=0.93, anchor="w")

        popup.after(1000, check_time)  # Check every second

    def on_close():
        """Stop video and close popup on exit."""
        player.stop()
        popup.destroy()

    popup.protocol("WM_DELETE_WINDOW", on_close)

    # Define buttons
    btn1 = tk.Button(popup, text="Rent a Unit First Time", width=20, height=1,
                     font=custom_font, command=lambda: goto_video(130))
    btn2 = tk.Button(popup, text="Access a Unit Already Rented", width=20, height=1,
                     font=custom_font, command=lambda: goto_video(257))
    btn3 = tk.Button(popup, text="Unique Question?", width=20, height=1,
                     font=custom_font, command=lambda: goto_video(351))
    btn4 = tk.Button(popup, text="Speak to Live Person", width=20, height=1,
                     font=custom_font, command=lambda: goto_video(437))

    # Store buttons in list
    buttons.extend([btn1, btn2, btn3, btn4])

    # Initially hide buttons
    btn1.place_forget()
    btn2.place_forget()
    btn3.place_forget()
    btn4.place_forget()

    # Start checking video time
    popup.after(1000, check_time)
    
    
    
    
#     popup = tk.Toplevel(root)
#     popup.title("Video Player")
#     popup.geometry("870x500")
#       
#     # Create a label to display the video
#     video_label = tk.Label(popup)
#     video_label.pack(expand=True, fill="both")
#     
# 
#     # Initialize video variables
#     video_path = "/home/pi/Downloads/Sale Rep Promo 25 mb (1).mp4"
#     # "/home/pi/Downloads/welcome-video_1.mp4"  # Default video file path
#     audio_path = "/home/pi/Downloads/wp_temp_audio.mp3"
#     video_cap = None
#     start_time = None
#    # is_paused = False  # Flag to control pause and resume
# 
#     
#     # Initialize pygame mixer for audio playback
#     pygame.mixer.init()
# 
#     #Extract audio from the video
# #     audio_path = "/home/pi/Downloads/wp_temp_audio.mp3"
# #     extract_audio(video_path, audio_path)
# #     pygame.mixer.music.load(audio_path)  # Load audio
# #     pygame.mixer.music.play()  # Start playing audio
#     
#     buttons = []
#     custom_font = font.Font(family="Helvetica", size=12, weight="bold")
#     btn1 = tk.Button(
#         popup,
#         text="Rent a Unit First Time",
#         width=20,
#         height=1,
#         bg="#f0f0f0",  # Green background
#         fg="Black",    # White text
#         font=custom_font,  # Apply custom font
#         relief="raised",  # 3D raised effect
#         bd=4,  # Border width
#         activebackground="#e6e6e6",  # Lighter green when hovered
#         activeforeground="black",  # White text when hovered
#         #command=lambda: change_video("/home/pi/Downloads/video_3.mp4")
#         command=lambda: goto_video(130)
#     )
#    
#     btn1.place(anchor="w", relx=0.35, rely=0.50)
#     buttons.append(btn1)
#     btn1.place_forget()  # Hide the button initially
# 
#     btn2 = tk.Button(
#         popup,
#         text="Access a Unit Already Rented",
#         width=20,
#         height=1,
#         bg="#f0f0f0",  # Green background
#         fg="Black",    # White text
#         font=custom_font,  # Apply custom font
#         relief="raised",  # 3D raised effect
#         bd=4,  # Border width
#         activebackground="#e6e6e6",  # Lighter green when hovered
#         activeforeground="black",  # White text when hovered
#         #command=lambda: change_video("/home/pi/Downloads/video_2.mp4")
#         command=lambda: goto_video(257)
#     )
#     btn2.place(relx=0.65, rely=0.50, anchor="w")
#     buttons.append(btn2)
#     btn2.place_forget()  # Hide the button initially
# 
#     btn3 = tk.Button(
#         popup,
#         text="Unique Question?",
#         width=20,
#         height=1,
# #         bg="#f0f5f5",  # Background color
# #         fg="black",    # Text color
#         bg="#f0f0f0",  # Green background
#         fg="Black",    # White text
#         font=custom_font,  # Apply custom font
#         relief="raised",  # 3D raised effect
#         bd=4,  # Border width
#         activebackground="#e6e6e6",  # Lighter green when hovered
#         activeforeground="black",  # White text when hovered
#         #command=lambda: change_video("/home/pi/Downloads/video_2.mp4")
#         command=lambda: goto_video(351)
#     )
#     btn3.place(relx=0.35, rely=0.93, anchor="w")
#     buttons.append(btn3)
#     btn3.place_forget()  # Hide the button initially
#     #btn3.pack(anchor="e", padx=10, pady=10)
# 
#     btn4 = tk.Button(
#         popup,
#         text="Speak to Live Person",
#         width=20,
#         height=1,
# #         bg="#f0f5f5",  # Background color
# #         fg="black",    # Text color
#         bg="#f0f0f0",  # Green background
#         fg="Black",    # White text
#         font=custom_font,  # Apply custom font
#         relief="raised",  # 3D raised effect
#         bd=4,  # Border width
#         activebackground="#e6e6e6",  # Lighter green when hovered
#         activeforeground="black",  # White text when hovered
#        # command=lambda: change_video("/home/pi/Downloads/video_2.mp4")
#         command=lambda: goto_video(437)
#     )
#     btn4.place(relx=0.65, rely=0.93, anchor="w")
#     buttons.append(btn4)
#     btn4.place_forget()  # Hide the button initially
#     
# 
#     def play_video():
#         nonlocal video_cap,start_time
#         if video_cap is None:
#             video_cap = cv2.VideoCapture(video_path)
#             start_time = cv2.getTickCount()
#             
#              # Load and play audio
#             if pygame.mixer.get_init():
#                 try:
#                     pygame.mixer.music.load(audio_path)
#                     pygame.mixer.music.set_volume(1.5)  # Adjust volume if necessary
#                     pygame.mixer.music.play(loops=0, start=0.0)
#                     pygame.mixer.music.play()
#                 except pygame.error as e:
#                     print(f"Error loading audio: {e}")
#             
#             
# #             # Load and play audio
# #             audio_path = video_path.replace('.mp4', '.mp3')  # Assuming the audio file is in MP3 format
# #             pygame.mixer.music.load(audio_path)
# #             pygame.mixer.music.play(-1)  # Loop audio indefinitely
# 
#     
#         ret, frame = video_cap.read()
#         if ret:
#             # Convert the frame to RGB and display it
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             img = ImageTk.PhotoImage(Image.fromarray(frame))
#             video_label.config(image=img)
#             video_label.image = img
#             
#              # Calculate elapsed time
#             if start_time is not None:
#                 elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
#                 current_pos = video_cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Get current position in seconds
#                 #if current_pos >= 120:
#                 if elapsed_time >= 53:  # Show buttons after 51 seconds
#                     btn1.place(relx=0.35, rely=0.50, anchor="w")
#                     btn2.place(relx=0.65, rely=0.50, anchor="w")
#                     btn3.place(relx=0.35, rely=0.93, anchor="w")
#                     btn4.place(relx=0.65, rely=0.93, anchor="w")
#                     pause_video()
#                         
# #             # Pause at 2:00 minutes (120 seconds)
# #                 if current_pos >= 120:  # 2 minutes
# #                     pause_video()
# #              # Calculate elapsed time
# #             elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
# #             if elapsed_time >= 42:  # Show buttons after 42 seconds
# #                 btn1.place(anchor="w", relx=0.7, rely=0.25)
# #                 btn2.place(anchor="w", relx=0.7, rely=0.35)
#             
#             video_label.after(10, play_video)
#         else:
#             video_cap.release()
#             if pygame.mixer.get_init():
#                 pygame.mixer.music.stop()  # Stop audio when video ends
#             video_cap = None  # Reset video capture for reuse
#             popup.destroy()
# 
#     def change_video(new_path):
#         nonlocal video_path, video_cap
#         video_path = new_path
#         if video_cap is not None:
#             #pygame.mixer.music.stop()
#             video_cap.release()
#             if pygame.mixer.get_init():
#                 pygame.mixer.music.stop()  # Stop audio if video is changed
#             video_cap = None  # Reset the video capture
#             
#             if os.path.exists(audio_path):
#                 try:
#                     os.remove(audio_path)
#                     print(f"Deleted temporary audio file: {audio_path}")
#                 except Exception as e:
#                     print(f"Error deleting file: {e}")
#             
#         play_video()  # Start playing the new video
#                        
# #         # Extract audio from the new video
#         audio_path = "/home/pi/Downloads/wp_temp_audio.mp3"
#         extract_audio(new_video_path, audio_path)  # Extract audio from video
#         pygame.mixer.music.load(audio_path)  # Load new audio
#         pygame.mixer.music.play()  # Play audio
#         
#           # Hide all buttons
#         for button in buttons:
#             button.place_forget()
#             
#     def forward_video(seconds):
#         """Forward the video by a specified number of seconds."""
#         nonlocal video_cap, start_time
#         if video_cap is not None:
#             current_pos = video_cap.get(cv2.CAP_PROP_POS_MSEC)  # Get current position in milliseconds
#             new_pos = current_pos + (seconds * 1000)  # Calculate new position
#             video_cap.set(cv2.CAP_PROP_POS_MSEC, new_pos)  # Set new position
#             start_time = cv2.getTickCount() - (new_pos / 1000 * cv2.getTickFrequency())  # Update start_time
#     
#     def goto_video(seconds):
#         """Forward the video by a specified number of seconds."""
#         nonlocal video_cap, start_time
#         if video_cap is not None:            
#             new_pos = (seconds * 1000)  # Calculate new position
#             video_cap.set(cv2.CAP_PROP_POS_MSEC, new_pos)  # Set new position
#             start_time = cv2.getTickCount() - (new_pos / 1000 * cv2.getTickFrequency())  # Update start_time
#             
#              # Sync audio with the video
#             if pygame.mixer.get_init():
#                 pygame.mixer.music.stop()
#                 pygame.mixer.music.play(start=new_pos / 1000)  # Start audio at new position
#         
# #         nonlocal video_cap, start_time
# #         if video_cap is not None:
# #             current_pos = video_cap.get(cv2.CAP_PROP_POS_MSEC)  # Get current position in milliseconds
# #             new_pos = current_pos + (seconds * 1000)  # Calculate new position
# #             video_cap.set(cv2.CAP_PROP_POS_MSEC, new_pos)  # Set new position
# #             start_time = cv2.getTickCount() - (new_pos / 1000 * cv2.getTickFrequency())  # Update start_time
# 
#     def handle_keypress(event):
#         """Handle keypress events."""
#         if event.char == "1":
#             goto_video(130)  # Forward by 20 seconds
#         elif event.char == "2":
#             goto_video(257)  # Forward by 20 seconds
#         elif event.char == "3":
#             goto_video(351)  # Forward by 20 seconds            
#         elif event.char == "4":
#             goto_video(437)  # Forward by 40 seconds
# 
#     # Bind keypress events to the popup window
#     popup.bind("<KeyPress>", handle_keypress)
#     
#     # Start playing the initial video
#     play_video()
#     popup.transient(root)

#     buttons = []
#     
#     btn1 = tk.Button(
#         popup,
#         text="Rent a Unit First Time",
#         width=20,
#         height=1,
#         bg="#f0f5f5",  # Background color
#         fg="black",    # Text color
#         #relief="flat", # Flat style
#         command=lambda: change_video("/home/pi/Downloads/video_3.mp4")
#     )
#     btn1.place(anchor="w", relx=0.7, rely=0.25)
#     buttons.append(btn1)
# 
#     btn2 = tk.Button(
#         popup,
#         text="Access a Unit Already Rented",
#         width=20,
#         height=1,
#         bg="#f0f5f5",  # Background color
#         fg="black",    # Text color
#         #relief="flat", # Flat style
#         command=lambda: change_video("/home/pi/Downloads/video_2.mp4")
#     )
#     btn2.place(relx=0.7, rely=0.45, anchor="w")
#     buttons.append(btn2)
# 
#     btn3 = tk.Button(
#         popup,
#         text="Unique Question?",
#         width=20,
#         height=1,
#         bg="#f0f5f5",  # Background color
#         fg="black",    # Text color
#         #relief="flat", # Flat style
#         command=lambda: change_video("/home/pi/Downloads/video_2.mp4")
#     )
#     btn3.place(relx=0.7, rely=0.65, anchor="w")
#     buttons.append(btn3)
#     #btn3.pack(anchor="e", padx=10, pady=10)
# 
#     btn4 = tk.Button(
#         popup,
#         text="Speak to a Live Person",
#         width=20,
#         height=1,
#         bg="#f0f5f5",  # Background color
#         fg="black",    # Text color
#         #relief="flat", # Flat style
#         command=lambda: change_video("/home/pi/Downloads/video_2.mp4")
#     )
#     btn4.place(relx=0.7, rely=0.85, anchor="w")
#     buttons.append(btn4)   
    
  
# Open_video_btn = tk.Button(
#     middle_frame,
#     text="AI Support",
#     width=30,
#     height=2,
#     bg="#f0f5f5",  # Background color
#     fg="black",    # Text color
#     #relief="flat", # Flat style
#     command=lambda: open_video_popup()
# )
# Open_video_btn.pack(anchor="e", padx=10, pady=10)
# 
# register_button = tk.Button(
#     middle_frame,
#     text="Rent a Unit First Time",
#     width=30,
#     height=2,
#     bg="#f0f5f5",  # Background color
#     fg="black",    # Text color
#     #relief="flat", # Flat style
#     command=open_register_popup
# )
# register_button.pack(anchor="e", padx=10, pady=10)
# 
# Login_button = tk.Button(
#     middle_frame,
#     text="Access a Unit Already Rented",
#     width=30,
#     height=2,
#     bg="#f0f5f5",  # Background color
#     fg="black",    # Text color
#     #relief="flat", # Flat style
#     command=Login_popup
# )
# Login_button.pack(anchor="e", padx=10, pady=10)
# 
# Contact_button = tk.Button(
#     middle_frame,
#     text="Contact Owner Directly",
#     width=30,
#     height=2,
#     bg="#f0f5f5",  # Background color
#     fg="black",    # Text color
#     #relief="flat", # Flat style
#     #command=open_register_popup
# )
# Contact_button.pack(anchor="e", padx=10, pady=10)
# 
# SpeakLive_button = tk.Button(
#     middle_frame,
#     text="Speak to Live Person",
#     width=30,
#     height=2,
#     bg="#f0f5f5",  # Background color
#     fg="black",    # Text color
#     #relief="flat", # Flat style
#     #command=Login_popup
# )
# SpeakLive_button.pack(anchor="e", padx=10, pady=10)
def create_rounded_button(frame, text, command, width=300, height=80, bg="white", fg="gray", border_color="gray", border_width=2):
    """Create a rounded button with border using Pillow."""
    # Create a blank image with transparent background
    radius = height // 2
    button_image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(button_image)

    # Draw the border (outer rounded rectangle)
    draw.rounded_rectangle(
        [(border_width, border_width), (width - border_width, height - border_width)],
        radius=radius,
        outline=border_color,
        width=border_width,
        fill=bg
    )

    # Convert the image to a PhotoImage for Tkinter
    button_photo = ImageTk.PhotoImage(button_image)

    # Create a label to act as the button
    button_label = tk.Label(
        frame,
        text=text,
        image=button_photo,
        compound="center",
        fg=fg,
        font=("Arial", 14, "bold"),
        bd=0,
        cursor="hand2"
    )
    button_label.image = button_photo  # Keep a reference to avoid garbage collection
    #button_label.pack(pady=15)  # Add spacing between buttons
    button_label.pack(anchor="e", padx=10, pady=10)

    # Bind the click event to the command
    button_label.bind("<Button-1>", lambda event: command())


# Add the custom rounded button

create_rounded_button(
    middle_frame, "Access a Unit Already Rented", Login_popup, width=300, height=50, 
    bg="white", fg="gray", border_color="gray", border_width=2
)
create_rounded_button(
    middle_frame, "Contact Owner Directly", open_register_popup, width=300, height=50, 
    bg="white", fg="gray", border_color="gray", border_width=2
)
create_rounded_button(
    middle_frame, "Speak to Live Person" ,open_register_popup, width=300, height=50, 
    bg="white", fg="gray", border_color="gray", border_width=2
)

def create_rounded_button_for_TopFrame(frame, text, command,x,y, width=300, height=80, bg="white", fg="gray", border_color="gray", border_width=2):
    """Create a rounded button with border using Pillow."""
    # Create a blank image with transparent background
    radius = height // 2
    button_image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(button_image)

    # Draw the border (outer rounded rectangle)
    draw.rounded_rectangle(
        [(border_width, border_width), (width - border_width, height - border_width)],
        radius=radius,
        outline=border_color,
        width=border_width,
        fill=bg
    )

    # Convert the image to a PhotoImage for Tkinter
    button_photo = ImageTk.PhotoImage(button_image)

    # Create a label to act as the button
    button_label = tk.Label(
        frame,
        text=text,
        image=button_photo,
        compound="center",
        fg=fg,
        font=("Arial", 14, "bold"),
        bd=0,
        cursor="hand2"
    )
    button_label.image = button_photo  # Keep a reference to avoid garbage collection
    #button_label.pack(pady=15)  # Add spacing between buttons
    #button_label.pack(anchor="e", padx=10, pady=10)
    button_label.place(x=x, y=y, anchor="e")

    # Bind the click event to the command
    button_label.bind("<Button-1>", lambda event: command())


create_rounded_button_for_TopFrame(
    top_frame, "AI Support Agent", open_video_popup,x=860, y=220, width=300, height=50, 
    bg="white", fg="gray", border_color="gray", border_width=2
)
create_rounded_button_for_TopFrame(
    top_frame, "Rent a Unit First Time", open_register_popup,x=1190, y=220, width=300, height=50, 
    bg="white", fg="gray", border_color="gray", border_width=2
)



# #Video buttons
# btn1 = tk.Button(
#     middle_frame,
#     text="Rent a Unit First Time",
#     width=30,
#     height=2,
#     bg="#f0f5f5",  # Background color
#     fg="black",    # Text color
#     #relief="flat", # Flat style
#     command=lambda: change_video("/home/pi/Downloads/video_2.mp4")
# )
# btn1.pack(anchor="e", padx=10, pady=10)
# 
# btn2 = tk.Button(
#     middle_frame,
#     text="Access a Unit Already Rented",
#     width=30,
#     height=2,
#     bg="#f0f5f5",  # Background color
#     fg="black",    # Text color
#     #relief="flat", # Flat style
#     command=lambda: change_video("/home/pi/Downloads/video_3.mp4")
# )
# btn2.pack(anchor="e", padx=10, pady=10)
# 
# btn3 = tk.Button(
#     middle_frame,
#     text="Unique Question?",
#     width=30,
#     height=2,
#     bg="#f0f5f5",  # Background color
#     fg="black",    # Text color
#     #relief="flat", # Flat style
#     command=lambda: change_video("/home/pi/Downloads/video_4.mp4")
# )
# btn3.pack(anchor="e", padx=10, pady=10)
# 
# btn4 = tk.Button(
#     middle_frame,
#     text="Speak to a Live Person",
#     width=30,
#     height=2,
#     bg="#f0f5f5",  # Background color
#     fg="black",    # Text color
#     #relief="flat", # Flat style
#     command=lambda: change_video("/home/pi/Downloads/video_5.mp4")
# )
# btn4.pack(anchor="e", padx=10, pady=10)
    
support_label = tk.Label(top_frame, text="Support Person ON CALL\n(Real person's face)", width=50, height=15, bg="white")
support_label.pack(side="right", padx=20)

support_label.bind("<Button-1>", lambda e: run_videocall())


#Face_button = tk.Button(middle_frame, text="Face that gains Access",command=lambda:Rec_Photo_details,width=30, height=3)
#Face_button.pack(pady=10)

# Add button for "Push for Assistance"
#push_button = tk.Button(middle_frame, text="Push for Assistance", width=30, height=2, command=lambda: messagebox.showinfo("Assistance", "Assistance requested"))
#push_button.pack(pady=10)

# Create grid of buttons for units
units_frame_top = tk.Frame(top_frame)
units_frame_bottom = tk.Frame(top_frame)

units_frame_top.pack(pady=20)
units_frame_bottom.pack(pady=20)

def Update_Unit_Image(StoreChamberName,Status):
    if(StoreChamberName == "Unit 1"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")           
            
    if(StoreChamberName == "Unit 2"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
    if(StoreChamberName == "Unit 3"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
    if(StoreChamberName == "Unit 4"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
    if(StoreChamberName == "Unit 5"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
    if(StoreChamberName == "Unit 6"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
    if(StoreChamberName == "Unit 7"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
    if(StoreChamberName == "Unit 8"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
    if(StoreChamberName == "Unit 9"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
     
    if(StoreChamberName == "Unit 10"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
    if(StoreChamberName == "Unit 11"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
    if(StoreChamberName == "Unit 12"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
    if(StoreChamberName == "Unit 13"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
    if(StoreChamberName == "Unit 14"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
    if(StoreChamberName == "Unit 15"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
    if(StoreChamberName == "Unit 16"):
        if(Status == 0):
            buttons[StoreChamberName].config(bg="gray")
        if(Status == 1):
            buttons[StoreChamberName].config(bg="green")
        if(Status == 2):
            buttons[StoreChamberName].config(bg="red")
            
            
# List of top units (Unit 1 - Unit 8)
top_units = ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5", "Unit 6", "Unit 7", "Unit 8"]
buttons = {}

for i, unit in enumerate(top_units):
    btn = tk.Button(units_frame_top, text=unit, width=5, height=2, bg="white")
    btn.grid(row=0, column=i, padx=5)
    buttons[unit] = btn

# List of bottom units (Unit 11 - Unit 18)
bottom_units = ["Unit 9", "Unit 10", "Unit 11", "Unit 12", "Unit 13", "Unit 14", "Unit 15", "Unit 16"]
# Create buttons for the bottom units and add to frame
for i, unit in enumerate(bottom_units):
    btn = tk.Button(units_frame_bottom, text=unit, width=5, height=2, bg="white")  # All buttons are white
    btn.grid(row=1, column=i, padx=5)
    buttons[unit] = btn

def create_button_grid(parent, rows, cols, unit_labels):
    buttons = {}
    grid_frame = tk.Frame(parent)  # Create a separate frame for the grid
    for i in range(rows):
        for j in range(cols):
            index = i * cols + j
            if index < len(unit_labels):
                unit = unit_labels[index]
                btn = tk.Button(grid_frame, text=unit, width=5, height=2, bg="green")
                btn.grid(row=i, column=j, padx=5, pady=5)
                buttons[unit] = btn
    return grid_frame, buttons


# Create the first grid (5x5)
tk.Label(middle_frame, text="5 X 5", bg="white", font=("Arial", 12, "bold")).place(x=630, y=120)
grid_frame, grid_buttons = create_button_grid(middle_frame, 2, 2,["Unit 1", "Unit 2", "Unit 3", "Unit 4"])
grid_frame.place(x=565, y=150) 

tk.Label(middle_frame, text="5 X 10", bg="white", font=("Arial", 12, "bold")).place(x=850, y=120)
grid_frame, grid_buttons = create_button_grid(middle_frame, 2, 2, ["Unit 5", "Unit 6", "Unit 7", "Unit 8"])
grid_frame.place(x=790, y=150) 

tk.Label(middle_frame, text="10 X 20", bg="white", font=("Arial", 12, "bold")).place(x=1075, y=120)
grid_frame, grid_buttons = create_button_grid(middle_frame, 2, 2, ["Unit 9", "Unit 10", "Unit 11", "Unit 12"])
grid_frame.place(x=1020, y=150) 

def Construct_url():
    templet_url = "https://truckovernight.azurewebsites.net/api/slotsapi/GetSelfStoreApi"
    return templet_url

def get_and_parse_json(url):
    try:
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            print(data)
            # Extract required key-value pairs
            total =  data['total']
            extracted_data = []
            
            for row in data['rows']:
                extracted_data.append({
                    'StoreChamberId': row['StoreChamberId'],
                    'StoreChamberName': row['StoreChamberName'],                                                                                                                   
                    'Status': row['Status']
                })
            
            return total, extracted_data
            
        else:
            print("Request failed with status code:", response.status_code)
            return None, None
    except Exception as e:
        print("An error occurred:", e)
        return None, None

def submit_request():
    url = Construct_url()

    # Trigger GET request and parse JSON
    total, extracted_data = get_and_parse_json(url)
    
    #update_tag_number_text.set("")
    if total is not None and extracted_data is not None:
            #print("Total:", total)
            #print("Extracted data:",extracted_data)
            for item in extracted_data:     
                Update_Unit_Image(item['StoreChamberName'],item['Status'])
                
def FP_Construct_url(): #GetFpApi
    
    tp_templet_url = "https://truckovernight.azurewebsites.net/api/ProducerAPI/GetFingerprintByUserId?id={}"
    return tp_templet_url

def Fp_get_and_parse_json(Fp_url):
    try:
        print(Fp_url)
        response = requests.get(Fp_url)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            #print(data)           
            Fp_extracted_data = []
            
            for row in data:
                Fp_extracted_data.append(row)
            
            total = len(Fp_extracted_data)
            print('**************************',total)
            return total, Fp_extracted_data
            
        else:
            print("Request failed with status code:", response.status_code)
            return None, None
    except Exception as e:
        print("An error occurred:", e)
        return None, None

def Fp_request():
    Fp_url = FP_Construct_url()   
     # Trigger GET request and parse JSON
    total, Fp_extracted_data = Fp_get_and_parse_json(Fp_url)
    
    #update_tag_number_text.set("")
    if total is not None and Fp_extracted_data is not None:
            print("Total:", total)
            print("Extracted data:",Fp_extracted_data)
            for item in Fp_extracted_data:
                FpId = item['fingerprint']
                print("------------------------- Fp_id is ",FpId)
               

def close_app():
    #subprocess.run(["sudo", "reboot"], check=True)
    #subprocess.run(["sudo", "shutdown", "now"])
    pygame.mixer.music.stop()
    root.destroy()

close_button = tk.Button(bottom_frame, text="Close Application", command=close_app, width=20, height=2, bg="red", fg="white")
close_button.pack(pady=20)


#Update_Unit_Image(StoreChamberName,Status)
submit_request()
threading.Thread(target=update_camera, daemon=True).start()
# video_thread = threading.Thread(target=update_video, daemon=True)
# video_thread.start()
# Start the Tkinter main loop
root.mainloop()

# Release the camera when the window is closed
#cap.release()
cv2.destroyAllWindows()



