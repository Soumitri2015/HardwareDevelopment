from tkinter import *
from tkinter import ttk, messagebox, PhotoImage
import tkinter as tk
import cv2
from pathlib import Path
from PIL import Image, ImageTk
import pyautogui
import subprocess
import requests
import os
import threading
from time import time
import time
from queue import Queue
import pytesseract
from tkinter import StringVar
import re
import requests
import json
from datetime import datetime
from datetime import datetime, timedelta
import sys
import numpy as np
import tkinter.font as tkFont 
import pytz
from escpos.printer import Usb
from dateutil import parser
import configparser


config = configparser.ConfigParser()
config.read('/home/steve/config.ini')

siteid = config['settings']['SiteId']


ExitCode="7210"
TempExitCode=""

RebootCode ="5210"
TempRebootCode =""

CompanyId = 16
SiteId = siteid

# OUTPUT_PATH = Path(__file__).parent
OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"/home/steve/Desktop/mobile_cart/Tkinter-Designer/build/assets/frame0")
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/steve/Downloads/New_assets")
# ASSETS_PATH = OUTPUT_PATH / Path(r"F:\Upwork\test_env\production\new mobile cart\Tkinter-Designer\build\assets\frame0")

window = tk.Tk()

def go_fullscreen():
    window.attributes('-fullscreen', True)
            
window.geometry("1920x1200+0+0")
go_fullscreen()
window.configure(bg = "#2B2264")
warning_box = None

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
    global warning_box  # Access the global warning box reference

    signal_strength = get_network_strength()
    if signal_strength is not None:
        if signal_strength < -60:  # Threshold for poor signal
            if warning_box is None:  # Show warning only if not already displayed
                warning_box = tk.Toplevel(window)
                warning_box.title("Network Alert")
                warning_label = tk.Label(warning_box, text="Your network connection is poor.", fg="red", font=("Arial", 14))
                warning_label.pack(padx=20, pady=20)
                # Add a close button
                close_button = tk.Button(warning_box, text="Close", command=warning_box.destroy)
                close_button.pack(pady=10)
                warning_box.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable manual close
        else:
            # If the network is good, close the warning box if it exists
            if warning_box is not None:
                warning_box.destroy()
                warning_box = None
    else:
        messagebox.showerror("Network Alert", "Please connect to a network.")

    #window.attributes('-fullscreen', True)
    go_fullscreen()
    # Repeat every 5 seconds    
    window.after(5000, update_signal_strength)
    
  

def open_popup():
    global popup
    window.after(5000, go_fullscreen)


# ASSETS_PATH = OUTPUT_PATH / Path(r"/home/pi/Desktop/production/Tkinter-Designer/build/assets/frame0")
my_dict = {    
    '1309':'01',
    '1310':'02',
    '1311':'03',
    '1312':'04',
    '1313':'05',
    '1314':'06',
    '1315':'07',
    '1316':'08',
    '1317':'09',
    '1318':'10',
    '1319':'11',
    '1320':'12',
    '1321':'13',
    '1322':'14',
    '1323':'15',
    '1324':'16',
    '1325':'17',
    '1326':'18',
    '1327':'19',
    '1328':'20',
    '1879':'21',
    '1880':'22',
    '1881':'23'   
}
slotList = [
    {
        "Id": 1,
        "Name": "01",
        "SlotId": 1309,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 2,
        "Name": "02",
        "SlotId": 1310,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 3,
        "Name": "03",
        "SlotId": 1311,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 4,
        "Name": "04",
        "SlotId": 1312,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 5,
        "Name": "05",
        "SlotId": 1313,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 6,
        "Name": "06",
        "SlotId": 1314,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 7,
        "Name": "07",
        "SlotId": 1315,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 8,
        "Name": "08",
        "SlotId": 1316,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 9,
        "Name": "09",
        "SlotId": 1317,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 10,
        "Name": "10",
        "SlotId": 1318,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 11,
        "Name": "11",
        "SlotId": 1319,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 12,
        "Name": "12",
        "SlotId": 1320,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 13,
        "Name": "13",
        "SlotId": 1321,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 14,
        "Name": "14",
        "SlotId": 1322,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 15,
        "Name": "15",
        "SlotId": 1323,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    },
    {
        "Id": 16,
        "Name": "16",
        "SlotId": 1324,
        "Status":0,
        "WarningCount": 0,
        "TruckTag": "",
        "SiteId": "",
        "CompanyId": "",
        "IsWarningToday": 0,
        "Image": "null",
        "ImagePath" : "image_6.png"
    }   
]
  

shared_queue = Queue()
submit_btn_queue=Queue()
shared_queue_for_slot_id = Queue()
wait_to_capture=Queue()
mutex=threading.Lock()

window.after(2000, open_popup)

def license_plate_reader():
    # pass
    while True:
        if not wait_to_capture.empty():
           if wait_to_capture.get()==1:
               print("wait for 5 sec")
               time.sleep(5)
               print("wait relese")
               wait_to_capture.put(0) #resume 
        result = subprocess.run(["alpr", "-c", "us", "-n", "1", "frame1.jpg"], capture_output=True)
        output = result.stdout.decode("utf-8").strip()

        lines = output.split('\n')
        if "No license plates found" not in output:
            plate_info = lines[1].split('\t')
            number_plate = plate_info[0].strip().lstrip('-')
            confidence = float(plate_info[1].split(':')[1].strip())
            number_plate = number_plate.replace(" ", "")
            print("number_plate length", len(number_plate))
            if len(number_plate) >= 2:
                shared_queue.put(number_plate)
                print("-----------SlotId_plate_reader----------shared_queue.put(number_plate)")
                
                
                
            if(len(number_plate)>=6):
                print("---------------------wait_to_capture.put(1)")
                wait_to_capture.put(1) #pause for 5sec after
        else:
            pass
            #print("No license plates found")


def SlotId_plate_reader():
    # pass
    while True:
        detectedSlot = ""
        img = cv2.imread('frame2.jpg', 0)
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            custom_config = r'--oem 3 --psm 6'
            ocr_result = pytesseract.image_to_string(gray, config=custom_config)
            #print('ocr result is ',ocr_result)
            Number = ocr_result.strip()  
            if bool(re.search(r'\d', Number)):
                Number = int(''.join(c for c in str(Number) if c.isdigit()))
                two_digit_number = str(Number)[-2:].zfill(2)
                if two_digit_number:
                    space_id=get_key_from_value(my_dict, two_digit_number)
                    if space_id:
                        detectedSlot = two_digit_number
                        shared_queue_for_slot_id.put(two_digit_number)
                        
#         if detectedSlot == "":
#             result = subprocess.run(["alpr", "-c", "us", "-n", "1", "frame2.jpg"], capture_output=True)
#             output = result.stdout.decode("utf-8").strip()
#             lines = output.split('\n')
#             if "No license plates found" not in output and output not in "":
#                 plate_info = lines[1].split('\t')
#                 Slot_number_plate = plate_info[0].strip().lstrip('-')
#                 confidence = float(plate_info[1].split(':')[1].strip())
#                 Slot_number_plate = Slot_number_plate.replace(" ", "")
#                 print("Slot_number_plate length", len(Slot_number_plate))
#                 if len(Slot_number_plate) >= 2:
#                      Slot_number_plate = int(''.join(filter(str.isdigit, Slot_number_plate)))
#                      print("Slot id", Slot_number_plate)
#                      Slot_number_plate = str(Slot_number_plate)[-2:].zfill(2)
#                      shared_queue_for_slot_id.put(Slot_number_plate)
#                      print("Slot Text", Slot_number_plate)
#             else:
#                 pass
                #print("No license plates found")
                                

# def slot_ID_reader():

        
#     while True:
#         try:
#             image = cv2.imread('frame2.jpg', 0)
#             thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#             thresh = cv2.GaussianBlur(thresh, (3,3), 0)
#             data = pytesseract.image_to_string(thresh, lang='eng',config='--psm 6')
#             print(data)
#             numbers = re.findall(r'\d+', data)
#             result = ''.join(numbers)
# 
#             if(len(result)<=1):
#                 try:
#                     q=int(result)
#                     # print("result=====",q)
#                     shared_queue_for_slot_id.put(int(result))
#                 except:
#                     pass
# 
#         except:
#             pass

def get_key_from_value(dictionary, search_value):
    for key, value in dictionary.items():
        if value == search_value:
            return key
    return None

def get_value_from_key(dictionary, search_value):
    for key, value in dictionary.items():
        if key == search_value:
            return value
    return None

