import datetime as dt
import speech_recognition as sr
import wikipedia as wp
import pyttsx3 as tts
import webbrowser as wb
import os
from scipy.io.wavfile import write
import smtplib
from playsound import playsound
import sounddevice as sd
from opl import openplay
from searchipc import searching

# voice
engine = tts.init("sapi5")
voices = engine.getProperty("voices")
print(voices[1].id)
engine.setProperty("voice", voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# greeting
def wishme():
    h = int(dt.datetime.now().hour)
    if 0 <= h <= 12:
        speak("good morning")
    elif 12 < h <= 16:
        speak("good after noon")
    elif 16 < h <= 24:
        speak("good evening")
    speak("hello sir, how can i help you")


# email sender
# noinspection PyShadowingNames
def sendEmail(to, content):

    f = open(os.path.join(cdpath, "email.txt"), "r")
    f2 = open(os.path.join(cdpath, "emailre.txt"), 'r')
    # noinspection PyShadowingNames
    l = f.read().split()
    l2 = f2.readlines()
    for i in l2:
        if to in i:
            maili = i.split()[1]
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(l[0], l[1])
    # noinspection PyUnboundLocalVariable
    server.sendmail(l[0], maili, content)
    server.close()
    f.close()
    f2.close()


# command
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 1000
        r.pause_threshold = 1
        audio = r.listen(source)
    # noinspection PyShadowingNames
    try:
        print("Recognizing...")
        # noinspection PyShadowingNames
        query = r.recognize_google(audio, language="en-in")
        print(f"User Said : {query}\n")
    except Exception as e:
        print(e)
        print("Say it again!")
        return "None"
    return query


# recording playing
def recplay(rec):
    s = rec + ".wav"
    fs = 44100  # Sample rate
    print('For how time should i record')
    speak('For how time should i record')
    # noinspection PyBroadException
    try:
        t1 = takecommand().split()

        if t1[1] == "second" or t1[1] == "seconds" or t1[1] == "sec":
            t = int(t1[0])
        if t1[1] == "minute" or t1[1] == "minutes" or t1[1] == "min":
            t = int(t1[0]) * 60
        if t1[1] == "hour" or t1[1] == "hours":
            t = int(t1[0]) * 60 * 60
    except:
        print("recoding started for 30sec")
        t = 30
    # noinspection PyUnboundLocalVariable
    seconds = t  # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(s, fs, myrecording)  # Save as WAV
    speak("recording completed")


# noinspection PyShadowingNames
def playrec(name):
    s = name + ".wav"
    playsound(s)


c = 0

if __name__ == '__main__':
    # logic
    c = 0
    response = os.popen("wmic logicaldisk get caption")
    list1 = []

    for line in response.readlines():
        line = line.strip("\n")
        line = line.strip("\r")
        line = line.strip(" ")
        if line == "Caption" or line == "":
            continue
        list1.append(line)
        print(list1)

    list1.remove("C:")
    list1.append("C:/")
    print(list1)
    cdpath = os.getcwd()
    print(cdpath)
    '''lf = []
    lp = []
    for drive in list1:
        for (root, dirs, files) in os.walk(drive, topdown=True):
            for file in files:
                if "saturday.py" in file.lower():
                    lf.append(file)
                    lp.append(root)
                    print(file, root)

            del root
            del dirs
            del files
        print(len(lf))
        for fint in range(len(lf)):
            pa = os.path.join(lp[fint], lf[fint])
            delf = open(pa, "r")
            xtu = len(delf.readlines())
            delf.close()
            print(xtu)
            if xtu != 338:
                os.remove(pa)
                print("done")'''

    wishme()
    condition = True
    while condition:
        query = takecommand().lower()

        # code for wikipedia
        if "wikipedia" in query:
            print("Searching...")
            query = query.replace("wikipedia", "")
            results = wp.summary(query, sentences=3)
            speak("According to Wikipedia")
            speak(results)

        # code for site
        elif "open google" in query:
            wb.open("www.google.com")

        elif "open youtube" in query:
            wb.open("www.youtube.com")

        elif "open stackoverflow" in query:
            wb.open("www.stackoverflow.com")

        # time or date
        elif 'the time' in query:
            strTime = dt.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif "today's date" in query or 'today date' in query or 'date today' in query:
            strDate = dt.datetime.now().strftime("%d %m %Y")
            speak(f"Sir, the date is {strDate}")

        # installing
        elif "install python module" in query:
            mlist = os.listdir("pipinstaller")
            print("Tell the module name to install")
            speak("Tell the module name to install")
            pmname = takecommand().lower()

            os.system('cmd /k "pip install {}"'.format(pmname))

        # code for file opening
        elif "open " in query:
            sqlist = ""
            dlist = query.split()
            print(dlist)
            lnth = len(dlist)
            if dlist[lnth - 1] == "lnk" or dlist[lnth - 1] == "exe":
                print(dlist[lnth - 3])
                if dlist[lnth - 2] == "dot":
                    dlist[lnth - 3] = dlist[lnth - 3] + "." + dlist[lnth - 1]
                dlist.pop(0)
                dlist.pop(-1)
                dlist.pop(-1)
                print(dlist)
                sqlist = " ".join(dlist)
                print(sqlist)
                openplay(sqlist, list1)
            else:
                openplay(query[5:], list1)
        # code for searching inside your pc
        elif "search " in query or "find " in query:
            cl = query.split()
            cl.pop(0)
            query = " ".join(cl)
            l = searching(query, list1)
            searchedlist = l[0]
            searchedlistpath = l[1]
            c = 1
            speak("sir there are " + str(len(searchedlist)) + " searched result")
            print("sir there are " + str(len(searchedlist)) + " searched result")
            if len(searchedlist) > 0:
                for sl in searchedlist:
                    print(c, sl, end="\n")
                    speak(sl)
                    c = c + 1
                con1 = 1
                while con1:
                    print("which file you want to select")
                    speak("which file you want to select")
                    option = takecommand().lower()
                    print(option)
                    if option == "nothing":
                        # noinspection PyStatementEffect
                        con1 = 0
                        break

                    # noinspection PyBroadException
                    try:
                        option = int(option)
                        if 1 <= option < c:
                            con1 = 0
                        else:
                            print("Please select required numeric option")
                            speak("Please select required numeric option")
                            pass
                    except:
                        pass

                # noinspection PyUnboundLocalVariable
                if option != "nothing":
                    speak("sir you can perform certain operation on file or folder")
                    print("1. delete file or folder")
                    speak("1. delete file or folder")
                    print("2. open file or folder")
                    speak("2. open file or folder")
                    print("3. nothing")
                    speak("3. nothing")

                    con2 = 1
                    while con2:
                        speak("what yo want to do ")
                        query2 = takecommand().lower()
                        # noinspection PyBroadException
                        try:
                            query2 = int(query2[0])
                            if query2 == 1:
                                con2 = 0
                                # noinspection PyUnboundLocalVariable
                                os.remove(os.path.join(searchedlistpath[option - 1], searchedlist[option - 1]))
                            elif query2 == 2:
                                con2 = 0
                                os.startfile(os.path.join(searchedlistpath[option - 1], searchedlist[option - 1]))
                            elif query2 == 3:
                                con2 = 0
                        except:
                            if "delete" in query2:
                                con2 = 0
                                os.remove(os.path.join(searchedlistpath[option - 1], searchedlist[option - 1]))
                            elif "open" in query2:
                                con2 = 0
                                os.startfile(os.path.join(searchedlistpath[option - 1], searchedlist[option - 1]))
                            elif "nothing" in query2:
                                con2 = 0

        # sending mail
        elif 'send email to' in query or 'send mail to' in query:
            l = query.split()

            try:
                speak("What should I say?")
                content = takecommand()
                to = l[3]
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry sir. I am not able to send this email")

        # recording
        elif "start recording" in query:
            if query.split()[-1] != "recording" and query.split()[-1] != "as":
                recplay(query.split()[-1])
            else:
                volist = list(filter(lambda x: "voice" in x, os.listdir(cdpath)))
                name = "voice" + str(len(volist))
                recplay(name)
        elif "play recording" in query:
            playrec(query.split()[-1])
        elif "play last recording" in query:
            volist = list(filter(lambda x: "voice" in x, os.listdir(cdpath)))
            name = "voice" + str(len(volist) - 1)
            playrec(name)

        # shutdown or restart pc
        elif "shutdown" in query:
            print("shutdown")
            os.system('shutdown /s /t 1')
        elif "restart" in query:
            os.system('shutdown /r /t 1')

        # exiting
        elif "saturday exit" in query or "good night" in query:
            if "saturday exit" in query:
                print("Bye Sir")
                speak("Bye Sir")
            else:
                print("Good Night Sir")
                speak("Good Night Sir")
            condition = False
