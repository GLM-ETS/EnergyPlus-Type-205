import sys, pickle, shutil, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QPushButton, QLabel, QHBoxLayout, \
    QVBoxLayout, QComboBox, QLineEdit, QSlider, QSpacerItem, QMessageBox
from PyQt6.QtGui import QPixmap, QPainter, QMouseEvent
from PyQt6.QtGui import QIcon, QFont
from addition import *
from PyQt6.QtCore import Qt
class params(object):
    def __init__(self):
        super().__init__()
        self.LAI = 1
        self.CAC = 1
        self.Afv = 1
        self.P_LED = 120
        self.rho_v = 0.05
        self.LED_eff = 0.52
        self.zone_name = ""

    def dump(self, folder_path):
        with open(folder_path + "/" + "Type205_params.pkl", 'wb') as handle:
            pickle.dump(self.__dict__,handle)
        return




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.params = params()
        self.idf_loaded = False
        self.initUI()



    def initUI(self):

        layout = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()

        w = []
        w2 = []

        label = QLabel("EnergyPlus CEA Generator",self)
        label.setFont(QFont("Sanserif", 24))
        w.append(label)

        w.append(QSpacerItem(20,20))

        button = QPushButton('Select .idf', self)
        button.setToolTip('Select EnergyPlus Input File')
        w.append(button)
        w.append(QSpacerItem(20, 20))

        label2 = QLabel(".idf Thermal Zones",self)
        label2.setFont(QFont("Sanserif", 12))
        w.append(label2)

        self.box = QComboBox(self)
        w.append(self.box)
        w.append(QSpacerItem(20, 20))

        d = {}
        names_dict = {"LAI" : {"slider_max":50},"CAC":{"slider_max":100}, "Afv":{"slider_max":10}}

        names = list(names_dict.keys())


        for x in range(1, len(names)+1):
            s = "layout_D{0}".format(x)
            d[s] = QVBoxLayout()

            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, names_dict[names[x-1]]["slider_max"])
            slider.setValue(getattr(self.params,names[x-1]))
            slider.setSingleStep(1)
            slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            slider.setObjectName("slider_"+names[x - 1])
            slider.valueChanged.connect(self.selection_changed)


            lab = QLabel(names[x - 1] + " : " + str(getattr(self.params,names[x-1])))
            lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lab.setObjectName("label_"+names[x - 1])

            d[s].addWidget(slider)
            d[s].addWidget(lab)
            w2.append(d[s])

        d_LED ={}
        LED_dict = {"P_LED": {"max": 500}, "LED_eff": {"max": 100}, "rho_v": {"max": 10}}
        LED_names = list(LED_dict.keys())

        w3 = []
        for x in range(1, len(LED_names)+1):
            s = "layout_D{0}".format(x)
            d[s] = QVBoxLayout()
            button2 = QLineEdit()
            button2.textChanged.connect(self.selection_changed)
            button2.setObjectName("field_" + LED_names[x - 1])
            d[s].addWidget(button2)
            lab = QLabel(LED_names[x - 1] +" : " +str(getattr(self.params,LED_names[x-1])))
            lab.setObjectName("label_" + LED_names[x - 1])
            d[s].addWidget(lab)
            w3.append(d[s])

        button3 = QPushButton("Select Output Dir",self)
        button3.clicked.connect(lambda: self.select_output())

        layout4.addWidget(button3)
        button4 = QPushButton("Generate", self)
        button4.clicked.connect(lambda: self.generate())
        layout4.addWidget(button4)


        w.append(layout2)
        w.append(layout3)
        w.append(QSpacerItem(20, 20))
        w.append(layout4)

        for item in w:
            if type(item) == QHBoxLayout or type(item) == QVBoxLayout:
                layout.addLayout(item)
            elif type(item)==QSpacerItem:
                layout.addSpacerItem(item)
            else:
                layout.addWidget(item)

        for item in w2:
            if type(item) == QHBoxLayout or type(item) == QVBoxLayout:
                layout2.addLayout(item)
            else:
                layout2.addWidget(item)

        for item in w3:
            if type(item) == QHBoxLayout or type(item) == QVBoxLayout:
                layout3.addLayout(item)
            else:
                layout3.addWidget(item)





        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button.clicked.connect(lambda: self.choose_idf())

        widget = QWidget()
        widget.setLayout(layout)

        self.options = self.set_options_widgets([layout2, layout3, layout4])
        self.setCentralWidget(widget)
        self.options_hidden = True
        self.toggle_options()

    def generate(self):
        try:
            path = getattr(sys, '_MEIPASS', os.getcwd())

            self.params.zone_name = self.box.currentText()
            self.params.dump(self.output_path)

            shutil.copyfile(self.input_path,self.output_path+ "/" + "CEA_idf.idf")
            with open(self.output_path+ "/" + "CEA_idf.idf","a") as f:
                f.write(addition(self.params.zone_name))

            shutil.copyfile(path + "/" + "Type205.py" , self.output_path + "/" + "Type205.py")
            shutil.copyfile(path + "/" + "main.py",self.output_path + "/" + "main.py")

            dlg = QMessageBox(self)
            dlg.setWindowTitle("Done !")
            dlg.setText("Files Generated")
            dlg.exec()
        except Exception as e:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Oups !")
            dlg.setText(str(e))
            dlg.exec()
        return

    def select_output(self):
        self.output_path = QFileDialog.getExistingDirectory(self, "Select Output Dir")
        return

    def selection_changed(self):
        if type(self.sender())==QLineEdit:
            identifier = "_".join(self.sender().objectName().split("_")[1:])
            try:
                value = float(self.sender().text())
            except:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Oups !")
                dlg.setText("Use . as decimal separator")
                dlg.exec()
                return
        elif type(self.sender())==QSlider:
            identifier = self.sender().objectName().split("_")[1]
            value = self.sender().value() /10
        setattr(self.params,identifier,value)
        lab = self.findChild(QLabel,"label_" + identifier)
        lab.setText(identifier + " : "+str(value))
        lab.adjustSize()
        return

    def set_options_widgets(self, layout_list):
        w = []
        for l in layout_list:
                for idx in range(l.count()):
                    try:
                        for x in range(l.itemAt(idx).count()):
                            w.append(l.itemAt(idx).itemAt(x).widget())
                    except:
                        w.append(l.itemAt(idx).widget())
        return w

    def toggle_options(self):
        for w in self.options:
            if self.options_hidden:
                w.hide()
            elif ~self.options_hidden:
                w.show()
        return

    def choose_idf(self):
        import_dialog = QFileDialog()
        import_dialog.setWindowTitle('Select .idf file:')
        import_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        import_dialog.setNameFilter('IDF files (*.idf)')
        import_dialog.setDefaultSuffix('idf')

        if import_dialog.exec()==1 and len(import_dialog.selectedFiles())==1:
            self.box.clear()
            self.box.addItems(self.parse_thermal_zones(import_dialog.selectedFiles()[0]))
            self.options_hidden = False
            self.toggle_options()
            return import_dialog.selectedFiles()[0]

    def parse_thermal_zones(self,path):
        self.input_path = path
        with open(path) as f:
            lines = f.readlines()  # list containing lines of file
            zones = []  # To store column names
            l = len(lines)
            for idx, line in enumerate(lines):
                line = line.strip()  # remove leading/trailing white spaces
                if line == "Zone,":
                    if idx < (l - 1):
                        next = lines[idx + 1]
                        zones.append(next.strip().split(",")[0])

            return zones


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())