def combobox_callback(choice):
    print(prkng_slt_cmbx.get())
    choice=prkng_slt_cmbx.get()
    space_id=get_key_from_value(my_dict, choice)
    post_list[1]=space_id
    submit_btn_queue.put(0)

    # Print the result
    try:
        plate_value = json_data['results'][0]['plate']
        print("Plate value:", plate_value)
        post_list[0]=plate_value
        no_plate.set(plate_value)
        post_list[3]="wait"
        wait_to_capture.put(1) # for pausing capturing for 5sec
    except:
        print("Plate Not Recongnise")
        no_plate.set("Recapture")

def button_function():
    print("button pressed")
  
    
  # Print the result
    try:
        plate_value = json_data['results'][0]['plate']
        print("Plate value:", plate_value)
        post_list[0]=plate_value
        prkng_slt_cmbx.set(plate_value)
        post_list[3]="wait"
        wait_to_capture.put(1) # for pausing capturing for 5sec
    except:
        print("Slot Not Recongnise")
        #no_plate.set("Recapture")
        prkng_slt_cmbx.set("Recapture")


def close_window(vid, window):
    if vid.isOpened():
        vid.release()
    window.destroy()
    
def submit_btn():
    submit_btn_queue.put(1)
    
    choice = StringVar()
    choice=prkng_slt_cmbx.get()
  #  print("No parking slot number is : ",choice)
    choice=get_key_from_value(my_dict, choice)
    post_list[1]=choice
    
    truck_tag_input = no_plate.get()
    slot_input =  post_list[1]
    
    url = construct_url()
    clear_tag_number_text()

    total, extracted_data = get_and_parse_json(url) 
    print("Extracted data:",extracted_data)
    match_found = False
    
    if total is not None and extracted_data is not None:
        for item in extracted_data:
            if item['TruckTag'] == truck_tag_input and str(item['SlotId'] == slot_input.strip()) and item['Status'] == 3:
                
                match_found = True
                break
    
    if match_found:
        url = Warning_url()
        clear_tag_number_text()
        truck_tag = no_plate.get()

        total, extracted_data = get_and_parse_warning_json(url)
        #print("CheatparkData ====================================",extracted_data)
        if total is not None and extracted_data is not None:
            truck_tag_count = 0
            for item in extracted_data:
                if item['Tag'].strip() == truck_tag:
                     truck_tag_count += 1     
           # truck_tag_count = sum(1 for item in extracted_data if item['TruckTag'] == truck_tag)
            
            # Display warnings based on the count of TruckTag matches
            if truck_tag_count == 0:
                print("First Warning", "No truck tag found.")           
                First_Warning_msg() 
                 
            elif truck_tag_count == 1:
                print("Second Warning", "One truck tag found.")
                Second_Warning_msg() 
                
            elif truck_tag_count >= 2:
                print("Last Warning", f"{truck_tag_count} truck tags found.")
                Last_Warning_msg()                             
        else:
            First_Warning_msg()            
            
    else:
        if post_list[0] != "0" and post_list[1] != "0":
            new_image_path = relative_to_assets("button_1_2.png") 

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            button_1.config(image=new_image)
            button_1.image = new_image
            #time.sleep(2)
            
            Parking_Slot = StringVar()
            Parking_Slot = prkng_slt_cmbx.get()
            #print("inside submit function ------------------------------", Parking_Slot)
            
            no_plate.set("")
            prkng_slt_cmbx.set("")
            if(Parking_Slot != "No Parking Area"):           
                url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateTruckLotBookingByHardWares"
                # Define the JSON payload
                payload = {
                    "CompanyId": 16,
                    "SiteId": SiteId,
                    "Status": 1,
                    "SlotId": post_list[1],
                    "TruckTag": post_list[0]
                }
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    # print("Response:", response.json())
                    if not (f"{response.json()}") == "0":
                        print(f"Slot status updated! Booking ID: {response.json()}")
                        
                else:
                    print(f"Request failed with status code: {response.status_code}")
                    print("Response content:", response.text)
                
            else:
                new_image_path = relative_to_assets("button_1_2.png") 

                # Load the new image
                new_image = PhotoImage(file=new_image_path)

                # Update the canvas create_image method with the new image
                button_1.config(image=new_image)
                button_1.image = new_image
                no_plate.set("")
                prkng_slt_cmbx.set("")
                
                #print("inside submit function ------------------------------", choice)
                url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateParkingViolators"
                #print(url)
                # Define the JSON payload
                payload = {
                    "Tag":post_list[0],   
                    "Image":"",
                    "SiteId": SiteId,
                    "Status": 1,
                    "SlotId": Parking_Slot
                }
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    print("Cheatpark Response:", response.json())
                    if not (f"{response.json()}") == "0":
                        print(f"Slot status updated! Booking ID: {response.json()}")
                        
                else:
                    print(f"Request failed with status code: {response.status_code}")
                    print("Response content:", response.text)


#keyboard
x_axis = 58
y_axis = 740
button_width = 7
button_height = 3  # Adjust height if necessary
x_spacing = 20  # Adjust horizontal spacing between buttons
y_spacing = 15  # Adjust vertical spacing between buttons
space_btn_in_x=500
new_line_x_axis=58
zero_btn_in_x = 1630


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def select(value):
    global TempExitCode
    global TempRebootCode
    global ExitCode
    
    if(str(value)=="Z0"):
        value = '0'
        
    if(str(value)=="<--"):
        value ='backspace'
    
    TempRebootCode=TempRebootCode+str(value)
    TempExitCode=TempExitCode+str(value)
    print("==================================================================",TempExitCode)              
    
    if(str(TempExitCode)==ExitCode):
        print("exit")
        sys.exit()
    if(str(value)=="7"):
        TempExitCode="7"
    if(str(value)=="5"):
        TempRebootCode="5"
    if value == 'Space':
        print("space")

    elif value == 'Shift':
        for button in leftShiftButtons:
            command = lambda x=button: select(x)
            if button != 'Space' and button != "new_line":
                Button(window, text=button, command=command, width=button_width).place(x=x_axis, y=y_axis)

            if button == 'Space':
                Button(window, text=button, command=command, width=50).place(x=space_btn_in_x, y=(y_axis+10))

            x_axis += button_width * 10 + x_spacing  # Add spacing between buttons
            if button == "new_line":
                x_axis = new_line_x_axis
                y_axis += button_height * 10 + y_spacing  # Add spacing between rows

    elif value == 'Caps':
        print("Caps Lock")

        for button in capsButtons:
            command = lambda x=button: select(x)
            if button != 'Space' and button != "new_line":
                Button(window, text=button, command=command, width=button_width).place(x=x_axis, y=y_axis)

            if button == 'Space':
                Button(window, text=button, command=command, width=50).place(x=space_btn_in_x, y=(y_axis+10))

            x_axis += button_width * 10 + x_spacing  # Add spacing between buttons
            if button == "new_line":
                x_axis = new_line_x_axis
                y_axis += button_height * 10 + y_spacing  # Add spacing between rows

    elif value == 'Shift':
        print("Shift")

        for button in buttons:
            command = lambda x=button: select(x)
            if button != 'Space' and button != "new_line":
                Button(window, text=button, command=command, width=button_width).place(x=x_axis, y=y_axis)

            if button == 'Space':
                Button(window, text=button, command=command, width=50).place(x=space_btn_in_x, y=(y_axis+10))

            x_axis += button_width * 10 + x_spacing  # Add spacing between buttons
            if button == "new_line":
                x_axis = new_line_x_axis
                y_axis += button_height * 10 + y_spacing  # Add spacing between rows

    elif value == 'new_line':
        # Handle new line key press
        print("New Line")
    elif value == 'CAPS':
        # Handle caps lock key press
        print("Caps Lock")
        for button in buttons:
            command = lambda x=button: select(x)
            if button != 'Space' and button != "new_line":
                Button(window, text=button, command=command, width=button_width).place(x=x_axis, y=y_axis)

            if button == 'Space':
                Button(window, text=button, command=command, width=50).place(x=space_btn_in_x, y=(y_axis+10))

            x_axis += button_width * 10 + x_spacing  # Add spacing between buttons
            if button == "new_line":
                x_axis = new_line_x_axis
                y_axis += button_height * 10 + y_spacing  # Add spacing between rows

    else:
        try:
            pyautogui.press(value)
        except:
            print("errr in keyboard",value)

# Initialize the video sources
post_list = ["0", "0"]
video_source1 = 0
#video_source2 = 2
cam_width, cam_height = 640, 480

vid1 = cv2.VideoCapture(video_source1,cv2.CAP_V4L)
vid1.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
vid1.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

canvas = Canvas(
    window,
    bg = "#2B2264",
    height = 580,
    width = 1920,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)
    

