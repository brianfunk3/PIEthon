from py import functions
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QLabel, QLineEdit, QRadioButton, QVBoxLayout, QMessageBox,
                             QPushButton, QScrollArea, QHBoxLayout, QGroupBox, QFormLayout, QCheckBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from os.path import exists, expanduser
from os import mkdir

class prevButton(QPushButton):

    def __init__(self, cols, rows, form, dframe):
        super().__init__()
        self.cols = cols
        self.rows = rows
        self.form = form
        self.dframe = dframe
        self.setText('preview')
        self.clicked.connect(self.colPreview)
        self.setMinimumWidth(100)
        self.setObjectName('previewbutton')

    def getcols(self):
        return self.cols

    def getrows(self):
        return self.rows

    def getform(self):
        return self.form

    def colPreview(self):
        for i in range(self.rows):
            self.form.itemAt(i).widget().setText(str(self.dframe.iloc[i, self.cols]))


class preview(QWidget):

    def __init__(self, dframe, dtype, startdate, enddate):
        self.dframe = dframe
        self.dtype = dtype
        self.startdate = startdate
        self.enddate = enddate
        super().__init__()

        self.initUI()

    def initUI(self):
        self.center()

        mygroupbox = QGroupBox('Select Columns to Keep')
        myform = QFormLayout()

        buttonlist = []
        checklist = []

        previewform = QVBoxLayout()
        allcheck = QCheckBox('Keep All ' +str(len(self.dframe.columns)) + ' Columns')
        allcheck.setChecked(True)
        allcheck.stateChanged.connect(lambda: self.allcheckfunct(checklist, allcheck.checkState()))
        rangenum = min(100, len(self.dframe))

        for i in range(len(self.dframe.columns)):
            tempcheck = QCheckBox(self.dframe.columns[i])
            tempcheck.setChecked(True)
            checklist.append(tempcheck)
            tempbutt = prevButton(i, rangenum, previewform, self.dframe)
            buttonlist.append(tempbutt)
            myform.addRow(checklist[i], buttonlist[i])
        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        scroll.horizontalScrollBar().setEnabled = False
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        onecolvlayout = QVBoxLayout()
        onecolvlayout.addWidget(allcheck)
        onecolvlayout.addWidget(scroll)

        layout = QHBoxLayout()
        layout.addLayout(onecolvlayout)

        previewbox = QGroupBox('Preview (' +str(len(self.dframe.index)) + ' Records Total)')

        previewlist = []

        for i in range(rangenum):
            previewlist.append(QLabel(' '))
            previewlist[i].setObjectName('previewlabel')
            previewform.addWidget(previewlist[i])

        previewbox.setLayout(previewform)
        previewscroll = QScrollArea()
        previewscroll.horizontalScrollBar().setEnabled = False
        previewscroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        previewscroll.setWidget(previewbox)
        layout.addWidget(previewscroll)

        subbox = QGroupBox('')
        #subbox.setFixedWidth(150)

        radiocero = QRadioButton('Documents/PIEthon/exports')
        radiocero.setChecked(True)
        radiouno = QRadioButton('Downloads')
        radiodos = QRadioButton('Documents')
        radiotres = QRadioButton('Desktop')

        radiolist = []

        radiolist.append(radiocero)
        radiolist.append(radiouno)
        radiolist.append(radiodos)
        radiolist.append(radiotres)

        subform = QVBoxLayout()
        subbut = QPushButton('Export')
        subbut.clicked.connect(lambda: self.export(checklist, radiolist))

        closebut = QPushButton('Close')
        closebut.clicked.connect(self.close)

        for radio in radiolist:
            subform.addWidget(radio)

        self.exportname = QLineEdit(self)
        self.exportname.setText(str(self.dtype) + '_' + str(self.startdate) + '_' + str(self.enddate))

        exportlabel = QLabel('.csv')

        hboy = QHBoxLayout()
        hboy.addWidget(self.exportname)
        hboy.addWidget(exportlabel)

        subform.addLayout(hboy)

        subbox.setLayout(subform)
        layout.addWidget(subbox)

        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(closebut)
        buttonlayout.addSpacing(300)
        buttonlayout.addWidget(subbut)

        totalvlayout = QVBoxLayout(self)
        totalvlayout.addLayout(layout)
        totalvlayout.addSpacing(15)
        totalvlayout.addLayout(buttonlayout)

        self.setStyleSheet(open(functions.resource_path("resources\\iu_stylesheet.qss"), "r").read())

        self.setWindowTitle('PIEthon')
        self.setWindowIcon(QIcon(functions.resource_path('resources\\PIEcon.png')))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def allcheckfunct(self, checklist, bool):
        for widget in checklist:
            widget.setChecked(bool)


    def export(self, checklist, radiolist):
        expath = ''
        for radio in radiolist:
            if radio.isChecked():
                if radio.text() == 'Documents/PIEthon/exports':
                    if not exists(expanduser('~/Documents/PIEthon')):
                        mkdir(expanduser('~/Documents/PIEthon/'))
                    if not exists(expanduser('~/Documents/PIEthon/exports')):
                        mkdir(expanduser('~/Documents/PIEthon/exports'))
                    expath = expanduser('~/Documents/PIEthon/exports/')
                if radio.text() == 'Downloads':
                    expath = expanduser('~/Downloads/')
                if radio.text() == 'Documents':
                    expath = expanduser('~/Documents/')
                if radio.text() == 'Desktop':
                    expath = expanduser('~/Desktop/')
        drops = []
        for widget in checklist:
            if (not widget.isChecked()):
                drops.append(widget.text())
                #self.dframe.drop(widget.text())
        newframe = self.dframe.drop(columns=drops)
        try:
            newframe.to_csv(expath + self.exportname.text() + '.csv')
        except:
            newframe.to_csv(expath + str(self.dtype) + '_' + str(self.startdate) + '_' + str(self.enddate) + '.csv')

        buttonReply = QMessageBox.information(self, 'Export Successful', 'Data exported to ' + str(expath), QMessageBox.Ok)

        """
        msg = QMessageBox()
        msg.setIcon(QIcon(functions.resource_path('resources\\PIEcon.png')))
        msg.setText('Export Successful!')
        msg.setInformativeText('Data exported to ' + str(expath))
        msg.setStandardButtons(QMessageBox.Ok)
        """