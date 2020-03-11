import PySpin
from PyQt5.QtCore import Qt
# from PyQt5 import QtGui  # (the example applies equally well to PySide)
from PyQt5.QtWidgets import *
import cv2

win_width = 1600
win_height = 900

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
        camera.BeginAcquisition()
        count = 0
        view_mode = 1
        save_mode = 0
        mask = cv2.createBackgroundSubtractorMOG2(history=3,
                                                  varThreshold=100,
                                                  detectShadows=False)
        ch = 12
        sub_ch = []
        sum_ch1 = [0] * ch

        file_stem = cam_field1_1.text()
        cur_dir = Path(cwDir)
        cur_file = cur_dir / file_stem
        ##    suffix = '.avi'
        ##    out = cv2.VideoWriter(str(Path(str(cur_file)+suffix)), cv2.VideoWriter_fourcc(*'MJPG'), 25.0, (c_width, c_height), isColor=False)

        if (local_angle != angle):
            rad = math.radians(abs(angle))
            cos = math.cos(rad)
            sin = math.sin(rad)

            # original frame capture dimensions
            ##        y1,x1 = frame.shape
            y1 = c_height
            x1 = c_width
            image_center = (x1 / 2, y1 / 2)

            # rotated array dimensions
            y2 = (y1 * cos) + (x1 * sin)
            x2 = (x1 * cos) + (y1 * sin)
            rot_x = int(abs(x2 - x1))
            rot_y = int(abs(x1 * sin))
            rot_width = int(x1 - abs(x2 - x1))
            rot_height = int((y1 * cos) - (x1 * sin))

            # Maxtrix transformation
            M = cv2.getRotationMatrix2D((image_center), angle, 1)
            M[0, 2] += ((x2 / 2) - image_center[0])
            M[1, 2] += ((y2 / 2) - image_center[1])

            print('angle has changed')
            local_angle = angle

        ## assigning subchannels - sub_ch
        for x in range(ch + 1):
            sub_ch_x = round(x * (roi_width / (ch)))
            sub_ch.append(sub_ch_x)

        if menu1.currentText() == 'AVI':
            suffix = '.avi'
            out = cv2.VideoWriter(str(Path(str(cur_file) + suffix)), 0x00000000, 25.0, (rot_width, rot_height),
                                  isColor=False)
        elif menu1.currentText() == 'MJPG':
            suffix = '.avi'
            out = cv2.VideoWriter(str(Path(str(cur_file) + suffix)), cv2.VideoWriter_fourcc(*'MJPG'), 25.0,
                                  (rot_width, rot_height), isColor=False)
        elif menu1.currentText() == 'MP4':
            suffix = '.mp4'
            out = cv2.VideoWriter(str(Path(str(cur_file) + suffix)), 0x00000022, 25.0, (rot_width, rot_height),
                                  isColor=False)
        else:
            suffix = '.avi'
            out = cv2.VideoWriter(str(Path(str(cur_file) + suffix)), cv2.VideoWriter_fourcc(*'MJPG'), 25.0,
                                  (rot_width, rot_height), isColor=False)
        filename = Path(str(cur_file) + suffix)
        console_print('The saved file name = ' + str(filename))

        while (no_cancel and count <= int(cam_field4.text())):

            count += 1
            image_primary = cam.GetNextImage()
            frame = np.array(image_primary.GetNDArray())

            if chk_box2.isChecked():
                frame = cv2.flip(frame, -1)

            if angle != 0:
                frame = cv2.warpAffine(frame, M, (int(x2), int(y2)))
                frame_crop = frame[rot_y:(rot_y + rot_height), rot_x:(rot_x + rot_width)]  # img[y:y+h, x:x+w]

            if angle == 0:
                frame_crop = frame
            out.write(frame_crop)

            frame_count = frame_crop[roi_y:(roi_y + int(roi_width * 110 / 840)), roi_x:(roi_x + roi_width)]
            frame_mask = mask.apply(frame_count)
            frame_mask = cv2.medianBlur(frame_mask, blur_value)
            frame_mask = cv2.threshold(frame_mask, 125, 255, cv2.THRESH_BINARY)[1]

            # find contours
            contours, hierarcy = cv2.findContours(frame_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # list of all the coordinates (tuples) of each cell
            coord_list = []

            # to find the coordinates of the cells
            for i in range(len(contours)):
                avg = np.mean(contours[i], axis=0)
                coord = (int(avg[0][0]), int(avg[0][1]))  ##Coord is (y,x)
                ##            if Show == 1:
                ##                cv2.circle(frame_count, coord, 10, (255, 0, 255), 1)
                ch_pos = int(math.floor((coord[0]) / sub_ch[1]))
                try:
                    sum_ch1[ch_pos] += 1
                except:
                    # Undeclared variable?
                    error += 1

            if FPS < 26 or (count % (int(FPS / 5)) == 0):

                if chk_box4.isChecked() and (capture_width + capture_height) > 0:
                    cv2.putText(frame_crop, 'ROI', (roi_x + 10, roi_y + 30), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(frame_crop, 'Capture Size', (capture_x + 10, capture_y + 30), font, 0.5,
                                (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(frame_crop, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (255, 255, 255),
                                  3, 1, 0)
                    cv2.rectangle(frame_crop, (capture_x, capture_y),
                                  (capture_x + capture_width, capture_y + capture_height), (255, 255, 255), 3, 1, 0)
                    # draw lines on crop frame
                    ##
                    for x in range(ch):
                        cv2.putText(frame_crop, str(x + 1),
                                    ((roi_x + sub_ch[x] + 10), (roi_y + int(roi_width * 110 / 840) - 25)), font, 0.5,
                                    (255, 255, 255), 1, cv2.LINE_AA)
                        cv2.line(frame_crop, ((roi_x + sub_ch[x]), roi_y),
                                 ((roi_x + sub_ch[x]), (roi_y + int(roi_width * 110 / 840))), (200, 200, 100), 2)

                qformat = QImage.Format_Indexed8
                img = QImage(frame, int(x2), int(y2), int(x2), qformat)
                img = img.copy(rot_x, rot_y, rot_width, rot_height)  # copy(int x, int y, int width, int height)
                img = QPixmap.fromImage(img)

                if chk_box3.isChecked():
                    img = img.scaled(round(width * (0.6)) - 50, round(height * (0.6)) - 25,
                                     aspectRatioMode=Qt.KeepAspectRatio)

                cv2.imshow('frame_count', frame_count)

                label.setPixmap(img)
                cv2.waitKey(Delay)

            image_primary.Release()
            bar1.setValue(count)

        out.release
        cam.EndAcquisition()
        pass

    def save_npy(self):
        return

    def save_avi(self):
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

        save_avi_btn = ("QPushButton { background-color: rgb(25,120,250); font: bold 12px;}"
                    "QPushButton { border-color: rgb(40,40,15); border-width: 2px; }"
                    "QPushButton { border-style: inset; border-radius: 4px; padding: 10px; }"
                    "QPushButton:pressed { background-color: rgb(25,120,200) }")

        btn1 = QPushButton('Video'); btn1.setStyleSheet(cam_btn)
        btn2 = QPushButton('SAVE NPY');btn2.setStyleSheet(save_btn);btn2.setFixedSize(80, 40)
        btn3 = QPushButton('SAVE AVI'); btn3.setStyleSheet(save_avi_btn);btn3.setFixedSize(80, 40)
        btn1.setFixedSize(80, 40)

        # btn1.clicked.connect(self.video)
        # btn2.clicked.connect(self.save_data)
        # btn3.clicked.connect(self.save_avi)

        label = QLabel()
        label.setText('Test Window')
        label.setAlignment(Qt.AlignCenter)

        windowLayout = QGridLayout()  ##define layout - Box type
        windowLayout.addWidget(btn3, 0, 5, 1, 1)
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