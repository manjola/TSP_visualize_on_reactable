from PySide.QtGui import* 
from PySide.QtCore import* 

class Special(QGraphicsItem): 
    
    def __init__(self): 
        QGraphicsItem.__init__(self)
        self.angle=0.0 #rotation angle 
        self.diam=0.15 #diameter of area when angle=0.0 degrees 
        self.special=QGraphicsRectItem(-0.025,-0.025,0.05, 0.05) #special object representation        
        self.area=QGraphicsEllipseItem(-self.diam/2,-self.diam/2,self.diam, self.diam)  #area the special object affects
        self.special.setParentItem(self)
        self.area.setParentItem(self)
                         
    def boundingRect(self):
        return self.childrenBoundingRect()
        
    def shape(self):
        path = QPainterPath()
        path.addEllipse(-self.diam/2,-self.diam/2,self.diam, self.diam)
        return path
             
    def paint(self, painter, option, widget):
        self.special.setPen(QPen(Qt.black, 0.01)) 
        self.special.setBrush(QBrush(Qt.darkGreen))
        self.area.setPen(QPen(Qt.darkGreen,0.01, Qt.DashLine))
            
    def update(self):
        """Called when the special object is rotated, or when its position is changed.
        It updates the special object angle and the area it affects."""
        self.setRotation(self.angle)
        if self.angle==0:
            self.diam=0.15
        else:
            self.diam= 0.15+0.00125* self.angle
        self.area.setRect(-self.diam/2,-self.diam/2,self.diam, self.diam)
        
            
        
        
  
        
        