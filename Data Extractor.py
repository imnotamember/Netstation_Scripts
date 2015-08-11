__author__ = 'Joshua Zosky'

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PyQt4 code borrowed from:
ZetCode PyQt4 tutorial

In this example, we select a file with a
QtGui.QFileDialog and display its contents
in a QtGui.QTextEdit.

author: Jan Bodnar
website: zetcode.com
last edited: October 2011
"""

import csv
import os
import sys
from PyQt4 import QtGui


class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()
        self.dict_header = ["segment #",
                            "_dbrain_18cluster_LORB",
                            "_dbrain_18cluster_RORB",
                            "_dbrain_18cluster_LP",
                            "_dbrain_18cluster_RP",
                            "_dbrain_18cluster_LIF",
                            "_dbrain_18cluster_RIF",
                            "_dbrain_18cluster_LPF",
                            "_dbrain_18cluster_RPF",
                            "_dbrain_18cluster_LT",
                            "_dbrain_18cluster_RT",
                            "_dbrain_18cluster_LIT",
                            "_dbrain_18cluster_RIT",
                            "_dbrain_18cluster_LTP",
                            "_dbrain_18cluster_RTP",
                            "_dbrain_18cluster_LO",
                            "_dbrain_18cluster_RO",
                            "_dbrain_18cluster_LIO",
                            "_dbrain_18cluster_RIO",
                            "delete me"]
        self.dict_save_header = ["subject #",
                                 "segment #",
                                 "_dbrain_18cluster_LORB",
                                 "_dbrain_18cluster_RORB",
                                 "_dbrain_18cluster_LP",
                                 "_dbrain_18cluster_RP",
                                 "_dbrain_18cluster_LIF",
                                 "_dbrain_18cluster_RIF",
                                 "_dbrain_18cluster_LPF",
                                 "_dbrain_18cluster_RPF",
                                 "_dbrain_18cluster_LT",
                                 "_dbrain_18cluster_RT",
                                 "_dbrain_18cluster_LIT",
                                 "_dbrain_18cluster_RIT",
                                 "_dbrain_18cluster_LTP",
                                 "_dbrain_18cluster_RTP",
                                 "_dbrain_18cluster_LO",
                                 "_dbrain_18cluster_RO",
                                 "_dbrain_18cluster_LIO",
                                 "_dbrain_18cluster_RIO"]
        self.overall_data = []
        self.initUI()

    def initUI(self):

        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open Analysis File(s)')
        openFile.triggered.connect(self.showDialogOpen)

        saveFile = QtGui.QAction(QtGui.QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+O')
        saveFile.setStatusTip('Save Analysis File(s)')
        saveFile.triggered.connect(self.showDialogSave)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()

    def showDialogOpen(self):

        fnames = QtGui.QFileDialog.getOpenFileNames(self, 'Open file(s)', '/home')

        if fnames is None:
            return

        fileListing = ""
        self.overall_data = []

        for names in fnames:
            names = '%s' % names
            fileListing += names + "\n"
            subject_number = self.get_subject_number((os.path.basename(names))[4:9])
            self.overall_data.extend(self.extract_data(names, subject_number))

        fileListing += "%s rows of data ready to save." % (len(self.overall_data))

        self.textEdit.setText(fileListing)

    def showDialogSave(self):

        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', filter='*.csv', selectedFilter='*.csv' '/home')

        if fname is None:
            return

        with open(fname, 'w') as csvfile:
            fieldnames = self.dict_save_header
            dictwriter = csv.DictWriter(csvfile, fieldnames, lineterminator='\n')
            dictwriter.writeheader()
            dictwriter.writerows(self.overall_data)

    def extract_data(self, file_names, subject_number):
        return_data = []
        with open(file_names, 'rb') as csvfile:
            dictreader = csv.DictReader(csvfile, fieldnames=self.dict_header, delimiter='\t')
            for rows in dictreader:
                if rows['segment #'][0:7] == 'Segment':
                    rows = {key: value for key, value in rows.items() if key != 'delete me'}
                    rows['subject #'] = subject_number
                    return_data.append(rows)
        return return_data

    def get_subject_number(self, fname):
        message = "Are you sure this is the correct subject number: %s?" % fname
        reply = QtGui.QMessageBox.question(self,
                                           'Message',
                                           message,
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            return fname
        else:
            return '-9999'

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()