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
import pyautogui

# Initialize the main application window
root = tk.Tk()
root.title("Support System with Camera")
root.geometry("1920x1200")  # Set the window size
#root.attributes('-fullscreen', True)

def go_fullscreen():
    root.attributes('-fullscreen', False)

def open_popup():
    root.after(2000,go_fullscreen)  

root.after(2000,open_popup)

warning_box = None
IsChamber = None
def get_network_strength():
    try:
        # Run the `iwconfig` command
        result = subprocess.run(['iwconfig'], capture_output=True, text=True)
        output = result.stdout

        # Find signal level
        for line in output.splitlines():
            if "Signal level" in line:
                # Parse the signal level
                signal_strength = int(line.split("Signal level=")[1].split()[0].replace('dBm', ''))
                return signal_strength
        return None  # Signal level not found
    except Exception as e:
        return None

def update_signal_strength():  
    global warning_box , IsChamber # Access the global warning box reference

    signal_strength = get_network_strength()
    if signal_strength is not None:
        if signal_strength < -60:  # Threshold for poor signal
            if warning_box is None:  # Show warning only if not already displayed
                warning_box = tk.Toplevel(root)
                warning_box.title("Network Alert")
                warning_label = tk.Label(warning_box, text="Your network connection is poor.", fg="red", font=("Arial", 14))
                warning_label.pack(padx=20, pady=20)
                # Add a close button
               # close_button = tk.Button(warning_box, text="Close", command=warning_box.destroy)
                close_button = tk.Button(warning_box, text="Close", command=close_warning_box)
                close_button.pack(pady=10)
                warning_box.protocol("WM_DELETE_WINDOW", lambda: None)
                if IsChamber == 0:
                    StoreChamberUnits()
                
        else:
            if warning_box is not None:  # If network is good, close the warning box
                close_warning_box()
            # If the network is good, close the warning box if it exists
#             if warning_box is not None:
#                 warning_box.destroy()
#                 warning_box = None
    else:
        messagebox.showerror("Network Alert", "Please connect to a network.")

    #window.attributes('-fullscreen', True)
    go_fullscreen()
    # Repeat every 5 seconds    
    root.after(5000, update_signal_strength)
def close_warning_box():
    global warning_box
    if warning_box:
        warning_box.destroy()
        warning_box = None

update_signal_strength()

CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

# video_path = "/home/pi/Downloads/video_4.mp4"  # Default video path for playback
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

def run_videocall():
    camera_cap.release()
    camera_label.after_cancel(update_camera)
    try:
        subprocess.Popen(["python3", "/home/steve/Downloads/Open_browser.py"])
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
display_label.pack(fill="both", padx=10, pady=10)


