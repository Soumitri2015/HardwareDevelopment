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
import time
from datetime import datetime
from datetime import datetime, timedelta
import sys
import numpy as np
import tkinter.font as tkFont
import pytz
#from escpos.printer import Usb
from dateutil import parser



ExitCode="7210"
TempExitCode=""

RebootCode ="5210"
TempRebootCode =""

# OUTPUT_PATH = Path(__file__).parent
OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"/home/steve/Desktop/mobile_cart/Tkinter-Designer/build/assets/frame0")
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/steve/Downloads/New_assets")
# ASSETS_PATH = OUTPUT_PATH / Path(r"F:\Upwork\test_env\production\new mobile cart\Tkinter-Designer\build\assets\frame0")

window = tk.Tk()

def go_fullscreen():
    window.attributes('-fullscreen', False)


window.geometry("1920x1200+0+0")
#window.attributes('-fullscreen', True)
go_fullscreen()
window.configure(bg = "#2B2264")

# Global variable to store reference to the open warning box
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

# def get_network_strength():
#     try:
#         # Run the `iwconfig` command
#         result = subprocess.run(['iwconfig'], capture_output=True, text=True)
#         output = result.stdout
# 
#         # Find signal level
#         for line in output.splitlines():
#             if "Signal level" in line:
#                 # Parse the signal level
#                 signal_strength = int(line.split("Signal level=")[1].split()[0].replace('dBm', ''))
#                 return signal_strength
#         return None  # Signal level not found
#     except Exception as e:
#         return None

# def show_network_alert():
#     # Fetch current network strength
#     signal_strength = get_network_strength()
#     if signal_strength is not None:
#         # Customize thresholds for poor/good connection
#         if signal_strength < -60:  # Example threshold for poor signal
#             messagebox.showwarning("Network Alert", "Your network connection is poor.")
#         #else:
#             #messagebox.showinfo("Network Status", "Your network connection is good.")
#     else:
#         messagebox.showerror("Network Alert", "Please connect to a network.")
#         
#     window.attributes('-fullscreen', True)
#     # Repeat every 5 seconds
#     window.after(5000, show_network_alert)


# ASSETS_PATH = OUTPUT_PATH / Path(r"/home/pi/Desktop/production/Tkinter-Designer/build/assets/frame0")
my_dict = {
    '1020': '01',
    '1019': '02',
    '1018': '03',
    '1017': '04',
    '1016': '05',
    '1013': '06',
    '1012': '07',
    '1011': '08',
    '1010': '09',
    '1009': '10',
    '1007': '11',
    '1005': '12',
    '1006': '13',
    '1308': '14',
    '1307': '15',
    '1306': '16',

}

# my_dict = {
#     '1020': '01',
#     '1019': '02',
#     '1018': '03',
#     '1017': '04',
#     '1016': '05',
#     '1013': '06',
#     '1012': '07',
#     '1011': '08',
#     '1010': '09',
#     '1009': '10',
#     '1007': '11',
#     '1005': '12',
#     '1006': '13',
#     '1308': '14',
#     '1307': '15',
#     '1306': '16',
#     '1305': '17',
#     '1304': '18',
#     '1303': '19',
#     '1302': '20',
#     '1301': '21',
#     '1300': '22',
#     '1298': '23',
#     '1296': '24',
#     '1014': '25',
#     '1021': '26'
# }

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
#         print("license_plate_reader : ",output)
        #print(f"output: {output}")

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
#         if not wait_to_capture.empty():
#            if wait_to_capture.get()==1:
#                print("wait for 5 sec")
#                time.sleep(5)
#                print("wait relese")
#                wait_to_capture.put(0) #resume
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
                        
        if detectedSlot == "":
            result = subprocess.run(["alpr", "-c", "us", "-n", "1", "frame2.jpg"], capture_output=True)
            output = result.stdout.decode("utf-8").strip()
            #print("SlotId_plate_reader : " ,output)
            #print(f"output: {output}")ot status updated! Booking ID
            lines = output.split('\n')
            if "No license plates found" not in output and output not in "":
                plate_info = lines[1].split('\t')
                Slot_number_plate = plate_info[0].strip().lstrip('-')
                confidence = float(plate_info[1].split(':')[1].strip())
                Slot_number_plate = Slot_number_plate.replace(" ", "")
                print("Slot_number_plate length", len(Slot_number_plate))
                if len(Slot_number_plate) >= 2:
                     Slot_number_plate = int(''.join(filter(str.isdigit, Slot_number_plate)))
                     print("Slot id", Slot_number_plate)
                     Slot_number_plate = str(Slot_number_plate)[-2:].zfill(2)
                     shared_queue_for_slot_id.put(Slot_number_plate)
                     print("Slot Text", Slot_number_plate)
            else:
                pass
                #print("No license plates found")
                                

def slot_ID_reader():

        
    while True:
        try:
            image = cv2.imread('frame2.jpg', 0)
            thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            thresh = cv2.GaussianBlur(thresh, (3,3), 0)
            data = pytesseract.image_to_string(thresh, lang='eng',config='--psm 6')
            print(data)
            numbers = re.findall(r'\d+', data)
            result = ''.join(numbers)

            if(len(result)<=1):
                try:
                    q=int(result)
                    # print("result=====",q)
                    shared_queue_for_slot_id.put(int(result))
                except:
                    pass

        except:
            # print("some error occor")
            pass



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
#     print("combobox dropdown clicked:", choice)
#     print("type and value ",type(choice),choice)
    space_id=get_key_from_value(my_dict, choice)
    post_list[1]=space_id
    submit_btn_queue.put(0)
#     print("submit button Queue put---------------------------------------- 0")

    
#     Recent Commeny code
# def trigger_no_plate_recong_api():
#     regions = ["mx", "us-ca","in"] # Change to your country
#     with open(r'captured_image.png', 'rb') as fp:
#         response = requests.post(
#             'https://api.platerecognizer.com/v1/plate-reader/',
#             data=dict(regions=regions),  #Optional
#             files=dict(upload=fp),
#             headers={'Authorization': 'Token 11a9ce11e17b984c3798749866b1e08e50f0fccc'})
#     print(response.json())
#     json_data = response.json()

    # Extract the "plate" value
    

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

# def capture_image():  #Recent comment code
#     
#     no_plate.set(post_list[0])
#     ret, frame = vid1.read()
#     if ret:
#         cv2.imwrite("captured_image.png", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#         print("Image captured successfully!")
#         trigger_no_plate_recong_api()


# def Capture_slot_number_api():
#     regions = ["mx", "us-ca","in"] # Change to your country
#     with open(r'captured_image.png', 'rb') as fp:
#         response = requests.post(
#             'https://app.newfrontiersystems.com/api/BookingAPI/TextDetection',
#             data=dict(regions=regions),  #Optional
#             files=dict(upload=fp),
#             #headers={'Authorization': 'Token 11a9ce11e17b984c3798749866b1e08e50f0fccc'}
#             )
#     # print(response.json())
#     json_data = response.json()
    
    
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

# def Capture_Slot_Number():
#     prkng_slt_cmbx.set(post_list[0])
#     ret, frame = vid2.read()
#     if ret:
#         cv2.imwrite("captured_image.png", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#         print("Image captured successfully!")
#         Capture_slot_number_api()


def close_window(vid, window):
    if vid.isOpened():
        vid.release()
    window.destroy()
    
