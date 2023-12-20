import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QTextCursor



class TransparentTextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.matrix_timer = QTimer(self)
        self.matrix_timer.timeout.connect(self.matrix_effect)
        self.matrix_timer.start(100)  # Adjust the timing for effect speed

    def initUI(self):
        # Set the background image
        background = QPixmap('RainGirl.png')
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(palette)

        # Create a transparent text edit widget for the matrix effect
        self.matrix_text_edit = QTextEdit(self)
        self.matrix_text_edit.setStyleSheet("background: transparent; color: green; font-family: 'Courier New'; font-size: 12pt;")
        self.matrix_text_edit.setAttribute(Qt.WA_TranslucentBackground)
        self.matrix_text_edit.setReadOnly(True)
        self.setCentralWidget(self.matrix_text_edit)

        # Set the window size and title
        self.setGeometry(300, 300, 1024, 768)
        self.setWindowTitle('☠︎₦Ɇ₮ⱤɄ₦₦ɆⱤ V1☠︎')
        self.show()

    def matrix_effect(self):
        # Generate random text for Matrix-like effect
        text = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(80)) + '\n'
        self.matrix_text_edit.moveCursor(QTextCursor.End)
        self.matrix_text_edit.insertPlainText(text)
        self.matrix_text_edit.ensureCursorVisible()

def main():
    app = QApplication(sys.argv)
    editor = TransparentTextEditor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