def Login_popup():
    popup = tk.Toplevel()
    popup.title("Login Popup")
    popup.geometry("500x350")
    popup.configure(bg="#e0ebeb")

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

    popup.transient(root)
    
    # Submit button
    def submit_email():
        email = email_entry.get()
        username = username_entry.get()
        url = "https://truckovernight.azurewebsites.net/api/ProducerAPI/StoreUserLogin"
        auth_token = "LPvJs79vG3XQL-dSRKIPIXRRk7zJNWMLDbpsGuc1Hdx-Y9XwjvzsIw=="

        headers = {
            #'Token': f'Bearer {auth_token}',
            'Token': auth_token,
            'Content-Type': 'application/json'
        }

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
        else:
           print(f"Request failed with status code: {response.status_code}")
           print("Response content:", response.text)
        
    submit_button = tk.Button(
            popup, 
            text="Submit", 
            command= submit_email,
            font=("Arial", 16),  
            height=2,  
            width=35,  
            bg="#009999",  
            fg="white",  
            relief="raised"        
        )
    submit_button.grid(row=5, column=0, columnspan=2, pady=20,sticky="e")
    Login_fp_button = tk.Button(
            popup, 
            text="Finger print", 
            command= Login_Fp_submit,
            font=("Arial", 16),  
            height=2,  
            width=35,  
            bg="#009999",  
            fg="white",  
            relief="raised"       
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
        fingerprint_image = Image.open("/home/steve/Downloads/fingerprint.png")  # Replace with your image path
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
    auth_token = "LPvJs79vG3XQL-dSRKIPIXRRk7zJNWMLDbpsGuc1Hdx-Y9XwjvzsIw=="

    headers = {
                'Token': auth_token,
                'Content-Type': 'application/json'
              }
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
           
        if name and email and phone:
            url = "https://truckovernight.azurewebsites.net/api/ProducerAPI/StoreChamberUserRegistration"
            auth_token = "LPvJs79vG3XQL-dSRKIPIXRRk7zJNWMLDbpsGuc1Hdx-Y9XwjvzsIw=="
            headers = {
                        'Token': auth_token,
                        'Content-Type': 'application/json'
                      }
            #print(url)
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
    
    help_link = tk.Label(popup, text="help?", fg="blue", bg="#e0ebeb", font=("Arial", 12), cursor="hand2")
    help_link.grid(row=6, column=1, columnspan=2, pady=10, sticky="e")
    help_link.bind("<Button-1>", lambda e: Open_rent_unit_video())
    
    success_label = tk.Label(popup, text="", font=("Arial", 10))
    success_label.grid(row=7, column=0, columnspan=2, pady=10)


def Open_rent_unit_video():
    popup = tk.Toplevel(root)
    popup.title("Video Player")
    popup.geometry("870x500")

    # VLC Instance
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new("/home/steve/Downloads/Rent First Time.mp4") 
    player.set_media(media)

    # Create a frame to hold the video
    video_frame = tk.Frame(popup, width=870, height=500)
    video_frame.pack(expand=True, fill="both")

    popup.update_idletasks()  
    time.sleep(0.1)

    player.set_xwindow(video_frame.winfo_id()) 
    # player.set_hwnd(video_frame.winfo_id())
    
    def on_close():
        """Stop video and close popup on exit."""
        player.stop()
        popup.destroy()

    popup.protocol("WM_DELETE_WINDOW", on_close)

    player.play()
    popup.transient(root)
    


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
                found_match = True
                break
    if found_match:
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
            auth_token = "LPvJs79vG3XQL-dSRKIPIXRRk7zJNWMLDbpsGuc1Hdx-Y9XwjvzsIw=="
            headers = {
                        'Token': auth_token,
                        'Content-Type': 'application/json'
                      }
            #print(url)
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
    
info_frame = tk.Frame(middle_frame)
info_frame.pack(anchor="w", pady=5)

#Vertically 
green_label = tk.Label(info_frame, text="●", font=("Arial", 21), fg="green")
green_label.grid(row=0, column=0, padx=5, sticky="w")
green_text = tk.Label(info_frame, text="- Available to Rent", font=("Arial", 15))
green_text.grid(row=0, column=1, padx=5, sticky="w")

red_label = tk.Label(info_frame, text="●", font=("Arial", 21), fg="red")
red_label.grid(row=0, column=2, padx=5, sticky="w")
red_text = tk.Label(info_frame, text="- Already Rented", font=("Arial", 15))
red_text.grid(row=0, column=3, padx=5, sticky="w")

gray_label = tk.Label(info_frame, text="●", font=("Arial", 21), fg="gray")
gray_label.grid(row=0, column=4, padx=5, sticky="w")
gray_text = tk.Label(info_frame, text="- Reserved", font=("Arial", 15))
gray_text.grid(row=0, column=5, padx=5, sticky="w")


def open_video_popup():
    try:
        subprocess.Popen(["python3","/home/steve/Downloads/AI_assest.py"])
    except Exception as e:
        print(f"Error: {e}")    
    
    
  #     camera_cap.release()
  #  camera_label.after_cancel(update_camera)
#     try:
#         subprocess.Popen(["python3", "/home/steve/Downloads/AI_assest.py"])
#     except Exception as e:
#         print(f"Error starting videocall: {e}")
        
#     popup = tk.Toplevel(root)
#     popup.title("Video Player")
#     popup.geometry("870x500")
# 
#     # VLC Instance
#     instance = vlc.Instance()
#     player = instance.media_player_new()
#     media = instance.media_new("/home/steve/Downloads/New Welcome Video.mp4")
#     player.set_media(media)
# 
#     # Embedding VLC in Tkinter window
#     video_frame = tk.Frame(popup, width=870, height=500)
#     video_frame.pack(expand=True, fill="both")
#     popup.update_idletasks()
#     player.set_xwindow(video_frame.winfo_id())

#     player.play()
# 
#     # Initialize button list and state tracking
#     buttons = []
#     buttons_shown = False
#     custom_font = font.Font(family="Helvetica", size=12, weight="bold")
# 
#     def show_buttons():
#         """Show buttons and pause the video."""
#         nonlocal buttons_shown
#         if not buttons_shown:
#             btn1.place(relx=0.35, rely=0.50, anchor="w")
#             btn2.place(relx=0.65, rely=0.50, anchor="w")
#             btn3.place(relx=0.35, rely=0.93, anchor="w")
#             btn4.place(relx=0.65, rely=0.93, anchor="w")
#             player.pause()
#             buttons_shown = True
# 
#     def hide_buttons():
#         """Hide all buttons."""
#         for button in buttons:
#             button.place_forget()
#         popup.update_idletasks()
# 
#     def goto_video(seconds):
#         """Jump to a specific time in the video and hide buttons."""
#         if seconds == "register":
#             player.stop()
#             popup.destroy()
#             open_register_popup()
#         if seconds == "Login":
#             player.stop()
#             popup.destroy()
#             open_Login_Fp_popup()   
#         else:
#             player.set_time(seconds * 1000)  # VLC time is in milliseconds
#             player.play()
#             hide_buttons()

#     def check_time():
#         """Check the current video time and show buttons at 2 minutes and 7 seconds."""
#         current_time = player.get_time() // 1000  # Convert ms to seconds
# 
#         if current_time >= 186 and not buttons_shown:
#             show_buttons()
# 
#         popup.after(1000, check_time)  # ✅ Check every second
# 
#     def on_close():
#         """Stop video and close popup on exit."""
#         player.stop()
#         popup.destroy()
# 
#     popup.protocol("WM_DELETE_WINDOW", on_close)
# 
#     # Define buttons
#     btn1 = tk.Button(popup, text="Rent a Unit First Time", width=20, height=1,
#                      font=custom_font, command=lambda: goto_video("register"))
#     btn2 = tk.Button(popup, text="Access a Unit Already Rented", width=20, height=1,
#                      font=custom_font, command=lambda: goto_video("Login"))
#     btn3 = tk.Button(popup, text="Unique Question?", width=20, height=1,
#                      font=custom_font, command=lambda: goto_video(351))
#     btn4 = tk.Button(popup, text="Speak to Live Person", width=20, height=1,
#                      font=custom_font, command=lambda: goto_video(437))
# 
#     # Store buttons in list
#     buttons.extend([btn1, btn2, btn3, btn4])
#     for btn in buttons:
#         btn.place_forget()
# 
#     # Start checking video time
#     popup.after(1000, check_time)
#     popup.transient(root)


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

# Create a subframe for support section (icon + text + button)
support_frame = tk.Frame(top_frame, bg="white", width=300, height=250)
support_frame.pack(side="right", padx=30, pady=10)
support_frame.pack_propagate(False)  # Prevent resizing

# Load and resize the icon
icon_image = Image.open("/home/steve/Downloads/customer-service.png")
icon_image = icon_image.resize((60, 60))  # Slightly smaller
call_icon = ImageTk.PhotoImage(icon_image)

# Icon label
icon_label = tk.Label(
    support_frame,
    image=call_icon,
    bg="white"
)
icon_label.image = call_icon
icon_label.pack(pady=(20, 5))  # Push icon slightly up

# Text label
text_label = tk.Label(
    support_frame,
    text="Support Person ON CALL",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="black"
)
text_label.pack(pady=(5, 10))  # Space between icon and button

# Rounded button using modified function without 'place'
def create_centered_rounded_button(parent, text, command, width=260, height=50, bg="white", fg="gray", border_color="gray", border_width=2):
    radius = height // 2
    button_image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(button_image)
    draw.rounded_rectangle(
        [(border_width, border_width), (width - border_width, height - border_width)],
        radius=radius,
        outline=border_color,
        width=border_width,
        fill=bg
    )
    button_photo = ImageTk.PhotoImage(button_image)

    button_label = tk.Label(
        parent,
        text=text,
        image=button_photo,
        compound="center",
        fg=fg,
        font=("Arial", 13, "bold"),
        bd=0,
        bg="white",
        cursor="hand2"
    )
    button_label.image = button_photo
    button_label.pack(pady=(0, 10))  # Padding below the button
    button_label.bind("<Button-1>", lambda event: command())

# Add the button
create_centered_rounded_button(support_frame, "Speak to Live Person", run_videocall)



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
    btn = tk.Button(units_frame_bottom, text=unit, width=5, height=2, bg="white") 
    btn.grid(row=1, column=i, padx=5)
    buttons[unit] = btn

def StoreChamberUnits():
    global IsChamber
    def create_button_grid(parent, labels, grid_size):
        frame = tk.Frame(parent)
        buttons = []
        for i, label in enumerate(labels):
            btn = tk.Button(frame, text=label, width=10, height=2, command=lambda l=label, g=grid_size: StoreChamber_Payment(l, g))
            btn.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            buttons.append(btn)
        return frame, buttons

    def scroll_left():
        canvas.xview_scroll(-1, "units")  

    def scroll_right():
        canvas.xview_scroll(1, "units")    

    canvas = tk.Canvas(middle_frame)
    h_scrollbar = tk.Scrollbar(middle_frame, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=h_scrollbar.set)

    left_button = tk.Button(middle_frame, text="◀", font=("Arial", 10, "bold"), command=scroll_left, width=1, height=1)
    right_button = tk.Button(middle_frame, text="▶", font=("Arial", 10, "bold"), command=scroll_right, width=1, height=1)

    # Layout
    left_button.pack(side="left", padx=10, pady=10)
    canvas.pack(side="left", fill="both", expand=True)
    right_button.pack(side="right", padx=10, pady=10)
    #h_scrollbar.pack(side="bottom", fill="x")

    # Drag-to-scroll support
    def on_touch_scroll_start(event):
        canvas.scan_mark(event.x, event.y)

    def on_touch_scroll_move(event):
        canvas.scan_dragto(event.x, event.y, gain=1)

    canvas.bind("<ButtonPress-1>", on_touch_scroll_start)
    canvas.bind("<B1-Motion>", on_touch_scroll_move)

    # --- API Call and UI Building ---
    siteId = 3
    url = f"https://truckovernight.azurewebsites.net/api/ProducerAPI/GetStorechamberList?siteid={siteId}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            IsChamber = 1
            data = response.json()
           # print("API Response:", data)
     
            grid_sizes = {}
            for item in data:
                dimension = item['Dimension']
                chamber_names = item['StoreChamberName']
                if dimension and chamber_names:
                    units = [u.strip() for u in chamber_names.split(',')]

                    frame = tk.Frame(scrollable_frame, padx=10, pady=10)
                    
                    title = f"{dimension}"
                    tk.Label(frame, text=title, font=("Arial", 12, "bold")).pack(pady=(0, 10))

                    grid_frame, grid_buttons = create_button_grid(frame, units, dimension)
                    grid_frame.pack()
                    frame.pack(side="left", padx=20, pady=10)

            # UI generation
            for grid_size, units in grid_sizes.items():
                frame = tk.Frame(middle_frame)
                tk.Label(frame, text=grid_size, font=("Arial", 12, "bold")).pack()
                grid_frame, grid_buttons = create_button_grid(frame, units, grid_size)
                grid_frame.pack()
                frame.pack(side="left", padx=10, pady=10)
        
        else:
            print("API call failed. Status:", response.status_code)
            print("Response content:", response.text)
    except Exception as e:
        print("Error during API call:", e)

root.after(2000,StoreChamberUnits)

# def create_button_grid(parent, rows, cols, labels, grid_size):
#     frame = tk.Frame(parent)
#     buttons = []
#     
#     for i, label in enumerate(labels):
#         btn = tk.Button(frame, text=label, width=10, height=2, command=lambda l=label, g=grid_size: StoreChamber_Payment(l,g))
#         btn.grid(row=i // cols, column=i % cols, padx=5, pady=5)
#         buttons.append(btn)
#     
#     return frame, buttons
#  
# grid_size = "5X5"
# tk.Label(middle_frame, text=grid_size,  font=("Arial", 12, "bold")).place(x=630, y=120)
# grid_frame, grid_buttons = create_button_grid(middle_frame, 2, 2, ["Unit 1", "Unit 2", "Unit 3", "Unit 4"],grid_size)
# grid_frame.place(x=525, y=150)
# 
# grid_size = "5X10"
# tk.Label(middle_frame, text=grid_size, font=("Arial", 12, "bold")).place(x=930, y=120)
# grid_frame, grid_buttons = create_button_grid(middle_frame, 2, 2, ["Unit 5", "Unit 6", "Unit 7", "Unit 8"],grid_size)
# grid_frame.place(x=835, y=150)
# 
# grid_size = "10X20"
# tk.Label(middle_frame, text=grid_size,  font=("Arial", 12, "bold")).place(x=1240, y=120)
# grid_frame, grid_buttons = create_button_grid(middle_frame, 2, 2, ["Unit 9", "Unit 10", "Unit 11", "Unit 12"],grid_size)
# grid_frame.place(x=1150, y=150)


l = None
g = None
storeId = None
Rent_price = None
SiteId = None
PaymentIntentId = None
storechamberId = None
loader_popup = None

def StoreChamber_Payment(unit_name, grid_size):
    global l, g, SiteId, Rent_price, storechamberId
    l = unit_name  
    g = grid_size
    Storechamber()
    url = payment_Construct_url()
    response = requests.get(url)
    #print("+++++++++",response)
    
    if response.status_code == 200:
             print("Response:", response.json())
             if not (f"{response.json()}") == "0":
                    data = response.json()
                    UnitName = data['StoreChamberName']
                    UnitId = data['StoreChamberId']
                    Rent_price = data['PricePerSlot']
                    SiteId = data['SiteId']
                    display_label.config(
                        text=f"\n\nUnit Name : \t{UnitName} \nPrice : \t\t${Rent_price}0",
                        font=("Arial", 16),
                        fg="black",
                        bg="white",
                        anchor="n", 
                        justify="left",
                        padx=10
                    )
                    display_label.pack(fill="both", padx=10, pady=(10, 10))
                    
                    payment_button.place(x=850, y=795, width=200, height=50)
                                          
             else:
               print(f"Request failed with status code: {response.status_code}")
               print("Response content:", response.text)


def show_loader():
    global loader_popup
    loader_popup = tk.Toplevel()
    loader_popup.title("Loading...")
    loader_popup.geometry("500x350")
    loader_popup.configure(bg="white")

    gif_path = "/home/steve/Downloads/Loading_icon.gif"
    gif = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(gif.seek(i) or gif) for i in range(gif.n_frames)]
    print("----------------------------------",frames)

    # Label for Loader GIF
    gif_label = tk.Label(loader_popup, bg="white")
    gif_label.pack(pady=20)

    def animate(index=0):
        if loader_popup and index < len(frames):  # Ensure the popup exists
            gif_label.config(image=frames[index])
            loader_popup.after(100, animate, (index + 1) % len(frames))

    animate()  # Start GIF animation
    root.update_idletasks()
    loader_popup.transient(root)

