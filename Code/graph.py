from PySide.QtGui import* 
from PySide.QtCore import* 
from node import* 
from edge import*
from tspalgorithm import*
from tour import*
from special import*
from text import*
from cursor import*

class Graph(QGraphicsScene):
    signal=Signal() #graph signal
    def __init__(self): 
        QGraphicsScene.__init__(self)
        self.setItemIndexMethod(QGraphicsScene.NoIndex) #fixes cache problem with TUIO remove
        self.nodelist=[] #list of nodes   
        self.edgemap={} #mapping (n2,n1): E(n2,n1)
        self.idmap={}    #mapping of (session id: node) 
        self.cursormap={} #mapping of (session id: cursor)
        self.specialmap={} #mapping (id: special object)
        self.change= (None,None,None) #( type of object, changes made, node changed if any) 
        self.tsp=TSPAlgorithm(self,None) #initiate with an algorithm instance
        self.signal.connect(self.tsp.start) #connect graph signal to slot
        self.timer1=QTimer() #timer1
        self.timer2=QTimer() #timer2
        self.timer2.timeout.connect(self.tsp.run2Opt)
        self.Text=Text()
        self.Text.scale()
        self.addItem(self.Text)
        self.disableedgesmap={} #mapping of (n2, n1): E(n2,n1)
        self.cursornodemap={} #mapping of (cursor: node)
        
        
        self.timer3=QTimer() #timer3
        
    def isspecialobject(self,tuionode): 
        """Returns True if tuionode is a special object"""
        if tuionode.id%5==0:
            return True
     
    def getangle(self,tuionode):
        """Returns the angle of the tuionode"""
        return tuionode.angle
        
    def changecoeff(self, area, coeff, bool):
        """Changes the coefficient of the edges that intersect the area
        to the given coeff, as well as the properties of the edges based on the 
        boolean bool."""
        intersectionlist=area.collidingItems(Qt.IntersectsItemShape)
        for item in intersectionlist:
            if item.__class__.__name__=='Edge':
                item.coeff=coeff
                item.change(bool,'dashed')
               
    def closestnode(self,cursor,list):
        """Takes an object: cursor, and a list of nodes: list.
        Returns the node of the list which is closest to the cursor.
        If two nodes are equally close to the cursor, it returns only one of them;
        the one that appears first in the list."""
        x=cursor.x() #coordinates of the cursor
        y=cursor.y()
        mindist= x**2+ y**2 #minimum distance
        minitem=None #item that returns minimum distance
        for item in list:
            distance=(x-item.x())**2+ (y-item.y())**2
            if distance<mindist:
                mindist=distance
                minitem=item
        return minitem   
        
    def condition(self):
        """if the cursornodemap is empty, emits the signal"""
        if len(self.cursornodemap)==0:
            self.change= ('Cursor',None,None)
            self.signal.emit()
        
    def addcursor(self,tuiocursor):
        """takes care of adding a cursor to the graph"""
        x=tuiocursor.xpos
        y=tuiocursor.ypos
        c=Cursor()#create cursor instance
        c.setPos(x, y)
        self.cursormap[tuiocursor.sessionid]=c #update cursor mapping
        self.addItem(c) #add cursor to the scene               
        intersectingnodeslist=[] #list of nodes that are in the vicinity of the cursor/finger
        intersectionlist=c.areacursor.collidingItems(Qt.IntersectsItemShape)
        for item in intersectionlist:
            if item.__class__.__name__=='Node':
                intersectingnodeslist.append(item)
        if intersectingnodeslist!=[]: #if cursor near some node
            n=self.closestnode(c, intersectingnodeslist) #closest node to the cursor/finger    
            c.node=n #set cursor node to n
            self.cursornodemap[c]=n #update cursor map
            if len(self.cursornodemap)==2: #if there's another cursor
                s=self.cursornodemap.copy()
                s.pop(c)
                c2=s.keys()[0] #second cursor
                n2=c2.node
                pair=(n,n2) 
                #if pair in disable edges map
                if (n,n2) in self.disableedgesmap:
                    edge=self.disableedgesmap[(n,n2)]
                    edge.active=True #enable the edge
                    self.disableedgesmap.pop((n,n2)) #remove edge from disabled map
                elif (n2,n) in self.disableedgesmap:
                    edge=self.disableedgesmap[(n2,n)]
                    edge.active=True
                    self.disableedgesmap.pop((n2,n))
                #otherwise
                else:
                    if (n,n2) in self.edgemap:
                        edge=self.edgemap[(n,n2)]
                        edge.active=False #disable the edge
                        self.disableedgesmap[(n,n2)]=edge #add edge to disabled map
                    elif (n2,n) in self.edgemap:
                        edge=self.edgemap[(n2,n)]
                        edge.active=False #disable the edge
                        self.disableedgesmap[(n2,n)]=edge #add edge to disabled map    
              
    def updatecursor(self,tuiocursor):
        """takes care of updating the cursor"""
        x=tuiocursor.xpos
        y=tuiocursor.ypos
        epsilon=0.01
        c=self.cursormap[tuiocursor.sessionid]
        euclideandistancesquare=(x-c.x())**2+ (y-c.y())**2
        if euclideandistancesquare>epsilon**2:
            c.setPos(x, y) 
        
    def removecursor(self,tuiocursor):
        """takes care of removing the cursor"""
        c=self.cursormap[tuiocursor.sessionid]#cursor to remove
        self.removeItem(c) #remove cursor from scene
        self.cursormap.pop(tuiocursor.sessionid) #remove from cursormap
        if c in self.cursornodemap:
            self.cursornodemap.pop(c)
            c.node=None
            self.condition()
        
    def addnode(self, tuionode):
        """takes care of adding a node or special object to the graph"""
        x=tuionode.xpos
        y=tuionode.ypos
        #when a special object is added, check for the edges its area intersects:
        if self.isspecialobject(tuionode)==True:
            #1.Add
            s=Special() 
            s.setPos(x,y)
            s.angle=self.getangle(tuionode)
            s.update() 
            self.specialmap[tuionode.id]=s 
            self.addItem(s)
            #2.change intersection weights
            self.changecoeff(s.area,2, True)
            #3.Run 2opt:
            self.change=("Special", None, None)
            self.signal.emit()     
        else:
            n=Node()#create node instance
            n.setPos(x, y)
            self.idmap[tuionode.sessionid]=n #update mapping
            self.addItem(n) #add node to the scene 
            for node in self.nodelist: 
                e=Edge(n,node,1)
                self.edgemap[(n,node)]=e #update edge map
                self.addItem(e) #add edge to the scene           
            self.nodelist.append(n)#update node list
            self.change= ("Node","Node Added.", n)
            #when a new node is added check if new edges created intersect with the special objects:
            for id in self.specialmap:
                s=self.specialmap[id]
                self.changecoeff(s.area,2,True)
            self.signal.emit() 
                
    def updatenode(self,tuionode):
        """takes care of updating the node or special object"""
        x=tuionode.xpos
        y=tuionode.ypos
        epsilon=0.01
        epsilonangle=5
        if self.isspecialobject(tuionode)==True:  
            #1.Update the angle/coordinates
            s=self.specialmap[tuionode.id]
            euclideandistancesquare=(x-s.x())**2+ (y-s.y())**2
            angledifference=abs(tuionode.angle-s.angle)
            if euclideandistancesquare>epsilon**2: #does it needs update
                self.changecoeff(s.area,1,False)
                s.setPos(x,y)
                #2.Change the weights for the new area:
                self.changecoeff(s.area,2,True) 
                #3. Run 2opt
                self.change=("Special", None, None)
                self.signal.emit()        
            if angledifference>epsilonangle: #does it needs update
                self.changecoeff(s.area,1,False)
                if s.angle!=tuionode.angle:
                    s.angle=self.getangle(tuionode)
                    s.update()
                #2.Change the weights for the new area:
                self.changecoeff(s.area,2,True) 
                #3. Run 2opt
                self.change=("Special", None, None)
                self.signal.emit()        
        else:
            n=self.idmap[tuionode.sessionid]
            euclideandistancesquare=(x-n.x())**2+ (y-n.y())**2
            if euclideandistancesquare>epsilon**2:
                n.setPos(x, y) #udpate node
                for node in self.nodelist:
                    if (node,n) in self.edgemap:
                        self.edgemap[(node,n)].update()
                        self.edgemap[(node,n)].coeff=1 #set edge coeff to 1
                        self.edgemap[(node,n)].dashed=False #set dashed to False
                    elif (n,node) in self.edgemap:
                        self.edgemap[(n,node)].update()
                        self.edgemap[(n,node)].coeff=1
                        self.edgemap[(n,node)].dashed=False 
                self.change= ("Node","Node Updated.", None)
                for id in self.specialmap:
                    s=self.specialmap[id]
                    self.changecoeff(s.area, 2, True)
                self.signal.emit() 
               
    def removenode(self,tuionode): 
        """takes care of removing a node or special object"""
        if self.isspecialobject(tuionode)==True:
            #1.Remove
            s=self.specialmap[tuionode.id]
                #2.Change weights
            self.changecoeff(s.area,1, False)
            self.specialmap.pop(tuionode.id)
            self.removeItem(s)
            #3.Run 2opt
            self.change=("Special", None, None)
            self.signal.emit()  
        else:
            n=self.idmap[tuionode.sessionid]#node to remove
            self.nodelist.remove(n) #remove node n from node list
            self.idmap.pop(tuionode.sessionid)
            self.removeItem(n)      #remove node n from scene
            edict=dict(self.edgemap)
            for node in self.nodelist:
                if (node,n) in self.edgemap:
                    self.removeItem(edict[(node,n)]) #remove edge from scene
                    self.edgemap.pop((node,n)) #remove edge from edgemap
                elif (n,node) in self.edgemap:
                    self.removeItem(edict[(n,node)])
                    self.edgemap.pop((n,node))
            self.change= ("Node","Node Removed.", n)
            #when edges are removed, it doesn't matter what their coeff is,
            #we don't need to care about the special objects in this case
            self.signal.emit() 
        
    def getedge(self, node1, node2): 
        """returns edge with given endpoints n1, n2"""
        if (node1,node2) in self.edgemap:
            return self.edgemap[(node1,node2)]
        elif (node2,node1) in self.edgemap:
            return self.edgemap[(node2,node1)]
        else:
            print "edge does not exist", node1, node2
       
        
 
