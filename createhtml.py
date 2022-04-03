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
        self.xx = MyFile.FileSystem()
        self.optionTemp = self.xx.readFile("Template\\option.txt")
        

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
        textOption = b""
        WordList = self.Words[Language]
        SentenceList = self.Sentences[Language]
        a = 0

        for Word in WordList:
            Item = WordList[Word]
            jsonWords[WordList[Word]['Id']] = WordList[Word]
            WordId = str(WordList[Word]['Id']).encode()
            textOption += self.optionTemp.replace(b"XXXid",WordId)\
                                            .replace(b"XXXword",WordList[Word]['Word'].encode())\
                                            .replace(b"XXXrole",b"word")

            a+=1
            if a>4:
                break

        textJson = str(jsonWords).encode().replace(b'\n',b' ').replace(b'\r',b'').replace(b'\\n',b' ')
        textJson += b"\r\n"
        textJson = textJson.replace(b"'[" ,b"[").replace(b"]'" ,b"]") 
        for Key in list(Item.keys()):    
            K = Key.encode()    
            textJson = textJson.replace(b"'%s'" % K,b"%s" % K)

        return textJson,textOption



    def htmlSentenceExport(self,Language = 'EN'):
        jsonSentences = {}
        textJson = b"\r\n"
        textOption = b""
        SentenceList = self.Sentences[Language]
        a=0
        for Sentence in SentenceList:
            Item = SentenceList[Sentence]
            Item['Start'] = self.convertToSec(Item['Start'])
            Item['Stop'] = self.convertToSec(Item['Stop'])
            Item['Duration'] = 1000*(Item['Stop'] - Item["Start"])       
            jsonSentences[Item['Id']] = Item   
            WordId = str(Item['Id']).encode()
            textOption += self.optionTemp.replace(b"XXXid",WordId)\
                                            .replace(b"XXXword",Item['Text'].encode())\
                                            .replace(b"XXXrole",b"sentence")
            a+=1
            if a>4:
                break  



        textJson = str(jsonSentences).encode().replace(b'\n',b' ').replace(b'\r',b'').replace(b'\\n',b' ')
        textJson += b"\r\n"
        textJson = textJson.replace(b"'[" ,b"[").replace(b"]'" ,b"]") 
        for Key in list(Item.keys()):    
            K = Key.encode()    
            textJson = textJson.replace(b"'%s'" % K,b"%s" % K)        

        return textJson, textOption
            

        
        

if __name__ == "__main__":
    html = htmlCreator()
    enWords,wordOption = html.htmlWordExport()
    enSentences,sentenceOption = html.htmlSentenceExport()
    czWords,notUsed = html.htmlWordExport("CZ")
    czSentences,notUsed = html.htmlSentenceExport("CZ")

##    T = T.replace(b'\n',b' ').replace(b'\r',b'')
    xx = MyFile.FileSystem()
    htmlTemp = xx.readFile("Template\\Temp.html")
    htmlTemp = htmlTemp.replace(b"XXXenWords",enWords)
    htmlTemp = htmlTemp.replace(b"XXXenSentence",enSentences)
    htmlTemp = htmlTemp.replace(b"XXXczWords",czWords)
    htmlTemp = htmlTemp.replace(b"XXXczSentence",czSentences)
    htmlTemp = htmlTemp.replace(b"XXXoptionWord",wordOption)
    htmlTemp = htmlTemp.replace(b"XXXoptionSentence",sentenceOption)
    
    xx.SaveFile(htmlTemp,"html\\skeleton.html")
    