def hide_loader():
    global loader_popup
    if loader_popup:
        loader_popup.destroy()  # Close the popup
        loader_popup = None
    root.update_idletasks()   

def open_payment_popup():
    global Rent_price, SiteId,PaymentIntentId
 #   print("-------------------------Rent_price",Rent_price)
#    print("--------------------------SiteId",SiteId)
    
    url = "https://truckovernight.azurewebsites.net/api/ProducerAPI/InititateTeerminalPayment"
    print("----------",url)
    payload = {
                   "Amount":Rent_price,
                   "SelfStoreId":SiteId
              }
    show_loader()
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Response:", response.json())
        if not (f"{response.json()}") == "0":
             data = response.json()               
             PaymentIntentId = data.get('PaymentIntentId')
             Check_payment_Status()
        else:
           print(f"Request failed with status code: {response.status_code}")
           print("Response content:", response.text)


def Check_payment_Status():
    global PaymentIntentId
    id = PaymentIntentId
    url = f"https://truckovernight.azurewebsites.net/api/ProducerAPI/ChecKStatusOfPaymentIntent?id={id}"
    response = requests.get(url)
    if response.status_code == 200:
             print("Response:", response.json())
             if not (f"{response.json()}") == "0":
                 data = response.json()
                 status = data['Status']
                 print("------------ data : ",status)
                 if status.lower() == "succeeded":  # Case insensitive check
                                         
                     Payment_Success_msg(status)
                     hide_loader()
                         
             else:
               print(f"Request failed with status code: {response.status_code}")
               print("Response content:", response.text)
               
               
    hide_loader()           
               