def update_video1():
    try:
        post_list[0]=no_plate.get()
    except:
        print("error in update function to update post_list")
    ret, frame1 = vid1.read()
    if ret:
        usa_timezone = pytz.timezone('US/Eastern')
        date_text = datetime.now(usa_timezone).strftime("%Y-%m-%d %H:%M:%S")
        
        # Add the date text to the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        font_color = (255, 255, 255)  # White color
        thickness = 2
        position = (10, 470)  # Position where the date will be placed
        (text_width, text_height), baseline = cv2.getTextSize(date_text, font, font_scale, thickness)
       
        
        background_color = (0, 0, 0)  # Black background
        rectangle_position = (position[0] - 5, position[1] - text_height - 5)
        rectangle_end = (position[0] + text_width + 5, position[1] + 5)
        cv2.rectangle(frame1, rectangle_position, rectangle_end, background_color, cv2.FILLED)
        
        cv2.putText(frame1, date_text, position, font, font_scale, font_color, thickness,cv2.LINE_AA)
        
        cv2.imwrite("frame1.jpg", cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        frame1 = Image.fromarray(frame1)
        frame1 = ImageTk.PhotoImage(image=frame1)
        canvas.itemconfig(image_1, image=frame1)
        canvas.image_1 = frame1
        window.after(50, update_video1)
          

def update_truck_image(slot_id, status):
    global icon_images_ref
    global image
    global imageref

    index_position = None

    for index, slot in enumerate(slotList):
        if slot["SlotId"] == slot_id:
            index_position = index
            break

    if index_position is None:
        return 

    # Status-based image selection
    status_images = {
        0: "image_6.png",
        1: "image_5.png",
        2: "image_4.png",
        3: "image_3.png"
    }       
    new_image_path = relative_to_assets(status_images.get(status, "image_6.png"))
    new_image = PhotoImage(file=new_image_path)

    # Update image references correctly
    image[index_position] = new_image  
    canvas.itemconfig(imageref[index_position], image=new_image)
        
    slot_name = next((s["Name"] for s in slotList if s["SlotId"] == slot_id), None)
    if status == 0 and slot_name in tag_number_texts:
        canvas.itemconfig(tag_number_texts[slot_name], text="")

    # Cleanup old icons if necessary
    if f"{slot_id}_img" in icon_images_ref:
        canvas.delete(icon_images_ref[f"{slot_id}_img"])
        canvas.delete(icon_images_ref[f"{slot_id}_text"])
        del icon_images_ref[f"{slot_id}_img"]
        del icon_images_ref[f"{slot_id}_text"]


canvas = Canvas(
    window,
    bg = "#2B2264",
    height = 1080,
    width = 1920,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    380.0,
    290.0,
    image=image_image_1
)

canvas.create_text(
    250.0,
    11.0,
    anchor="nw",
    text="License Plate",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 36 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    270.0,
    583.5,
    image=entry_image_1
)
no_plate = StringVar()
#no_plate.set("Click Capture button")
no_plate.set("")
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    textvariable=no_plate  
    ,font=("Arial Bold", 20)
)

entry_1.place(
    x=120.0,
    y=551.0,
    width=300.0,
    height=63.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    595.0,
    583.5,
    image=entry_image_2
)
 

prkng_slt_cmbx = StringVar()
#prkng_slt_cmbx.set("Enter Slot")
prkng_slt_cmbx.set("")
#prkng_slt_cmbx.trace("w", on_entry_change)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    textvariable=prkng_slt_cmbx, # Assign StringVar to textvariable
    font=("Arial Bold", 20)
)

entry_2.place(
    x=515.0,
    y=551.0,
    width=160.0,
    height=63.0
)


button_image_1 = PhotoImage(
    file=relative_to_assets("button_1_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=submit_btn,
    relief="flat"
)
button_1.place(
    x=55.0,
    y=641.0,
    width=640.0,
    height=73.0
)

canvas.create_rectangle(
    752.0,
    0.0,
    1920.0,
    730.0,
    #fill="#FFF9F9",
    fill="white",
    outline="")

fullscreen_image = PhotoImage(
    file=relative_to_assets("Fullscreen.png"))
FS_image = canvas.create_image(
    1890.0,
    22.0,
    image=fullscreen_image
)
canvas.tag_bind(FS_image, "<Button-1>", lambda event: go_fullscreen())

Warning_image = PhotoImage(
    file=relative_to_assets("printer-icon.png"))
W_image = canvas.create_image(
    1890.0,
    75.0,
    image=Warning_image
)
canvas.tag_bind(W_image, "<Button-1>", lambda event: open_warning_popup())

def Click_Cart_Truck(spaceNo):
    prkng_slt_cmbx.set(spaceNo)
    slot = next((s for s in slotList if s["Name"] == spaceNo), None)    
    if slot is not None:
        no_plate.set(slot["TruckTag"])  

start_y = 698.0  
offset_y = 44.0
start_x = 820.0  
global icon_images_ref
icon_images_ref = {}
image = {}
imageref = {}

for index, slot in enumerate(slotList):
    slot_id = slot["SlotId"]
    truck_name = slot["Name"]
    image_path = slot["ImagePath"]

    image[index] = PhotoImage(file=relative_to_assets(image_path))    
    y_position = start_y - (index * offset_y)
    imageref[index] = canvas.create_image(start_x, y_position, image=image[index])    
    icon_images_ref[slot_id] = {"image": imageref[index], "photo": image[index]}
    canvas.tag_bind(imageref[index], "<Button-1>", lambda event, name=truck_name: Click_Cart_Truck(name))


start_y = 680  
step = -44    

for index, slot in enumerate(slotList):
    canvas.create_text(
        878.0,
        start_y + index * step,  
        anchor="nw",
        text=slot["Name"], 
        fill="#000000",
        font=("Inter Medium", 32 * -1)
    )



tag_number_texts = {}
start_y = 685  
step = -44   

# Creating text elements dynamically for each slot
for index, slot in enumerate(slotList):
    slot_name = slot["Name"]

    tag_number_texts[slot_name] = canvas.create_text(
        1015.0,  
        start_y + index * step,  
        anchor="nw",
        text=" ", 
        fill="#000000",
        font=("Inter Medium", -23)  
    )

# Function to update tag number dynamically
def update_tag_number_text(truck_tag, slot_id, status):
    slot_name = next((slot["Name"] for slot in slotList if slot["SlotId"] == slot_id), None)

    if slot_name is None:
        print(f"Slot ID {slot_id} not found!")
        return 

    if slot_name in tag_number_texts:
        canvas.itemconfig(tag_number_texts[slot_name], text=truck_tag)
        

    
def clear_tag_number_text():
    for tag_id in tag_number_texts.values():
        #canvas.itemconfig(tag_id, text="")
        canvas.itemconfig(tag_number_texts[slot_name], text="")
        #print(tag_number_texts[slot_name],"tag_id")
                 

icon_images_ref = {}
click_counts = 0
IsCheckWarning = 0

def CheatPark_Warning_Message(slot_id, status, isWarningToday, warningCount, tTag):
    global icon_images_ref, click_counts, IsCheckWarning

    # Find slot details dynamically
    slot = next((s for s in slotList if s["SlotId"] == slot_id), None)
    
    if not slot:
        print(f"Slot ID {slot_id} not found in slotList!")
        return  

    slot_name = slot["Name"]  
    y_position = 697 - (int(slot_name) - 1) * 44  

    if status == 3 and isWarningToday == "0":
        # Load the image
        icon_image = PhotoImage(file=relative_to_assets("printer-icon.png"))
        icon_images_ref[slot_id] = icon_image  

        # Create icon dynamically
        img = canvas.create_image(950.0, y_position, image=icon_image)
        icon_images_ref[f"{slot_id}_img"] = img  

        # Create text dynamically if not exists
        if f"{slot_id}_text" not in icon_images_ref:
            text_id = canvas.create_text(990.0, y_position, text="", font=("Arial", 14), fill="black")
            icon_images_ref[f"{slot_id}_text"] = text_id  

        # Bind click event
        canvas.tag_bind(img, "<Button-1>", lambda event: Warning_Messages(tTag, slot_name, warningCount))
        canvas.itemconfig(icon_images_ref[f"{slot_id}_text"], text=str(warningCount))

    else:  # If status is not 3 or warning is already issued
        if f"{slot_id}_img" in icon_images_ref:
            canvas.delete(icon_images_ref[f"{slot_id}_img"])
            canvas.delete(icon_images_ref[f"{slot_id}_text"])
            del icon_images_ref[f"{slot_id}_img"]
            del icon_images_ref[f"{slot_id}_text"]
            click_counts = 0

        if slot_id in icon_images_ref:
            del icon_images_ref[slot_id]

canvas.create_text(
    1190.0,
    11.0,
    anchor="nw",
    text="NO PARKING VIOLATORS",
    fill="black",
    font=("Inter ExtraBold", 20 * -1)
)

def clear_notag_number_text():         
    for sid in list(active_slot_ids):
        if sid in truck_tags:           
            canvas.delete(truck_tags[sid])
        if sid in warning_texts:
            canvas.delete(warning_texts[sid])
        if sid in print_icons:
            canvas.delete(print_icons[sid])
        if sid in cross_icons:
            canvas.delete(cross_icons[sid])
    active_slot_ids.clear()
    displayed_tags.clear()


def show_no_parking():
    prkng_slt_cmbx.set("No Parking Area")

camera_img = PhotoImage(file="/home/steve/Downloads/New_assets/camera.png") 
CameraIcon = canvas.create_image(
    1460.0,
    6.0,
    anchor="nw",
    image=camera_img
)
canvas.tag_bind(CameraIcon, "<Button-1>", lambda event: show_no_parking())

def Warning_For_Outside_Park(tag_text,slot_id):
    space_No = 0
    Tag_id=tag_text
    parking_violation_warning_demo(Tag_id,space_No)

    if Tag_id in truck_tags:
        canvas.delete(truck_tags[Tag_id])
        del truck_tags[Tag_id]

    if Tag_id in print_icons:
        canvas.delete(print_icons[Tag_id])
        del print_icons[Tag_id]

    displayed_tags.discard(Tag_id)


def Remover_Trucks_In_ParkingArea(canvas, slot_id, tag_id, tag_text, tag_key):
   # canvas.delete(tag_id)  # Remove the tag text from canvas
   # displayed_tags.discard(tag_key):
   # Trucktag = tag_text
   # print("----------------------------------------------------- Trucktag",Trucktag)
    url = "https://truckovernight.azurewebsites.net/api/bookingapi/UpdateParkingViolators"
    #print(url)
    # Define the JSON payload
    payload = {
        "Tag":tag_text,
        "Image":"",
        "SiteId": SiteId,
        "Status": 2,
        }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Cheatpark Response:", response.json())
        if not (f"{response.json()}") == "0":
            print(f"Slot status updated! Booking ID: {response.json()}")
            
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:", response.text)      
        

truck_tags = {}
x_pos = 32
y_pos_offset = 0
displayed_tags = set()
print_icons = {}
warning_texts = {}
cross_icons = {}
active_slot_ids = []

print_icon_image = tk.PhotoImage(file="/home/steve/Downloads/New_assets/printer-icon.png")
cross_icon_image = tk.PhotoImage(file="/home/steve/Downloads/New_assets/cross-icon.png")


def cheatpark_tag_number_text(slot_id,tag_text,isWarningToday, warningCount):
    global y_pos_offset,active_slot_ids
    tag_key = f"{slot_id}-{tag_text}"
    
#     if tag_key in displayed_tags:
#         return 
         
    y_position = x_pos + 32 + y_pos_offset
    # print("-----------active_slot_ids 1",active_slot_ids)
    if slot_id not in active_slot_ids:        
        active_slot_ids.append(slot_id)
   #  print("-----------active_slot_ids",active_slot_ids)    


#     row_index = len(displayed_tags)
#     y_position = y_base + (row_index * line_spacing)

    # Draw cross icon to the left of tag_text
    cross_icon_id = canvas.create_image(
        1190.0, y_position - 15,  
        image=cross_icon_image,
        anchor="nw"
    )
    cross_icons[slot_id]=cross_icon_id
    canvas.tag_bind(cross_icon_id, "<Button-1>", lambda event: Remover_Trucks_In_ParkingArea(canvas, slot_id, tag_id, tag_text, tag_key))

    # Draw truck tag
    tag_id = canvas.create_text(
        1230.0, y_position,
        text=tag_text,
        font=("Arial", 19),
        fill="black",
        anchor="w",
        tags="truck_tag"
    )
    truck_tags[slot_id] = tag_id

    warning_text_id = None
    if isWarningToday == "0":
    # Draw warning count
        warning_text_id = canvas.create_text(
            1350, y_position,
            text=str(warningCount),
            font=("Arial", 14, "bold"),
            fill="gray",
            anchor="w"
        )
        warning_texts[slot_id] = warning_text_id
        
        icon_id = canvas.create_image(
            1410.0, y_position - 20,
            image=print_icon_image,
            anchor="nw"
        )
        print_icons[slot_id] = icon_id

        # Bind click to delete icon + count
        def on_icon_click(event, sid=slot_id, icon=icon_id, warning=warning_text_id):
            canvas.delete(icon)
            if warning is not None:
                canvas.delete(warning)
            Warning_For_Outside_Park(tag_text, sid)

        canvas.tag_bind(icon_id, "<Button-1>", on_icon_click)
        
    displayed_tags.add(tag_key)
    y_pos_offset += 50


canvas.create_text(
    150.0,
    1015.0,
    anchor="nw",
    text="Contact  Support",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 30 * -1)
)
canvas.create_text(
    165.0,
    1050.0,
    anchor="nw",
    text="(386)266-0925",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 30 * -1)
)
     
        
# Add on-screen keyboard functionality
buttons = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=','<--', 'Del', 'new_line',
           'Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', '7', '8', '9', 'new_line',
           'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', 'Enter', '4', '5', '6', 'new_line',
           'Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift', '1', '2', '3','new_line',
           'Space','Z0']

