import re
import MujSoubor
import MujXLS
import vlc

##media = vlc.MediaPlayer("test.avi")
##media.set_time(2000)
##media.play()
##media.pause()


def Coding(Text):
    try:
        result = Text.decode('utf-8')
    except:
        result = Text.decode('cp1250').encode('utf-8')
    return result

yy = MujXLS.XLS()
xx = MujSoubor.Soubor()
regex = re.compile(b"[A-Za-z]+")
reSentences = re.compile(b"[A-Z][A-Za-z ,\r\n]+")
reTime = re.compile(b"[0-9]+:[0-9]+:[0-9 ,]+--> [0-9]+:[0-9]+:[0-9 ,]+")
reTimeStartStop = re.compile(b"[0-9]+:[0-9]+:[0-9 ,]+")

Languages = xx.ListDir("\\subtitles\\*")
xlsSheet = {}
for Language in Languages:

    Files = xx.ListFiles("\\subtitles\\" + Language + "\\*.*",True)
    for i in Files:
        titulky = Coding(xx.Nahraj(i))
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
            TimeStart = b"00"
            TimeStop = b"00"
            
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
yy.SaveXLS("subtitleDict.xlsx",xlsSheet)