def Payment_Success_msg(status):
     hide_loader()
     popup = tk.Toplevel(root)
     popup.title("Payment Success")
     popup.geometry("300x150")
     popup.configure(bg="white")
     Status = status
        
     # Add a welcome label
     welcome_label = tk.Label(
        popup,
        text=f"Payment {Status}",
        font=("Arial", 16),
        bg="white",
        fg="Green"
     )
     welcome_label.pack(pady=40)
     popup.transient(root)
     
payment_button = tk.Button(
    root,
    text="Pay Now",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="#0078D7",  # Modern blue color
    activebackground="#004c8c",
    activeforeground="white",
    relief="raised",
    bd=3,
    padx=5,
    pady=5,
    cursor="hand2",
    command=open_payment_popup
)
payment_button.place_forget()

def Storechamber():
    global l, storechamberId
    #url = store_url()
    url =  f"https://truckovernight.azurewebsites.net/api/ProducerAPI/GetStorechamberIdByName?StoreName={l}"
    #print(".......................",url)
    response = requests.get(url)
    if response.status_code == 200:
        # print("Response:", response.json())
         if not (f"{response.json()}") == "0":
             data = response.json()
             storechamberId = data
             print("----------------------storechamberId response is : ", storechamberId)                           
    else:
       print(f"Request failed with status code: {response.status_code}")
       print("Response content:", response.text)

