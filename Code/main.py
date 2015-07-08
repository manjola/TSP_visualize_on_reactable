import sys
import traceback
import signal
import tuio
import graph
import tspalgorithm               
import text
import cursor
from tspalgorithm import*
from PySide.QtGui import* 
from PySide.QtCore import* 

# initialize our application instance
app = QApplication(sys.argv)

graph = graph.Graph()

class TuioCallback(tuio.TuioCallback): 
    def __init__(self, graph):
        tuio.TuioCallback.__init__(self, threaded=False)
        self.graph = graph 
        
    def objectAdded(self, obj):
        """deals with adding a tuionode/object"""
        print "ObjectAdded"
        try:
            self.graph.addnode(obj)
        except:
            print "Error." + str(sys.exc_info()[1])
            traceback.print_tb(sys.exc_info()[2])
            exit(0)

    def objectUpdated(self, obj):
        """deals with updating a tuionode/object"""
        print "ObjectUpdated", obj
        try:
            self.graph.updatenode(obj)
        except:
            print "Error." + str(sys.exc_info()[1])
            traceback.print_tb(sys.exc_info()[2])
            exit(0)    

    def objectRemoved(self,obj):
        """deals with removing a tuionode/object"""
        print "ObjectRemoved", obj
        try:
            self.graph.removenode(obj)
        except:
            print "Error." + str(sys.exc_info()[1])
            traceback.print_tb(sys.exc_info()[2])
            exit(0)

    def cursorAdded(self, obj):
        """deals with adding a cursor/finger"""
        print "CursorAdded"
        try:
            self.graph.addcursor(obj)
        except:
            print "Error." + str(sys.exc_info()[1])
            traceback.print_tb(sys.exc_info()[2])
            exit(0)

    def cursorUpdated(self, obj):
        """deals with updating a cursor/finger"""
        print "CursorUpdated", obj
        try:self.graph.updatecursor(obj)
        except:
            print "Error." + str(sys.exc_info()[1])
            traceback.print_tb(sys.exc_info()[2])
            exit(0)    

    def cursorRemoved(self, obj):
        """deals with removing a cursor/finger"""
        print "CursorRemoved", obj
        try:self.graph.removecursor(obj)
        except:
            print "Error." + str(sys.exc_info()[1])
            traceback.print_tb(sys.exc_info()[2])
            exit(0)

# initialize our event handler with the graph instance
mc = TuioCallback(graph)
timer = QTimer()
timer.setInterval(20)
timer.timeout.connect(mc.run)
timer.start()

# set up the scene view
view = QGraphicsView(graph) 
view.resize(1024, 768) #resolution
matrix= QTransform(1024,0,0,768, 0, 0)
view.setTransform(matrix)
view.setSceneRect(0,0,1024,768) 
graph.setBackgroundBrush(QBrush(Qt.black, Qt.SolidPattern)) 
view.show()

# force application to quit when sending SIGINT
signal.signal(signal.SIGINT, signal.SIG_DFL)

# run the main event loop for gui
app.exec_()

# we need to stop our second thread in order to stop the application





