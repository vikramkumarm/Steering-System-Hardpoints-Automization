import tkinter as tk
from PIL import Image, ImageTk
import hashlib
from tkinter import messagebox
import socket
import sys
import os
from trial_core import hp
import pyotp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def hash_password(password):
    # Hash the password using SHA-256 (you can choose a different algorithm)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

stored_password = hash_password("12")
#stored_password = '8209dd894ea44de67e23c558d5b25ae801f998e2396fbbf3e05afad69e40ef8d'

def check_password(entered_password):
    # Hash the entered password for comparison
    entered_password_hash = hash_password(entered_password)
    return entered_password_hash == stored_password


def send_otp_email(email, otp):
    sender_email = "1357rc01@gmail.com"  # Replace with your Gmail email address
    app_password = "hpfd wieg bkgw mgki"  # Replace with your generated App Password
    subject = "OTP for Script Authentication"
    body = f"Your OTP for script authentication is: {otp}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, email, message.as_string())





def main_gui():
    def assign_inputdata():
        global Ax, Ay, Az, AA_prime, col_ang_range, col_len_range, Ex, Ey, Ez, centre_distance, pinion_length_range, offset_angle_range, mount_angle_range, max_UJ1_ang, max_UJ2, max_diff_in_UJ_angles
        Ax   = float(d1x.get())
        Ay   = float(d1y.get())
        Az   = float(d1z.get())
        
        AA_prime = float(d12.get())
        
        col_ang_max  = float(d2_max.get())
        col_ang_min  = float(d2_min.get())
        
        col_len_max  = float(d3_max.get())
        col_len_min  = float(d3_min.get())
        
        Ex   = float(d4x.get())
        Ey   = float(d4y.get())
        Ez   = float(d4z.get())
        
        centre_distance = float(d5.get())
        pinion_length_min = float(d6_min.get())
        pinion_length_max = float(d6_max.get())
        
        offset_angle_min = float(d7_min.get())
        offset_angle_max = float(d7_max.get())
        
        mount_angle_min  = float(d8_min.get())
        mount_angle_max  = float(d8_max.get())
        
        max_UJ1_ang = float(d9.get())
        max_UJ2_ang = float(d10.get())    
        max_diff_in_UJ_angles = float(d11.get())
        ss_col_angle       = float(d13.get())
        ss_col_length      = float(d14.get())
        ss_pinion_length   = float(d15.get())
        ss_offset_angle    = float(d16.get())
        ss_mount_angle     = float(d17.get())
        
        
        A = [Ax, Ay,Az]
        E = [Ex, Ey, Ez]
        col_ang_range = [col_ang_min, col_ang_max]
        col_len_range = [col_len_min, col_len_max]
        pinion_length_range = [ pinion_length_min, pinion_length_max ]
        offset_angle_range  = [offset_angle_min , offset_angle_max]
        mount_angle_range  = [mount_angle_min,  mount_angle_max]
        
        def clear_text():
            text_o = "                                                                                                           "
            text_none = text_o + "\n" + text_o
            tk.Label(data, text=text_none, fg='black', justify='center').grid(row=17, column=2, columnspan=3)

        clear_text()
        valid_ind = hp(A,AA_prime, col_ang_range , col_len_range, E, centre_distance, pinion_length_range, offset_angle_range,
                       mount_angle_range, max_UJ1_ang, max_UJ2_ang, max_diff_in_UJ_angles, ss_col_angle, ss_col_length,  ss_pinion_length, ss_offset_angle, ss_mount_angle )
             
        def display_ans(valid_ind):
            if valid_ind == 0:
                text = "There is no possible data with the constraints provided"
                tk.Label(data, text=text , fg = 'black', anchor='center').grid(row=17, column=2, columnspan = 3)
            elif valid_ind > 0:
                text1 = str(valid_ind) + "    possible options generated with the given constriants\nGenerated data is printed to 'Book1.xlsx"
                tk.Label(data, text=text1 , fg = 'black', anchor='center').grid(row=17 , column=2, columnspan = 3)
  
            else:
                pass
        display_ans(valid_ind)
      
    
    # # Function to load and display an image
    # def load_image(image_path, row, column, rowspan):
    #     image = Image.open(image_path)
    #     photo = ImageTk.PhotoImage(image)
    
    #     label = tk.Label(data, image=photo)
    #     label.image = photo  # Keep a reference to the image to prevent garbage collection
    #     label.grid(row=row, column=column, rowspan=rowspan, padx=20)
    #from PIL import Image, ImageTk

    def load_image(image_path, row, column, rowspan):
        image = Image.open(image_path)
        
        # Resize the image if needed
        # image = image.resize((width, height), Image.ANTIALIAS)
        
        tk_image = ImageTk.PhotoImage(image)
        
        label = tk.Label(data, image=tk_image)
        label.image = tk_image  # Keep a reference to the image to prevent garbage collection
        label.grid(row=row, column=column, rowspan=rowspan, padx=20)
        
        ###################input data  ##########################################
     
    tk.Label(data, text="Input the parameters below" , font = ('calibre',15,'normal') , fg = 'blue').grid(row=0 , pady = 4)
    tk.Label(data, text="A - point").grid(row=1)
    tk.Label(data, text="AA' length").grid(row=2)
    tk.Label(data, text="Column Angle").grid(row=3)
    tk.Label(data, text=" Column Length").grid(row=4)
    tk.Label(data, text=" E - point").grid(row=5)
    tk.Label(data, text=" Center distance ").grid(row=6)
    tk.Label(data, text=" Pinion length ").grid(row=7)
    tk.Label(data, text=" Offset Angle ").grid(row=8)
    tk.Label(data, text=" Mounting Angle ").grid(row=9)
    tk.Label(data, text=" Maximum UJ1 Angle ").grid(row=10)
    tk.Label(data, text=" Maximum UJ2 Angle ").grid(row=11)
    tk.Label(data, text=" UJ  angle diff. Threshold ").grid(row=12)
    
    tk.Label(data, text=' \n ' , fg = 'black').grid(row=17, column=2, columnspan = 3)
    tk.Label(data, text='' , fg = 'black').grid(row=18, column=2, columnspan = 3)
    
      
    def on_entry_click(event, entry, text):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.config(fg='black', justify='left')  # Change text color and font size
    def on_entry_leave(event, entry, text):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg='grey',  justify='left')  # Change text color and font size
    
    
    
    # Function to create and configure an entry with placeholder
    def create_entry(parent, text, row, column):
        if text == "Step size":
            text = ""
            entry = tk.Entry(parent,  fg='black', font = ('calibre',8,'italic'), justify='center', width =11)
            entry.insert(0, text)
            entry.bind("<FocusIn>", lambda event, e=entry: on_entry_click(event, e, text))
            entry.bind("<FocusOut>", lambda event, e=entry: on_entry_leave(event, e, text))
            entry.grid(row=row, column=column)
        else:
            entry = tk.Entry(parent,  fg='grey', justify='left')
            entry.insert(0, text)
            entry.bind("<FocusIn>", lambda event, e=entry: on_entry_click(event, e, text))
            entry.bind("<FocusOut>", lambda event, e=entry: on_entry_leave(event, e, text))
            entry.grid(row=row, column=column)
            
        return entry
    
    
    # Create entry widgets with smaller font size for the placeholder text
    d1x = create_entry(data, "x", 1, 1)
    d1y = create_entry(data, "y", 1, 2)
    d1z = create_entry(data, "z", 1, 3)
    d12 = create_entry(data, " ", 2, 1)
    d2_min = create_entry(data, "min", 3, 1)
    d2_max = create_entry(data, "max", 3, 2)
    d3_min = create_entry(data, "min", 4, 1)
    d3_max = create_entry(data, "max", 4, 2)
    d4x = create_entry(data, "x", 5, 1)
    d4y = create_entry(data, "y", 5, 2)
    d4z = create_entry(data, "z", 5, 3)
    d5 = create_entry(data, "", 6, 1)
    d6_min = create_entry(data, "min", 7, 1)
    d6_max = create_entry(data, "max", 7, 2)
    d7_min = create_entry(data, "min", 8, 1)
    d7_max = create_entry(data, "max", 8, 2)
    d8_min = create_entry(data, "min", 9, 1)
    d8_max = create_entry(data, "max", 9, 2)
    d9 = create_entry(data, "", 10, 1)
    d10 = create_entry(data, "", 11, 1)
    d11 = create_entry(data, "", 12, 1)

    frame1 = tk.Frame(data)
    frame1.grid(row=3, column=3)
    d13 = create_entry(frame1, "Step size", 0,1)
    d13.insert(0, 0.5)
    tk.Label(frame1, text="Step size",  font=('calibre', 8, 'italic')).grid(row=0, column = 0)
    
    frame2 = tk.Frame(data)
    frame2.grid(row=4, column=3)
    d14 = create_entry(frame2, "Step size", 0,1)
    d14.insert(0, 2)
    tk.Label(frame2, text="Step size", font=('calibre', 8, 'italic')).grid(row=0, column = 0)
    
    frame3 = tk.Frame(data)
    frame3.grid(row=7, column=3)
    d15 = create_entry(frame3, "Step size", 0,1)
    d15.insert(0, 1)
    tk.Label(frame3, text="Step size", font=('calibre', 8, 'italic')).grid(row=0, column = 0)
    
    frame4 = tk.Frame(data)
    frame4.grid(row=8, column=3)
    d16 = create_entry(frame4, "Step size", 0,1)
    d16.insert(0, 0.05)
    tk.Label(frame4, text="Step size", font=('calibre', 8, 'italic')).grid(row=0, column = 0)
    
    frame5 = tk.Frame(data)
    frame5.grid(row=9, column=3)
    d17 = create_entry(frame5, "Step size", 0,1)
    d17.insert(0, 0.1)
    tk.Label(frame5, text="Step size", font=('calibre', 8, 'italic')).grid(row=0, column = 0)
    ######################################################################################################################################################
    
    for label in [d1x, d1y, d1z, d12, d2_max, d2_min, d3_max, d3_min, d4x, d4y, d4z, d5, d6_min, d6_max, d7_min, d7_max, d8_min, d8_max, d9, d10, d11]:
        label.grid(padx=2, pady = 3)
    
    
    # Load and display the image
    current_directory = os.getcwd()
    file_name = 'Picture3.png'
    image_path = os.path.join(current_directory, file_name)
    load_image(image_path, row=1, column=5, rowspan=13)
    
    tk.Button(data, text='Submit', command=assign_inputdata ,font = ('calibre',12,'bold') ,bg = 'bisque4' , fg = 'black').grid(row=16, column=3, pady = 60)
    
    # Start the main loop
    data.mainloop()
    

