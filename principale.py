from PyQt5 import QtCore, QtGui, QtWidgets
import librosa
import librosa.display
from DTW import dtw
from python_speech_features import mfcc



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(80)
        MainWindow.resize(662, 489)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 30, 600, 16))
        self.label.setObjectName("label")
        self.button1 = QtWidgets.QPushButton(self.centralwidget)
        self.button1.setGeometry(QtCore.QRect(450, 170, 200, 28))
        self.button1.setObjectName("choisir")
        self.chemin1 = QtWidgets.QLabel(self.centralwidget)
        self.chemin1.setGeometry(QtCore.QRect(20, 170, 521, 21))
        self.chemin1.setObjectName("chemin")
        self.chemin2= QtWidgets.QLabel(self.centralwidget)
        self.chemin2.setGeometry(QtCore.QRect(20, 110, 521, 16))
        self.chemin2.setObjectName("chemin")
        self.button2 = QtWidgets.QPushButton(self.centralwidget)
        self.button2.setGeometry(QtCore.QRect(450, 110, 200, 28))
        self.button2.setObjectName("choisir")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 220, 1005, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.resultat = QtWidgets.QLabel(self.centralwidget)
        self.resultat.setGeometry(QtCore.QRect(20, 230, 400, 61))
        self.resultat.setObjectName("Resultat")
        self.button3= QtWidgets.QPushButton(self.centralwidget)
        self.button3.setGeometry(QtCore.QRect(450, 240, 200, 41))
        self.button3.setObjectName("comparer")
        MainWindow.setCentralWidget(self.centralwidget)
       
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dialog = QtWidgets.QFileDialog(self.centralwidget)
        self.dialog.setWindowTitle('Open wav File')
        self.dialog.setNameFilter('wav files (*.wav)')

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "Vous devez choisir deux audio pour les comparer et vérifier qu'ils sont de format wav"))
        self.button1.setText(_translate("MainWindow", "Choisir audio 2"))
        self.chemin1.setText(_translate("MainWindow", ""))
        self.chemin2.setText(_translate("MainWindow", ""))
        self.button2.setText(_translate("MainWindow", "Choisir audio 1"))
        self.resultat.setText(_translate("MainWindow", ""))
        self.button3.setText(_translate("MainWindow", "Comparaison"))
        self.button2.clicked.connect(self.selectWav1)
        self.button1.clicked.connect(self.selectWav2)
        self.button3.clicked.connect(self.Comparer)
        
    def selectWav1(self):
        self.dialog.setDirectory(QtCore.QDir.currentPath())
        self.dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if self.dialog.exec_() == QtWidgets.QDialog.Accepted:
            chemin1_wav = str(self.dialog.selectedFiles()[0])
            
        else:
            return None
        self.chemin2.setText(chemin1_wav)
        self.path1=chemin1_wav   
  
    def selectWav2(self):
        self.dialog.setDirectory(QtCore.QDir.currentPath())
        self.dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if self.dialog.exec_() == QtWidgets.QDialog.Accepted:
            chemin2_wav = str(self.dialog.selectedFiles()[0])
            
        else:
            return None
        self.chemin1.setText(chemin2_wav)        
        self.path2=chemin2_wav
        

    def Comparer(self):
        if self.path1=='' or self.path2=='':
            self.resultat.setText("Vous devez choisir les audio d'abord !") 
        else:    
            audio1,sample_rate1 = librosa.load(self.path1)
            audio2,sample_rate2 = librosa.load(self.path2)
            mfcc_audio1 = librosa.feature.mfcc(audio1, sr=sample_rate1)
            mfcc_audio2 = librosa.feature.mfcc(audio2, sr=sample_rate2)
            n1,c1=mfcc_audio1.shape
            n2,c2=mfcc_audio2.shape
        
       
            if n1 != n2 or c1 !=c2 : 
                mfcc_audio1=mfcc_audio1.reshape(-1,1)
                mfcc_audio2=mfcc_audio2.reshape(-1,1)
                matches, cost, mapping_1, mapping_2, matrix=dtw(mfcc_audio1,mfcc_audio2)
                if cost>1000:
                    res="les deux enregistrements que vous avez choisi sont différents"
                    self.resultat.setText("le coût est:"+str(cost)+"\n"+res)
                elif cost==0:
                    res1="les deux enregistrements que vous avez choisi sont similaires"
                    self.resultat.setText("le coût est:"+str(cost)+"\n"+res1)
            else :    
                matches, cost, mapping_1, mapping_2, matrix=dtw(mfcc_audio1,mfcc_audio2)
                if cost>1000:
                    res="Ils ne sont pas similaires"
                    self.resultat.setText("le coût est:"+str(cost)+"\n"+res)
                elif cost==0:
                    res1="Ils sont similaires"
                    self.resultat.setText("le coût est:"+str(cost)+"\n"+res1)          

    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    wind = QtWidgets.QMainWindow()
    wind.setWindowTitle("Belgacha Khaoula : Projet de traitement de la parole")
    wind.setWindowIcon(QtGui.QIcon("icone.png"))
    ex.setupUi(wind)
    wind.show()
    sys.exit(app.exec_())
