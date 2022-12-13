from PyQt5.QtWidgets import QApplication
import sys
import qdarkstyle

from model import Model
from view import View
from controller import Controller

class App(QApplication):
    def __init__(self,argv):
        super().__init__(argv)

        self.setStyleSheet(qdarkstyle.load_stylesheet())
        
        self._model = Model()

        self._view = View()

        self._controller = Controller(self._model,self._view)       


    
if __name__  == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
