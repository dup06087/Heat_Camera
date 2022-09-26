import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import Get_Equipment_status
# import prac_scroll
import prac_childwindow
from PyQt5.QtCore import *
from to_class.get_cam_num import camera_num

### Qt 실행
# app = QtWidgets.QApplication(sys.argv)
# MainWindow = QtWidgets.QMainWindow()
# ui = prac_scroll.Ui_MainWindow()
# ui = prac_childwindow.Ui_MainWindow()
# ui.setupUi(MainWindow)
# MainWindow.show()

### 장비가져오기 쓰레드 실행
thread_get_data = QThread()
class Worker_get_data(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        QtWidgets.QApplication.processEvents()
        self.temp = list(range(camera_num))
        self.volt1 = list(range(camera_num))
        self.volt2 = list(range(camera_num))
        self.current = list(range(camera_num))

    def get_temperature(self):   ### 반드시 str값!!!
        while True:
            try:
                for i in range(camera_num):
                    # print("temperature getting")
                    # test =
                    prac_childwindow.ui.status_label[i].setText(Get_Equipment_status.values[i])
                    QtWidgets.QApplication.processEvents()  ### 중요

                    # print("value[i] : ", Get_Equipment_status.values[i], "\n values end")
                    if (int(Get_Equipment_status.temp_outputs[i]) >= 25) and (int(Get_Equipment_status.volt1_outputs[i]) >= 25) and (int(Get_Equipment_status.volt2_outputs[i]) >= 25) and (int(Get_Equipment_status.volt3_outputs[i]) >= 25) and (int(Get_Equipment_status.current_outputs[i]) >= 25):
                        prac_childwindow.ui.lbl_prob_chk[i].setStyleSheet("background-color: rgb(255, 0, 0);")
                    else:
                        prac_childwindow.ui.lbl_prob_chk[i].setStyleSheet("background-color: rgb(255, 255, 255);")
            except:
                print("UI loading...")

worker_get_data = Worker_get_data()
worker_get_data.moveToThread(thread_get_data)
thread_get_data.started.connect(worker_get_data.get_temperature())

# sys.exit(prac_childwindow.app.exec_())