leftShiftButtons = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '<--', 'Del', 'new_line',
                    'Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', ']', '7', '8', '9', 'new_line',
                    'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', 'Enter', '4', '5', '6', 'new_line',
                    'Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '<', '>', '?', 'Shift', '1', '2', '3', 'new_line',
                    'Space','Z0']

capsButtons = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '<--', 'Del', 'new_line',
               'Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', '7', '8', '9', 'new_line',
               'CAPS', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', 'Enter', '4', '5', '6', 'new_line',
               'Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift', '1', '2', '3', 'new_line',
               'Space','Z0']


for button in buttons:
    command = lambda x=button: select(x)
    if button != 'Space' and button != "new_line" and button != "Z0":
        Button(window, text=button, command=command,height=2, width=button_width,font='sans 18 bold').place(x=x_axis, y=y_axis)

    if button == 'Space':
        Button(window, text=button, command=command,height=2, width=50,font='sans 18 bold').place(x=space_btn_in_x, y=(y_axis+8))
    
    if button == 'Z0':
        Button(window, text='0', command=command,height=2, width=button_width,font='sans 18 bold').place(x=zero_btn_in_x, y=(y_axis+8))
    

    x_axis += button_width * 14.5 + x_spacing  # Add spacing between buttons
    if button == "new_line":
        x_axis = new_line_x_axis
        y_axis += button_height * 17 + y_spacing  # Add spacing between rows


