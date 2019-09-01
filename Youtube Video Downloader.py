from __future__ import unicode_literals
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import re
import ffmpeg
#from ffprobe import FFProbe
import threading
import youtube_dl

class MainApplication:
    def __init__(self,master):
        #  Tk() - To create the main window
        self.master = master
        self.folder_path = None
        self.URL = ''

        # geometry() - To set the size of the window
        self.master.geometry("600x470+300+100")

        # resizable() - To make the window of constant size
        self.master.resizable(width=0,height=0)

        # To change the icon of the main window
        img = PhotoImage(file=r'myicon.png')
        img2 = img.subsample(3,3)
        self.master.tk.call('wm', 'iconphoto', self.master._w, img)   

        self.style = ttk.Style()
        self.style.configure("TButton")

        # ttk.Frame() - To create a frame that contains entrybox , search button
        self.topframe=ttk.Frame(self.master,relief=GROOVE,height=110,width=580)#,text="Type the URL")
        self.topframe.place(x=10,y=30)

        #Label() - To create a label on topframe
        self.label1=Label(self.topframe,text='Enter the URL of the YouTube video ', font=("Agency FB", 20))
        self.label1.place(x=110,y=5)


        # ttk.entry = To get the URL of the video through entry box
        self.Link=ttk.Entry(self.topframe,width=80)
        self.Link.place(x=40,y=50)

        # Entry error label if user inputs incorrect
        self.youtubeEntryError = Label(self.master, text="",font=("Comic Sans MS", 11))
        self.youtubeEntryError.place(x=150,y=103)

        # Asking where to save file label
        self.youtubeFileLocationLabel = ttk.Label(self.master, text="Please choose folder where to save file : ", font=("Agency FB", 20))
        self.youtubeFileLocationLabel.place(x=25,y=150)

        # Button to open directory
        self.youtubeFileLocationEntry = ttk.Button(self.master, text="Select Folder", command=self.SelectFolder)
        self.youtubeFileLocationEntry.place(x=370,y=158)

        # Entry label if user don`t choose directory
        # SelectFolder func
        self.fileLocationLabelError = Label(self.master, text="", font=(11))
        self.fileLocationLabelError.place(x=40,y=185)


		# What to download MP3 or MP4 label
        self.youtubeChooseLabel = ttk.Label(self.master, text="Please choose Type of File : ", font=("Agency FB", 20))
        self.youtubeChooseLabel.place(x=25,y=210)

        # RadioButton with two choices: MP3 or MP4
        # downloadChoices = [("Song MP3", 1), ("Video MP4", 2)]
                # RadioButton with two choices: MP3 or MP4
        downloadChoices = [("Video", 1), ("Audio", 2)]
        self.ChoicesVar = IntVar()
        self.ChoicesVar.set(1)
        i=1
        for text, mode in downloadChoices:
            if(i==1):
                self.youtubeChoices = ttk.Radiobutton(self.master, text=text, variable=self.ChoicesVar, value=mode).place(x=260,y=220)
                i=i+1
            else:
                self.youtubeChoices = ttk.Radiobutton(self.master, text=text, variable=self.ChoicesVar, value=mode).place(x=360,y=220)
        
        # ttk.Button -  search button to search the video
        self.download_btn=ttk.Button(self.master,text="Download",command=self.checkYoutubeLink)#,command=self.CheckURL)
        self.download_btn.place(x=250,y=270)

        self.downloading_status = Label(self.master, text="", font=(10))
        self.downloading_status.place(x=200,y=295)
 
        self.middleframe= ttk.Frame(self.master,relief=GROOVE,height=120,width=580)
        self.middleframe.place(x=10,y=330)

        #To set the image in the middle frame
        self.label2 = ttk.Label(self.middleframe,image=img2)
        self.label2.place(x=12,y=10)

        self.label3 = ttk.Label(self.middleframe,text="Download YouTube content for free to watch offline: videos,playlist.   Download heavy 4k, Full HD,HD Files fast & easily. Video Downloader will show you size before saving it.",wraplength=400)
        self.label3.place(x=130,y=30)

        # To Hold the Window until not close
        self.master.mainloop()

    #To get the Url Link from EntryBox
    def geturl(self):
        return self.Link.get()

    # To Select Folder to Save File
    def SelectFolder(self):
      self.FolderName =  filedialog.askdirectory()  # select folder to save file
      self.folder_path = self.FolderName
      
      if(len(self.FolderName) > 1):
        self.fileLocationLabelError.config(text=self.FolderName, fg="green")
        return True 
      else:
        self.fileLocationLabelError.config(text="Please choose folder!", fg="red")

    # To Check Whether URL is Valid
    def checkYoutubeLink(self):
        matchYoutubeLink = re.match('^https://www.youtube.com/.*', self.Link.get())
        self.URL= self.geturl()
        if(self.URL == ''):
            self.youtubeEntryError.config(text="Please Enter Video URL", fg="red")
        elif(not matchYoutubeLink):
            self.youtubeEntryError.config(text="Please Enter valid Youtube URL", fg="red")
        elif(not self.folder_path):
            self.fileLocationLabelError.config(text="Please choose folder!", fg="red")
        elif(matchYoutubeLink and self.folder_path):
            self.Download()

    #To Download Video
    def Download(self):
        threading.Thread(target=self.DownloadFile).start()

    # To download File
    def DownloadFile(self):
        try:
            URL = self.URL
            PATH = self.folder_path
            ydl_opts = {}
            os.chdir(PATH)
            check = False
            if(self.ChoicesVar.get()==1):
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    self.downloading_status.config(text="file is downloading...", fg="green")
                    ydl.download([URL])    
                    self.downloading_status.config(text="file is downloaded", fg="green")
                    check = true
            else:
                ydl_opts = { 
                'format': 'bestaudio/best', 
                'postprocessors': [{ 
                    'key': 'FFmpegExtractAudio', 
                    'preferredcodec': 'mp3',  
                    'preferredquality': '320',   # selected mp3 and 320
                }],
            }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    self.downloading_status.config(text="file is downloading...", fg="green")
                    check = True
                    ydl.download([URL]) 
                    self.downloading_status.config(text='File is downloaded!', fg="green")
                check = True
        except Exception:
            if check == True:
                self.downloading_status.config(text='File is downloaded!', fg="green")
            else:
                self.downloading_status.config(text='Sorry,something went wrong!', fg="red")
  
if __name__ == "__main__":
    root = Tk()
    root.title("YouTube Video Downloader")
    app = MainApplication(root)
