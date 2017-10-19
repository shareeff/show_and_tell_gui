from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import sys

from image_caption import ImageCaption


class UserInterface(QWidget):

    def __init__(self):
        super(UserInterface,self).__init__()
        self.video_size = QSize(320, 240)
        self.text_label_size = QSize(420,100)
        self.device = 0
        self.setup_ui()


    def setup_ui(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.CreateImageDisplayGroup())
        vbox.addWidget(self.CreateTextDisplay())
        self.setLayout(vbox)

        self.setWindowTitle("Image Caption Generator")
        self.resize(400, 350)

    def CreateImageDisplayGroup(self):
        groupbox = QGroupBox()
        hbox = QHBoxLayout()
        hbox.addWidget(self.CreateImageDisplay())
        hbox.addWidget(self.CreateControleGroup())
        groupbox.setLayout(hbox)

        return groupbox


    def CreateControleGroup(self):
        groupbox = QGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(self.CreateRadioButton())
        vbox.addWidget(self.CreateControlButton())
        groupbox.setLayout(vbox)

        return groupbox

    def CreateImageDisplay(self):
        groupbox = QGroupBox("Display Image")
        self.image_label = QLabel()
        self.image_label.setFixedSize(self.video_size)
        ImageLayout = QGridLayout()
        ImageLayout.addWidget(self.image_label)
        groupbox.setLayout(ImageLayout)

        return groupbox

    def CreateTextDisplay(self):
        groupbox = QGroupBox("Display Caption")
        self.text_label = QLabel()
        self.text_label.setFixedSize(self.text_label_size)
        TextLayout = QGridLayout()
        TextLayout.addWidget(self.text_label)
        groupbox.setLayout(TextLayout)

        return groupbox

    def CreateControlButton(self):
        groupbox = QGroupBox()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.StartVideoCapture)
        self.capture_button = QPushButton("Capture")
        self.capture_button.clicked.connect(self.CaptureImage)
        self.upload_button = QPushButton("Upload")
        self.upload_button.clicked.connect(self.UploadImage)
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.RunImageCaption)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.RunResetButton)
        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)
        ButtonLayout = QVBoxLayout()
        ButtonLayout.addWidget(self.start_button)
        ButtonLayout.addWidget(self.capture_button)
        ButtonLayout.addWidget(self.upload_button)
        ButtonLayout.addWidget(self.run_button)
        ButtonLayout.addWidget(self.reset_button)
        ButtonLayout.addWidget(self.quit_button)

        groupbox.setLayout(ButtonLayout)

        return groupbox

    def CreateRadioButton(self):
        groupbox = QGroupBox()
       # radio_button_group = QButtonGroup()
        self.button1 = QRadioButton("Device 0")
        self.button1.setChecked(True)
        self.button1.clicked.connect(self.Button0Clicked)
        #radio_button_group.addButton(self.button1)
        self.button2 = QRadioButton("Device 1")
        self.button2.clicked.connect(self.Button1Clicked)
        #radio_button_group.addButton(self.button2)
        RButtonLayout = QVBoxLayout()
        RButtonLayout.addWidget(self.button1)
        RButtonLayout.addWidget(self.button2)
        groupbox.setLayout(RButtonLayout)


        return groupbox

    def StartVideoCapture(self):
        self.setup_camera()

    def CaptureImage(self):
        if not self.capture.isOpened():
            self.capture = cv2.VideoCapture(self.device)
          #  self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
           # self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

        self.image_flag = 0;

        _, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        cv2.imwrite("current_frame.jpg", frame)
        self.timer.stop()
        self.capture.release()

        self.display_current_frame(frame)







    def UploadImage(self):
        filename = QFileDialog.getOpenFileName(self, "Open Image", QDir.currentPath(),
                                                     "Image Files (*.jpg *.jpeg)")
        #dialog = QFileDialog()
        #dialog.setFileMode(QFileDialog.AnyFile)
        #dialog.setFilter("Image Files (*.jpg *.jpeg)")
        #filenames = QStringList()
        self.image_flag = 1;
        current_frame = cv2.imread(filename[0])
        cv2.imwrite("current_frame.jpg", current_frame)
        self.display_current_frame(current_frame)
        print(filename)


    def RunImageCaption(self):
        caption_string = ImageCaption()
        caption = caption_string['0']+"\n"+caption_string['1']+"\n"+caption_string['2']+"\n"
        self.display_image_caption(caption)




    def RunResetButton(self): pass

    def Button0Clicked(self):

        self.device = 0

    def Button1Clicked(self):

        self.device = 1



    def setup_camera(self):
        """Initialize camera.
        """
        self.capture = cv2.VideoCapture(self.device)
       # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
       # self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
       # if not self.capture.isOpened() and self.device == 1:
        #    self.capture.release()
        #    self.button1.setChecked(True)
         #   self.Button0Clicked()
         #   self.capture = cv2.VideoCapture(self.device)


        _, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        image = QImage(frame, frame.shape[1], frame.shape[0],
                      frame.strides[0], QImage.Format_RGB888)
        image1 = QPixmap.fromImage(image)
        image_resize = image1.scaled(self.video_size.width(), self.video_size.height(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(image_resize)

    def display_current_frame(self,current_frame):

        if self.image_flag == 0:

            image = QImage(current_frame, current_frame.shape[1], current_frame.shape[0],
                    current_frame.strides[0], QImage.Format_RGB888)
            image1 = QPixmap.fromImage(image)
        else:
            image1 = QPixmap("current_frame.jpg")


        #image = QImage(current_frame)


        #self.image_label.setScaledContents(True)

        image_resize = image1.scaled(self.video_size.width(), self.video_size.height(), Qt.KeepAspectRatio)

        self.image_label.setPixmap(image_resize)


        #self.image_label.setPixmap(QPixmap.fromImage(image))
       # self.image_label.




    def display_image_caption(self, caption):

        self.text_label.setText(caption)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UserInterface()
    win.show()
    sys.exit(app.exec_())