def update_label():
    if not shared_queue.empty():
        number_plate = shared_queue.get()
        
        print("---------------------number_plate = shared_queue.get(soumitri)",number_plate)
        no_plate.set(number_plate)
        post_list[0]=number_plate
        #time.sleep(10)
        submit_btn_queue.put(0)
    if not shared_queue_for_slot_id.empty():
        slot_ID=shared_queue_for_slot_id.get()
        if(str(slot_ID).zfill(2) in my_dict.values()):
            # print("hdexuedudeueduyweewyuewuewyyuweyweiuewewuewiweu")
            prkng_slt_cmbx.set(str(slot_ID))
            space_id=get_key_from_value(my_dict, str(slot_ID).zfill(2))
            post_list[1]=space_id
            submit_btn_queue.put(0)
            
    if not submit_btn_queue.empty():
        btn_state=submit_btn_queue.get()
        print("submit butoon state-----------",btn_state)
        if btn_state ==1:
            # change image of butoon
            new_image_path = relative_to_assets("button_1_2.png")  

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            button_1.config(image=new_image)
            button_1.image = new_image
            submit_btn_queue.put(0)
        else:
            # change image of butoon
            new_image_path = relative_to_assets("button_1_1.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            button_1.config(image=new_image)
            button_1.image = new_image                
            
    window.after(5000, update_label)  # Adjust the interval as needed (here it's 1 second)
        
              
def get_and_parse_json(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            # Extract required key-value pairs
            total = data['total']
            extracted_data = []

            for row in data['rows']:
                extracted_data.append({
                    'SlotId': row['SlotId'],
                    'TruckTag': row['TruckTag'],
                    'Status': row['Status'],
                    'IsWarningToday':row['IsWarningToday'],
                    'WarningCount':row['WarningCount']
                })
            
            return total, extracted_data
        else:
            print("Request failed with status code:", response.status_code)
            return None, None
    except Exception as e:
        print("An error occurred:", e)
        return None, None


def construct_url():
    global CompanyId, SiteId
    current_timestamp = str(int(time.time() * 1000))  # Current timestamp in milliseconds
    
    date_time=datetime.now()
    if date_time.hour < 12:
        date_time=date_time - timedelta(days=1)
        
    date = date_time.strftime("%m/%d/%Y")  # Previous date in MM/DD/YYYY format
    # print(date)
    # URL template
    url_template = "https://truckovernight.azurewebsites.net/api/BookingAPI/GetBookingBydateAndTimeLeaveAndCompanyIdFor3rdPartyApi?date={}&CompanyId={}&SiteId={}&_={}"
    return url_template.format(date,CompanyId,SiteId, current_timestamp)
       

def live_preview():
    pass
    # list_to_check_blnk_prkng_spce=[]
    
    # # Construct URL
    # url = construct_url()

    # # Trigger GET request and parse JSON
    # total, extracted_data = get_and_parse_json(url)

    # # Print results
    # if total is not None and extracted_data is not None:
    #     print("Total:", total)
    #     print("Extracted data:")
    #     for item in extracted_data:
    #         print(type(item),item)
    #         print(type(item['SlotId']))
    #         update_truck_image(item['SlotId'],item['Status'])
    #         list_to_check_blnk_prkng_spce.append(str(item['SlotId']))
            
    #     for slt_id in my_dict:
    #         if slt_id not in list_to_check_blnk_prkng_spce:
    #             # print(slt_id ,"is blank")
    #             update_truck_image(int(slt_id),0)
                
            
    window.after(8000, live_preview)
            


def submit_post_req():
    global IsCheckWarning,y_pos_offset
    i=0
    while(1):
        time.sleep(1)
        
        if(i>=8):
            list_to_check_blnk_prkng_spce=[]
            
            # Construct URL
            url = construct_url()
            clear_tag_number_text()
            total, extracted_data = get_and_parse_json(url)
            clear_notag_number_text()
            if total is not None and extracted_data is not None:
             #   print("Total:", total)
             #   print("Extracted data:",extracted_data)
                y_pos_offset=0
                index = 0
                for item in extracted_data:
                    if(item["SlotId"] == None):
                        index = index + 1
                        truck_tag = item.get("TruckTag", "")
                        IsWarningToday = item.get("IsWarningToday")
                        WarningCount = item.get("WarningCount")
                
                        if truck_tag:  
                            cheatpark_tag_number_text(index, truck_tag,IsWarningToday, WarningCount)
                         
                    slot = next((s for s in slotList if s["SlotId"] == item["SlotId"]), None)
        
                    if slot:
                        # Update slot fields
                        slot["TruckTag"] = item["TruckTag"]
                        slot["Status"] = item["Status"]
                        slot["WarningCount"] = item["WarningCount"]
                        slot["IsWarningToday"] = item["IsWarningToday"]

                        # Update UI Elements
                        update_truck_image(slot["SlotId"], slot["Status"])
                        if slot["TruckTag"] != "":
                            update_tag_number_text(slot["TruckTag"], slot["SlotId"], slot["Status"])
                            

                        # Call Warning Message
                        CheatPark_Warning_Message(
                            slot["SlotId"], slot["Status"], slot["IsWarningToday"], slot["WarningCount"], slot["TruckTag"]
                        )
                        
            
                    
                    
#                     update_truck_image(item['SlotId'],item['Status'])
#                     #slot_id = item['SlotId']  # Define slot_id before using it
#                     #clear_printer_icon(slot_id) 
#                     #Print_Warning_Message(item['SlotId'],item['Status'])
#                     if(item['TruckTag'] != ""):                        
#                         update_tag_number_text(item['TruckTag'],item['SlotId'],item['Status'])  # Update the text widget with TruckTag
#                         CheatPark_Warning_Message(item['SlotId'],item['Status'],item['IsWarningToday'],item['WarningCount'],item['TruckTag'])



                        #clear_tag_number_text(item['TruckTag'],item['SlotId'])
                        #update_tag_number_text.set("")
        
                    #(Tag_1+(item['SlotId'])).Text = item['TruckTag']
                    
                    # print(item['Reboot'])
#                     if(item['Reboot']!= ""):
#                         if(item['Reboot']=='1'):
#                             subprocess.run(["sudo", "reboot"], check=True)

                    
                    list_to_check_blnk_prkng_spce.append(str(item['SlotId']))
      
                    
                for slt_id in my_dict:
                    if slt_id not in list_to_check_blnk_prkng_spce:
                        # print(slt_id ,"is blank")
                        update_truck_image(int(slt_id),0)
                                         

        IsCheckWarning = i
        #print("@@@@@", IsCheckWarning)
        i=i+1

def Warning_url():
    TruckTag = no_plate.get()
    return GetCheatParkTruckTagUrl(TruckTag)

def GetCheatParkTruckTagUrl(Tag_id):
    TruckTag = Tag_id
    url_template = "https://truckovernight.azurewebsites.net/api/BookingAPI/GetCheatParkDataByTruckTag?TruckTag={}"
    return url_template.format(TruckTag)

def get_and_parse_warning_json(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            extracted_data = []

            for row in data:
                extracted_data.append(row)                

            #total = extracted_data.length
            total = len(extracted_data)
            return total, extracted_data
        else:
            print("Request failed with status code:", response.status_code)
            return None, None
    except Exception as e:
        print("An error occurred:", e)
        return None, None

INACTIVITY_THRESHOLD = 90000000  # 1 minutes

# Initialize the activity timer variable
activity_timer = None

def reset_activity_timer():
     global activity_timer
     if activity_timer is not None:
         window.after_cancel(activity_timer)  # Cancel the previous timer
     activity_timer = window.after(INACTIVITY_THRESHOLD, show_popup)  # Set a new timer
  
    
def show_popup():    
    popup = tk.Toplevel()  #Tk()
    popup.title("Authentication")
    popup.geometry("580x480")
    popup.configure(bg = "#2B2264")
    popup.protocol("WM_DELETE_WINDOW", lambda: None)

    style = ttk.Style()
    style.configure("White.TLabel", foreground="white", background="#2B2264")
    label = ttk.Label(popup, text="Enter the Security Code:",font=("Helvetica", 20),style="White.TLabel")
    label.pack(pady=10)

    custom_font = tkFont.Font(family="Helvetica", size=20)
    
    entry = ttk.Entry(popup,font=custom_font)
    entry.pack(pady=5,ipadx=10, ipady=10)
    
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 18, "bold"))

    def check_code():
        if entry.get() == "12345":
            popup.destroy()  # Close the popup if the code is correct
            reset_activity_timer()
        else:
            messagebox.showerror("Error", "Incorrect code. Please try again.")
            
   # button_font = tkFont.Font(family="Helvetica", size=25, weight="bold")
    def delete_last_character():
        current_text = entry.get()
        if current_text:
            entry.delete(len(current_text)-1, tk.END)
       # Create a number pad
    def add_number(number):
        entry.insert(tk.END, str(number))
        
    
    # Create a grid of buttons (0-9)
    number_frame = tk.Frame(popup, bg="#2B2264")
    number_frame.pack()
    
    button_images = {
        "1": ImageTk.PhotoImage(file=relative_to_assets("btn_1.png")),
        "2": ImageTk.PhotoImage(file=relative_to_assets("btn_2.png")),
        "3": ImageTk.PhotoImage(file=relative_to_assets("btn_3.png")),
        "4": ImageTk.PhotoImage(file=relative_to_assets("btn_4.png")),
        "5": ImageTk.PhotoImage(file=relative_to_assets("btn_5.png")),
        "6": ImageTk.PhotoImage(file=relative_to_assets("btn_6.png")),
        "7": ImageTk.PhotoImage(file=relative_to_assets("btn_7.png")),
        "8": ImageTk.PhotoImage(file=relative_to_assets("btn_8.png")),
        "9": ImageTk.PhotoImage(file=relative_to_assets("btn_9.png")),
        "0": ImageTk.PhotoImage(file=relative_to_assets("btn_0.png")),
        "Backspace": ImageTk.PhotoImage(file=relative_to_assets("btn_backspace.png")),
        "$": ImageTk.PhotoImage(file=relative_to_assets("btn_dolar.png")),
        "Submit": ImageTk.PhotoImage(file=relative_to_assets("Submit.png"))
    }

    # Create buttons
    buttons = {}

    for i in range(3):
        for j in range(3):
            number = str(i * 3 + j + 1)
            buttons[number] = tk.Button(
                popup,
                image=button_images[number],
                command=lambda num=number: add_number(num),
                borderwidth=0,
                highlightthickness=0,
                relief="flat"
            )
            buttons[number].image = button_images[number]  # Prevent garbage collection
            buttons[number].place(x=170 + j * 80, y=120 + i * 60, width=70, height=50)

    # Backspace button
    buttons["Backspace"] = tk.Button(
        popup,
        image=button_images["Backspace"],
        command=delete_last_character,
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    buttons["Backspace"].image = button_images["Backspace"]
    buttons["Backspace"].place(x=170, y=300, width=70, height=50)

    # Zero button
    buttons["0"] = tk.Button(
        popup,
        image=button_images["0"],
        command=lambda: add_number(0),
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    buttons["0"].image = button_images["0"]
    buttons["0"].place(x=250, y=300, width=70, height=50)

    # Dollar button
    buttons["$"] = tk.Button(
        popup,
        image=button_images["$"],
        command=lambda: add_number('$'),
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    buttons["$"].image = button_images["$"]
    buttons["$"].place(x=330, y=300, width=70, height=50)

    # Submit button
    buttons["Submit"] = tk.Button(
        popup,
        image=button_images["Submit"],
        command=check_code,
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    buttons["Submit"].image = button_images["Submit"]
    buttons["Submit"].place(x=220, y=370, width=140, height=60)

    
    # Make sure the popup window is modal (i.e., it must be closed before returning to the main window)
    popup.transient(window)
    popup.grab_set()
    window.wait_window(popup)
    #detect_and_recognize_face()
    

#window.after(600000, show_popup)
window.bind("<Motion>", lambda event: reset_activity_timer())
window.bind("<KeyPress>", lambda event: reset_activity_timer())



def First_Warning_msg():
    global textbox
    W_popup = tk.Toplevel()
    W_popup.title("First Warning")
    W_popup.geometry("580x320")
    W_popup.configure(bg="#2B2264")
    W_popup.protocol("WM_DELETE_WINDOW", lambda: None)
    

    truck_tag_input = no_plate.get()
    large_font = tkFont.Font(family="Helvetica", size=30)
   
    # Add a textbox
    textbox = tk.Text(W_popup,height=1, width=20,font=large_font)
    textbox.tag_configure("center", justify='center')
    textbox.insert(tk.END, truck_tag_input)
    textbox.tag_add("center", "1.0", "end")
    textbox.pack(pady=20,ipadx=10, ipady=10)
    
    Close_font = tkFont.Font(family="Helvetica", size=12)
    print_button = tk.Button(W_popup, text="Print Receipt", command=print_first_receipt, font=Close_font)
    print_button.pack(side=tk.LEFT,padx=(150,20),pady=20)

    
    close_button = tk.Button(W_popup, text="Close", command=W_popup.destroy, font=Close_font)
    close_button.pack(side=tk.LEFT,padx=20,pady=20)
    
    W_popup.transient(window)
    
 
def print_first_receipt():
    url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateCheatPark"
    print(url)
    # Define the JSON payload
    payload = {           
              "SiteId": SiteId,
              "Status":1,
              #"Image": image_base64,
              "SlotId": post_list[1],
              "Tag": post_list[0]
             }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
         print("Response:", response.json())
         if not (f"{response.json()}") == "0":
               print(f"Slot status updated! Booking ID: {response.json()}")
                                        
    else:
       print(f"Request failed with status code: {response.status_code}")
       print("Response content:", response.text)
    
    truck_tag_input = no_plate.get()
    p = Usb(0x0fe6, 0x811e) 
    p._raw(b'\x1d\x21\x11')
    p.text("First Warning\n\n\n")
       
    p._raw(b'\x1d\x21\x11')
    p.text("TWO HOURS\n")
    p.text("FREE PARKING VIOLATION\n\n")
    p.text("BY\n\n")

    # Truck Number Section
    p._raw(b'\x1d\x21\x11')
    entered_text = textbox.get("1.0", tk.END).strip()
    truck_tag_input = entered_text 
    p.text(f"{entered_text}\n\n") 

    # Store Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True, width=8)
    p.text("at\n\n")
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=8, height=4)
    p.text("STORE NAME & NUMBER\n")
    p.text("Store Address\n\n")

    # Two Hours Free Parking Section
    #p._raw(b'\x1d\x21\x11')
    #p.set(align='center', bold=True)
    #p.text("Is Honored to Provide\n")
    p.set(align='center', width=8, height=4, bold=True)
    #p._raw(b'\x1d\x21\x11')
    #p.text("TWO HOURS\n")
   # p.text("FREE PARKING\n\n")
    #p.text("OR\n\n")
    
    # Overnight Parking Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True)
    p.text("OVERNIGHT PARKING\n")
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=8, height=4)
    p.text("Is Avaliabe\n\n")
    p.text("$18\n\n")

    # Purchase Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True)
    p.text("And May Be Purchased At\n")
    p.text("Store Fuel Desk\n\n\n")

    p.set(align='center')
    #p.text("PIC\n")
    #p.image("frame1.jpg")
    image_pic = Image.open("frame1.jpg")
    resized_pic = image_pic.resize((250, 250))  # Resize as needed
    p.image(resized_pic)
    #now = datetime.now()
    #current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    #p.set(align='center', bold=True, width=2)
    #p.text(f"{current_time}\n\n")
    
    # Line Spacing for Clean Output
    p.text("\n\n")

    # Cut the receipt
    p.cut()
    p.close()

def Second_Warning_msg():
    global textbox
    W_popup = tk.Toplevel()
    W_popup.title("Second Warning")
    W_popup.geometry("580x320")
    W_popup.configure(bg="#2B2264")
    W_popup.protocol("WM_DELETE_WINDOW", lambda: None)
    
    truck_tag_input = no_plate.get()
    large_font = tkFont.Font(family="Helvetica", size=30)
   
    # Add a textbox
    textbox = tk.Text(W_popup,height=1, width=20,font=large_font)
    textbox.tag_configure("center", justify='center')
    textbox.insert(tk.END, truck_tag_input)
    textbox.tag_add("center", "1.0", "end")
    textbox.pack(pady=10,ipadx=10, ipady=10)
    
    Close_font = tkFont.Font(family="Helvetica", size=12)
    print_button = tk.Button(W_popup, text="Print Receipt", command=print_second_receipt, font=Close_font)
    print_button.pack(side=tk.LEFT,padx=(150,20),pady=50)
    
    close_button = tk.Button(W_popup, text="Close", command=W_popup.destroy, font=Close_font)
    close_button.pack(side=tk.LEFT,padx=20,pady=30)
    
    
    W_popup.transient(window)


def print_second_receipt():
    #image_path = "/home/steve/Downloads/frame1.jpg"
    #with open(image_path, "rb") as image_file:
     #   image_bytes = image_file.read()
      #  image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    choice = StringVar()
    choice=prkng_slt_cmbx.get()
    choice=get_key_from_value(my_dict, choice)
    post_list[1]=choice

    url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateCheatPark"
    print(url)
    # Define the JSON payload
    payload = {           
              "SiteId": SiteId,
              "Status":1,
              #"Image": image_base64,
              "SlotId": post_list[1],
              "Tag": post_list[0]
             }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
         print("Response:", response.json())
         if not (f"{response.json()}") == "0":
               print(f"Slot status updated! Booking ID: {response.json()}")
                                        
    else:
       print(f"Request failed with status code: {response.status_code}")
       print("Response content:", response.text)

    truck_tag_input = no_plate.get()
    p = Usb(0x0fe6, 0x811e)
    
    p._raw(b'\x1d\x21\x11')
    p.text("Second Warning\n\n\n")
    
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=8, height=8, bold=True)
    p.text("FREE PARKING VIOLATION\n")
    p.text("BY\n")

    # Truck Number Section
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4, bold=True)
    #p.text("For\n")
    entered_text = textbox.get("1.0", tk.END).strip()
    truck_tag_input = entered_text
    p.text(f"{entered_text}\n\n")
    #p.text("TRUCK NO\n\n")

    # Store Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True, width=4)
    p.text("at\n\n")
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4)
    p.text("STORE NAME & NUMBER\n")
    p.text("Store Address\n\n")

    # Two Hours Free Parking Section
    #p._raw(b'\x1d\x21\x11')
    #p.set(align='center', bold=True)
    #p.text("Is Honored to Provide\n")
    #p._raw(b'\x1d\x21\x11')
    #p.set(align='center', width=4, height=4, bold=True)
    #p.text("TWO HOURS\n")
    #p.text("FREE PARKING\n\n")
    #p.text("OR\n\n")

    # Overnight Parking Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True)
    p.text("OVERNIGHT PARKING\n")
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4)
    p.text("Is Available\n")
    p.text("$18\n\n")

    # Purchase Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True)
    p.text("And May Be Purchased At\n")
    p.text("Store Fuel Desk\n")
    
    p._raw(b'\x1d\x21\x00')
    p.set(align='center', width=4, height=4, bold=True)
    p.text("Trespassing Violations are\n")
    p.text("Documented by Picture evidence\n")
    p.text("And Date and Time Stamped\n")
    p.text("As evidenced below\n\n\n")
    
    p.set(align='center')
    #p.text("PIC\n")
    #p.image("frame1.jpg")
    
    image_pic = Image.open("frame1.jpg")
    resized_pic = image_pic.resize((250, 250))  # Resize as needed
    p.image(resized_pic)
    
    #now = datetime.now()
    #current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    #p.set(align='center', bold=True, width=4)
    #p.text(f"{current_time}\n\n")
    
    # Line Spacing for Clean Output
    p.text("\n\n")

    # Cut the receipt
    p.cut()
    p.close()

