import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout


class FifteenPuzzle(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Пятнашки')
        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)
        self.buttons = []
        self.emptyButton = None
        self.initBoard()
        self.show()

    def initBoard(self):
        numbers = list(range(1, 16)) + [None]  # Список для перемешивания чисел и пустой клетки
        for row in range(4):
            for col in range(4):
                button = QPushButton('')
                button.setFixedSize(50, 50)
                self.buttons.append(button)
                self.gridLayout.addWidget(button, row, col)
                button.clicked.connect(lambda _, r=row, c=col: self.moveTile(r, c))
                num = numbers.pop(0)
                if num is not None:
                    button.setText(str(num))
                else:
                    button.setStyleSheet("background-color: white;")
                    self.emptyButton = button

    def moveTile(self, row, col):
        button = self.buttons[row * 4 + col]
        emptyRow, emptyCol = self.gridLayout.getItemPosition(self.gridLayout.indexOf(self.emptyButton))
        if (row == emptyRow and abs(col - emptyCol) == 1) or (col == emptyCol and abs(row - emptyRow) == 1):
            button.setText(self.emptyButton.text())
            button.setStyleSheet("")
            self.emptyButton.setText('')
            self.emptyButton.setStyleSheet("background-color: white;")
            self.emptyButton = button

    def keyPressEvent(self, event):
        key = event.key()
        if key == 16777234:  # Left arrow key
            emptyRow, emptyCol = self.gridLayout.getItemPosition(self.gridLayout.indexOf(self.emptyButton))
            if emptyCol < 3:
                self.moveTile(emptyRow, emptyCol + 1)
        elif key == 16777235:  # Up arrow key
            emptyRow, emptyCol = self.gridLayout.getItemPosition(self.gridLayout.indexOf(self.emptyButton))
            if emptyRow < 3:
                self.moveTile(emptyRow + 1, emptyCol)
        elif key == 16777236:  # Right arrow key
            emptyRow, emptyCol = self.gridLayout.getItemPosition(self.gridLayout.indexOf(self.emptyButton))
            if emptyCol > 0:
                self.moveTile(emptyRow, emptyCol - 1)
        elif key == 16777237:  # Down arrow key
            emptyRow, emptyCol = self.gridLayout.getItemPosition(self.gridLayout.indexOf(self.emptyButton))
            if emptyRow > 0:
                self.moveTile(emptyRow - 1, emptyCol)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    puzzle = FifteenPuzzle()
    sys.exit(app.exec_())