def payment_Construct_url():
    global l,g, storechamberId
    Dimension = g
    StoreName = l
    print("---------------------------- StoreName",StoreName)
    print("---------------------------- Dimension",Dimension)
    
    payment_templet_url = "https://truckovernight.azurewebsites.net/api/ProducerAPI/StorechamberUnitDetails?StorechamberId={}&Dimension={}&StoreName={}"
    return payment_templet_url.format(storechamberId,Dimension,StoreName)
       
def Construct_url():
    templet_url = "https://truckovernight.azurewebsites.net/api/slotsapi/GetSelfStoreApi"
    return templet_url
 
def get_and_parse_json(url):
    try:
       # print(url)
        response = requests.get(url)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            #print(data)

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
            #print("---------------------------- Extracted data:",extracted_data)
            for item in extracted_data:     
                Update_Unit_Image(item['StoreChamberName'],item['Status'])
                storechamberId = item['StoreChamberId']
                 

def FP_Construct_url():  
    tp_templet_url = "https://truckovernight.azurewebsites.net/api/ProducerAPI/GetFingerprintByUserId?id={}"
    auth_token = "LPvJs79vG3XQL-dSRKIPIXRRk7zJNWMLDbpsGuc1Hdx-Y9XwjvzsIw=="
    headers = {
                'Token': auth_token,
                'Content-Type': 'application/json'
              }
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

    if total is not None and Fp_extracted_data is not None:
            print("Total:", total)
            print("Extracted data:",Fp_extracted_data)
            for item in Fp_extracted_data:
                FpId = item['fingerprint']
               

def close_app():
    #subprocess.run(["sudo", "reboot"], check=True)
    #subprocess.run(["sudo", "shutdown", "now"])
    root.destroy()

#close_button = tk.Button(bottom_frame, text="Close Application", command=close_app, width=20, height=2, bg="red", fg="white")
#close_button.pack(pady=20)


def on_hover(event):
    close_button.config(bg="#b30000")  # Darker red on hover

def on_leave(event):
    close_button.config(bg="#d32f2f")
close_button = tk.Button(
    bottom_frame,
    text="Close Application",
    command=close_app,
    font=("Arial", 14, "bold"),
    width=15,
    height=2,
    bg="#d32f2f",  # Modern red color
    fg="white",
    activebackground="#b30000",
    activeforeground="white",
    relief="raised",
    bd=4,
    cursor="hand2"
)

close_button.pack(pady=10)
close_button.bind("<Enter>", on_hover)
close_button.bind("<Leave>", on_leave)

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



