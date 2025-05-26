import subprocess
import tkinter as tk

def open_voice_popup():
    subprocess.Popen([
        'chromium-browser',
        '--new-window',
        '--window-size=1000,600',
        '--enable-media-stream',
        '--noerrdialogs',
        '--disable-infobars',
        '--app=https://truckovernight.azurewebsites.net/home/voiceasst'
    ])

open_voice_popup()
# root = tk.Tk()
# root.title("AI Assistant")
# root.geometry("300x120")
# 
# btn = tk.Button(root, text="Open Voice Assistant", command=open_voice_popup, font=("Arial", 14))
# btn.pack(pady=40)

#root.mainloop()
