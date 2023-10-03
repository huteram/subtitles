import re
import MyFile
import MujXLS
import vlc

##media = vlc.MediaPlayer("test.avi")
##media.set_time(2000)
##media.play()
##media.pause()




## init 
yy = MujXLS.XLS()
xx = MyFile.FileSystem()



File = "c:\\Users\\milanhutera\\OneDrive - Doosan\\Python\\subtitles\\auxPrograms\\wordsLevel.xlsx"
Data = yy.ReadXLS(File)
         
for item in Data["words"]["Data"]:
    splitItem = item["Word"].split(". ")
    item["Word"] = splitItem[-1]
    
yy.SaveXLS("c:\\Users\\milanhutera\\OneDrive - Doosan\\Python\\subtitles\\auxPrograms\\level.xlsx",Data)

