
from gtts import gTTS
from playsound import playsound
import os
from main.mainui import Ui_MainWindow

import sys
import requests

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.submit_button.clicked.connect(self.getinformation)
        self.ui.play_sound_button.clicked.connect(self.playsound)
        self.language_code = None
    def getinformation(self):
        data_input = {
            "District" : self.ui.district_input.text(),
            "Crop" : self.ui.crop_input.text(),
            "LanguageCode"  : self.ui.language_input.text()
        }
        url = "http://127.0.0.1:8000/imd/getinfo/"
        response = requests.post(url,data=data_input)
        #print("get information has been clicked",district,crop,language)
        data = response.json()
        self.language_code = data["language_code"]
        #print("The output is",data["information_in_local_languages"])
        text_output = ""
        for i in range(len(data["titles"])):
            text_output += str(data["information_in_local_languages"]) + '\n'  

            
        if(text_output == ""):
            text_output = "No Output"
        self.ui.infromation_output.setText(text_output)
        print("logged the output for",data_input["District"])

    
    def playsound(self):
        text = self.ui.infromation_output.toPlainText()
        tts = gTTS(text,lang=(self.language_code),slow=False)
        #print(self.language_code)
        tts.save("temp_saved_audio.mp3")
        playsound("temp_saved_audio.mp3")
        os.remove("temp_saved_audio.mp3")
        
        
if __name__ == "__main__":
    
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

    