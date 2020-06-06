from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import sys


class Pencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pandemic Meter-ByUgrHs")
        self.setWindowIcon(QIcon("icons/virus.png"))
        self.setMinimumSize(QSize(750,750))
        self.bilgiEkran = "World"
        self.setUI()
        self.setStyleSheet(open("theme.qss","r").read())
        self.timer = QTimer()
        self.timer.timeout.connect(self.setUI)
        self.timer.start(300000)

        self.show()

    def setUI(self):
        r = requests.get("https://www.worldometers.info/coronavirus/")
        
        self.soup = BeautifulSoup(r.content, "html.parser")
        self.hasta, self.olum, self.kurtulan = self.durumlar()[0]
        self.hastaTr, self.olumTr, self.kurtulanTr = self.durumlar()[1]
        self.hastaEn, self.olumEn, self.kurtulanEn = self.durumlar()[2]

        if self.olumTr == " " or self.olumTr == "":
            self.olumTr = 0
        if self.kurtulanTr == " " or self.kurtulanTr == "":
            self.kurtulanTr =0
        if self.olumEn == " " or self.olumEn == "" or self.olumEn == "N/A":
            self.olumEn = 0
        if self.kurtulanEn == " " or self.kurtulanEn == "" or self.kurtulanEn == "N/A":
            self.kurtulanEn =0

        self.tarih = datetime.today().strftime("%d-%m-%Y")
        self.saat = datetime.today().strftime("%H:%M")

        self.setCentralWidget(self.anaWidget())



        self.effect = QGraphicsColorizeEffect(self.sonGuncelleme)
        self.sonGuncelleme.setGraphicsEffect(self.effect)

        animasyon = QPropertyAnimation(self.effect, b"color")
        animasyon.setStartValue(QColor(Qt.red))
        animasyon.setEndValue(QColor(Qt.black))
        animasyon.setDuration(1000)
        animasyon.start()

        self.animation = animasyon

        self.sonGuncelleme.setText("Son Guncelleme {} - {}".format(self.saat, self.tarih))




    def anaWidget(self):
        widget = QWidget()
        v_box = QVBoxLayout()
        dunyatrbox = QHBoxLayout()
        dunyatrbox.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        dunya = QToolButton()
        turkiye = QToolButton()
        england = QToolButton()

        dunya.setIcon(QIcon("icons/world.png"))
        dunya.setText("Dünya")
        dunya.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        dunya.setCursor(QCursor(Qt.PointingHandCursor))
        dunya.clicked.connect(lambda :self.degistir("dunya"))

        turkiye.setIcon(QIcon("icons/turkey.png"))
        turkiye.setText("Türkiye")
        turkiye.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        turkiye.setCursor(QCursor(Qt.PointingHandCursor))

        turkiye.clicked.connect(lambda : self.degistir("tr"))

        england.setIcon(QIcon("icons/en.png"))
        england.setText("İngiltere")
        england.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        england.setCursor(QCursor(Qt.PointingHandCursor))

        england.clicked.connect(lambda : self.degistir("en"))

        dunyatrbox.addWidget(dunya)
        dunyatrbox.addWidget(turkiye)
        dunyatrbox.addWidget(england)

        dunyaWidget = self.dunya()

        self.sonGuncelleme = QLabel("Son Guncelleme {} - {}".format(self.saat, self.tarih))
        self.sonGuncelleme.setAlignment(Qt.AlignHCenter)


        v_box.addLayout(dunyatrbox)

        #dünya ise
        v_box.addWidget(dunyaWidget)

        v_box.addLayout(self.bilgiler())
    
        v_box.addWidget(self.sonGuncelleme)
        widget.setLayout(v_box)


        return widget

    def degistir(self, ekran):
        self.bekleme = QDialog(self)

        v_box = QVBoxLayout()

        bekle = QLabel("deneme")
        bekle.setAlignment(Qt.AlignHCenter)
        loading = QMovie("icons/loading2.gif")
        loading.setScaledSize(QSize(200,200))
        bekle.setAttribute(Qt.WA_TranslucentBackground)
        bekle.setMovie(loading)
        loading.start()

        v_box.addWidget(bekle)

        self.bekleme.setLayout(v_box)
        self.bekleme.setAttribute(Qt.WA_TranslucentBackground)

        self.bekleme.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.bekleme.setWindowModality(Qt.ApplicationModal)

        ##Timer

        self.sayac = 0 
        self.gecis = QTimer()
        self.gecis.timeout.connect(lambda : self.time(ekran))
        self.gecis.start(1000)
        self.say = 0

        self.bekleme.show()

    def time(self, ekran):
        self.say +=1

        if self.say >= 2:
            self.say = 0
            if ekran=="tr":
                self.bilgiEkran = "tr"
                self.setCentralWidget(self.anaWidget())
            elif ekran=="en":
                self.bilgiEkran = "en"
                self.setCentralWidget(self.anaWidget())
            else:
                self.bilgiEkran = "dunya"
                self.setCentralWidget(self.anaWidget())
            self.gecis.stop()
            self.bekleme.close()


    def dunya(self):

        if self.bilgiEkran =="dunya":
            series = QPieSeries()
            series.append("Hasta", float(self.hasta))
            series.append("Olu", float(self.olum))
            series.append("Kurtulan", float(self.kurtulan))

            #kurtulan
            slice = QPieSlice()
            slice = series.slices()[2]
            slice.setExploded(True)
            slice.setLabelVisible(True)
            slice.setPen(QPen(Qt.darkGreen, 2))
            slice.setBrush(Qt.green)

            #olü
            slice = QPieSlice()
            sliceozel = series.slices()[1]
            sliceozel.setExploded(False)
            sliceozel.setLabelVisible(True)
            sliceozel.setPen(QPen(Qt.black, 2))
            sliceozel.setBrush(Qt.black)

            #hasta
            slice = QPieSlice()
            slice = series.slices()[0]
            slice.setExploded(False)
            slice.setLabelVisible(True)
            slice.setPen(QPen(Qt.darkGray, 2))
            slice.setBrush(Qt.gray)

            chart = QChart()
            chart.legend().hide()
            chart.addSeries(series)
            chart.createDefaultAxes()
            chart.setAnimationOptions(QChart.AllAnimations)
            chart.setTitle("Dünya Geneli COVID-19")
            chart.setTitleFont(QFont("Berlin Sans FB Demi", 22))

            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignTop)
            chart.legend().setFont(QFont("Berlin Sans FB Demi",16))
            chartview = QChartView(chart)
            chartview.setRenderHint(QPainter.Antialiasing)

            return chartview

        elif self.bilgiEkran =="en":
            series = QPieSeries()
            series.append("Hasta", float(self.hastaEn))
            series.append("Olu", float(self.olumEn))
            series.append("Kurtulan", float(self.kurtulanEn))

            #kurtulan
            slice = QPieSlice()
            slice = series.slices()[2]
            slice.setExploded(True)
            slice.setLabelVisible(True)
            slice.setPen(QPen(Qt.darkGreen, 2))
            slice.setBrush(Qt.green)

            #olü
            slice = QPieSlice()
            sliceozel = series.slices()[1]
            sliceozel.setExploded(False)
            sliceozel.setLabelVisible(True)
            sliceozel.setPen(QPen(Qt.black, 2))
            sliceozel.setBrush(Qt.black)

            #hasta
            slice = QPieSlice()
            slice = series.slices()[0]
            slice.setExploded(False)
            slice.setLabelVisible(True)
            slice.setPen(QPen(Qt.darkGray, 2))
            slice.setBrush(Qt.gray)

            chart = QChart()
            chart.legend().hide()
            chart.addSeries(series)
            chart.createDefaultAxes()
            chart.setAnimationOptions(QChart.AllAnimations)
            chart.setTitle("İngiltere Geneli COVID-19")
            chart.setTitleFont(QFont("Berlin Sans FB Demi", 22))

            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignTop)
            chart.legend().setFont(QFont("Berlin Sans FB Demi",16))
            chartview = QChartView(chart)
            chartview.setRenderHint(QPainter.Antialiasing)

            return chartview



        else:
            series = QPieSeries()
            series.append("Hasta", float(self.hastaTr))
            series.append("Olu", float(self.olumTr))
            series.append("Kurtulan", float(self.kurtulanTr))

            #kurtulan
            slice = QPieSlice()
            slice = series.slices()[2]
            slice.setExploded(True)
            slice.setLabelVisible(True)
            slice.setPen(QPen(Qt.darkGreen, 2))
            slice.setBrush(Qt.green)

            #olü
            slice = QPieSlice()
            sliceozel = series.slices()[1]
            sliceozel.setExploded(False)
            sliceozel.setLabelVisible(True)
            sliceozel.setPen(QPen(Qt.black, 2))
            sliceozel.setBrush(Qt.black)

            #hasta
            slice = QPieSlice()
            slice = series.slices()[0]
            slice.setExploded(False)
            slice.setLabelVisible(True)
            slice.setPen(QPen(Qt.darkGray, 2))
            slice.setBrush(Qt.gray)

            chart = QChart()
            chart.legend().hide()
            chart.addSeries(series)
            chart.createDefaultAxes()
            chart.setAnimationOptions(QChart.AllAnimations)
            chart.setTitle("Türkiye Geneli COVID-19")
            chart.setTitleFont(QFont("Berlin Sans FB Demi", 22))

            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignTop)
            chart.legend().setFont(QFont("Berlin Sans FB Demi",16))
            chartview = QChartView(chart)
            chartview.setRenderHint(QPainter.Antialiasing)

            return chartview

    def bilgiler(self):
        v_box = QVBoxLayout()
        v_box.setAlignment(Qt.AlignHCenter)

        if self.bilgiEkran == "dunya":
            hbox1 = QHBoxLayout()
            hasta = QLabel("Hasta:")
            self.hastaBilgi = QLabel(self.hasta)
            hbox1.addWidget(hasta)
            hbox1.addWidget(self.hastaBilgi)
            self.hastaBilgi.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.hastaBilgi.setCursor(QCursor(Qt.IBeamCursor))

            hbox2 = QHBoxLayout()
            olu = QLabel("Ölü:")
            self.oluBilgi = QLabel(self.olum)
            hbox2.addWidget(olu)
            hbox2.addWidget(self.oluBilgi)
            self.oluBilgi.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.oluBilgi.setCursor(QCursor(Qt.IBeamCursor))

            hbox3 = QHBoxLayout()
            kurtulan = QLabel("Kurtulan:")
            self.kurtulanBilgi = QLabel(self.kurtulan)
            self.kurtulanBilgi.setObjectName("kurtulan")
            self.kurtulanBilgi.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.kurtulanBilgi.setCursor(QCursor(Qt.IBeamCursor))
            hbox3.addWidget(kurtulan)
            hbox3.addWidget(self.kurtulanBilgi)

            v_box.addLayout(hbox1)
            v_box.addLayout(hbox2)
            v_box.addLayout(hbox3)

        elif self.bilgiEkran == "en":
            hbox1 = QHBoxLayout()
            hasta = QLabel("Hasta:")
            self.hastaBilgi = QLabel(str(self.hastaEn))
            hbox1.addWidget(hasta)
            hbox1.addWidget(self.hastaBilgi)

            hbox2 = QHBoxLayout()
            olu = QLabel("Ölü:")
            self.oluBilgi = QLabel(str(self.olumEn))
            hbox2.addWidget(olu)
            hbox2.addWidget(self.oluBilgi)

            hbox3 = QHBoxLayout()
            kurtulan = QLabel("Kurtulan:")
            self.kurtulanBilgi = QLabel(str(self.kurtulanEn))
            hbox3.addWidget(kurtulan)
            hbox3.addWidget(self.kurtulanBilgi)

            v_box.addLayout(hbox1)
            v_box.addLayout(hbox2)
            v_box.addLayout(hbox3)

    
        else:
            hbox1 = QHBoxLayout()
            hasta = QLabel("Hasta:")
            self.hastaBilgi = QLabel(str(self.hastaTr))
            hbox1.addWidget(hasta)
            hbox1.addWidget(self.hastaBilgi)

            hbox2 = QHBoxLayout()
            olu = QLabel("Ölü:")
            self.oluBilgi = QLabel(str(self.olumTr))
            hbox2.addWidget(olu)
            hbox2.addWidget(self.oluBilgi)

            hbox3 = QHBoxLayout()
            kurtulan = QLabel("Kurtulan:")
            self.kurtulanBilgi = QLabel(str(self.kurtulanTr))
            hbox3.addWidget(kurtulan)
            hbox3.addWidget(self.kurtulanBilgi)

            v_box.addLayout(hbox1)
            v_box.addLayout(hbox2)
            v_box.addLayout(hbox3)


        return v_box

    def durumlar(self):

        #dunya
        sorgu = self.soup.find_all("div",attrs={"class":"maincounter-number"})
        self.durumDunya = []
        self.durumTurkiye = []
        self.durumEngland = []
        for i in sorgu:
            self.durumDunya.append(i.text.strip().replace(",",""))

        #turkiye
        sorgu2 = self.soup.find_all("td",attrs={"style":"font-weight: bold; font-size:15px; text-align:left;"})
        for td in sorgu2:
            if td.text.strip() == "Turkey":
                hasta = td.findNext("td").text.strip().replace(",",".")
                olum = td.findNext("td").findNext("td").findNext("td").text.strip().replace(",",".")
                kurtulan = td.findNext("td").findNext("td").findNext("td").findNext("td").findNext("td").text.strip().replace(",",".")

                self.durumTurkiye.append(hasta)
                self.durumTurkiye.append(olum)
                self.durumTurkiye.append(kurtulan)
                break

        #england
        sorgu3 = self.soup.find_all("td",attrs={"style":"font-weight: bold; font-size:15px; text-align:left;"})
        for td in sorgu3:
            if td.text.strip() == "UK":
                hasta = td.findNext("td").text.strip().replace(",",".")
                olum = td.findNext("td").findNext("td").findNext("td").text.strip().replace(",",".")
                kurtulan = td.findNext("td").findNext("td").findNext("td").findNext("td").findNext("td").text.strip().replace(",",".")

                self.durumEngland.append(hasta)
                self.durumEngland.append(olum)
                self.durumEngland.append(kurtulan)
                break

        return self.durumDunya, self.durumTurkiye, self.durumEngland

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = Pencere()
    sys.exit(app.exec())
