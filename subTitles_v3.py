import re
import MyFile
import MujXLS
import vlc

##media = vlc.MediaPlayer("test.avi")
##media.set_time(2000)
##media.play()
##media.pause()

def convertToSec(Time):
    TimeList = Time.split(b":")
    gain = 1
    TimeMsec = 0
    for i in reversed(TimeList):
        TimeMsec += float(i.replace(b",",b"."))*gain
        gain *= 60
    return int(TimeMsec)


def Coding(Text):
    try:
        result = Text.decode('utf-8').encode('utf-8')
    except:
        result = Text.decode('cp1250').encode('utf-8')
    return result

yy = MujXLS.XLS()
xx = MyFile.FileSystem()

regex = re.compile("[A-Za-záčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ]+".encode('utf-8'))
reSentences = re.compile("[A-ZáčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ][A-Za-záčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ ,\r\n]+".encode('utf-8'))
reTime = re.compile(b"[0-9]+:[0-9]+:[0-9 ,]+--> [0-9]+:[0-9]+:[0-9 ,]+")
reTimeStartStop = re.compile(b"[0-9]+:[0-9]+:[0-9 ,]+")

Languages = xx.ListDir("\\subtitles\\*")
xlsSheet = {}
TimeSentence = {}
for Language in Languages:
    TimeSentence[Language] = {}

    Files = xx.listFile("\\subtitles\\" + Language + "\\")
    for i in Files:
        titulky = Coding(xx.readFile(i))
    counter = 1
    Words = {}
    Sentence = {}
    aSentence = {}

    auxSentence = 1
    auxWords = 1


    for i in re.split(b"\r\n[0-9]+\r\n",titulky):
        counter +=1
        Time = reTimeStartStop.findall(i)
        if len(Time) > 2:
            print ("too much times: ")
            print (Time)
            print ("from: ")
            print (i)
            TimeStart = "00"
            TimeStop = "00"
            
        else:
            TimeStart = Time[0]
            TimeStop = Time[1]
            Text = i.split(TimeStop)[-1][2:-2]
            if (Text.lower() not in aSentence):
                auxSentence += 1
                for Word in regex.findall(Text):
                    if (Word.lower() in Words):
                        if (auxSentence not in Words[Word.lower()]):
                            Words[Word.lower()].append(auxSentence)
                    else:
                        Words[Word.lower()] = [auxSentence]
                Sentence[auxSentence] = {}
                Sentence[auxSentence]["Id"] = auxSentence
                Sentence[auxSentence]["Text"] = Text
                Sentence[auxSentence]["Start"] = TimeStart
                Sentence[auxSentence]["Stop"] = TimeStop
                aSentence[Text.lower()] = auxSentence
                TimeRange = []
                if convertToSec(TimeStart) == convertToSec(TimeStop):
                    TimeRange.append(convertToSec(TimeStart))
                else:
                    for TimeItem in range(convertToSec(TimeStart),convertToSec(TimeStop)):
                        TimeRange.append(TimeItem)
                Sentence[auxSentence]["Range"] = str(TimeRange)[1:-1]
            
        
    DataSentence = []
    dataWords = []
    for i in Sentence:
        DataSentence.append(Sentence[i])
    for i in Words:
        aux = {}
        aux["Word"] = i
        aux["count"] = str(len(Words[i]))
        aux["sentence"] = str(Words[i])
        dataWords.append(aux)
    WordLanguage = Language + "_words"
    xlsSheet[WordLanguage] = {}
    xlsSheet[WordLanguage]["Data"] = dataWords
    xlsSheet[WordLanguage]["Head"] = {"Word":1,"count":2,"sentence":3}
    SentenceLanguage = Language + "_sentence"
    xlsSheet[SentenceLanguage] = {}
    xlsSheet[SentenceLanguage]["Data"] = DataSentence
    xlsSheet[SentenceLanguage]["Head"] = {"Id":1,"Text":2,"Start":3,"Stop":4}

SentenceConnection = {}
for Language in Languages:
    
    SentenceConnection[Language] = {}
    SentenceLanguage = Language + "_sentence"
    for i in xlsSheet[SentenceLanguage]["Data"]:
        for TimeSec in i["Range"].split(','):
            SentenceConnection[Language][int(TimeSec)] = i["Id"]

for Language in Languages:
    newData = []
    SentenceLanguage = Language + "_sentence"
    for i in xlsSheet[SentenceLanguage]["Data"]:
        for TimeSec in i["Range"].split(','):
            TimeSec = int(TimeSec)
            for LanguageOther in Languages:
                if LanguageOther != Language:
                    if TimeSec in SentenceConnection[LanguageOther]:
                        Id =  SentenceConnection[LanguageOther][TimeSec]
                    else:
                        Id = 0
                    IdName = LanguageOther+"_Id"
                    if IdName in i:
                        if (Id not in i[IdName]) and Id>0:
                            if i[IdName][0] == 0:
                                i[IdName] = [Id]
                            else:
                                i[IdName].append(Id)
                    else:
                        i[IdName] = [Id]
        i[IdName]=str(i[IdName])[1:-1]
        aux = i.pop("Range")
        newData.append(i)
    xlsSheet[SentenceLanguage]["Data"] = newData
    
    
                    
                
                
        
    

            
yy.SaveXLS("subtitleDict.xlsx",xlsSheet)

