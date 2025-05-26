# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import QUrl
# 
# class BrowserWindow(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Open Browser')
#         self.setGeometry(100, 100, 720, 430)
# 
#         # Create a QWebEngineView widget
#         self.browser = QWebEngineView()
# 
#         # Convert the URL string to a QUrl object
#         url = QUrl("https://google.com")
#         
#         # Set the URL in the browser
#         self.browser.setUrl(url)
# 
#         # Create a layout and add the browser to it
#         layout = QVBoxLayout()
#         layout.addWidget(self.browser)
#         
#         self.setLayout(layout)
# 
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Main Window')
#         self.setGeometry(100, 100, 1920, 1200)
# 
#         # Set the main window to fullscreen
#         #self.showFullScreen()
# 
#         # Create a vertical layout
#         layout = QVBoxLayout()
# 
#         # Create a widget to contain the layout
#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)
# 
#         # Create the open_browser button with smaller size
#         open_browser_btn = QPushButton('Open Browser', self)
#         open_browser_btn.setFixedSize(150, 50)  # Set the button size
#         open_browser_btn.clicked.connect(self.open_browser)
#         layout.addWidget(open_browser_btn)
# 
#         # Create the close_browser button with smaller size
#         close_browser_btn = QPushButton('Close Browser',self)
#         close_browser_btn.setFixedSize(150, 50)  # Set the button size
#         close_browser_btn.clicked.connect(self.close_browser)
#         layout.addWidget(close_browser_btn)
# 
#     def open_browser():
#         # Create and show the browser popup window
#         self.browser_window = BrowserWindow()
#         self.browser_window.exec_()
# 
#     def close_browser():
#          MainWindow.destroy()
#        
# # Initialize the application
# app = QApplication(sys.argv)
# 
# # Create and show the main window
# main_window = MainWindow()
# main_window.show()
# 
# # Execute the application's main loop
# sys.exit(app.exec_())

# ===================================  without class
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import QUrl
# 
# def open_browser():
#     # Create a dialog window for the browser
#     browser_window = QDialog()
#     browser_window.setWindowTitle('Embedded Browser')
#    # browser_window.geometry("720x430")
#     browser_window.setGeometry(100, 100, 720, 430)
# 
#     # Create a QWebEngineView widget
#     browser = QWebEngineView()
# 
#     # Convert the URL string to a QUrl object
#     url = QUrl("https://google.com")
#     
#     # Set the URL in the browser
#     browser.setUrl(url)
# 
#     # Create a layout and add the browser to it
#     layout = QVBoxLayout()
#     layout.addWidget(browser)
#     
#     browser_window.setLayout(layout)
# 
#     # Show the dialog
#     browser_window.exec_()
# 
# def main():
#     # Initialize the application
#     app = QApplication(sys.argv)
# 
#     # Create the main window
#     main_window = QMainWindow()
#     main_window.setWindowTitle('Main Window')
# 
#     # Set the main window to fullscreen
#     main_window.showFullScreen()
# 
#     # Create a vertical layout
#     layout = QVBoxLayout()
# 
#     # Create a widget to contain the layout
#     container = QWidget()
#     container.setLayout(layout)
#     main_window.setCentralWidget(container)
# 
#     # Create the open_browser button with smaller size
#     open_browser_btn = QPushButton('Open Browser', main_window)
#     open_browser_btn.setFixedSize(150, 50)  # Set the button size
#     open_browser_btn.clicked.connect(open_browser)
#     layout.addWidget(open_browser_btn)
# 
#     # Create the close_browser button with smaller size
#     close_browser_btn = QPushButton('Close Browser', main_window)
#     close_browser_btn.setFixedSize(150, 50)  # Set the button size
#     close_browser_btn.clicked.connect(app.quit)  # Close the entire application
#     layout.addWidget(close_browser_btn)
# 
#     # Show the main window
#     main_window.show()
# 
#     # Execute the application's main loop
#     sys.exit(app.exec_())
# 
# if __name__ == "__main__":
#     main()



#=========================================================================
# from tkinter import *
# from tkinter import ttk
# import tkinter as tk
# import webbrowser
# import tkinterweb
# 
# 
#     
# def Close_browser():
#     root.destroy()
#     
# 
# root = Tk()
# root.geometry("1920x1200+0+0")
# #root.attributes('-fullscreen', True)
# frame = tkinterweb.HtmlFrame(root)
# frame.load_website("https://google.com")
# frame.pack()
# 
# # def open_browser():
# #     popup = tk.Toplevel()
# #     popup.title("Open Browser")
# #     popup.geometry("720x430")
# #     popup.configure(bg = "#2B2264")
# #     frame = tkinterweb.HtmlFrame(popup)
# #     frame.load_website("https://google.com")
# #     frame.pack(fill="both", expand=True)
#     
#     
# #     frame = tkinterweb.HtmlFrame(popup)
# #     frame.load_website("https://google.com")
# #     frame.pack()
# 
# # 
# # button = tk.Button(root, text="Open Browser", command=open_browser)
# # button.pack(pady=20, ipadx=10, ipady=10)
# 
# button = tk.Button(root, text="Close", command=Close_browser)
# button.pack(pady=20, ipadx=10, ipady=10)
# 
# root.mainloop()

