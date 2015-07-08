from PySide.QtGui import* 
from PySide.QtCore import* 

class Text(QGraphicsRectItem):
    """Gives the length of the shortest tour"""
    
    def __init__(self):
        QGraphicsRectItem.__init__(self)
        self.unitext="" 
        self.text=QGraphicsTextItem(self.unitext)
        self.text.setParentItem(self)
                     
    def boundingRect(self):
        return QRect(0,0,0.2,0.3)
    
    def paint(self, painter, option, widget):
        self.text.setDefaultTextColor(Qt.black) 
       
    def scale(self):
        """scales the text size by 0.009"""
        self.setScale(0.009)
    
    def update(self, text):
        """updates unitext to given text"""
        self.unitext=text
        self.text.setPlainText(self.unitext)