def Last_Warning_msg():
    global textbox
    W_popup = tk.Toplevel()
    W_popup.title("Last Warning")
    W_popup.geometry("580x320")
    W_popup.configure(bg="#2B2264")
    W_popup.protocol("WM_DELETE_WINDOW", lambda: None)
    
    truck_tag_input = no_plate.get()
    large_font = tkFont.Font(family="Helvetica", size=30)
   
    # Add a textbox
    textbox = tk.Text(W_popup,height=1, width=20,font=large_font)
    textbox.tag_configure("center", justify='center')
    textbox.insert(tk.END, truck_tag_input)
    textbox.tag_add("center", "1.0", "end")
    textbox.config(padx=5, pady=10)
    textbox.pack(pady=20,ipadx=10, ipady=10)
    
    Close_font = tkFont.Font(family="Helvetica", size=12)
    print_button = tk.Button(W_popup, text="Print Receipt", command=print_Last_receipt, font=Close_font)
    print_button.pack(side=tk.LEFT,padx=(150,20),pady=50)
    
    
    close_button = tk.Button(W_popup, text="Close", command=W_popup.destroy, font=Close_font)
    close_button.pack(side=tk.LEFT,padx=20,pady=30)
    
    W_popup.transient(window)
       
       
def print_Last_receipt():
    image_path = "/home/steve/Downloads/frame1.jpg"
    #with open(image_path, "rb") as image_file:
     #   image_bytes = image_file.read()
      #  image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    choice = StringVar()
    choice=prkng_slt_cmbx.get()
    choice=get_key_from_value(my_dict, choice)
    post_list[1]=choice

    url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateCheatPark"
    print(url)
    # Define the JSON payload
    payload = {           
              "SiteId": SiteId,
              "Status":1,
              #"Image": image_base64,
              "SlotId": post_list[1],
              "Tag": post_list[0]
             }
    response = requests.post(url, json=payload)
    #print("++++++++++++++++++++++++++++++++++++++++",response)
    if response.status_code == 200:
         print("Response:", response.json())
         if not (f"{response.json()}") == "0":
               print(f"Slot status updated! Booking ID: {response.json()}")
                                        
    else:
       print(f"Request failed with status code: {response.status_code}")
       print("Response content:", response.text)

   
    truck_tag_input = no_plate.get()
    p = Usb(0x0fe6, 0x811e)
    
    p._raw(b'\x1d\x21\x11')
    p.text("Third Warning\n\n\n")
    
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=8, height=8, bold=True)
    p.text("FREE PARKING VIOLATION\n\n")
    p.text("BY\n\n")

    # Truck Number Section
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4)
    entered_text = textbox.get("1.0", tk.END).strip()
    truck_tag_input = entered_text
    p.text(f"{entered_text}\n\n")
    #p.text("TRUCK NO\n\n")

    # Store Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4)
    p.text("at\n\n")
    p.text("STORE NAME & NUMBER\n")
    p.text("Store Address\n\n")

    # Free Parking Information
    #p._raw(b'\x1d\x21\x11')
    #p.set(align='center', bold=True, width=4)
    #p.text("Is Honored to Provide\n")
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4, bold=True)
    #p.text("TWO HOURS\n")
    #p.text("FREE PARKING\n\n")
    #p.text("OR\n\n")

    # Overnight Parking Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4)
    p.text("OVERNIGHT PARKING\n")
    p.text("Is Available\n\n")
    p.text("$18\n\n")

    # Purchase Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True)
    p.text("And May Be Purchased At\n")
    p.text("Store Fuel Desk\n\n")

    # Warning Section
    p._raw(b'\x1d\x21\x00')
    p.set(align='center', width=4, height=4, bold=True)
    p.text("This is the THIRD and FINAL\n")
    p.text("Warning of Trespassing Violation\n")
    p.text("Of the Truck as evidenced below.\n\n")

    # Legal Information
    p._raw(b'\x1d\x21\x00')
    p.set(align='center', width=2, height=4, bold=True)
    p.text("Payment of overnight privileges shall\n")
    p.text("clear this and previous violations.\n")
    p.text("Future Violations of Free Parking\n")
    p.text("Shall result in Legal Enforcement.\n\n\n")

    # Show Picture Section
    p.set(align='center')
    #p.image("frame1.jpg")
    
    image_pic = Image.open("frame1.jpg")
    resized_pic = image_pic.resize((250, 250))  # Resize as needed
    p.image(resized_pic)


    #now = datetime.now()
    #current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    #p.set(align='center', bold=True, width=4)
    #p.text(f"{current_time}\n\n")
    
    #p.text("PIC\n\n")
    # If you have an image to print, include the following line:
    # p.image("path_to_image.jpg")
    
    
    # Line Spacing for Clean Output
    p.text("\n\n")

    # Cut the receipt
    p.cut()
    p.close()

