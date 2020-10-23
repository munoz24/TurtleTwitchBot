import tkinter as tk
from tkinter import *
from tkinter import messagebox
import threading
import socket
import time


def isint(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def send_message(message):
    botSock = socket.socket()
    botSock.connect((HOST, PORT))
    botSock.send(bytes("PASS " + BOTPASS + "\r\n", "UTF-8"))
    botSock.send(bytes("NICK " + BOTNICK + "\r\n", "UTF-8"))
    botSock.send(bytes("JOIN #" + NICK + "\r\n", "UTF-8"))

    botSock.send(bytes("PRIVMSG #" + NICK + " :" + message + "\r\n", "UTF-8"))


def bot(fr):
    global turtleflag
    global turtle1
    global turtle2
    global turtle3
    global turtle4
    global turtle5
    global turtle6

    def addtoturle(user, turtleselected):

        allturtles = turtle1 + turtle2 + turtle3 + turtle4 + turtle5 + turtle6
        for person in allturtles:
            if person == user:
                return

        if turtleselected == 1:
            turtle1.append(user)
        elif turtleselected == 2:
            turtle2.append(user)
        elif turtleselected == 3:
            turtle3.append(user)
        elif turtleselected == 4:
            turtle4.append(user)
        elif turtleselected == 5:
            turtle5.append(user)
        elif turtleselected == 6:
            turtle6.append(user)

    print("Bot is Running")

    sock = socket.socket()
    sock.connect((HOST, PORT))

    sock.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
    sock.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
    sock.send(bytes("JOIN #" + NICK + "\r\n", "UTF-8"))

    while True:
        line = str(sock.recv(1024))
        if "End of /NAMES list" in line:
            break

    while True:
        for line in str(sock.recv(1024)).split('\\r\\n'):

            parts = line.split(':')
            if len(parts) < 3:
                continue

            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                msg = parts[2][:len(parts[2])]

            count = 0
            for _ in fr.winfo_children():
                count += 1

            notbutton = 0
            for widget in fr.winfo_children():
                if count > 15:
                    if notbutton > 5:
                        widget.destroy()
                notbutton += 1

            usernamesplit = parts[1].split("!")
            username = usernamesplit[0]

            print(username + ": " + msg)

            command = msg
            command = command.split(" ")

            if command[0].lower() == "!turtle" and turtleflag:
                if len(command) == 2:
                    if isint(command[1]):
                        addtoturle(username, int(command[1]))
                        label = tk.Label(fr, text=username + ":" + msg, fg="black")
                        label.pack()


def clearSubs():
    global turtle1
    global turtle2
    global turtle3
    global turtle4
    global turtle5
    global turtle6

    MsgBox = tk.messagebox.askquestion('Deleting All Entries',
                                       'Are you sure you want to delete all turtle entries?',
                                       icon='warning')
    if MsgBox == 'yes':
        turtle1 = []
        turtle2 = []
        turtle3 = []
        turtle4 = []
        turtle5 = []
        turtle6 = []
        tk.messagebox.showinfo('Return', 'Entries were deleted')
    else:
        tk.messagebox.showinfo('Return', 'Entries were not deleted')


def startbot(button, button2, f):
    messagebox.showinfo(title="Information", message="Close main window to terminate bot")
    button2.config(state=ACTIVE)
    botThread = threading.Thread(target=bot, args=(f,))
    botThread.daemon = True
    botThread.start()
    button.config(text="Bot is Running")
    button.config(state=DISABLED)


def setflag(button, button2, entry, flag):
    global turtleflag

    button.config(state=DISABLED)
    button2.config(state=ACTIVE)
    if flag:
        # Sending Prompt
        send_message("It's time for a turtle race! Voting is open - type !turtle #, replacing # with a number 1-6. For "
                     "example, !turtle 3. Entries will not be accepted after the start of the race. Good luck!")
    else:
        # Sending Prompt
        send_message("Turtle race entries are closed - no more bets! Good luck!")
    if not flag:
        entry.config(state='normal')
    turtleflag = flag


def loopturtle(turtlelist, num):
    if len(turtlelist) is not 0:
        count = 0
        limit = 25
        currentindex = 0
        total = len(turtlelist)
        names = ""

        while total > currentindex:
            names = names + ", " + str(turtlelist[currentindex])
            currentindex += 1
            count += 1
            if count >= limit:
                send_message(names[1:])
                names = ""
                count = 0

        if names is not " ":
            send_message(names[1:])
    else:
        losersMSG1 = "/me No one picked Turtle "
        losersMSG2 = ". Better luck next time!"
        losers = losersMSG1 + str(num) + losersMSG2
        time.sleep(1)
        send_message(losers)


def sendtwitch(msg, selectedturtle):
    if isint(selectedturtle):
        if 7 > int(selectedturtle) > 0:
            send_message(msg)
            time.sleep(1)
            if int(selectedturtle) == 1:
                turtlethread = threading.Thread(target=loopturtle, args=(turtle1, 1,))
                turtlethread.start()
            elif int(selectedturtle) == 2:
                turtlethread = threading.Thread(target=loopturtle, args=(turtle2, 2,))
                turtlethread.start()
            elif int(selectedturtle) == 3:
                turtlethread = threading.Thread(target=loopturtle, args=(turtle3, 3,))
                turtlethread.start()
            elif int(selectedturtle) == 4:
                turtlethread = threading.Thread(target=loopturtle, args=(turtle4, 4,))
                turtlethread.start()
            elif int(selectedturtle) == 5:
                turtlethread = threading.Thread(target=loopturtle, args=(turtle5, 5,))
                turtlethread.start()
            elif int(selectedturtle) == 6:
                turtlethread = threading.Thread(target=loopturtle, args=(turtle6, 6,))
                turtlethread.start()


HOST = "irc.twitch.tv"
PORT = 6667
NICK = ""  # Twitch Channel
PASS = ""  # Get this from https://twitchapps.com/tmi/
# "oauth:(followed by a long string")

BOTNICK = ""  # Name of Bot (Second Twitch Account)
BOTPASS = ""  # Same format as the other PASS

turtleflag = False

turtle1 = []
turtle2 = []
turtle3 = []
turtle4 = []
turtle5 = []
turtle6 = []


def main():
    root = tk.Tk()
    root.title("Turtle Twitch Bot")
    root.iconbitmap('turtlebot_icon.ico')

    canvas = tk.Canvas(root, height=500, width=300, bg="#1fc522")
    canvas.pack(fill=BOTH, expand=YES)

    frame = tk.Frame(root, bg="#033104")
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    runBot = tk.Button(frame, text="Run Bot", padx=40, pady=20, fg="white", bg="black",
                       command=lambda: startbot(button=runBot, button2=allowturtle, f=frame))
    runBot.pack()

    allowturtle = tk.Button(frame, text="Enable Users to Select Turtle", fg="white", bg="black", state=DISABLED,
                            command=lambda: setflag(button=allowturtle, button2=disableturtle, entry=winningTurtle,
                                                    flag=True))
    allowturtle.pack()

    disableturtle = tk.Button(frame, text="Disable Users to Select Turtle", fg="white", bg="black", state=DISABLED,
                              command=lambda: setflag(button=disableturtle, button2=allowturtle, entry=winningTurtle,
                                                      flag=False))
    disableturtle.pack()

    Label(frame, text="Enter Winning Turtle Below", fg="white", bg="black").pack()
    winningTurtle = tk.Entry(frame, state='disabled')
    winningTurtle.pack()

    b = tk.Button(frame, text="Submit", fg="white", bg="black",
                  command=lambda: sendtwitch(msg="/me Turtle " + str(winningTurtle.get()) +
                                                 " has won the race. Here are your winners!",
                                             selectedturtle=winningTurtle.get()))
    b.pack()

    clearturtles = tk.Button(frame, text="Clear all Turtle Submission", fg="white", bg="black",
                             command=lambda: clearSubs())
    clearturtles.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
