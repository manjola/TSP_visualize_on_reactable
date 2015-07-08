from PySide.QtGui import* 
from PySide.QtCore import* 
from node import* 
from edge import* 
from graph import*
from tour import*
from text import*
from cursor import*
import random
  
class TSPAlgorithm:
    
    def __init__(self, graph, heuristic):
        self.graph=graph 
        self.heuristic=heuristic 
        self.tour=[] #a tour is a list of nodes
        self.Tour=Tour() #set Tour object instance
        self.graph.addItem(self.Tour) #add Tour object to scene
    
    def intermediate(self): 
        """starts QTimer2"""
        self.graph.timer2.start(1000) #timeout = 1 sec
      
    def start(self):
        """called each time a change in the graph happens"""
        self.graph.timer2.stop() #stop timer2
        self.graph.timer1.stop() #stop timer1
        self.unvisualizetour(self.Tour) 
        if self.graph.change[0]=="Special" or self.graph.change[0]=='Cursor':
            pass       
        else:
            if self.graph.change[1]== "Node Added.": #if a new node was added
                self.tour.append(self.graph.change[2])
            if self.graph.change[1]=="Node Updated." : #if node was updated
                pass 
            if self.graph.change[1]=="Node Removed.": #if a node was removed
                self.tour.remove(self.graph.change[2])     
        self.Tour.updatePolygon(self.tour)
        self.graph.timer1.singleShot(2000,self.intermediate) #wait for 1 second to see if changes occur
        text=""
        self.graph.Text.update(text)
        self.graph.setBackgroundBrush(QBrush(QColor(0, 168, 107), Qt.SolidPattern)) #Jade
        
    def visualizetour(self, tour):
        """visualizes tour"""
        l=len(self.graph.nodelist)
        if l>=3:
            tour.polygon.setPen(QPen(Qt.blue,0.01,Qt.SolidLine))
           
    def unvisualizetour(self, tour): 
        """unvisualizes tour"""
        l=len(self.graph.nodelist)
        if l>=3:
           tour.polygon.setPen(QPen())
        
    def getcost(self,tour):
        """returns cost of tour"""
        cost=0
        for i in range(-1, len(tour)-1):
            cost+=self.graph.getedge(tour[i],tour[i+1]).getweight()
        return cost
   
    def exchange2opt(self,l, a1,a2): 
        """returns the new tour with exchanged edges
        Takes a list l, with the endpoints of the edges to be exchanged, 
        respectively a1 for edge(a1,a1+1), and a2 for edged(a2,a2+1)
        -------a1,a1+1--------a2,a2+1---------  
           A              B              C     """
        A=l[: a1+1]                           
        B=l[a1+1: a2+1]                     
        C=l[a2+1 :] 
        B.reverse()
        return A+B+C   
    
    def gettuples(self,list):
        """creates a dictionary whose keys are tuples of the form (a,b), 
        where a,b are consecutive elements of the list"""
        s={}
        for i in range(-1,len(list)-1):
            s[(list[i],list[i+1])]=''
        return s
        
    def containsdisablededges(self, list):
        """returns True if the list contains disabled edges; False otherwise"""
        answer=False
        for key in self.graph.disableedgesmap:
            (a,b)=key
            if (a,b) in list or (b,a) in list:
                answer=True
                break
            else:
                pass
        return answer
                            
    def run2Opt(self): 
        """runs 2Opt TSP"""
        self.graph.setBackgroundBrush(QBrush(QColor( 0, 166, 147), Qt.SolidPattern)) #Persian green
        l=len(self.graph.nodelist)
        if l<=2: #number nodes<=2
            self.graph.timer2.stop()   
        else:
            t=self.tour
            T=self.Tour
            print 'start tour', self.getcost(t)
            self.visualizetour(T)
            if l==3: #number nodes==3
                [n1,n2,n3]=t
                e1=self.graph.getedge(n1, n2)
                e2=self.graph.getedge(n2, n3)
                e3=self.graph.getedge(n1, n3)
                if e1.active==False or e2.active==False or e3.active==False:
                    text='No solution is found.'
                    self.graph.Text.update(text)
                    T.polygon.setPen(QPen(Qt.red,0.01,Qt.SolidLine))
                else:
                    len_tour=self.getcost(t)
                    text='Local Optimal ' + str(len_tour)
                    self.graph.Text.update(text)
                self.graph.timer2.stop()
                self.graph.setBackgroundBrush(QBrush(Qt.green, Qt.SolidPattern))
                
                
            if l>3: #number nodes>3
                optimalcost=self.getcost(t) 
                for i in range(len(t)-2):  
                    for j in range(i+2, len(t)):     
                        if j==len(t)-1:
                            a=self.graph.getedge(t[i],t[i+1]) #original edges a, b
                            b=self.graph.getedge(t[j],t[0])
                            c1=a.getweight()+b.getweight()
                            a1=self.graph.getedge(t[i+1],t[0]) #new edges a1, b1, after exchanging two
                            b1=self.graph.getedge(t[i],t[j])
                            c2=a1.getweight()+b1.getweight()
                        else:
                            a=self.graph.getedge(t[i],t[i+1])
                            b=self.graph.getedge(t[j],t[j+1])
                            c1=a.getweight()+b.getweight()
                            a1=self.graph.getedge(t[i+1],t[j+1])
                            b1=self.graph.getedge(t[i],t[j])
                            c2=a1.getweight()+b1.getweight()
                        predicate=(a1.active and b1.active)
                        if c2<c1 and predicate==True: #exchange only if exchanged edges are active
                            print 'inner loop'
                            t_=self.exchange2opt(t,i,j)
                            optimalcost=self.getcost(t_)
                            self.tour=t_ 
                            self.Tour.updatePolygon(t_)
                            print optimalcost           
                if self.tour!=t:
                    print 'outer loop'
                    self.unvisualizetour(T) 
                    t=self.tour
                    print 'tour cost', self.getcost(t)
                    T=self.Tour
                    #self.visualizetour(T)
                    dictuples=self.gettuples(t)
                    ans=self.containsdisablededges(dictuples)
                    if ans==True:
                        text='No current solution'
                        self.graph.Text.update(text)
                        T.polygon.setPen(QPen(Qt.red,0.01,Qt.SolidLine))
                    else:
                         text='Current Solution ' + str(optimalcost)
                         self.graph.Text.update(text)
                         self.visualizetour(T)               
                else:
                    self.graph.timer2.stop()
                    dictuples=self.gettuples(t)
                    ans=self.containsdisablededges(dictuples)
                    if ans==True:
                        text='No solution is found'
                        self.graph.Text.update(text)
                        T.polygon.setPen(QPen(Qt.red,0.01,Qt.SolidLine))
                        #self.unvisualizetour(T)
                    else: 
                        text='Local Optimal ' + str(optimalcost)
                        self.graph.Text.update(text)
                    self.graph.setBackgroundBrush(QBrush(Qt.green, Qt.SolidPattern))
                    
    
        
      
   
