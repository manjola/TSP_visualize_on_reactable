import tuio
import threading

from tuio.objects import Tuio2DCursor
from tuio.objects import Tuio2DObject


class _TuioCallbackListener(tuio.observer.AbstractListener):
    """
    Private Helper Class to react on Tuio Events we get from pytuio

    Sorry, this is very hackish to get things done...
    
    notify is called when an object is added or updated

    notify_remove is called whenever an TUIO alive messages arrive. if this
    happens, whe compare which cursor or objects are still alive and then decide
    to call removeCursor/removeObject callbacks. This is a hack into pytuio as
    the original implementation does not deal with remove-stuff very well.
    If error might occour, please don't hesitate to ask!

    """
    _callback = None
    
    #stores whether a object is active
    _obj_cache = {}

    #stores whether a cursor is active    
    _cur_cache = {}
    
    
    
    def __init__(self, name, subject, callback):
        tuio.observer.AbstractListener.__init__(self, name, subject)
        self._callback = callback


    def notify(self, event):
        """
        This function will be called each time we get a set/update message via
        TUIO. It adds the given object to the cache and calls the right callback
        appropriately
        """

        # get the object we have to process
        obj = event.object
        
        # distinguish between Object and Cursor here
        if isinstance(event.object, Tuio2DObject):

            # check if object has been known before and either call added or
            # updated callbacks
            if obj.sessionid not in self._obj_cache:
                #finally add it to the cache anyway
                self._obj_cache[obj.sessionid] = obj
                self._callback.objectAdded(obj)
            else:
                self._callback.objectUpdated(obj)

        if isinstance(event.object, Tuio2DCursor):

            # check if object has been known before and either call added or
            # updated callbacks
            if obj.sessionid not in self._cur_cache:
                self._callback.cursorAdded(obj)
            else:
                self._callback.cursorUpdated(obj)
            # finally add it to the cache anyway
            self._cur_cache[obj.sessionid] = obj

       # print "NOTIFY", self._cur_cache.keys(), self._obj_cache.keys()


    def notifyRemove(self, event):
        """
        This function will be called each time we receive a TUIO "alive"
        messages which tells us about object removal
        """

        profile, message = event
        alive = message[3:]

        if str(type(profile)) == "<class 'tuio.profiles.Tuio2DcurProfile'>":
            # compare the alive message with current cache and remove all
            # cursors that are not in alive message anymore    
            diff = list(set(self._cur_cache.keys())-set(alive))
            for d in diff:
                self._callback.cursorRemoved(self._cur_cache[d])
                del self._cur_cache[d]

        else:
            # compare the alive message with current object cache and remove all
            # objects that are not in the alive message anymore
            diff = list(set(self._obj_cache.keys())-set(alive))
            for d in diff:
                self._callback.objectRemoved(self._obj_cache[d])
                del self._obj_cache[d]

        #print "NOTIFY_REMOVE: ", self._cur_cache.keys(), self._obj_cache.keys()
            




class TuioCallback(threading.Thread):
    """
    This class handles I/O to reactivision or tuio simulator
    
    It is designed in such a way that in can run in a different thread so that
    you can use another event loop in the mainthread (eg. "main()"-thread).

    This is necessary, as Qt/PySide needs it own eventloop later on.
    We then might inject object-events into Qt's eventloop from this different
    thread.

    Call the run() in order to start processing events. Mind however, that this
    blocks until a TUIO message has been received.

    You can make this class to have it's own thread. See the docs for __init__()
    to understand how. Then you have to call start() in order to start
    processing in a different thread. You can call stop() to leave.

    As CPython implementation uses a global interpreter lock, no race conditions
    actually should happen.

    You finally have to derive from this class and reimplement the callback
    handlers. Here you should implement the way you want to react on TUIO
    messages.

    """


    def __init__(self, host = '127.0.0.1', port = 3333, threaded = False):
        """
        sets up the TuioCallback instance

        parameters:

            host: which address to listen on. localhost by default
            port: the port to listen on
            threaded: decide whether it should be threaded or not.
        """

        # according to python docs we have to call this first
        threading.Thread.__init__(self,group=None, target=None, name=None, args=(), kwargs={})


        self._event = threading.Event()
        self._event.set()

        self._host = host
        self._port = port
        self._tracking = tuio.Tracking(host=host,port=port)
        self._callback = _TuioCallbackListener("Callback",
                                               self._tracking.eventManager,
                                               self)
        self.daemon = False


        
        if threaded:
            self.start()


    def __del__(self):
        self.stop()

    def stop(self):
        """ 
        Call this function to exit the eventloop and let the thread finish.
        """

        self._event.clear()
        
    def run(self):
        """
        This is the function that will be run inside another thread. We need
        this in order for our TuioLister to be event-based (can block when
        reading from sockets)

        You can use this function as simple eventloop as well.
        """
        
        # do infinite loop here
        # _event is stopping condition
        
        self._tracking.update()



    #### Callbacks you have to reimplement

    def objectAdded(self, obj):
        """ implement me """
        raise NotImplementedError("Must subclass me")

    def objectUpdated(self, obj):
        """ implement me """
        raise NotImplementedError("Must subclass me")

    def objectRemoved(self, obj):
        """ implement me """
        raise NotImplementedError("Must subclass me")


    def cursorAdded(self, obj):
        """ implement me """
        raise NotImplementedError("Must subclass me")

    def cursorUpdated(self, obj):
        """ implement me """
        raise NotImplementedError("Must subclass me")

    def cursorRemoved(self, obj):
        """ implement me """
        raise NotImplementedError("Must subclass me")



if __name__ == "__main__":

    # a simple test if threading does work as desired
    tc = TuioCallback(threaded=True)

    try:
        # make the main thread looping forever
        while True:
           pass 
    except KeyboardInterrupt:
        # if you interrupt by keyboard input, stop the thread 
        # aswell
        tc.stop()




