import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QPushButton, QLabel, QHBoxLayout, \
    QVBoxLayout, QComboBox, QDial, QSlider
from PyQt6.QtGui import QPixmap, QPainter, QMouseEvent
from PyQt6.QtGui import QIcon, QFont
from os.path import expanduser
# from prog_g import create_pdf
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QRect, QLineF, QEvent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.idf_loaded = False
        self.LAI = 1
        self.CAC = 1
        self.initUI()


    def initUI(self):

        layout = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()

        w = []
        w2 = []

        label = QLabel("EnergyPlus CEA Simulator",self)
        label.setFont(QFont("Sanserif", 24))
        w.append(label)

        button = QPushButton('Select .idf', self)
        button.setToolTip('Select EnergyPlus Input File')
        w.append(button)

        label2 = QLabel(".idf Thermal Zones",self)
        label2.setFont(QFont("Sanserif", 12))
        w.append(label2)

        self.box = QComboBox(self)
        w.append(self.box)

        d = {}
        names = ["LAI","CAC"]


        for x in range(1, len(names)+1):
            s = "layout_D{0}".format(x)
            d[s] = QVBoxLayout()
            slider = QSlider(Qt.Orientation.Horizontal)
            lab = QLabel(names[x - 1] + " : " )
            lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
            setattr(self,"label_{}".format(names[x-1]),lab)
            d[s].addWidget(slider)
            d[s].addWidget(lab)
            w2.append(d[s])

        w.append(layout2)
        w.append(layout3)

        for item in w:
            if type(item) == QHBoxLayout or type(item) == QVBoxLayout:
                layout.addLayout(item)
            else:
                layout.addWidget(item)

        for item in w2:
            if type(item) == QHBoxLayout or type(item) == QVBoxLayout:
                layout2.addLayout(item)
            else:
                layout2.addWidget(item)



        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button.clicked.connect(lambda: self.choose_idf())

        widget = QWidget()
        widget.setLayout(layout)

        self.options = self.set_options_widgets([layout2])
        self.setCentralWidget(widget)
        self.options_hidden = True
        self.toggle_options()

    def set_options_widgets(self, layout_list):
        w = []
        for l in layout_list:
                for idx in range(l.count()):
                    for x in range(l.itemAt(idx).count()):
                        w.append(l.itemAt(idx).itemAt(x).widget())
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
            self.box.addItems(self.parse_thermal_zones(import_dialog.selectedFiles()[0]))
            self.options_hidden = False
            self.toggle_options()
            return import_dialog.selectedFiles()[0]

    def parse_thermal_zones(self,path):
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