import re
import MujSoubor
import MujXLS
import vlc

##media = vlc.MediaPlayer("test.avi")
##media.set_time(2000)
##media.play()
##media.pause()

yy = MujXLS.XLS()
xx = MujSoubor.Soubor()
regex = re.compile(b"[A-Za-z]+")
reSentences = re.compile(b"[A-Z][A-Za-z ,\r\n]+[\.\!\?]")

reTime = re.compile(b"\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d .*?\r\n")

Files = xx.ListFiles("source\*.*",True)

for i in Files:
    titulky = xx.Nahraj(i)

titulky = titulky.replace(b"\r\n\r\n",b"XXXrn").replace(b"\r\n",b" ").replace(b"XXXrn",b"\r\n")
AllWords = regex.findall(titulky)
AllSentences = reSentences.findall(titulky)


a = reTime.findall(titulky)
WordsList = {}

def AddWord(List, Word,Sentence ):
    Item = Word.lower()
    if Item in List:
        Aux = List[Item]
        NewSentence = True
        for s in range(Aux["Sentence Counter"]):
            Counter = str(s+1)
            if Sentence == Aux["Sentence "+Counter]:
                NewSentence = False
                break
        if NewSentence:
            Aux["Sentence Counter"] += 1          
            Aux["Sentence "+str(Aux["Sentence Counter"])] = Sentence
            List[Item] = Aux
    else:
        Aux = {}
        Aux["Word"] = Word
        Aux["Sentence Counter"] = 1
        Aux["Sentence 1"] = Sentence
        List[Item] = Aux
    return List



for Sentence in AllSentences:
    Words = regex.findall(Sentence)
    for Word in Words:
        WordsList = AddWord(WordsList,Word,Sentence)

dictSheetData = []
for i in WordsList:
    dictSheetData.append(WordsList[i])

xlsSheet = yy.NewSheet("dict")
xlsSheet["dict"]["Data"] = dictSheetData
xlsSheet["dict"]["Head"] = {"Sentence Counter":1}
yy.SaveXLS("subtitleDict.xlsx",xlsSheet)



