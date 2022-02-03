import tkinter as tk

from tkinter import ttk
import tkinter.font as tkFont
import time, vlc
import MujXLS
import MyFile
import random
import os
import time

class htmlCreator:
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
        
    def convertToSec(self,Time):
        TimeList = Time.split(":")
        gain = 1
        TimeMsec = 0
        for i in reversed(TimeList):
            TimeMsec += float(i.replace(",","."))*gain
            gain *= 60
        return float(TimeMsec)


    def htmlJsonExport(self,Language = 'EN'):
        jsonList = []
        textJson = b"\r\n"
        WordList = list(self.Words[self.Language].keys())
        self.wordCounter=str(len(WordList)-1).encode()
        for Word in WordList:

            self.Times = []
            self.Word = Word
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
            aux = {}
            aux["word"] = Word
            aux[Language+"_sentence"] = self.OriginalSentence
            aux["CZ_sentence"] = self.TranslatedSentence
            aux["Start"] = self.convertToSec(self.Start)
            aux["Stop"] = self.convertToSec(self.Stop)
            aux["Duration"] = 1000*((aux["Stop"] - aux["Start"]) + 0.5)
            textJson += str(aux).encode().replace(b'\n',b' ').replace(b'\r',b'').replace(b'\\n',b' ')
            textJson += b",\r\n"
            jsonList.append(aux)
        
        textJson = textJson.replace(b"'word'",b"word")
        orgL = "'" + Language+"_sentence'"
        newL = Language+"_sentence"
        textJson = textJson.replace(orgL.encode(),newL.encode())
        textJson = textJson.replace(b"'CZ_sentence'",b"CZ_sentence")
        textJson = textJson.replace(b"'Start'",b"Start")
        textJson = textJson.replace(b"'Stop'",b"Stop")
        textJson = textJson.replace(b"'Duration'",b"Duration")
        textJson = textJson.replace(b": word",b": 'word'")
        textJson = textJson.replace(b": Start",b": 'Start'")
        textJson = textJson.replace(b": Stop",b": 'Stop'")
        textJson = textJson.replace(b": Duration",b": 'Duration'")
        return jsonList,textJson
            
            
                
            
        
        
        
        
        
        
        

if __name__ == "__main__":
    html = htmlCreator()
    k,T = html.htmlJsonExport()
##    T = T.replace(b'\n',b' ').replace(b'\r',b'')
    xx = MyFile.FileSystem()
    htmlTemp = xx.readFile("Template\\Temp.html")
    htmlTemp = htmlTemp.replace(b"XXXjson",T).replace(b"XXXlength",html.wordCounter)
    xx.SaveFile(htmlTemp,"html\\subtitleRandom.html")
    
