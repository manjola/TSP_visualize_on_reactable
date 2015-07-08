from PySide.QtGui import* 
from PySide.QtCore import* 

class Cursor(QGraphicsItem): 
   "Cursor works in the simulation as fingers do in the reactable"
   
    def __init__(self): 
        QGraphicsItem.__init__(self)
        self.cursor= QGraphicsEllipseItem(-0.005,-0.005,0.01, 0.01)
        self.areacursor=QGraphicsEllipseItem(-0.05,-0.05,0.1, 0.1)
        self.node=None #keeps track of the node of the graph closest to the cursor
        self.cursor.setParentItem(self)
        self.areacursor.setParentItem(self)
                                
    def boundingRect(self):
        return self.childrenBoundingRect()
    
    def shape(self):
        path = QPainterPath()
        path.addEllipse(-0.05,-0.05,0.1, 0.1)
        return path
         
    def paint(self, painter, option, widget):
        self.cursor.setPen(QPen(Qt.black,0.01)) 
        self.cursor.setBrush(QBrush(Qt.black))
        #self.areacursor.setOpacity(0.0)
        
    
        
    