# # 
# import sys
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtWebEngineWidgets import *
# import time
# import cv2
# import os
# 
# os.environ["QT_PLUGIN_PATH"] = "/usr/lib/qt5/plugins"
# os.environ["QT_QPA_PLATFORM"] = "xcb"
# os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")
# 
# 
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.browser = QWebEngineView()        
#         self.browser.setUrl(QUrl('https://app.newfrontiersystems.com/home/videocalling?siteId=3021'))
#         self.setCentralWidget(self.browser)
#         self.showMaximized()
# app = QApplication(sys.argv)
# QApplication.setApplicationName('Example Custom Browser')
# window = MainWindow()
# app.exec_()

# 
#
#===============================================================
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import QUrl
# 
# 
# class BrowserWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Embedded Browser')
#         self.setGeometry(100, 100, 820, 490)
#         
#         # Create a QWebEngineView widget
#         self.browser = QWebEngineView()
# 
#         # Convert the URL string to a QUrl object
#         url = QUrl("https://app.newfrontiersystems.com/home/videocalling?siteId=3021")
#         
#         # Set the URL in the browser
#         self.browser.setUrl(url)
# 
#         # Set the browser as the central widget
#         self.setCentralWidget(self.browser)
#         #self.browser.page().featurePermissionRequested.connect(self.onFeaturePermissionRequested)
# 
# # def onFeaturePermissionRequested(self, url, feature):
# #         if feature in (QWebEnginePage.MediaVideoCapture, QWebEnginePage.MediaAudioCapture):
# #             # Grant permission for video and audio capture (camera, microphone)
# #             self.browser.page().setFeaturePermission(url, feature, QWebEnginePage.PermissionGrantedByUser)
#             
# 
# # Initialize the application
# app = QApplication(sys.argv)
# 
# # Create and show the browser window
# window = BrowserWindow()
# window.show()
# #window.showFullScreen()
# 
# # Execute the application's main loop
# sys.exit(app.exec_())


   

#====================================== Working ===================================
# import tkinter as tk
# import subprocess
# import pyautogui
# import time
# 
# class WebBrowserApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Simple Web Browser")
# 
#         # Create an Entry widget for URL input
#         self.url_entry = tk.Entry(root,text="https://app.newfrontiersystems.com/home/videocalling?siteId=3021", width=40)
#         self.url_entry.pack(padx=10, pady=10)
# 
#         # Create a "Go" button to navigate to the entered URL
#         self.go_button = tk.Button(root, text="Go", command=self.navigate)
#         self.go_button.pack()
# 
#     def navigate(self):
#         url = self.url_entry.get()
#         try:
#             # Open Chromium with the specified URL
#             subprocess.run(["chromium-browser", url])
# 
#             # Delay to allow the browser to open
#             time.sleep(0.5)  # Adjust time as needed
# 
#             # Simulate pressing F11 to enter full-screen mode
#             pyautogui.press('f11')
#         except Exception as e:
#             print(f"Error: {e}")
# 
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = WebBrowserApp(root)
#     root.mainloop()
#==========================================================================================
# import tkinter as tk
# import subprocess
# import pyautogui
# import time
# 
# class WebBrowserApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Simple Web Browser")
# 
#         # Automatically navigate to the specified URL when the app starts
#         self.navigate()
# 
#     def navigate(self):
#         url = "https://truckovernight.azurewebsites.net/home/videocalling?siteId=3021"  # The URL to open
#         try:
#             # Open Chromium with the specified URL
#             subprocess.run(["chromium-browser", url])
# 
#             # Delay to allow the browser to open
#             time.sleep(0.5)  # Adjust time as needed
# 
#             # Simulate pressing F11 to enter full-screen mode
#             pyautogui.press('f11')
#         except Exception as e:
#             print(f"Error: {e}")
# 
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = WebBrowserApp(root)
#     root.mainloop()



#====================================================Working ======================================
# import tkinter as tk
# import subprocess
# import pyautogui
# import time
# 
# 
# def navigate():
#     url = "https://truckovernight.azurewebsites.net/home/videocalling?siteId=3021"  # The URL to open
#     try:
#         # Open Chromium with the specified URL
#         subprocess.run(["chromium-browser", url])
# 
#         # Delay to allow the browser to open
#         time.sleep(1)  # Adjust time as needed
# 
#         # Simulate pressing F11 to enter full-screen mode
#         pyautogui.press('f11')
#     except Exception as e:
#         print(f"Error: {e}")
# 
# if __name__ == "__main__":
#     navigate()

#============================================================================================

# from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import Qt, QUrl
# import sys
# 
# class VideoCallPopup(QMainWindow):
#     def __init__(self):
#         super().__init__()
# 
#         self.setWindowTitle("Video Call")
#         self.browser = QWebEngineView()
#         
#         # ✅ Fix is here: wrap URL with QUrl()
#         self.browser.setUrl(QUrl("https://truckovernight.azurewebsites.net/home/videocalling?siteId=3021"))
# 
#         self.setCentralWidget(self.browser)
#         self.showFullScreen()
# 
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = VideoCallPopup()
#     sys.exit(app.exec_())



# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import QUrl, Qt
# 
# class VideoCallApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
# 
#         self.setWindowTitle("Video Calling")
#         self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)  # borderless
# 
#         # Web browser widget
#         self.browser = QWebEngineView()
#         self.browser.setUrl(QUrl("https://truckovernight.azurewebsites.net/home/videocalling?siteId=3021"))
# 
#         # Optional Close Button inside the window
#         close_button = QPushButton("Close Call")
#         close_button.clicked.connect(self.close)
# 
#         # Layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.browser)
#         layout.addWidget(close_button)
# 
#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)
# 
#         self.showFullScreen()  # Make it fullscreen automatically
# 
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = VideoCallApp()
#     sys.exit(app.exec_())


# import subprocess
# import pyautogui
# import time
# import os
# 
# def navigate():
#     global browser_process
#     url = "https://truckovernight.azurewebsites.net/home/videocalling?siteId=3021"
# 
#     try:
#         # Open Chromium in kiosk (fullscreen) mode with a custom close button
#         browser_process = subprocess.Popen([
#             "chromium-browser", 
#             "--kiosk",  # Fullscreen mode
#             "--disable-pinch",  # Disable zooming
#             "--disable-infobars",  # Hide extra UI
#             "--noerrdialogs",  # Suppress error dialogs
#             "--disable-session-crashed-bubble",  # No session restore popup
#             "--app=" + url  # Open the specific URL
#         ])
# 
#         # Delay to allow the browser to load
#         time.sleep(2)  
# 
#         # Simulate pressing F11 (in case --kiosk does not work)
#         pyautogui.press('f11')
# 
#         # Inject JavaScript to add a "Close Call" button
#         add_close_button()
# 
#     except Exception as e:
#         print(f"Error: {e}")
# 
# def add_close_button():
#     """Injects JavaScript to add a 'Close Call' button to the webpage."""
#     js_code = """
#         var btn = document.createElement('button');
#         btn.innerHTML = 'Close Call';
#         btn.style.position = 'fixed';
#         btn.style.bottom = '20px';
#         btn.style.left = '50%';
#         btn.style.transform = 'translateX(-50%)';
#         btn.style.padding = '10px 20px';
#         btn.style.background = 'red';
#         btn.style.color = 'white';
#         btn.style.fontSize = '16px';
#         btn.style.border = 'none';
#         btn.style.cursor = 'pointer';
#         document.body.appendChild(btn);
#         btn.onclick = function() {
#             window.close();
#         };
#     """
#     
#     # Run JavaScript in Chromium's console
#     subprocess.run(["chromium-browser", "--remote-debugging-port=9222", "--headless", f"javascript:{js_code}"])
# 
# if __name__ == "__main__":
#     navigate()
#url = "https://truckovernight.azurewebsites.net/home/videocalling?siteId=3021"
#======================================================================= OR ===========================================
import subprocess
import time
import pyautogui
import os

def navigate():
    global browser_process
    siteid = '3bvKIliIuKY='
    url = f"https://truckovernight.azurewebsites.net/home/videocalling?siteId={siteid}"
   # url = "https://truckovernight.azurewebsites.net/home/videocalling?siteId=3021"
    

    try:
        # Open Chromium in kiosk mode
        browser_process = subprocess.Popen([
            "chromium-browser", 
            "--kiosk", 
            "--disable-pinch", 
            "--disable-infobars", 
            "--noerrdialogs", 
            "--disable-session-crashed-bubble",
            "--remote-debugging-port=9222",  # Enable DevTools Protocol
            url
        ])

        # Delay to allow browser to load
        time.sleep(5)  

        # Simulate pressing F11 in case --kiosk fails
        pyautogui.press('f11')

        # Inject JavaScript
        add_close_button()

    except Exception as e:
        print(f"Error: {e}")

def add_close_button():
    """Injects JavaScript to add a 'Close Call' button that closes Chromium."""
    js_code = """
        var btn = document.createElement('button');
        btn.innerHTML = 'Close Call';
        btn.style.position = 'fixed';
        btn.style.bottom = '20px';
        btn.style.left = '50%';
        btn.style.transform = 'translateX(-50%)';
        btn.style.padding = '10px 20px';
        btn.style.background = 'red';
        btn.style.color = 'white';
        btn.style.fontSize = '16px';
        btn.style.border = 'none';
        btn.style.cursor = 'pointer';
        document.body.appendChild(btn);
        
        btn.onclick = function() {
            window.close();
        };
    """

    # Start a local server to listen for the close request
    subprocess.Popen(["python3", "-m", "http.server", "5000"])
    
    # Inject JavaScript using DevTools Protocol
    subprocess.run([
        "chromium-browser",
        "--remote-debugging-port=9222",
        "--headless",
        f"javascript:{js_code}"
    ])

if __name__ == "__main__":
    navigate()

