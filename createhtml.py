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


    def __initLanguages(self,Languages):
        for Language in Languages:
            self.Words[Language] = {}
            self.Sentences[Language] = {}
            
       
    def convertToSec(self,Time):
        TimeList = Time.split(":")
        gain = 1
        TimeMsec = 0
        for i in reversed(TimeList):
            TimeMsec += float(i.replace(",","."))*gain
            gain *= 60
        return float(TimeMsec)


    def htmlWordExport(self,Language = 'EN'):
        jsonWords = {}
        textJson = b"\r\n"
        WordList = self.Words[Language]
        SentenceList = self.Sentences[Language]
        a = 0

        for Word in WordList:
            Item = WordList[Word]
            jsonWords[WordList[Word]['Id']] = WordList[Word]
            a+=1
            if a>4:
                break

        textJson = str(jsonWords).encode().replace(b'\n',b' ').replace(b'\r',b'').replace(b'\\n',b' ')
        textJson += b",\r\n"

        for Key in list(Item.keys()):    
            K = Key.encode()    
            textJson = textJson.replace(b"'%s'" % K,b"%s" % K)

        return textJson



    def htmlSentenceExport(self,Language = 'EN'):
        jsonWords = {}
        textJson = b"\r\n"
        SentenceList = self.Sentences[Language]
        for Sentence in SentenceList:
            Item = SentenceList[Sentence]
            Item['Start'] = self.convertToSec(Item['Start'])
            Item['Stop'] = self.convertToSec(Item['Stop'])
            Item['Duration'] = 1000*(Item['Stop'] - Item["Start"])       
            jsonWords[Item['Id']] = Item     



        textJson = str(jsonList).encode().replace(b'\n',b' ').replace(b'\r',b'').replace(b'\\n',b' ')
        textJson += b",\r\n"
        
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
    T = html.htmlWordExport()
##    T = T.replace(b'\n',b' ').replace(b'\r',b'')
    xx = MyFile.FileSystem()
    htmlTemp = xx.readFile("Template\\Temp.html")
    htmlTemp = htmlTemp.replace(b"XXXjson",T)
    xx.SaveFile(htmlTemp,"html\\subtitleRandom.html")
    
