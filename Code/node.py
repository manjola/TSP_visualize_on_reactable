from PySide.QtGui import* 
from PySide.QtCore import* 

class Node(QGraphicsItem): 
    """A node in the graph is an instance of this class"""
                         
    def __init__(self): 
        QGraphicsItem.__init__(self)
        self.node= QGraphicsEllipseItem(-0.025,-0.025,0.05, 0.05)
        self.node.setOpacity(0.6)
        self.node.setParentItem(self)
 
    def boundingRect(self):
        return self.childrenBoundingRect()
    
    def shape(self):
        path = QPainterPath()
        path.addEllipse(-0.025,-0.025,0.05, 0.05)
        return path
             
    def paint(self, painter, option, widget):
        self.node.setPen(QPen(Qt.black,0.01)) 
        self.node.setBrush(QBrush(Qt.darkBlue))
        
        
    
    


