import sys


from PyQt5.QtWidgets import *

import ANALYSOR.SongFilter.songFilter_byKeyWord as tool





class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(500, 300)
        self.setWindowTitle("数据分析")

        self.widget_main = QWidget()

        self.group_box_main = QGroupBox("请输入关键词:")
        self.label_main = QLabel("请键入信息")
        self.label_info = QLabel("运行时界面可能会未响应")

        self.radiobox_comment = QRadioButton("评论预测")
        self.radiobox_key_word = QRadioButton("关键词检索")
        self.radiobox_key_word.setChecked(True)

        self.textEdit = QPlainTextEdit()
        self.btn_confirm = QPushButton("Confirm")
        self.btn_close = QPushButton("Close")

        # layout_main = QVBoxLayout()
        layout_main = QGridLayout()

        self.setCentralWidget(self.widget_main)

        self.widget_main.setLayout(layout_main)

        layout_main.addWidget(self.label_main, 0, 0, 1, 4)
        layout_main.addWidget(self.textEdit, 1, 0, 1, 4)
        layout_main.addWidget(self.btn_confirm, 2, 3, 1, 1)
        layout_main.addWidget(self.btn_close, 2, 2, 1, 1)
        layout_main.addWidget(self.label_info, 2, 0, 1, 1)

        layout_main.addWidget(self.radiobox_comment, 0, 2, 1, 1)
        layout_main.addWidget(self.radiobox_key_word, 0, 3, 1, 1)

        self.btn_confirm.clicked.connect(self.on_btn_confirm_clicked)
        self.btn_close.clicked.connect(self.on_btn_close_clicked)

    def on_btn_confirm_clicked(self):
        string = self.textEdit.toPlainText()
        print(string)

        if self.radiobox_key_word.isChecked():
            tool.run(string)

    @staticmethod
    def on_btn_close_clicked(self):
        sys.exit(0)



# 生命;意义;力量;价值;疯狂;酒;欲望;生活


def main():

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
    pass


if __name__ == '__main__':
    main()



