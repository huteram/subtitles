import re
import MyPkg.MyFile as MyFile
import MyPkg.MujXLS as MujXLS

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


## init 
yy = MujXLS.XLS()
xx = MyFile.FileSystem()

# regex - expretion for all words.
# reSentences - all sentence.
# reTime - Time row.
# reTimeStartStop - find times in time row.
regex = re.compile("[A-Za-záčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ]+".encode('utf-8'))
reSentences = re.compile("[A-ZáčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ][A-Za-záčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ ,\r\n]+".encode('utf-8'))
reTime = re.compile(b"[0-9]+:[0-9]+:[0-9 ,]+--> [0-9]+:[0-9]+:[0-9 ,]+")
reTimeStartStop = re.compile(b"[0-9]+:[0-9]+:[0-9 ,]+")
knownWords = {}

if (xx.FileExists("subtitles\\knownWords.txt")):
    knownWordsTxt = xx.readFile("subtitles\\knownWords.txt")

    for i in knownWordsTxt.split(b"\r\n"):
        knownWords[i.upper()] = 1

    



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
