import sys
import json

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt, 
    QSettings,
    QByteArray,
    QTimer,
)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)

from PySide6.QtWidgets import QApplication, QMainWindow, QMenu
from PySide6.QtGui import QAction
from CAS_interface_small import Ui_MainWindow
from PySide6.QtNetwork import QTcpSocket, QTcpServer, QHostAddress
from PySide6.QtHttpServer import QHttpServer

import CAS_logic

WEBAPI_PORT = 8881


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.lines = [
            self.ui.Line1,
            self.ui.Line2,
            self.ui.Line3,
            self.ui.Line4,
            self.ui.Line5,
            self.ui.Line6,
            self.ui.Line7,
            self.ui.Line8,
            self.ui.Line9,
            self.ui.Line10,
        ]

        self.update_lines()
        self.update_counts()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    
    def contextMenuEvent(self, event):
        # Create a context menu
        context_menu = QMenu(self)

        # Add a "Close" action to the context menu
        close_action = QAction("Close", self)
        close_action.triggered.connect(self.close)  # Connect the action to the close method

        # Add the action to the menu
        context_menu.addAction(close_action)

        # Show the context menu at the mouse position
        context_menu.exec(event.globalPos())

    def mousePressEvent(self, event):
        # Store the positions of mouse and window and
        # change the window position relative to them.
        self.windowPos = self.pos()
        self.mousePos = event.globalPos()
        super(MainWindow, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.move(self.windowPos + event.globalPos() - self.mousePos)
        super(MainWindow, self).mouseMoveEvent(event)
    
    def closeEvent(self, event):
        self.writeSettings()

    def writeSettings(self):
        settings = QSettings("settings.ini", QSettings.IniFormat)
        settings.beginGroup("MainWindow")
        settings.setValue("x", self.pos().x())
        settings.setValue("y", self.pos().y())
        settings.setValue("w", self.width())
        settings.setValue("h", self.height())
        settings.endGroup()
        
    def readSettings(self):
        settings = QSettings("settings.ini", QSettings.IniFormat)
        settings.beginGroup("MainWindow")
        x = int(settings.value("x", 40))
        y = int(settings.value("y", 40))
        w = int(settings.value("w", 323))
        h = int(settings.value("h", 179))

        self.setGeometry(QRect(x, y, w, h))
        settings.endGroup()


    def update_lines(self):

        # if len(CAS_logic.final_mssgs_list) < 10 or CAS_logic.final_mssgs_list[0] == None:
        #     CAS_logic.final_mssgs_list.append ('END')
        # elif 'END' in CAS_logic.final_mssgs_list:
        #     pass

        for line in self.lines:
            line.setText("")

        for msg, line in zip(CAS_logic.final_mssgs_list, self.lines):
            if msg is None:
                continue

            if msg == "END":
                line.setText(f"{msg}")
            else:
                line.setText(f"{msg.text}")

            if msg == "END":
                line.setStyleSheet(
                    "color: rgb(255, 255, 255);\n" "background-color: rgb(0, 0, 0);"
                )
                line.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # красное непрочитанное сообщение
            elif msg.color == "R" and msg.isread == False:
                line.setStyleSheet(
                    "background-color: rgb(254, 0, 0);\n" "color: rgb(255, 255, 255);"
                )          
            # красное прочитанное сообщение
            elif msg.color == "R" and msg.isread == True:
                line.setStyleSheet(
                    "color: rgb(254, 0, 0);\n" "background-color: rgb(0, 0, 0);"
                )
            # желтое непрочитанное сообщение
            elif msg.color == "A" and msg.isread == False:
                line.setStyleSheet(
                    "color: rgb(0,0,0);\n" "background-color: rgb(254, 203, 0);"
                )
            # желтое прочитанное сообщение
            elif msg.color == "A" and msg.isread == True:
                line.setStyleSheet(
                    "color: rgb(254, 203, 0);\n" "background-color: rgb(0, 0, 0);"
                )
            # белое непрочитанное сообщение
            elif msg.color == "W" and msg.isread == False:
                line.setStyleSheet(
                    "color: rgb(0,0,0);\n" "background-color: rgb(255, 255, 255);"
                )
            # белое прочитанное сообщение
            elif msg.color == "W" and msg.isread == True:
                line.setStyleSheet(
                    "color: rgb(255, 255, 255);\n" "background-color: rgb(0, 0, 0);"
                )

            if msg != "END":
                line.setIndent(5)
                line.setAlignment(Qt.AlignmentFlag.AlignLeft)
            
        return
    

    def update_counts(self):
            self.ui.amber_mssgs_down_count.setText(f"{CAS_logic.amber_count_down_str}")
            self.ui.amber_mssgs_up_count.setText(f"{CAS_logic.amber_count_up_str}")
            self.ui.white_mssgs_down_count.setText(f"{CAS_logic.white_count_down_str}")
            self.ui.white_mssgs_up_count.setText(f"{CAS_logic.white_count_up_str}")

def show_message(request):
    json_body = json.loads(request.body().toStdString())
    message = json_body["message"]
    msg_color = CAS_logic.add_mssg(message)
    if msg_color == "W":
        QTimer.singleShot(5000, app, lambda: print(f"{message} прочитано"))

    window.update_lines()


def scroll_up(request):
    CAS_logic.scroll_for_1_message(scroll_for_one_mssg_bttn_up=True, scroll_for_one_mssg_bttn_down=False)
    window.update_lines()

def hide_message(request):
    json_body = json.loads(request.body().toStdString())
    message = json_body["message"]
    CAS_logic.remove_message(message)
    window.update_lines()
    print(CAS_logic.final_mssgs_list)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.setWindowTitle("CAS")
    window.readSettings()

    web_server = QHttpServer()
    web_server.route("/api/show_message", show_message)
    web_server.route("/api/scroll_up", scroll_up)
    web_server.route("/api/hide_message", hide_message)

    tcp_server = QTcpServer()
    tcp_server.listen(QHostAddress("0.0.0.0"), WEBAPI_PORT) 
    web_server.bind(tcp_server)

    sys.exit(app.exec())
