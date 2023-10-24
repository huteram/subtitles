import re
import MyPkg.MyFile as MyFile
import MyPkg.MujXLS as MujXLS
import requests
import bs4 as bs

def convertToSec(Time):
    TimeList = Time.split(b":")
    gain = 1
    TimeMsec = 0
    for i in reversed(TimeList):
        TimeMsec += float(i.replace(b",",b"."))*gain
        gain *= 60
    return int(TimeMsec)


def Coding(Text):
    if type(Text) is str:
        result = Text.encode('utf-8')
    else:
        try:
            result = Text.decode('utf-8').encode('utf-8')
        except:
            result = Text.decode('cp1250').encode('utf-8')
    return result

def readSourceHtml(Word):
    Url = 'https://slovnik.seznam.cz/preklad/cesky_anglicky/'.encode()
    try:
        Url += Word.encode()
    except:
        Url += Word
    Respons = requests.get(Url, allow_redirects=True)
    Soup = bs.BeautifulSoup(Respons.content, 'html.parser')
    return Soup

def findEnglishWord(Soup, Word):
    Translation = Soup.find_all(class_="TranslatePage-word--word")
    if len(Translation) > 0:
        result = Translation[0].text
    else:
        result = Word
    return result    

def findCzechEnglishTranslation(Soup):
    Translation = Soup.find_all(class_="Box-content-line")
    result = None
    if len(Translation) > 0:
        result = Translation[0].text
    else:
        Translation = Soup.find_all(class_="TranslatePage-results-short")
        if len(Translation)>0:
            Translation = Translation[0].findAll('a')
            newWord = Translation[0].text
            newSoup = readSourceHtml(newWord)
            result = findEnglishWord(newSoup, newWord)
        else:
            result = None
    return result


## init 
yy = MujXLS.XLS()
xx = MyFile.FileSystem()

# regex - expretion for all words.
# reSentences - all sentence.
# reTime - Time row.
# reTimeStartStop - find times in time row.
regex = re.compile('\w+')
reTime = re.compile(b"[0-9]+:[0-9]+:[0-9 ,]+--> [0-9]+:[0-9]+:[0-9 ,]+")
reTimeStartStop = re.compile(b"[0-9]+:[0-9]+:[0-9 ,]+")
knownWords = {}

if (xx.FileExists("subtitles\\knownWords.txt")):
    KnownWordData = yy.ReadXLS(xx.localDirectory(__file__) + '\\spreadSheets\\known.xlsx')
    for Language in KnownWordData:
        for Word in KnownWordData[Language]['Data']:
            knownWords[Coding(Word['Word'].upper())] = Language

    



# in subtitles directory there should be directory with the languages. 
# For example (\\subtitles\\CZ, \\subtitles\\EN) Czech and English. The directory names are used for distinguesh languages. 
Languages = xx.ListDir("\\subtitles\\*")
# set excel sheet.
xlsSheet = {}
TimeSentence = {}


