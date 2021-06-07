from tkinter import *
import pymysql
from tkinter import ttk
import paho.mqtt.client as mqtt
import random

# Connecting Database
db = pymysql.connect(
    host='localhost',
    user='aman',
    password='aman0611',
    db='sunoye',
    charset='utf8mb4')
cursor = db.cursor()


# Main Frame Window
tk = Tk()
tk.title("SunOye 2.0")

# Variables
room_no = StringVar()
password = StringVar()
username = StringVar()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    ttk.Label(message_window, text=msg.payload.decode("utf-8"), font=("Courier", 10)).pack(anchor='w')





# create the client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# enable TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

# set username and password
client.username_pw_set("perfecto", "Aman0611")

# connect to HiveMQ Cloud on port 8883
client.connect("ae6c8cfe6e654a4ebf55c86ec9b1e196.s1.eu.hivemq.cloud", 8883)

# publish "Hello" to the topic "my/test/topic"
client.loop_start()






# Destroy A Window Function
def destroyed(a):
    a.destroy()


# Room Already Exist
def no_exist():
    global failed_message
    failed_message = Toplevel(login_screen)
    failed_message.title("Invalid Message")
    Label(failed_message, text="Room Doesn't exist", fg='red').pack()
    Label(failed_message, text="").pack()
    Button(failed_message, text="Ok", relief="groove", height=1, width=10, command=lambda a=failed_message: destroyed(a)).pack()
    failed_message.grab_set()
    global room_no
    global password
    global username

    room_no.set("")
    password.set("")
    username.set("")


# Failed to login Function
def failed():
    global failed_message
    failed_message = Toplevel(login_screen)
    failed_message.title("Invalid Message")
    Label(failed_message, text="Invalid Room Number or Passcode", fg='red').pack()
    Label(failed_message, text="").pack()
    Button(failed_message, text="Ok", relief="groove", height=1, width=10, command=lambda a=failed_message: destroyed(a)).pack()
    failed_message.grab_set()
    global room_no
    global password
    global username

    room_no.set("")
    password.set("")
    username.set("")


# Leave the chat function
def leave():
    global tk
    sql = "update roomtable set members = members - 1 where room_no = %s"
    cursor.connection.ping()
    cursor.execute(sql,[(room_no.get())])
    db.commit()
    sql = "select *  from roomtable  where room_no = %s"
    cursor.connection.ping()
    cursor.execute(sql,[(room_no.get())])
    db.commit()
    results = cursor.fetchall()

    for rows in results:
        if rows[3] == 0:
            sql = "update roomtable set active = 'n' where room_no = %s"
            cursor.connection.ping()
            cursor.execute(sql,[(room_no.get())])
            db.commit()
    tk.destroy()
    client.loop_stop()
    db.close()


# Login Window
def login_win():
    # tk.withdraw()
    global opt_window
    opt_window.destroy()
    global login_screen
    login_screen = Toplevel(tk)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Enter the Room Credentials").pack()
    Label(login_screen, text="").pack()

    global room_no
    global password
    global username

    Label(login_screen, text="Room Number").pack()
    room = Entry(login_screen, textvariable=room_no)
    room.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Passcode").pack()
    pass_entry = Entry(login_screen, textvariable=password, show="*")
    pass_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Enter Your Name").pack()
    user_entry = Entry(login_screen, textvariable=username)
    user_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Enter", width=10, height=1, command=login_verify).pack()
    Label(login_screen, text="").pack()


# Login Verification
def login_verify():
    rno = room_no.get()
    passw = password.get()
    cursor.connection.ping()
    sql = "select * from roomtable where room_no = %s and passcode = %s"
    cursor.execute(sql,[(rno),(passw)])
    results = cursor.fetchall()
    if results:
        for i in results:
            if(i[2]=='n'):
                no_exist()
                break
            logged()
            global login_screen
            destroyed(login_screen)
            strr = "Welcome to Room " + str(room_no.get()) + ".\tUsername: " + str(username.get()) + "\tPasscode: " + str(password.get())
            Label(message_window, text=strr, font=("Arial", 12)).pack(anchor='w')
            break
    else:
        failed()


# To Subscribe to a topic
def subs(rno):
    # Subscribe to topic
    global topic_dir
    topic_dir = "sunoye/room/" + str(rno)
    client.subscribe(topic_dir)
    print("Subscribed")