def submit_btn():
    submit_btn_queue.put(1)
    
    choice = StringVar()
    choice=prkng_slt_cmbx.get()
    choice=get_key_from_value(my_dict, choice)
    post_list[1]=choice
    
    truck_tag_input = no_plate.get()
    slot_input =  post_list[1]
   
    #print("inside submit function ", post_list[1])
    
    url = construct_url()
    clear_tag_number_text()

    total, extracted_data = get_and_parse_json(url)  # Assuming this gets the truck data
    print("Extracted data:",extracted_data)
    match_found = False
    
    if total is not None and extracted_data is not None:
        for item in extracted_data:
            #print("-----------------------------------",item['TruckTag'])
            if item['TruckTag'] == truck_tag_input and str(item['SlotId'] == slot_input.strip()) and item['Status'] == 3:
                
                match_found = True
                break
    
    if match_found:
        url = Warning_url()
        clear_tag_number_text()
        truck_tag = no_plate.get()

       # print("----------------",url)
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
                First_Warning_msg()  # Custom function for the first warning
                 
            elif truck_tag_count == 1:
                print("Second Warning", "One truck tag found.")
                Second_Warning_msg() 
                
            elif truck_tag_count >= 2:
                print("Last Warning", f"{truck_tag_count} truck tags found.")
                Last_Warning_msg()  
                
            
        else:
            First_Warning_msg()
               
                 
    else:    
        if (post_list[0]!="0" and post_list[1]!="0") :        
            new_image_path = relative_to_assets("button_1_2.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            button_1.config(image=new_image)
            button_1.image = new_image
            #time.sleep(2)
            no_plate.set("")
            prkng_slt_cmbx.set("")
            print("inside submit function ", post_list[1])
            url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateTruckLotBookingByHardWares"
            # Define the JSON payload
            payload = {
                "CompanyId": 16,
                "SiteId": 3021,
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
            
        #time.sleep(2)
#         new_image_path = relative_to_assets("button_1_3.png") 
#         new_image = PhotoImage(file=new_image_path)
#         button_1.config(image=new_image)
#         button_1.image = new_image
        
    # submit_btn_button.configure(fg_color="#1F6AA5")

    #submit_btn_queue.put(0)
    #window.after(2000, submit_btn_queue.put(0))



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
        # x_axis = 41
        # y_axis = 800
        # button_width = 10
        # button_height = 3  # Adjust height if necessary
        # x_spacing = 20  # Adjust horizontal spacing between buttons
        #y_spacing = 15  # Adjust vertical spacing between buttons
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
        # Handle caps lock key press
        print("Caps Lock")
        # x_axis = 41
        # y_axis = 800
        # button_width = 10
        # button_height = 3  # Adjust height if necessary
        # x_spacing = 20  # Adjust horizontal spacing between buttons
        # y_spacing = 15  # Adjust vertical spacing between buttons

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
        # Handle shift key press
        print("Shift")
        # x_axis = 41
        # y_axis = 800
        # button_width = 10
        # button_height = 3  # Adjust height if necessary
        # x_spacing = 20  # Adjust horizontal spacing between buttons
        # y_spacing = 15  # Adjust vertical spacing between buttons

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
        # x_axis = 41
        # y_axis = 800
        # button_width = 10
        # button_height = 3  # Adjust height if necessary
        # x_spacing = 20  # Adjust horizontal spacing between buttons
        # y_spacing = 15  # Adjust vertical spacing between buttons

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
        # Handle other key presses
        # print(f"Key pressed: {value}")
        try:
            pyautogui.press(value)
        except:
            print("errr in keyboard",value)


# window = tk.Tk()
# 
# 
# # window.geometry("1920x1200")
# window.geometry("1920x1200+0+0")
# #window.lift()
# # window.overrideredirect(True)
# # window.wm_attributes('-type', 'toolbar')
# window.attributes('-fullscreen', True)
# #width= window.winfo_screenwidth() 
# #height= window.winfo_screenheight()
# #setting tkinter window size
# #window.geometry("%dx%d" % (width, height))
# #window.attributes('-fullscreen', True)
# #window.attributes("-topmost",True)
# window.configure(bg = "#2B2264")


# Initialize the video sources
post_list = ["0", "0"]
video_source1 = 0
#video_source2 = 2
cam_width, cam_height = 640, 480


print("new ...........................")

vid1 = cv2.VideoCapture(video_source1,cv2.CAP_V4L)
vid1.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
vid1.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)
#vid1.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))

# print("new ...........................11")
# vid2 = cv2.VideoCapture(video_source2,cv2.CAP_V4L)
# # vid2.set(cv2.CAP_PROP_FPS, 30.0)
# # vid2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
# # vid2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
# vid2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# vid2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)



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
        

# def update_video2():
#     ret, frame2 = vid2.read()
#     if ret:
#         cv2.imwrite("frame2.jpg", cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))
#         frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
#         frame2 = Image.fromarray(frame2)
#         frame2 = ImageTk.PhotoImage(image=frame2)
#         canvas.itemconfig(image_2, image=frame2)
#         canvas.image_2 = frame2
#         window.after(50, update_video2)



def update_truck_image(slot_id,status):
    global icon_images_ref
    if(slot_id==1020):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file
           
            # Load the new image
            new_image = PhotoImage(file=new_image_path)
            

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_3, image=new_image)
            canvas.image_3 = new_image
            canvas.itemconfig(TagNumber_1020, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_3, image=new_image)
            canvas.image_3 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_3, image=new_image)
            canvas.image_3 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_3, image=new_image)
            canvas.image_3 = new_image
            
        
    if(slot_id==1019):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_4, image=new_image)
            canvas.image_4 = new_image
            canvas.itemconfig(TagNumber_1019, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_4, image=new_image)
            canvas.image_4 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_4, image=new_image)
            canvas.image_4 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_4, image=new_image)
            canvas.image_4 = new_image
            
    if(slot_id==1018):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_5, image=new_image)
            canvas.image_5 = new_image
            canvas.itemconfig(TagNumber_1018, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_5, image=new_image)
            canvas.image_5 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_5, image=new_image)
            canvas.image_5 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_5, image=new_image)
            canvas.image_5 = new_image
            
    if(slot_id==1017):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_18, image=new_image)
            canvas.image_18 = new_image
            canvas.itemconfig(TagNumber_1017, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_18, image=new_image)
            canvas.image_18 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_18, image=new_image)
            canvas.image_18 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_18, image=new_image)
            canvas.image_18 = new_image
            
        
    if(slot_id==1016):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_14, image=new_image)
            canvas.image_14 = new_image
            canvas.itemconfig(TagNumber_1006, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_14, image=new_image)
            canvas.image_14 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_14, image=new_image)
            canvas.image_14 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_14, image=new_image)
            canvas.image_14 = new_image
            
    if(slot_id==1013):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_17, image=new_image)
            canvas.image_17 = new_image
            canvas.itemconfig(TagNumber_1013, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_17, image=new_image)
            canvas.image_17 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_17, image=new_image)
            canvas.image_17 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_17, image=new_image)
            canvas.image_17 = new_image
            
        
    if(slot_id==1012):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_16, image=new_image)
            canvas.image_16 = new_image
            canvas.itemconfig(TagNumber_1012, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_16, image=new_image)
            canvas.image_16 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_16, image=new_image)
            canvas.image_16 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_16, image=new_image)
            canvas.image_16 = new_image
            
        
    if(slot_id==1011):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_15, image=new_image)
            canvas.image_15 = new_image
            canvas.itemconfig(TagNumber_1011, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_15, image=new_image)
            canvas.image_15 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_15, image=new_image)
            canvas.image_15 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_15, image=new_image)
            canvas.image_15 = new_image
            
        
    if(slot_id==1010):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_13, image=new_image)
            canvas.image_13 = new_image
            canvas.itemconfig(TagNumber_1010, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_13, image=new_image)
            canvas.image_13 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_13, image=new_image)
            canvas.image_13 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_13, image=new_image)
            canvas.image_13 = new_image
            
        
    if(slot_id==1009):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_6, image=new_image)
            canvas.image_6 = new_image
            canvas.itemconfig(TagNumber_1009, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_6, image=new_image)
            canvas.image_6 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_6, image=new_image)
            canvas.image_6 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_6, image=new_image)
            canvas.image_6 = new_image
            
        
    if(slot_id==1007):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_12, image=new_image)
            canvas.image_12 = new_image
            canvas.itemconfig(TagNumber_1007, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_12, image=new_image)
            canvas.image_12 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_12, image=new_image)
            canvas.image_12 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_12, image=new_image)
            canvas.image_12 = new_image
            
        
    if(slot_id==1005):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_11, image=new_image)
            canvas.image_11 = new_image
            canvas.itemconfig(TagNumber_1005, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
        
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_11, image=new_image)
            canvas.image_11 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_11, image=new_image)
            canvas.image_11 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_11, image=new_image)
            canvas.image_11 = new_image
            
        
    if(slot_id==1006):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_10, image=new_image)
            canvas.image_10 = new_image
            canvas.itemconfig(TagNumber_1006, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0

        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_10, image=new_image)
            canvas.image_10 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_10, image=new_image)
            canvas.image_10 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_10, image=new_image)
            canvas.image_10 = new_image
            
        
    if(slot_id==1306):        
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_7, image=new_image)
            canvas.image_7 = new_image
            canvas.itemconfig(TagNumber_1306, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_7, image=new_image)
            canvas.image_7 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_7, image=new_image)
            canvas.image_7 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_7, image=new_image)
            canvas.image_7 = new_image
            

    if(slot_id==1308):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_9, image=new_image)
            canvas.image_9 = new_image
            canvas.itemconfig(TagNumber_1308, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_9, image=new_image)
            canvas.image_9 = new_image
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_9, image=new_image)
            canvas.image_9 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_9, image=new_image)
            canvas.image_9 = new_image
            
        
    if(slot_id==1307):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_8, image=new_image)
            canvas.image_8 = new_image
            canvas.itemconfig(TagNumber_1307, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_8, image=new_image)
            canvas.image_8 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_8, image=new_image)
            canvas.image_8 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_8, image=new_image)
            canvas.image_8 = new_image
            
        
    if(slot_id==1306):
        if(status==0):
            
            new_image_path = relative_to_assets("image_6.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_7, image=new_image)
            canvas.image_7 = new_image
            canvas.itemconfig(TagNumber_1306, text="")
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
        if(status==1):
            
            new_image_path = relative_to_assets("image_5.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_7, image=new_image)
            canvas.image_7 = new_image
            
        if(status==2):
            
            new_image_path = relative_to_assets("image_4.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_7, image=new_image)
            canvas.image_7 = new_image
        if(status==3):
            
            new_image_path = relative_to_assets("image_3.png")  # Provide the path to the new image file

            # Load the new image
            new_image = PhotoImage(file=new_image_path)

            # Update the canvas create_image method with the new image
            canvas.itemconfig(image_7, image=new_image)
            canvas.image_7 = new_image
            
        

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
# 
# image_image_2 = PhotoImage(
#     file=relative_to_assets("image_2.png"))
# image_2 = canvas.create_image(
#     1052.0,
#     290.0,
#     image=image_image_2
# )

canvas.create_text(
    250.0,
    11.0,
    anchor="nw",
    text="License Plate",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 36 * -1)
)
# 
# canvas.create_text(
#     932.0,
#     11.0,
#     anchor="nw",
#     text="Parking Space",
#     fill="#FFFFFF",
#     font=("Inter ExtraBold", 36 * -1)
# )

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
    textvariable=no_plate  # Assign StringVar to textvariable
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


#  
# slot_no_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
#                  '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22',
#                  '23', '24', '25', '26']
# style = ttk.Style()
# style.configure('TCombobox', arrowsize=30)
# 
# prkng_slt_cmbx = ttk.Combobox(window,values=slot_no_list, width = 30,font=("Arial Bold", 25))
# prkng_slt_cmbx.set("Select Space")
# prkng_slt_cmbx.bind("<<ComboboxSelected>>", combobox_callback)
# window.option_add('*TCombobox*Listbox.font', ('Arial', 30)) 
 

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


# Adding combobox drop down list 

# prkng_slt_cmbx.place(x=902.0,
#     y=551.0,
#     width=300.0,
#     height=63.0)
  
# entry_2 = Entry(
#     bd=0,
#     bg="#D9D9D9",
#     fg="#000716",
#     highlightthickness=0
# )
# entry_2.place(
#     x=502.0,
#     y=401.0,
#     width=300.0,
#     height=63.0
# )





button_image_1 = PhotoImage(
    file=relative_to_assets("button_1_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=submit_btn,
    relief="flat"
)
# button_1.place(
#     x=102.0,
#     y=518.0,
#     width=710.0,
#     height=75.0
# )
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
    #print("space  = ", spaceNo)
    prkng_slt_cmbx.set(spaceNo)
    if(spaceNo == "01"):
        no_plate.set(canvas.TagNumber_1020)       
        
    if(spaceNo == "02"):
        no_plate.set(canvas.TagNumber_1019)
        
    if(spaceNo == "03"):
        no_plate.set(canvas.TagNumber_1018)
        
    if(spaceNo == "04"):
        no_plate.set(canvas.TagNumber_1017)
        
    if(spaceNo == "05"):
        no_plate.set(canvas.TagNumber_1016)
        
    if(spaceNo == "06"):
        no_plate.set(canvas.TagNumber_1013)
        
    if(spaceNo == "07"):
        no_plate.set(canvas.TagNumber_1012)
        
    if(spaceNo == "08"):
        no_plate.set(canvas.TagNumber_1011)
        
    if(spaceNo == "09"):
        no_plate.set(canvas.TagNumber_1010)
        
    if(spaceNo == "10"):
        no_plate.set(canvas.TagNumber_1009)
        
    if(spaceNo == "11"):
        no_plate.set(canvas.TagNumber_1007)
        
    if(spaceNo == "12"):
        no_plate.set(canvas.TagNumber_1005)
        
    if(spaceNo == "13"):
        no_plate.set(canvas.TagNumber_1006)
        
    if(spaceNo == "14"):
        no_plate.set(canvas.TagNumber_1308)
        
    if(spaceNo == "15"):
        no_plate.set(canvas.TagNumber_1307)
        
    if(spaceNo == "16"):
        no_plate.set(canvas.TagNumber_1306)   

image_image_3 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_3 = canvas.create_image(
    820.0,
    698.0,
    image=image_image_3
)
canvas.tag_bind(image_3, "<Button-1>", lambda event: Click_Cart_Truck("01"))

image_image_4 = PhotoImage(
    file=relative_to_assets("image_6.png"))   
image_4 = canvas.create_image(
    820.0,
    654.0,
    image=image_image_4
)
canvas.tag_bind(image_4, "<Button-1>", lambda event: Click_Cart_Truck("02"))

image_image_5 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_5 = canvas.create_image(
    820.0,
    610.0,
    image=image_image_5
    
)
canvas.tag_bind(image_5, "<Button-1>", lambda event: Click_Cart_Truck("03"))

image_image_18 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_18 = canvas.create_image(
    820.0,
    566.0,
    image=image_image_18
)
canvas.tag_bind(image_18, "<Button-1>", lambda event: Click_Cart_Truck("04"))

#truck_tag = canvas.TagNumber_1016
image_image_14 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_14 = canvas.create_image(
    820.0,
    522.0,
    image=image_image_14
)
canvas.tag_bind(image_14, "<Button-1>", lambda event: Click_Cart_Truck("05"))

image_image_17 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_17 = canvas.create_image(
    820.0,
    478.0,
    image=image_image_17
)
canvas.tag_bind(image_17, "<Button-1>", lambda event: Click_Cart_Truck("06"))

image_image_16 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_16 = canvas.create_image(
    820.0,
    434.0,
    image=image_image_16
)
canvas.tag_bind(image_16, "<Button-1>", lambda event: Click_Cart_Truck("07"))

image_image_15 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_15 = canvas.create_image(
    820.0,
    390.0,
    image=image_image_15
)
canvas.tag_bind(image_15, "<Button-1>", lambda event: Click_Cart_Truck("08"))

image_image_13 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_13 = canvas.create_image(
    820.0,
    346.0,
    image=image_image_13
)
canvas.tag_bind(image_13, "<Button-1>", lambda event: Click_Cart_Truck("09"))

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    820.0,
    302.0,
    image=image_image_6
)
canvas.tag_bind(image_6, "<Button-1>", lambda event: Click_Cart_Truck("10"))

image_image_12 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_12 = canvas.create_image(
    820.0,
    258.0,
    image=image_image_12
)
canvas.tag_bind(image_12, "<Button-1>", lambda event: Click_Cart_Truck("11"))

image_image_11 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_11 = canvas.create_image(
    820.0,
    214.0,
    image=image_image_11
)
canvas.tag_bind(image_11, "<Button-1>", lambda event: Click_Cart_Truck("12"))

image_image_10 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_10 = canvas.create_image(
    820.0,
    170.0,
    image=image_image_10
)
canvas.tag_bind(image_10, "<Button-1>", lambda event: Click_Cart_Truck("13"))

image_image_9 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_9 = canvas.create_image(
    820.0,
    126.0,
    image=image_image_9
)
canvas.tag_bind(image_9, "<Button-1>", lambda event: Click_Cart_Truck("14"))

image_image_8 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_8 = canvas.create_image(
    820.0,
    82.0,
    image=image_image_8
)
canvas.tag_bind(image_8, "<Button-1>", lambda event: Click_Cart_Truck("15"))

image_image_7 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_7 = canvas.create_image(
    820.0,
    38.0,
    image=image_image_7
)
canvas.tag_bind(image_7, "<Button-1>", lambda event: Click_Cart_Truck("16"))

canvas.create_text(
    878.0,
    680.0,
    anchor="nw",
    text="01",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    636.0,
    anchor="nw",
    text="02",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    592.0,
    anchor="nw",
    text="03",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    548.0,
    anchor="nw",
    text="04",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    504.0,
    anchor="nw",
    text="05",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    460.0,
    anchor="nw",
    text="06",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    416.0,
    anchor="nw",
    text="07",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    372.0,
    anchor="nw",
    text="08",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    328.0,
    anchor="nw",
    text="09",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    284.0,
    anchor="nw",
    text="10",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    240.0,
    anchor="nw",
    text="11",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    196.0,
    anchor="nw",
    text="12",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    152.0,
    anchor="nw",
    text="13",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    108.0,
    anchor="nw",
    text="14",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    64.0,
    anchor="nw",
    text="15",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

canvas.create_text(
    878.0,
    20.0,
    anchor="nw",
    text="16",
    fill="#000000",
    font=("Inter Medium", 32 * -1)
)

# Showing TagNumber
TagNumber_1020 = canvas.create_text(
    1015.0,
    685.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)

TagNumber_1019 = canvas.create_text(
    1015.0,
    641.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1018 = canvas.create_text(
    1015.0,
    597.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1017 = canvas.create_text(
    1015.0,
    553.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1016 = canvas.create_text(
    1015.0,
    509.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1013 = canvas.create_text(
    1015.0,
    465.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1012 = canvas.create_text(
    1015.0,
    421.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1011 = canvas.create_text(
    1015.0,
    377.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1010 = canvas.create_text(
    1015.0,
    333.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1009 = canvas.create_text(
    1015.0,
    289.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1007 = canvas.create_text(
    1015.0,
    245.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1005 = canvas.create_text(
    1015.0,
    201.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1006 = canvas.create_text(
    1015.0,
    157.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1308 = canvas.create_text(
    1015.0,
    113.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1307 = canvas.create_text(
    1015.0,
    69.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)
TagNumber_1306 = canvas.create_text(
    1015.0,
    25.0,
    anchor="nw",
    text=" ",
    fill="#000000",
    font=("Inter Medium", 23 * -1)
)

def update_tag_number_text(truck_tag,slot_id, status):
    if(slot_id == 1020 ):
        canvas.itemconfig(TagNumber_1020, text=truck_tag)
        canvas.TagNumber_1020 = truck_tag        
        
    if(slot_id == 1019):
        canvas.itemconfig(TagNumber_1019, text=truck_tag)
        canvas.TagNumber_1019 = truck_tag
        
    if(slot_id == 1018):
        canvas.itemconfig(TagNumber_1018, text=truck_tag)
        canvas.TagNumber_1018 = truck_tag
        
    if(slot_id == 1017):
        canvas.itemconfig(TagNumber_1017, text=truck_tag)
        canvas.TagNumber_1017 = truck_tag
        
    if(slot_id == 1016):      
        canvas.itemconfig(TagNumber_1016, text=truck_tag)
        canvas.TagNumber_1016 = truck_tag
        
    if(slot_id == 1013):
        canvas.itemconfig(TagNumber_1013, text=truck_tag)
        canvas.TagNumber_1013 = truck_tag
        
    if(slot_id == 1012):
        canvas.itemconfig(TagNumber_1012, text=truck_tag)
        canvas.TagNumber_1012 = truck_tag
        
    if(slot_id == 1011):
        canvas.itemconfig(TagNumber_1011, text=truck_tag)
        canvas.TagNumber_1011 = truck_tag
        
    if(slot_id == 1010):
        canvas.itemconfig(TagNumber_1010, text=truck_tag)
        canvas.TagNumber_1010 = truck_tag
        
    if(slot_id == 1009):
        canvas.itemconfig(TagNumber_1009, text=truck_tag)
        canvas.TagNumber_1009 = truck_tag
        
    if(slot_id == 1007):
        canvas.itemconfig(TagNumber_1007, text=truck_tag)
        canvas.TagNumber_1007 = truck_tag
        
    if(slot_id == 1005):
        canvas.itemconfig(TagNumber_1005, text=truck_tag)
        canvas.TagNumber_1005 = truck_tag      
          
    if(slot_id == 1006):
        canvas.itemconfig(TagNumber_1006, text=truck_tag)
        canvas.TagNumber_1006 = truck_tag
        
    if(slot_id == 1308):
        canvas.itemconfig(TagNumber_1308, text=truck_tag)
        canvas.TagNumber_1308 = truck_tag
        
    if(slot_id == 1307):
        canvas.itemconfig(TagNumber_1307, text=truck_tag)
        canvas.TagNumber_1307 = truck_tag
        
    if(slot_id == 1306):
        canvas.itemconfig(TagNumber_1306, text=truck_tag)
        canvas.TagNumber_1306 = truck_tag      
        
 
def clear_tag_number_text():
    canvas.TagNumber_1020 = ""
    canvas.TagNumber_1019 = ""
    canvas.TagNumber_1018 = ""
    canvas.TagNumber_1017 = ""
    canvas.TagNumber_1016 = ""
    canvas.TagNumber_1013 = ""
    canvas.TagNumber_1012 = ""
    canvas.TagNumber_1011 = ""
    canvas.TagNumber_1010 = ""
    canvas.TagNumber_1009 = ""
    canvas.TagNumber_1007 = ""
    canvas.TagNumber_1005 = ""
    canvas.TagNumber_1006 = ""
    canvas.TagNumber_1308 = ""
    canvas.TagNumber_1307 = ""
    canvas.TagNumber_1306 = ""
    

icon_images_ref = {}
click_counts =  0
IsCheckWarning = 0

def CheatPark_Warning_Message(slot_id, status, isWarningToday,warningCount,tTag):
    global icon_images_ref,click_counts, IsCheckWarning
    
    if slot_id == 1020:
        if status == 3 and isWarningToday == "0":
            icon_image_1 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            # Store reference to prevent garbage collection
            icon_images_ref["1020"] = icon_image_1  
            img_1 = canvas.create_image(950.0, 697.0, image=icon_image_1)
            click_counts = 0
            icon_images_ref["1020_img"] = img_1
            if "1020_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 697.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1020_text"] = text_id

            # Bind click event
            canvas.tag_bind(img_1, "<Button-1>", lambda event: Warning_Messages(tTag, "01",warningCount))
            canvas.itemconfig(icon_images_ref["1020_text"], text=str(warningCount)) 
            #print("++++", IsCheckWarning)
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1020, "01")
#                 
        else:
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
                
                if slot_id in icon_images_ref:
                    del icon_images_ref[slot_id]
                           
           
    if slot_id == 1019:
        if status == 3 and isWarningToday == "0":
            icon_image_2 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            
            # Store reference to prevent garbage collection
            icon_images_ref["1019"] = icon_image_2  
            
            img_2 = canvas.create_image(950.0, 653.0, image=icon_image_2)
            click_counts = 0
            icon_images_ref["1019_img"] = img_2
            if "1019_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 653.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1019_text"] = text_id

            # Bind click event
            canvas.tag_bind(img_2, "<Button-1>", lambda event: Warning_Messages(tTag, "02",warningCount))
            canvas.itemconfig(icon_images_ref["1019_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                     Warning_Messages(canvas.TagNumber_1019, "02")
        else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id]           
    if slot_id == 1018:
        if status == 3 and isWarningToday == "0":
           # print("Status is 1018, showing the image...")
            icon_image_3 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            # Store reference to prevent garbage collection
            icon_images_ref["1018"] = icon_image_3  
            
            img_3 = canvas.create_image(950.0, 609.0, image=icon_image_3)
            click_counts = 0
            icon_images_ref["1018_img"] = img_3
            if "1018_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 609.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1018_text"] = text_id

            # Bind click event
            canvas.tag_bind(img_3, "<Button-1>", lambda event: Warning_Messages(tTag, "03",warningCount))
            canvas.itemconfig(icon_images_ref["1018_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1018, "03")
        else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id]         

    if slot_id == 1017:
        if status == 3 and isWarningToday == "0":
           # print("Status is 1017, showing the image...")
            icon_image_4 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            # Store reference to prevent garbage collection
            icon_images_ref["1017"] = icon_image_4  
            
            img_4 = canvas.create_image(950.0, 565.0, image=icon_image_4)
           # print("Image created with ID:", img_4)
            click_counts = 0
            icon_images_ref["1017_img"] = img_4
            if "1017_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 565.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1017_text"] = text_id

            # Bind click event
            canvas.tag_bind(img_4, "<Button-1>", lambda event: Warning_Messages(tTag, "04",warningCount))
            canvas.itemconfig(icon_images_ref["1017_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1017, "04")
        else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id]      
                
    if slot_id == 1016:
        if status == 3 and isWarningToday == "0":
           # print("Status is 1016, showing the image...")
            icon_image_5 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            # Store reference to prevent garbage collection
            icon_images_ref["1016"] = icon_image_5  
            
            img_5 = canvas.create_image(950.0, 521.0, image=icon_image_5)
            click_counts = 0
            icon_images_ref["1016_img"] = img_5
            if "1016_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 521.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1016_text"] = text_id
            
            canvas.tag_bind(img_5, "<Button-1>", lambda event: Warning_Messages(tTag, "05",warningCount))
            canvas.itemconfig(icon_images_ref["1016_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1016, "05")
        else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id]        
                
    if slot_id == 1013:
        if status == 3 and isWarningToday == "0":
            #print("Status is 1013, showing the image...")
            icon_image_6 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            # Store reference to prevent garbage collection
            icon_images_ref["1013"] = icon_image_6  
            
            img_6 = canvas.create_image(950.0, 477.0, image=icon_image_6)
            click_counts = 0
            icon_images_ref["1013_img"] = img_6
            if "1013_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 477.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1013_text"] = text_id
            # Bind click event
            canvas.tag_bind(img_6, "<Button-1>", lambda event: Warning_Messages(tTag, "06",warningCount))
            canvas.itemconfig(icon_images_ref["1013_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1013, "06")
        else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id]        
        
    if slot_id == 1012:
        if status == 3 and isWarningToday == "0":
            #print("Status is 1012, showing the image...")
            icon_image_7 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            # Store reference to prevent garbage collection
            icon_images_ref["1012"] = icon_image_7  
            
            img_7 = canvas.create_image(950.0, 433.0, image=icon_image_7)
            click_counts = 0
            icon_images_ref["1012_img"] = img_7
            if "1012_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 433.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1012_text"] = text_id
            # Bind click event
            canvas.tag_bind(img_7, "<Button-1>", lambda event: Warning_Messages(tTag, "07",warningCount))
            canvas.itemconfig(icon_images_ref["1012_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1012, "07")
        else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id]       

    if slot_id == 1011:
        if status == 3 and isWarningToday == "0":
            #print("Status is 1011, showing the image...")
            icon_image_8 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            # Store reference to prevent garbage collection
            icon_images_ref["1011"] = icon_image_8  
            
            img_8 = canvas.create_image(950.0, 389.0, image=icon_image_8)
            click_counts = 0
            icon_images_ref["1011_img"] = img_8
            if "1011_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 389.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1011_text"] = text_id
            # Bind click event
            canvas.tag_bind(img_8, "<Button-1>", lambda event: Warning_Messages(tTag, "08",warningCount))
            canvas.itemconfig(icon_images_ref["1011_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1011, "08")
        else:
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0        
                
    if slot_id == 1010:
        if status == 3 and isWarningToday == "0":
           # print("Status is 1010, showing the image...")
            icon_image_9 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            # Store reference to prevent garbage collection
            icon_images_ref["1010"] = icon_image_9  
            
            img_9 = canvas.create_image(950.0, 345.0, image=icon_image_9)
            click_counts = 0
            icon_images_ref["1010_img"] = img_9
            if "1010_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 345.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1010_text"] = text_id

            # Bind click event
            canvas.tag_bind(img_9, "<Button-1>", lambda event: Warning_Messages(tTag, "09",warningCount))
            canvas.itemconfig(icon_images_ref["1010_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1010, "09")
        else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id]         
                
    if slot_id == 1009:
        if status == 3 and isWarningToday == "0":
            icon_image_10 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            icon_images_ref["1009"] = icon_image_10
            
            img_10 = canvas.create_image(950.0, 301.0, image=icon_image_10)
            click_counts = 0
            icon_images_ref["1009_img"] = img_10
            if "1009_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 301.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1009_text"] = text_id

            # Bind click event
            canvas.tag_bind(img_10, "<Button-1>", lambda event: Warning_Messages(tTag, "10",warningCount))
            canvas.itemconfig(icon_images_ref["1009_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1009, "10")
        else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id]        
                
    if slot_id == 1007:
        if status == 3 and isWarningToday == "0":
            #print("Status is 1007, showing the image...")
            icon_image_11 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            # Store reference to prevent garbage collection
            icon_images_ref["1007"] = icon_image_11  
            
            img_11 = canvas.create_image(950.0, 257.0, image=icon_image_11)
            click_counts = 0
            icon_images_ref["1007_img"] = img_11
            if "1007_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 257.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1007_text"] = text_id

            # Bind click event
            canvas.tag_bind(img_11, "<Button-1>", lambda event: Warning_Messages(tTag, "11",warningCount))
            canvas.itemconfig(icon_images_ref["1007_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1007, "11")
#                
        else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id]        
        
    if slot_id == 1005:
        if status == 3 and isWarningToday == "0":
            icon_image_12 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            icon_images_ref["1005"] = icon_image_12  
            
            img_12 = canvas.create_image(950.0, 213.0, image=icon_image_12)
            click_counts = 0
            icon_images_ref["1005_img"] = img_12
            if "1005_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 213.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1005_text"] = text_id

            # Bind click event
            canvas.tag_bind(img_12, "<Button-1>", lambda event: Warning_Messages(tTag, "12",warningCount))
            canvas.itemconfig(icon_images_ref["1005_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1005, "12")
        else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
                
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id]         
                
     
    if slot_id == 1006:
         if status == 3 and isWarningToday == "0":
            #print("Status is 1006, showing the image...")
            icon_image_13 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            # Store reference to prevent garbage collection
            icon_images_ref["1006"] = icon_image_13  
            
            img_13 = canvas.create_image(950.0, 169.0, image=icon_image_13)
            click_counts = 0
            icon_images_ref["1006_img"] = img_13
            if "1006_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 169.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1006_text"] = text_id

            # Bind click event
            canvas.tag_bind(img_13, "<Button-1>", lambda event: Warning_Messages(tTag, "13",warningCount))
            canvas.itemconfig(icon_images_ref["1006_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1006, "13")
         else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id]      
                
    if slot_id == 1308: 
        if status == 3 and isWarningToday == "0":
            #print("Status is 1308, showing the image...")
            icon_image_14 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            # Store reference to prevent garbage collection
            icon_images_ref["1308"] = icon_image_14  
            
            img_14 = canvas.create_image(950.0, 125.0, image=icon_image_14)
            click_counts = 0
            icon_images_ref["1308_img"] = img_14
            if "1308_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 125.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1308_text"] = text_id

            # Bind click event
            canvas.tag_bind(img_14, "<Button-1>", lambda event: Warning_Messages(tTag, "14",warningCount))
            canvas.itemconfig(icon_images_ref["1308_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1308, "14")
                
        else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id]
                
    if slot_id == 1307:         
        if status == 3 and isWarningToday == "0":
            icon_image_15 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            # Store reference to prevent garbage collection
            icon_images_ref["1307"] = icon_image_15  
            
            img_15 = canvas.create_image(950.0, 81.0, image=icon_image_15)
            click_counts = 0
            icon_images_ref["1307_img"] = img_15
            if "1307_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 81.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1307_text"] = text_id

            # Bind click event
            canvas.tag_bind(img_15, "<Button-1>", lambda event: Warning_Messages(tTag, "15",warningCount))
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1307, "15")
               # warningCount = 0
            canvas.itemconfig(icon_images_ref["1307_text"], text=str(warningCount)) 
                
        else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id] 
                    
    if slot_id == 1306:
        if status == 3 and isWarningToday == "0":
            #print("Status is 1306, showing the image...")
            icon_image_16 = PhotoImage(file=relative_to_assets("printer-icon.png"))
            # Store reference to prevent garbage collection
            icon_images_ref["1306"] = icon_image_16  
            
            img_16 = canvas.create_image(950.0, 37.0, image=icon_image_16)
            click_counts = 0
            icon_images_ref["1306_img"] = img_16
            if "1306_text" not in icon_images_ref:
                text_id = canvas.create_text(990.0, 37.0, text="", font=("Arial", 14), fill="black")
                icon_images_ref["1306_text"] = text_id

            # Bind click event
            canvas.tag_bind(img_16, "<Button-1>", lambda event: Warning_Messages(tTag,"16",warningCount))
            canvas.itemconfig(icon_images_ref["1306_text"], text=str(warningCount)) 
#             if(IsCheckWarning < 10):
#                 Warning_Messages(canvas.TagNumber_1306, "16")
        else: 
            if f"{slot_id}_img" in icon_images_ref:
                canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
                canvas.delete(icon_images_ref[f"{slot_id}_text"])
                del icon_images_ref[f"{slot_id}_img"]  # Remove reference
                del icon_images_ref[f"{slot_id}_text"]
                click_counts = 0
            
            if slot_id in icon_images_ref:
                del icon_images_ref[slot_id]         
        canvas.update()   
        canvas.update_idletasks()  # Ensure UI updates

# def clear_printer_icon():
#     global icon_images_ref
#     slot_ids = [
#         "1020", "1019", "1018", "1017", "1016", "1013", "1012", "1011",
#         "1010", "1009", "1007", "1005", "1006", "1308", "1307", "1306"
#     ]
# 
#     for slot_id in slot_ids:
#         # Check if the image exists before deleting
#         if f"{slot_id}_img" in icon_images_ref:
#             canvas.delete(icon_images_ref[f"{slot_id}_img"])  # Remove from canvas
#             #print("---------------------------------",canvas.delete(icon_images_ref[f"{slot_id}_img"]))
#             del icon_images_ref[f"{slot_id}_img"]  # Remove reference
#         
#         if slot_id in icon_images_ref:
#             del icon_images_ref[slot_id]
#     
 

# image_TagNumber_1 = PhotoImage(
#     file=relative_to_assets("image_6.png"))
# TagNumber_1 = canvas.create_image(
#     1590.0,
#     63.0,
#     Tag=image_TagNumber_1
# )

# image_image_19 = PhotoImage(
#     file=relative_to_assets("image_19.png"))
# image_19 = canvas.create_image(
#     1305.0,
#     385.0,
#     image=image_image_19
# )
#Recent commented code for camera
# button_image_2 = PhotoImage(
#     file=relative_to_assets("button_2.png"))
# button_2 = Button(
#     image=button_image_2,
#     borderwidth=0,
#     highlightthickness=0,
#     command=lambda:capture_image(),
#     relief="flat"
# )
# button_2.place(
#     x=650.0,
#     y=23.0,
#     width=30.0,
#     height=27.0
# )

# button_image_3 = PhotoImage(
#     file=relative_to_assets("button_3.png"))
# button_3 = Button(
#     image=button_image_3,
#     borderwidth=0,
#     highlightthickness=0,
#     #command=lambda: print("button_3 clicked"),
#     command=lambda: Capture_Slot_Number(),
#     relief="flat"
# )
# button_3.place(
#     x=1337.0,
#     y=23.0,
#     width=30.0,
#     height=27.0
# )
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

# button_image_4 = PhotoImage(
#     file=relative_to_assets("Reboot.png"))
# button_4 = Button(
#     image=button_image_4,
#     borderwidth=0,
#     highlightthickness=0,
#     command=lambda:open_text_box(),
#     relief="flat"
# )
# button_4.place(
#     x=60.0,
#     y=1015.0,
#     width=45.0,
#     height=45.0
# )


# def open_text_box():    
#     global RebootCode
#     global TempRebootCode
#     
#     if(str(TempRebootCode)==RebootCode):
#         subprocess.run(["sudo", "reboot"], check=True)  
        
        
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
#         print("submit button Queue put-------------------------------- 0")
    if not shared_queue_for_slot_id.empty():
        slot_ID=shared_queue_for_slot_id.get()
        # print("in update fn and shared_que",str(slot_ID))
        if(str(slot_ID).zfill(2) in my_dict.values()):
            # print("hdexuedudeueduyweewyuewuewyyuweyweiuewewuewiweu")
            prkng_slt_cmbx.set(str(slot_ID))
            space_id=get_key_from_value(my_dict, str(slot_ID).zfill(2))
            post_list[1]=space_id
            submit_btn_queue.put(0)
#             print("submit button Queue put ---------------------0")
            
    if not submit_btn_queue.empty():
        btn_state=submit_btn_queue.get()
#         print("submit button Queue -----------------------------------------------------------------------------------------GET")
        print("submit butoon state-----------",btn_state)
        if btn_state ==1:
            # change image of butoon
            new_image_path = relative_to_assets("button_1_2.png")  # Provide the path to the new image file

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
        # print(url)
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            #print(data)
            # Extract required key-value pairs
            total = data['total']
            #print(total)
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
    current_timestamp = str(int(time.time() * 1000))  # Current timestamp in milliseconds
    
    date_time=datetime.now()
    if date_time.hour <12:
        date_time=date_time - timedelta(days=1)
        
    date = date_time.strftime("%m/%d/%Y")  # Previous date in MM/DD/YYYY format
    # print(date)
    # URL template
    url_template = "https://truckovernight.azurewebsites.net/api/BookingAPI/GetBookingBydateAndTimeLeaveAndCompanyIdFor3rdPartyApi?date={}&CompanyId=16&SiteId=3021&_={}"
    return url_template.format(date, current_timestamp)
   


# def live_preview():
#     while(1):
#         time.sleep(10)
#         # Construct URL
#         url = construct_url()

#         # Trigger GET request and parse JSON
#         total, extracted_data = get_and_parse_json(url)

#         # Print results
#         if total is not None and extracted_data is not None:
#             print("Total:", total)
#             print("Extracted data:")
#             for item in extracted_data:
#                 print(type(item),item)
#                 print(type(item['SlotId']))
#                 update_truck_image(item['SlotId'],item['Status'])
                
                
                

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
    global IsCheckWarning
    i=0
    while(1):
#         if (post_list[0]!="0" and post_list[1]!="0") :
#              print("inside submit function")
#             url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateTruckLotBookingByHardWares"
#             # Define the JSON payload
#             payload = {
#                 "CompanyId": 16,
#                 "SiteId": 3021,
#                 "Status": 1,
#                 "SlotId": post_list[1],
#                 "TruckTag": post_list[0]
#             }
#             response = requests.post(url, json=payload)
#             if response.status_code == 200:
#                 print("Request successful")
#                 # You can print or handle the response content here if needed
#                 print("Response:", response.json())
#                 if not (f"{response.json()}") == "0":
#                     print(f"Slot status updated! Booking ID: {response.json()}")
#             else:
#                 print(f"Request failed with status code: {response.status_code}")
#                 print("Response content:", response.text)
        time.sleep(1)
        
        if(i>=8):
            list_to_check_blnk_prkng_spce=[]
            
            # Construct URL
            url = construct_url()
            clear_tag_number_text()
            #clear_printer_icon()
            # Trigger GET request and parse JSON
            total, extracted_data = get_and_parse_json(url)
            
            #update_tag_number_text.set("")
            if total is not None and extracted_data is not None:
#                print("Total:", total)
                #print("Extracted data:",extracted_data)
                for item in extracted_data:     
                    update_truck_image(item['SlotId'],item['Status'])
                    #slot_id = item['SlotId']  # Define slot_id before using it
                    #clear_printer_icon(slot_id) 
                    #Print_Warning_Message(item['SlotId'],item['Status'])
                    if(item['TruckTag'] != ""):                        
                        update_tag_number_text(item['TruckTag'],item['SlotId'],item['Status'])  # Update the text widget with TruckTag
                        CheatPark_Warning_Message(item['SlotId'],item['Status'],item['IsWarningToday'],item['WarningCount'],item['TruckTag'])
                    
                        #clear_tag_number_text(item['TruckTag'],item['SlotId'])
                        #update_tag_number_text.set("")
                        
                      #print('----------',item['TruckTag'])
        
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
    #print("-------------------------GetCheatParkTruckTagUrl",TruckTag)
    url_template = "https://truckovernight.azurewebsites.net/api/BookingAPI/GetCheatParkDataByTruckTag?TruckTag={}"
    return url_template.format(TruckTag)

def get_and_parse_warning_json(url):
    try:
        #print(url)
        response = requests.get(url)
        #print("----------------------------------------",response)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            #print(data)
            # Extract required key-value pairs
            
            extracted_data = []

            for row in data:
                extracted_data.append(row)
#                 extracted_data.append({
#                     #'SlotId': row['SlotId'],
#                     'Tag': row['Tag'],
#                     'Status': row['Status']
#                 })

            #total = extracted_data.length
            total = len(extracted_data)
            #print(total)
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

# Load the face classifier
#face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Assume that the authenticated user's face is pre-saved
#AUTHENTICATED_FACE_HASH = "precomputed_hash_here"  # Replace with your actual precomputed hash

# Initialize video capture
#video_capture = cv2.VideoCapture(1)
# 
# video_source2 = 1
# #video_source2 = 2
# #cam_width, cam_height = 640, 480
# print("new video_source2...........................")
# video_capture = cv2.VideoCapture(video_source2,cv2.CAP_V4L)
# 
# def detect_and_recognize_face():
#     ret, frame = video_capture.read()
#     if not ret:
#         return False
# 
#     gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
# 
#     for (x, y, w, h) in faces:
#         face = frame[y:y+h, x:x+w]
#         face_hash = hashlib.md5(face).hexdigest()
#         if face_hash == AUTHENTICATED_FACE_HASH:
#             return True  # Face recognized
# 
#     return False  # Face not recognized
# 
# 
# def reset_activity_timer():
#     global activity_timer
#     if activity_timer is not None:
#         window.after_cancel(activity_timer)  # Cancel the previous timer
# 
#     if detect_and_recognize_face():
#         # Face recognized, reset the timer without showing the popup
#         activity_timer = window.after(INACTIVITY_THRESHOLD, reset_activity_timer)
#     else:
#         # Face not recognized, set the timer to show the popup after inactivity
#         activity_timer = window.after(INACTIVITY_THRESHOLD, show_popup)


def reset_activity_timer():
     global activity_timer
     if activity_timer is not None:
         window.after_cancel(activity_timer)  # Cancel the previous timer
     activity_timer = window.after(INACTIVITY_THRESHOLD, show_popup)  # Set a new timer
  
    
def show_popup():    
    popup = tk.Toplevel()  #Tk()
    popup.title("Authentication")
    #popup.geometry("1920x730")
    popup.geometry("580x480")
    popup.configure(bg = "#2B2264")
    popup.protocol("WM_DELETE_WINDOW", lambda: None)
    
#     popup_width = 1910
#     popup_height = 720
#     screen_width = popup.winfo_screenwidth()
#     screen_height = popup.winfo_screenheight()
#     x_position = (screen_width // 2) - (popup_width // 2)
#     y_position = (screen_height // 2) - (popup_height // 2)
#     popup.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")

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
    image_path = "/home/steve/Downloads/frame1.jpg"
    #with open(image_path, "rb") as image_file:
     #   image_bytes = image_file.read()
      #  image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    

    url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateCheatPark"
    print(url)
    # Define the JSON payload
    payload = {           
             # "SiteId": 3021,
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
              #"SiteId": 3021,
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
              #"SiteId": 3021,
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

# popup_image = PhotoImage(
#     file=relative_to_assets("warning.png"))
# button_5 = Button(
#     image=popup_image,
#     borderwidth=0,
#     highlightthickness=0,
#     command=lambda:open_warning_popup(),
#     relief="flat"
# )
# button_5.place(
#     x=420.0,
#     y=1015.0,
#     width=45.0,
#     height=45.0
# )
button1_image = None
button2_image = None
button3_image = None
button4_image = None
W_popup = None


def open_warning_popup():
    global W_popup

    # Check if popup is already open
    if W_popup and W_popup.winfo_exists():
        return  # Do nothing if popup is already open
    
    global textbox, button1_image, button2_image, button3_image, button4_image
    W_popup = tk.Toplevel()
    #W_popup.title("Popup Box")
    W_popup.geometry("580x320")
    #W_popup.configure(bg="#a2c3c3")
    W_popup.configure(bg="white")
    W_popup.protocol("WM_DELETE_WINDOW", lambda: None)
    

    #style = ttk.Style()
    #style.configure("White.TLabel", foreground="white", background="#2B2264")

    label = tk.Label(W_popup, text="Enter Truck Number")
    label.pack(pady=(10, 0))
    
    large_font = tkFont.Font(family="Helvetica", size=30)

    # Add a textbox
    textbox = tk.Text(W_popup,height=1, width=20,font=large_font)
    textbox.pack(pady=10,ipadx=10, ipady=10)
    
    #btn_font = tkFont.Font(family="Helvetica", size=15)
    
    # Add four buttons
    button1_image = PhotoImage(
    file=relative_to_assets("First_warning.png"))
    button1 = Button(
        W_popup,  
        image=button1_image,  
        borderwidth=0,
        highlightthickness=0,
        command=lambda: on_button_click(1),  
        relief="flat"
    )    
    button1.place(
        x=40.0,
        y=150.0,
        width=140.0,
        height=50.0
    )
    
    button2_image = PhotoImage(
    file=relative_to_assets("Second_warning.png"))
    button2 = Button(
        W_popup,  
        image=button2_image,  
        borderwidth=0,
        highlightthickness=0,
        command=lambda: on_button_click(2),  
        relief="flat"
    )    
    button2.place(
        x=213.0,
        y=150.0,
        width=140.0,
        height=50.0
    )
    
    button3_image = PhotoImage(
    file=relative_to_assets("Last_warning.png"))
    button3 = Button(
        W_popup,  
        image=button3_image,  
        borderwidth=0,
        highlightthickness=0,
        command=lambda: on_button_click(3),  
        relief="flat"
    )    
    button3.place(
        x=390.0,
        y=150.0,
        width=140.0,
        height=50.0
    )
    
    button4_image = PhotoImage(
    file=relative_to_assets("Close.png"))
    button4 = Button(
        W_popup,  
        image=button4_image,  
        borderwidth=0,
        highlightthickness=0,
        command=lambda: button_action(4,W_popup),  
        relief="flat"
    )    
    button4.place(
        x=213.0,
        y=220.0,
        width=140.0,
        height=50.0
    )
    
#     button1 = tk.Button(W_popup, text="First Warning", command=lambda: on_button_click(1))
#     button1.pack(side=tk.LEFT,padx=(30, 10), pady=10)
#
#     button2 = tk.Button(W_popup, text="Second Warning", command=lambda: on_button_click(2))
#     button2.pack(side=tk.LEFT, padx=10, pady=10)
# 
#     button3 = tk.Button(W_popup, text="Third Warning", command=lambda: on_button_click(3))
#     button3.pack(side=tk.LEFT, padx=10, pady=10)
#     
#     button4 = tk.Button(W_popup, text="Close", command=lambda: button_action(4,W_popup))
#     button4.pack(side=tk.LEFT, padx=10, pady=10)
#
  
    W_popup.transient(window)
    #W_popup.grab_set()
    #window.wait_window(W_popup)

def on_button_click(button_number):
    if button_number == 1:
        print("Button 1 clicked!")
        Fist_Warning()
            
    if button_number == 2:
        print("Button 2 clicked!")
        Second_Warning()
            
    if button_number == 3:
        print("Button 3 clicked!")
        Third_Warning()       
    
def button_action(button_number,W_popup):                                          
        if button_number == 4:
            global popup_window
            popup_window = None
            W_popup.destroy()    
        
def Fist_Warning():
    #image_path = "/home/steve/Downloads/frame1.jpg"
    #with open(image_path, "rb") as image_file:
     #   image_bytes = image_file.read()
      #  image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    

    url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateCheatPark"
    print(url)
    # Define the JSON payload
    payload = {           
             # "SiteId": 3021,
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
def Second_Warning():
    
    choice = StringVar()
    choice=prkng_slt_cmbx.get()
    choice=get_key_from_value(my_dict, choice)
    post_list[1]=choice

    url = "https://truckovernight.azurewebsites.net/api/bookingapi/CreateCheatPark"
    print(url)
    # Define the JSON payload
    payload = {           
              #"SiteId": 3021,
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
    
def Third_Warning():
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
              #"SiteId": 3021,
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
    
    
#     global click_counts, IsCheckWarning
#     choice = space_No
#     choice=get_key_from_value(my_dict, choice)
#     Slot_Id=choice
    
#     url = GetCheatParkTruckTagUrl(Tag_id)
#     today_date = datetime.today().date()
#     total, extracted_data = get_and_parse_warning_json(url)
#     print("CheatparkData ====================================",extracted_data)
#     isWarningIssuedToday = 0
#     if total is not None and extracted_data is not None:
#         truck_tag_count = 0
#         click_counts = 0
#         isWarningIssuedToday = 0
#         for item in extracted_data:
#             date = parser.parse(item['CreatedDate']).date()
#             if item['Tag'].strip() == Tag_id and date != today_date:
#                 truck_tag_count += 1
#             if item['Tag'].strip() == Tag_id and date == today_date:
#                 isWarningIssuedToday = 1
#         if(isWarningIssuedToday == 0):          
#             if Slot_Id + "_text" in icon_images_ref:
#                 if(truck_tag_count > 2):
#                     truck_tag_count = 3
#                 canvas.itemconfig(icon_images_ref[Slot_Id + "_text"],text=f"( {truck_tag_count} )")
                
#             if(IsCheckWarning < 20):
#                 print("-----", IsCheckWarning)
#                 # Display warnings based on the count of TruckTag matches
#                 if truck_tag_count == 0 and Tag_id != "":
#                     print("First Warning", "No truck tag found.")           
#                     first_warning_demo(Tag_id,space_No)  # Custom function for the first warning
# 
#                 elif truck_tag_count == 1 and Tag_id != "":
#                     print("Second Warning", "One truck tag found.")
#                     second_warning_demo(Tag_id,space_No) 
#                     
#                 elif truck_tag_count >= 2 and Tag_id != "":
#                     print("Last Warning", f"{truck_tag_count} truck tags found.")
#                     last_warning_demo(Tag_id,space_No)
 
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
              "SiteId": 3021,
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
              "SiteId": 3021,
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
              "SiteId": 3021,
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
    

# Initialize the activity timer
reset_activity_timer()
# slot_id_thread = threading.Thread(target=slot_ID_reader, daemon=True)
# slot_id_thread.start()
license_plate_thread = threading.Thread(target=license_plate_reader, daemon=True)
license_plate_thread.start()
SlotId_plate_thread = threading.Thread(target=SlotId_plate_reader, daemon=True)
SlotId_plate_thread.start()
submit_post_req_thread = threading.Thread(target=submit_post_req, daemon=True)
submit_post_req_thread.start()

#show_network_alert()

#video_capture.release()
cv2.destroyAllWindows()
# live_preview()
update_label()
update_video1()
#update_video2()
window.resizable(False, False)
#thread1.join()
window.mainloop()







