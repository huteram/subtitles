# importing time and vlc
import time, vlc
import MujXLS
import random

# method to play video

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
        
     
# call the video method
yy = MujXLS.XLS()
Dict = yy.ReadXLS("subtitleDict.xlsx")
Words = {}
Sentences = {}
Languages = ['CZ','EN']
init = False
for Language in Languages:
    if not(init):
        Words[Language] = {}
        Sentences[Language] = {}
    for word in Dict[Language+"_words"]["Data"]:
        Words[Language][word["Word"]]=word
    for sentence in Dict[Language+"_sentence"]["Data"]:
        Sentences[Language][sentence["Id"]]=sentence


inputSet = ""

Player = VideoPlayer("\\avi\\Man.On.The.Moon.mp4")



while inputSet != "0":
    Times = []
    enSentenceList = set()
    czSentenceList = set()
    enW = random.choice(list(Words["EN"].keys()))
    print("en word: ",enW)
    enId = int(Words["EN"][enW]['sentence'][1:-1].split(",")[0])    
    enSentence = Sentences["EN"][enId]['Text']
    Times.append(Sentences["EN"][enId]['Start'])
    Times.append(Sentences["EN"][enId]['Stop'])
    czId = Sentences["EN"][enId]['CZ_Id']
    czSentence = "Nejsou CZ titulky."
    enId = ""
    
    if czId != '0':
        czSentence = ""
        for czItem in czId.split(','):
            czSentence += Sentences["CZ"][int(czItem)]["Text"]
            enId += Sentences["CZ"][int(czItem)]['EN_Id']+','
            Times.append(Sentences["CZ"][int(czItem)]['Start'])
            Times.append(Sentences["CZ"][int(czItem)]['Stop'])
    if len(enId) > 0:
        enSentence = ""
        for enItem in enId.split(','):
            if enItem != "":
                enSentence += Sentences["EN"][int(enItem)]["Text"] +" "
                Times.append(Sentences["EN"][int(enItem)]['Start'])
                Times.append(Sentences["EN"][int(enItem)]['Stop'])
            
            
    Times.sort()
    print ("CZ subtitle: ",czSentence)
    print (Times[0]," --> ",Times[-1])
    print ("\r\n\r\n")
    print ("EN subtitle: ",enSentence)
    print ("\r\n\r\n\r\n\r\n")
    Player.PlayPartStr(Times[0],Times[-1])
    
    inputSet = input()
    while inputSet == "":
        Player.PlayPartStr(Times[0],Times[-1])
        inputSet = input()
        
    
    
    

