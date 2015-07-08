from PySide.QtGui import* 
from PySide.QtCore import* 
from node import*
               
class Tour(QGraphicsItem): 
 
    def __init__(self): 
        QGraphicsItem.__init__(self)
        self.polygon=QGraphicsPolygonItem()
        self.polygon.setParentItem(self)
    
    def boundingRect(self):
        return self.childrenBoundingRect()
             
    def paint(self, painter, option, widget): 
        pass
        
    def updatePolygon(self,nodelist):
        p=QPolygonF()
        for node in nodelist:
            p.append(QPointF(node.x(), node.y()))
        self.polygon.setPolygon(p)
       
        