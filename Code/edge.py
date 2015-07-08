from PySide.QtGui import* 
from PySide.QtCore import* 
from math import*

class Edge(QGraphicsItem): 
     
    def __init__(self, node1, node2, coeff): 
        QGraphicsItem.__init__(self)
        self.node1=node1
        self.node2=node2
        self.coeff=coeff 
        self.length=sqrt((self.node1.x()-self.node2.x())**2+(self.node1.y()-self.node2.y())**2) #euclidian distance
        self.dashed=False #dashed or not
        self.count=0  #if count=0, edge is active; if count=1, edge is disabled
        self.active=True #abled or disabled
        self.edge=QGraphicsLineItem(self.node1.x(), self.node1.y(), self.node2.x(), self.node2.y())
        self.edge.setParentItem(self)
        
    def boundingRect(self): 
        return self.childrenBoundingRect()
        
    def shape(self):
        path = QPainterPath()
        p=QPolygonF()
        p.append(QPointF(self.node1.x(),self.node1.y()))
        p.append(QPointF(self.node2.x(), self.node2.y()))
        path.addPolygon(p)
        return path
            
    def paint(self, painter, option, widget):
        pen=QPen(Qt.black, 0.0025, Qt.SolidLine)
        if self.active==False: #if disabled --> cyan color
            #color=pen.color()
            #color.setAlpha(0)
            #pen.setColor(color)
            pen.setColor(QColor(0, 255, 255))
            #pen.setColor(QColor(0,255,255,0))
            self.edge.setPen(pen)
            #self.edge.setOpacity(0.0)
        elif self.dashed==True: #set style to dashed
            pen.setStyle(Qt.DashLine)
            self.edge.setPen(pen)
        else: #normal
            self.edge.setPen(pen)
            
    def getweight(self): 
        """returns the weight of the egde"""
        if self.active==False:
            return 10**6
        else:
            return self.coeff*int(100*self.length) 
 
    def update(self):
        """updates the edge attributes"""
        self.edge.setLine(self.node1.x(), self.node1.y(), self.node2.x(), self.node2.y())
        self.length=sqrt((self.node1.x()-self.node2.x())**2+(self.node1.y()-self.node2.y())**2)  
    
    def change(self, bool, var):
        """changes the edge properties depending on the boolean bool and the variable var.
        var takes two values, 'abled' or 'dashed'"""
        if var=='abled':
            self.active=bool
        elif var=='dashed':
            self.dashed=bool    
        else:
            return 'value is not correct'
        
       
             
        
            
       
        
        
        
        
            
        
     
        