def Warning_Messages(Tag_id,space_No,warningCount):
    print("------Tag_id",Tag_id)
    print("------space_No",space_No)
    print("------------------warningCount",warningCount)
    
    if(warningCount == 0):
        print("First Warning", "No truck tag found.")           
        first_warning_demo(Tag_id,space_No) 
    if(warningCount == 1):
        second_warning_demo(Tag_id,space_No)
    if(warningCount >= 2):
        last_warning_demo(Tag_id,space_No)
    
def first_warning_demo(Tag_id,space_No):   
    choice = space_No
    choice=get_key_from_value(my_dict, choice)
    post_list[1]=choice

    truck_tag_input = Tag_id
    url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateCheatPark"
    # Define the JSON payload
    payload = { 
              "Status":1,
              "SlotId": post_list[1],
              "SiteId": SiteId,
              "Tag": truck_tag_input  #post_list[0]
             }
    print(payload)
    response = requests.post(url, json=payload)
    if response.status_code == 200:
         print("Response:", response.json())
         if not (f"{response.json()}") == "0":
               print(f"Slot status updated! Booking ID: {response.json()}")
                                        
    else:
       print(f"Request failed with status code: {response.status_code}")
       print("Response content:", response.text)
    
    p = Usb(0x0fe6, 0x811e)
    
    p.set(align='center', width=8, height=4)
    p._raw(b'\x1d\x21\x11')
    p.text("First Warning\n\n\n")
    
    p.set(align='center', width=8, height=4)   
    p._raw(b'\x1d\x21\x11')
    p.text("TWO HOURS\n")
    p.text("FREE PARKING VIOLATION\n\n")
    p.text("BY\n\n")

    # Truck Number Section
    p.set(align='center', width=8, height=4)
    p._raw(b'\x1d\x21\x11')
    #entered_text = textbox.get("1.0", tk.END).strip()
    #truck_tag_input = entered_text 
    p.text(f"{truck_tag_input}\n\n") 

    # Store Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True, width=8)
    p.text("at\n\n")
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=8, height=4)
    p.text("STORE NAME & NUMBER\n")
    p.text("Store Address\n\n")

    # Two Hours Free Parking Section
    #p._raw(b'\x1d\x21\x11')
    #p.set(align='center', bold=True)
    #p.text("Is Honored to Provide\n")
    p.set(align='center', width=8, height=4, bold=True)
    #p._raw(b'\x1d\x21\x11')
    #p.text("TWO HOURS\n")
   # p.text("FREE PARKING\n\n")
    #p.text("OR\n\n")
    
    # Overnight Parking Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True)
    p.text("OVERNIGHT PARKING\n")
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=8, height=4)
    p.text("Is Avaliabe\n\n")
    p.text("$18\n\n")

    # Purchase Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True)
    p.text("And May Be Purchased At\n")
    p.text("Store Fuel Desk\n\n\n")

    p.set(align='center')
    #p.text("PIC\n")
    #p.image("frame1.jpg")
    image_pic = Image.open("frame1.jpg")
    resized_pic = image_pic.resize((250, 250))  # Resize as needed
    p.image(resized_pic)
    #now = datetime.now()
    #current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    #p.set(align='center', bold=True, width=2)
    #p.text(f"{current_time}\n\n")
    
    # Line Spacing for Clean Output
    p.text("\n\n")

    # Cut the receipt
    p.cut()
    p.close()