for Language in Languages:

    
    TimeSentence[Language] = {}
    Files = xx.listFile("\\subtitles\\" + Language + "\\")
    for i in Files:
        titulky = Coding(xx.readFile(i))
    titulky = titulky.replace(b"\r\n",b"\n")

    counter = 1
    Words = {}
    Sentence = {}
    aSentence = {}
    idSentence = 1
    idWord = 1

    for Subtitle in re.split(b"\n[0-9]+\n",titulky):
        counter +=1
        Time = reTimeStartStop.findall(Subtitle)
        if len(Time) > 2:
            print ("too much times: ")
            print (Time)
            print ("from: ")
            print (Subtitle)
            TimeStart = "00"
            TimeStop = "00"
            
        else:
            TimeStart = Time[0]
            TimeStop = Time[1]
            Text = Subtitle.split(TimeStop)[-1][1:-1]
            if (Text.lower() not in aSentence):
                Sentence[idSentence] = {}
                Sentence[idSentence]["Words"] = []
                for Word in regex.findall(Text.decode('utf-8')):
                    if not(Word.upper() in knownWords or Word.isdigit()):
                        htmlWordSoup = readSourceHtml(Word)
                        translation = findCzechEnglishTranslation(htmlWordSoup)
                        if translation is None :
                            print (Word, " was not find in dictionary")
                        else:
                            if Language == 'EN':
                                Word = findEnglishWord(htmlWordSoup, Word)
                                WordCz = findCzechEnglishTranslation(htmlWordSoup)
                            
                            if (Word.lower() in Words):
                                # check if this sentence is already added to the word's sentence list.                        
                                if (idSentence not in Words[Word.lower()]["sentence"]):
                                    Words[Word.lower()]["sentence"].append(idSentence)
                                    Sentence[idSentence]["Words"].append(Words[Word.lower()]["Id"])
                            else:
                                Words[Word.lower()] = {}
                                Words[Word.lower()]["sentence"] = [idSentence]
                                Words[Word.lower()]["Id"] = idWord                        
                                Sentence[idSentence]["Words"].append(idWord)
                                if Language == 'EN':
                                    Words[Word.lower()]["Translation"] = WordCz

                                idWord += 1
                
                Sentence[idSentence]["Id"] = idSentence
                Sentence[idSentence]["Text"] = Text
                Sentence[idSentence]["Start"] = TimeStart
                Sentence[idSentence]["Stop"] = TimeStop
                aSentence[Text.lower()] = idSentence
                TimeRange = []
                if convertToSec(TimeStart) == convertToSec(TimeStop):
                    TimeRange.append(convertToSec(TimeStart))
                else:
                    for TimeItem in range(convertToSec(TimeStart),convertToSec(TimeStop)):
                        TimeRange.append(TimeItem)
                Sentence[idSentence]["Range"] = str(TimeRange)
                idSentence += 1
            
        
    DataSentence = []
    dataWords = []
    for i in Sentence:
        Sentence[i]["Words"] = str(Sentence[i]["Words"])
        DataSentence.append(Sentence[i])
    for i in Words:
        
        aux = {}
        aux["Word"] = i
        aux["Id"] = Words[i]["Id"]
        aux["count"] = str(len(Words[i]["sentence"]))
        aux["sentence"] = str(Words[i]["sentence"])
        dataWords.append(aux)
    WordLanguage = Language + "_words"
    xlsSheet[WordLanguage] = {}
    xlsSheet[WordLanguage]["Data"] = dataWords
    xlsSheet[WordLanguage]["Head"] = {"Id":1,"Word":2,"count":3,"sentence":4}
    SentenceLanguage = Language + "_sentence"
    xlsSheet[SentenceLanguage] = {}
    xlsSheet[SentenceLanguage]["Data"] = DataSentence
    xlsSheet[SentenceLanguage]["Head"] = {"Id":1,"Text":2,"Start":3,"Stop":4,"Words":5,}

SentenceConnection = {}
for Language in Languages:
    
    SentenceConnection[Language] = {}
    SentenceLanguage = Language + "_sentence"
    for i in xlsSheet[SentenceLanguage]["Data"]:
        TimeRange = i["Range"][1:-1].split(',')
        for TimeSec in TimeRange:
            SentenceConnection[Language][int(TimeSec)] = i["Id"]

for Language in Languages:
    newData = []
    SentenceLanguage = Language + "_sentence"
    for i in xlsSheet[SentenceLanguage]["Data"]:
        TimeRange = i["Range"][1:-1].split(',')
        for TimeSec in TimeRange:
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
        i[IdName]=str(i[IdName])
        aux = i.pop("Range")
        newData.append(i)
    xlsSheet[SentenceLanguage]["Data"] = newData
    
         
yy.SaveXLS("subtitleDict.xlsx",xlsSheet)