def is_valid_ip():
    # Define a list of allowed IP addresses
    allowed_ips = ["172.20.74.81", "172.20.73.210"]

    # Get the system's IP address
    current_ip = socket.gethostbyname(socket.gethostname())

    # Check if the IP is in the whitelist
    return current_ip in allowed_ips

if not is_valid_ip():
    print("Unauthorized access. Exiting.")
    sys.exit()
    

# Create the main GUI window
data = tk.Tk()
data.title('Steering system HP')

# Label and entry for password
password_label = tk.Label(data, text="Password:")
password_label.grid(row=2, column=2, padx=(60, 1))
password_entry = tk.Entry(data, show="*")
password_entry.grid(row=2, column=3)
tk.Label(data, text="                  ").grid(row=1, column=4)

otp_label = tk.Label(data, text="Enter OTP:")
otp_label.grid(row=4, column=2, padx=(60, 1))
otp_entry = tk.Entry(data)
otp_entry.grid(row=4, column=3)

otp_button = tk.Button(data, text='Send OTP', command=lambda: send_otp_email("vikrammuthkani@gmail.com", totp.now()))
otp_button.grid(row=3, column=3, pady=20)



secret_key = pyotp.random_base32()
totp = pyotp.TOTP(secret_key)  # Use the generated secret key

def on_submit():
    entered_password = password_entry.get()
    entered_otp = otp_entry.get()

    if check_password(entered_password) and totp.verify(entered_otp):
        password_label.grid_forget()
        password_entry.grid_forget()
        otp_label.grid_forget()
        otp_entry.grid_forget()
        otp_button.grid_forget()
        submit_button.grid_forget()
        main_gui()
    else:
        messagebox.showerror("Error", "Incorrect password or OTP")
        data.destroy()
# Create the main GUI window

submit_button = tk.Button(data, text='Submit', command=on_submit, font=('calibre', 12, 'bold'), bg='bisque4', fg='black')
submit_button.grid(row=5, column=3, pady=60)

data.mainloop()