def second_warning_demo(Tag_Id,space_No):
    choice = space_No
    choice=get_key_from_value(my_dict, choice)
    post_list[1]=choice
    
    truck_tag_input = Tag_Id
    url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateCheatPark"
    
    # Define the JSON payload
    payload = {
              "SiteId": SiteId,
              "Status":1,
              "SlotId": post_list[1],
              "Tag": truck_tag_input
             }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
         print("Response:", response.json())
         if not (f"{response.json()}") == "0":
               print(f"Slot status updated! Booking ID: {response.json()}")
                                        
    else:
       print(f"Request failed with status code: {response.status_code}")
       print("Response content:", response.text)
    
    
    p = Usb(0x0fe6, 0x811e)
    
    p._raw(b'\x1d\x21\x11')
    p.text("Second Warning\n\n\n")
    
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=8, height=8, bold=True)
    p.text("FREE PARKING VIOLATION\n")
    p.text("BY\n")

    # Truck Number Section
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4, bold=True)
    #p.text("For\n")
    p.text(f"{truck_tag_input}\n\n")
    #p.text("TRUCK NO\n\n")

    # Store Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True, width=4)
    p.text("at\n\n")
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4)
    p.text("STORE NAME & NUMBER\n")
    p.text("Store Address\n\n")

    # Two Hours Free Parking Section
    #p._raw(b'\x1d\x21\x11')
    #p.set(align='center', bold=True)
    #p.text("Is Honored to Provide\n")
    #p._raw(b'\x1d\x21\x11')
    #p.set(align='center', width=4, height=4, bold=True)
    #p.text("TWO HOURS\n")
    #p.text("FREE PARKING\n\n")
    #p.text("OR\n\n")

    # Overnight Parking Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True)
    p.text("OVERNIGHT PARKING\n")
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4)
    p.text("Is Available\n")
    p.text("$18\n\n")

    # Purchase Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True)
    p.text("And May Be Purchased At\n")
    p.text("Store Fuel Desk\n")
    
    p._raw(b'\x1d\x21\x00')
    p.set(align='center', width=4, height=4, bold=True)
    p.text("Trespassing Violations are\n")
    p.text("Documented by Picture evidence\n")
    p.text("And Date and Time Stamped\n")
    p.text("As evidenced below\n\n\n")
    
    p.set(align='center')
    #p.text("PIC\n")
    #p.image("frame1.jpg")
    
    image_pic = Image.open("frame1.jpg")
    resized_pic = image_pic.resize((250, 250))  # Resize as needed
    p.image(resized_pic)
    
    #now = datetime.now()
    #current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    #p.set(align='center', bold=True, width=4)
    #p.text(f"{current_time}\n\n")
    
    # Line Spacing for Clean Output
    p.text("\n\n")

    # Cut the receipt
    p.cut()
    p.close()
    

def last_warning_demo(Tag_id,space_No):
    
    choice = space_No
    choice=get_key_from_value(my_dict, choice)
    post_list[1]=choice
    
    truck_tag_input = Tag_id
    url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateCheatPark"
    # Define the JSON payload
    payload = {
              "SiteId": SiteId,
              "Status":1,
              "SlotId": post_list[1],
              "Tag": truck_tag_input
             }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
         print("Response:", response.json())
         if not (f"{response.json()}") == "0":
               print(f"Slot status updated! Booking ID: {response.json()}")
                                        
    else:
       print(f"Request failed with status code: {response.status_code}")
       print("Response content:", response.text)
    
    p = Usb(0x0fe6, 0x811e)
    
    p._raw(b'\x1d\x21\x11')
    p.text("Third Warning\n\n\n")
    
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=8, height=8, bold=True)
    p.text("FREE PARKING VIOLATION\n\n")
    p.text("BY\n\n")

    # Truck Number Section
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4)
    p.text(f"{truck_tag_input}\n\n")
    #p.text("TRUCK NO\n\n")

    # Store Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4)
    p.text("at\n\n")
    p.text("STORE NAME & NUMBER\n")
    p.text("Store Address\n\n")

    # Free Parking Information
    #p._raw(b'\x1d\x21\x11')
    #p.set(align='center', bold=True, width=4)
    #p.text("Is Honored to Provide\n")
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4, bold=True)
    #p.text("TWO HOURS\n")
    #p.text("FREE PARKING\n\n")
    #p.text("OR\n\n")

    # Overnight Parking Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=4, height=4)
    p.text("OVERNIGHT PARKING\n")
    p.text("Is Available\n\n")
    p.text("$18\n\n")

    # Purchase Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True)
    p.text("And May Be Purchased At\n")
    p.text("Store Fuel Desk\n\n")

    # Warning Section
    p._raw(b'\x1d\x21\x00')
    p.set(align='center', width=4, height=4, bold=True)
    p.text("This is the THIRD and FINAL\n")
    p.text("Warning of Trespassing Violation\n")
    p.text("Of the Truck as evidenced below.\n\n")

    # Legal Information
    p._raw(b'\x1d\x21\x00')
    p.set(align='center', width=2, height=4, bold=True)
    p.text("Payment of overnight privileges shall\n")
    p.text("clear this and previous violations.\n")
    p.text("Future Violations of Free Parking\n")
    p.text("Shall result in Legal Enforcement.\n\n\n")

    # Show Picture Section
    p.set(align='center')
    #p.image("frame1.jpg")
    
    image_pic = Image.open("frame1.jpg")
    resized_pic = image_pic.resize((250, 250))  # Resize as needed
    p.image(resized_pic)


    #now = datetime.now()
    #current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    #p.set(align='center', bold=True, width=4)
    #p.text(f"{current_time}\n\n")
    
    #p.text("PIC\n\n")
    # If you have an image to print, include the following line:
    # p.image("path_to_image.jpg")
    
    
    # Line Spacing for Clean Output
    p.text("\n\n")

    # Cut the receipt
    p.cut()
    p.close()

def parking_violation_warning_demo(Tag_id,space_No):
    post_list[1]=space_No
    truck_tag_input = Tag_id
    url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateCheatPark"
    # Define the JSON payload
    payload = { 
              "Status":2,
              "SlotId": post_list[1],
              "SiteId": SiteId,
              "Tag": truck_tag_input 
             }
    print(payload)
    response = requests.post(url, json=payload)
    if response.status_code == 200:
         print("Response:", response.json())
         if not (f"{response.json()}") == "0":
               print(f"Slot status updated! Booking ID: {response.json()}")
                
    else:
       print(f"Request failed with status code: {response.status_code}")
       print("Response content:", response.text)
    
    p = Usb(0x0fe6, 0x811e)
    
    p.set(align='center', width=8, height=4)
    p._raw(b'\x1d\x21\x11')
    p.text("parking_violation_warning_demo\n\n\n")
    
    p.set(align='center', width=8, height=4)   
    p._raw(b'\x1d\x21\x11')
    p.text("NO PARKING VIOLATION\n\n")
    p.text("BY\n\n")

    # Truck Number Section
    p.set(align='center', width=8, height=4)
    p._raw(b'\x1d\x21\x11')
    p.text(f"{truck_tag_input}\n\n") 

    # Store Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True, width=8)
    p.text("At\n\n")

    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=8, height=4)
    p.text("STORE NAME & NUMBER\n")
    p.text("Store Address\n\n")
    p.set(align='center', width=8, height=4, bold=True)


    # Overnight Parking Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True)
    p.text("OVERNIGHT PARKING\n")
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', width=8, height=4)
    p.text("$18\n\n")

    # Purchase Information
    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True)
    p.text("In designated spaces\n")
    p.text("May be available\n")
    p.text("Check with Fuel Desk\n\n\n")

    p._raw(b'\x1d\x21\x11')
    p.set(align='center', bold=True)
    p.text("No parking violation is a\n")
    p.text("TRESPASSING OFFENSE\n")
    p.text("Punishable by\n\n\n")
    #p.text()

    p.set(align='center')
    image_pic = Image.open("frame1.jpg")
    resized_pic = image_pic.resize((250, 250))  # Resize as needed
    p.image(resized_pic)
    
    # Line Spacing for Clean Output
    p.text("\n\n")

    # Cut the receipt
    p.cut()
    p.close()



# Initialize the activity timer
reset_activity_timer()
license_plate_thread = threading.Thread(target=license_plate_reader, daemon=True)
license_plate_thread.start()
SlotId_plate_thread = threading.Thread(target=SlotId_plate_reader, daemon=True)
SlotId_plate_thread.start()
submit_post_req_thread = threading.Thread(target=submit_post_req, daemon=True)
submit_post_req_thread.start()


cv2.destroyAllWindows()
update_label()
update_video1()
window.resizable(False, False)
window.mainloop()


