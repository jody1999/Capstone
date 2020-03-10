import PySpin
from PyQt5.QtCore import Qt
# from PyQt5 import QtGui  # (the example applies equally well to PySide)
from PyQt5.QtWidgets import *

win_width = 1375
win_height = 750

class TestSetup:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_camera(self):
        system = PySpin.System.GetInstance()

        try:
            # [GET] camera list
            cam_list = system.GetCameras()
            cam = cam_list.GetByIndex(0)
        except:
            print("Cameras not found")
            return

        cam.Init()
        cam.BeginAcquisition()
        cam.EndAcquisition()
        num_cameras = cam_list.GetSize()
        print("Camera Detected")
        # [LOAD] default configuration
        cam.UserSetSelector.SetValue(PySpin.UserSetSelector_Default)
        cam.UserSetLoad()
        return cam

    def video_capture(self):
        camera = self.get_camera()
        pass

    def save_npy(self):
        return

    def widget_setup(self):
        '''
        Set up the GUI with only capture and save buttons.
        We will try saving the file first as a npy file then a AVI file? And benchmark both.
        '''

        app = QApplication([])
        w = QWidget()
        w.setWindowTitle('The window for testing')
        w.setMinimumWidth(win_width)
        w.setMinimumHeight(win_height)


        save_btn = ("QPushButton { background-color: rgb(25,120,250); font: bold 12px;}"
                    "QPushButton { border-color: rgb(40,40,15); border-width: 2px; }"
                    "QPushButton { border-style: inset; border-radius: 4px; padding: 10px; }"
                    "QPushButton:pressed { background-color: rgb(25,120,200) }")

        cam_btn = ("QPushButton { background-color: rgb(200,200,200); font: bold 12px;}"
                   "QPushButton { border-color: rgb(40,40,15); border-width: 2px; }"
                   "QPushButton { border-style: inset; border-radius: 4px; padding: 10px; }"
                   "QPushButton:pressed { background-color: rgb(180,180,180) }")

        btn1 = QPushButton('Video'); btn1.setStyleSheet(cam_btn)
        btn2 = QPushButton('SAVE');btn2.setStyleSheet(save_btn);btn2.setFixedSize(80, 40)
        btn1.setFixedSize(80, 40)

        # btn1.clicked.connect(self.video)
        # btn2.clicked.connect(self.save_data)

        label = QLabel()
        label.setText('Test Window')
        label.setAlignment(Qt.AlignCenter)

        windowLayout = QGridLayout()  ##define layout - Box type
        windowLayout.addWidget(btn2, 0, 3, 1, 1)
        windowLayout.addWidget(btn1, 0, 1, 1, 1)

        box1 = QGroupBox('Buttons')
        box1.setFixedSize(self.width * 0.985, self.height * 0.25)
        box2 = QGroupBox('View Video')
        # box2.setFixedSize(win_height * 1.5, win_width * 0.25)
        box1.setLayout(windowLayout)

        bigLayout = QGridLayout()
        bigLayout.addWidget(box1, 2,0,1,5)
        videoLayout = QGridLayout()  ##define layout - Box type
        videoLayout.addWidget(label, 0, 0)
        box2.setLayout(videoLayout)
        bigLayout.addWidget(box2, 0, 0, 1, 5)
        w.setLayout(bigLayout)

        w.show()
        app.exec_()

def main():
    widget = TestSetup(win_width,win_height)
    widget.widget_setup()


if __name__=="__main__":
    main()