# Successful Logged In
def logged():
    subs(room_no.get())
    # Increase Member count for room_no
    cursor.connection.ping()
    sql = "update roomtable set members = members + 1 where room_no = %s"
    cursor.execute(sql,[(room_no.get())])
    db.commit()
    # Set Active for room_no
    sql = "update roomtable set active = 'y' where room_no = %s"
    cursor.connection.ping()
    cursor.execute(sql, [(room_no.get())])
    db.commit()
    tk.deiconify()


# Message Sending Function
def send(event=None):
    global msg
    global mesg
    mesg = str(username.get()) + "->>" + str(msg.get())
    canvas.yview_moveto('1.0')
    msg.set("")
    global topic_dir
    client.publish(topic_dir, mesg)


# Retrace Option Window
def go_home():
    global full_warn
    global username
    username.set("")
    full_warn.destroy()
    option_window()


# Room Full
def room_new():
    global room_no
    global password
    sql = "select count(*) from roomtable"
    cursor.connection.ping()
    cursor.execute(sql)
    print("ok")
    (i,) = cursor.fetchone()
    passw = random.randint(10000,99999)
    print(i)
    print(passw)
    rno = 'r' + str(i)
    print(rno)
    sql = "insert into roomtable values(%s, %s, 'y', 1)"
    cursor.execute(sql,[(rno),(passw)])
    db.commit()
    subs(rno)
    room_no.set(rno)
    password.set(passw)
    strr = "Welcome to Room " + str(room_no.get()) + ".\tUsername: " + str(username.get()) + "\tPasscode: " + str(password.get())
    Label(message_window, text=strr, font=("Arial", 12)).pack(anchor='w')
    tk.deiconify()


# New Room Function
def new_room():
    global create_window
    create_window.destroy()

    sql = "select * from roomtable where active = 'n'"

    global room_no
    global password

    cursor.connection.ping()
    cursor.execute(sql)
    results = cursor.fetchone()
    if results:
        room_no.set(results[0])
        password.set(results[1])
        # subs(room_no.get())
        strr = "Welcome to Room " + str(room_no.get()) + ".\tUsername: " + str(username.get()) + "\tPasscode: " + str(password.get())
        Label(message_window, text=strr, font=("Arial", 12)).pack(anchor='w')
        logged()
        tk.deiconify()
    else:
        room_new()


# Create New Room Window
def create_room():
    global opt_window
    opt_window.destroy()
    global create_window
    create_window = Toplevel(tk)
    create_window.geometry("300x250")

    global username

    Label(create_window, text="").pack()
    Label(create_window, text="Create Room").pack()
    Label(create_window, text="").pack()
    Label(create_window, text="Username").pack()
    user_entry = Entry(create_window, textvariable=username)
    user_entry.pack()
    Label(create_window, text="").pack()
    Button(create_window, text="Create Room", command=new_room).pack()


# First Window (New Room/Existing Room)
def option_window():
    tk.withdraw()
    global opt_window
    opt_window = Toplevel(tk)
    opt_window.title("Option Window")
    opt_window.geometry("300x150")
    Label(opt_window, text="").pack()
    Button(opt_window, text="Join an Existing Room", width=20, height=1, command=login_win).pack()

    Label(opt_window, text="").pack()
    Button(opt_window, text="Create a New Room", width=20, height=1, command=create_room).pack()





# Call Option Window First
option_window()



# Message Variable
msg = StringVar()

container = ttk.Frame(tk)  # Container Frame
canvas = Canvas(container, width=650, height=600)

# Scrollbar
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

# Message Window
message_window = ttk.Frame(canvas)
message_window.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Creating Message Window in Canvas
canvas.create_window((0, 0), window=message_window, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)




# Packing Canvas Components
container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Message Entry Field and Send Button and Leave Button
msg_field = Entry(tk, textvariable=msg, width=90)
msg_field.bind("<Return>", send)
msg_field.pack(side="left", padx=2)
send_btn = Button(tk, text="Send", command=send, width=7)
send_btn.pack(side="left")
exit_btn = Button(tk, text="Leave", command=leave, width=7, bg='red', fg='white')
exit_btn.pack(padx=2)



# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
tk.protocol("WM_DELETE_WINDOW", leave)
tk.mainloop()
