import tkinter as tk

from tkinter import ttk
import tkinter.font as tkFont
import time, vlc
import MujXLS
import MyFile
import random
import os
import time

class VideoPlayer:
    def __init__(self,source):
        self.player = vlc.MediaPlayer(source)
        # play the video
        self.player.play()
        time.sleep(1)
##        self.player.set_time(Time)
        self.player.pause()
        # wait time
##        time.sleep(Duration)
        self.offset = 0
        self.scale = 1
        self.player.pause()
    def PlayPart(self, Time, Duration):
        self.player.set_time(Time)
        self.player.pause()
        # wait time
        time.sleep(Duration)
        self.player.pause()

    def convertToMsec(self,Time):
        TimeList = Time.split(":")
        gain = 1000
        TimeMsec = 0
        for i in reversed(TimeList):
            TimeMsec += float(i.replace(",","."))*gain
            gain *= 60
        TimeMsec *= self.scale
        return int(TimeMsec)
    def PlayPartStr(self, Start, End):
        
        Time = self.convertToMsec(Start)
        EndTime = self.convertToMsec(End)
        Time += self.offset
        EndTime += self.offset
        self.player.set_time(Time)
        self.player.play()
        print(Time,EndTime)
        while self.player.get_time() < EndTime:
            time.sleep(0.1)
        time.sleep(1.5)
        self.player.pause()

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size

        xx = MyFile.FileSystem()
        Files = xx.listFile("avi")
        self.FilmFile = Files[0]
        if self.FilmFile.count("readMe.txt")>0:
            self.FilmFile = ""
            if len(Files)>1:
                self.FilmFile = Files[1]
            else:
                print("Film file is missing.")
        
        width=1400
        height=200
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.wordListBox=tk.Listbox(root)
        self.wordListBox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.wordListBox["font"] = ft
        self.wordListBox["fg"] = "#333333"
        self.wordListBox["justify"] = "center"
        self.wordListBox.place(x=10,y=20,width=157,height=30)

        NEXT=tk.Button(root)
        NEXT["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        NEXT["font"] = ft
        NEXT["fg"] = "#000000"
        NEXT["justify"] = "center"
        NEXT["text"] = "Next"
        NEXT.place(x=10,y=60,width=70,height=30)
        NEXT["command"] = self.NEXT_command

        showEnglish=tk.Button(root)
        showEnglish["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        showEnglish["font"] = ft
        showEnglish["fg"] = "#000000"
        showEnglish["justify"] = "center"
        showEnglish["text"] = "Show English"
        showEnglish.place(x=10,y=100,width=158,height=30)
        showEnglish["command"] = self.showEnglish_command

        showCzech=tk.Button(root)
        showCzech["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        showCzech["font"] = ft
        showCzech["fg"] = "#000000"
        showCzech["justify"] = "center"
        showCzech["text"] = "Show Czech"
        showCzech.place(x=10,y=140,width=157,height=30)
        showCzech["command"] = self.showCzech_command

        self.SentenceOrg=tk.Listbox(root)
        self.SentenceOrg["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.SentenceOrg["font"] = ft
        self.SentenceOrg["fg"] = "#333333"
        self.SentenceOrg["justify"] = "center"
        self.SentenceOrg.place(x=180,y=20,width=580,height=147)

        self.SentenceTran=tk.Listbox(root)
        self.SentenceTran["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.SentenceTran["font"] = ft
        self.SentenceTran["fg"] = "#333333"
        self.SentenceTran["justify"] = "center"
        self.SentenceTran.place(x=800,y=20,width=580,height=147)

        REPEAT=tk.Button(root)
        REPEAT["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        REPEAT["font"] = ft
        REPEAT["fg"] = "#000000"
        REPEAT["justify"] = "center"
        REPEAT["text"] = "Repeat"
        REPEAT.place(x=90,y=60,width=77,height=30)
        REPEAT["command"] = self.REPEAT_command

        if self.FilmFile != "":
            self.Player = VideoPlayer("\\avi\\Man.On.The.Moon.mp4")

        self.MySubtitle = subtitles()

    def NEXT_command(self):
        self.MySubtitle.randomWord()
        self.wordListBox.delete(0)
        self.wordListBox.insert(0,self.MySubtitle.Word)
        self.wordListBox.see(0)
        self.SentenceOrg.delete(0)
        self.SentenceOrg.insert(0,self.MySubtitle.OriginalSentence)
        self.SentenceOrg.see(0)
        self.SentenceTran.delete(0)
        self.SentenceTran.insert(0,self.MySubtitle.TranslatedSentence)
        self.SentenceTran.see(0)
        if self.FilmFile != "":
           self.Player.PlayPartStr(self.MySubtitle.Start,self.MySubtitle.Stop)

    def showEnglish_command(self):
        print("showEnglish")


    def showCzech_command(self):
        print("showCzech")


    def REPEAT_command(self):
        if self.FilmFile != "":
            self.Player.PlayPartStr(self.MySubtitle.Start,self.MySubtitle.Stop)

class subtitles:
    def __init__(self):
        self.__yy = MujXLS.XLS()
        self.Subtitles = self.__yy.ReadXLS("subtitleDict.xlsx")
        self.Words = {}
        self.Sentences = {}
        self.Times = []
        self.Start = ''
        self.Stop = ''
        self.Language = 'EN'
        self.enSentenceList = set()
        self.czSentenceList = set()
        
        Languages = ['CZ','EN']
        self.__initLanguages(Languages)

        for Language in Languages:
            for word in self.Subtitles[Language+"_words"]["Data"]:
                self.Words[Language][word["Word"]]=word
            for sentence in self.Subtitles[Language+"_sentence"]["Data"]:
                self.Sentences[Language][sentence["Id"]]=sentence
        self.randomWord()

    def __initLanguages(self,Languages):
        for Language in Languages:
            self.Words[Language] = {}
            self.Sentences[Language] = {}
            
    def randomWord(self,Language = 'EN'):
        self.Times = []
        self.Word = random.choice(list(self.Words[self.Language].keys()))
        WordId = int(self.Words[self.Language][self.Word]['sentence'][1:-1].split(",")[0])
        WordSentence = self.Sentences[self.Language][WordId]['Text']

        self.Times.append(self.Sentences[self.Language][WordId]['Start'])
        self.Times.append(self.Sentences[self.Language][WordId]['Stop'])

        WordCzId = self.Sentences[Language][WordId]['CZ_Id']
        self.TranslatedSentence = "Nejsou CZ titulky."
        self.OriginalSentence = "No original sentence."

        WordIds = ""

        if WordCzId != 0:
            self.TranslatedSentence = ""
            for czItem in WordCzId.split(','):
                if int(czItem) > 0:
                    self.TranslatedSentence += self.Sentences["CZ"][int(czItem)]["Text"]
                    WordIds += self.Sentences["CZ"][int(czItem)][Language + '_Id'].replace('\n',' ')+','
                    self.Times.append(self.Sentences["CZ"][int(czItem)]['Start'])
                    self.Times.append(self.Sentences["CZ"][int(czItem)]['Stop'])

        if len(WordIds) > 0:
            self.OriginalSentence = ""
            for WordItem in WordIds.split(','):
                if WordItem != "":
                    self.OriginalSentence += self.Sentences[Language][int(WordItem)]["Text"] +" "
                    self.Times.append(self.Sentences[Language][int(WordItem)]['Start'])
                    self.Times.append(self.Sentences[Language][int(WordItem)]['Stop'])
                    
        self.Times.sort()
        self.Start = self.Times[0]
        self.Stop = self.Times[-1]
                
            
        
        
        
        
        
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
