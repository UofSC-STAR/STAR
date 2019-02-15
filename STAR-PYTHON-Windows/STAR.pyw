
from pydub import AudioSegment
from pocketsphinx.pocketsphinx import *
#from sphinxbase.sphinxbase import *
from os import environ,path,chdir,remove
from pydub.utils import make_chunks
import mechanize
import re
from easygui import*
import datetime






############################ GRAPHICS SUPPORT #####################
"""Simple object oriented graphics library  

The library is designed to make it very easy for novice programmers to
experiment with computer graphics in an object oriented fashion. It is
written by John Zelle for use with the book "Python Programming: An
Introduction to Computer Science" (Franklin, Beedle & Associates).

LICENSE: This is open-source software released under the terms of the
GPL (http://www.gnu.org/licenses/gpl.html).

PLATFORMS: The package is a wrapper around Tkinter and should run on
any platform where Tkinter is available.

INSTALLATION: Put this file somewhere where Python can see it.

OVERVIEW: There are two kinds of objects in the library. The GraphWin
class implements a window where drawing can be done and various
GraphicsObjects are provided that can be drawn into a GraphWin. As a
simple example, here is a complete program to draw a circle of radius
10 centered in a 100x100 window:

--------------------------------------------------------------------
from graphics import *

def main():
    win = GraphWin("My Circle", 100, 100)
    c = Circle(Point(50,50), 10)
    c.draw(win)
    win.getMouse() # Pause to view result
    win.close()    # Close window when done

main()
--------------------------------------------------------------------
GraphWin objects support coordinate transformation through the
setCoords method and mouse and keyboard interaction methods.

The library provides the following graphical objects:
    Point
    Line
    Circle
    Oval
    Rectangle
    Polygon
    Text
    Entry (for text-based input)
    Image

Various attributes of graphical objects can be set such as
outline-color, fill-color and line-width. Graphical objects also
support moving and hiding for animation effects.

The library also provides a very simple class for pixel-based image
manipulation, Pixmap. A pixmap can be loaded from a file and displayed
using an Image object. Both getPixel and setPixel methods are provided
for manipulating the image.

DOCUMENTATION: For complete documentation, see Chapter 4 of "Python
Programming: An Introduction to Computer Science" by John Zelle,
published by Franklin, Beedle & Associates.  Also see
http://mcsp.wartburg.edu/zelle/python for a quick reference"""

__version__ = "5.0"

# Version 5 8/26/2016
#     * update at bottom to fix MacOS issue causing askopenfile() to hang
#     * update takes an optional parameter specifying update rate
#     * Entry objects get focus when drawn
#     * __repr_ for all objects
#     * fixed offset problem in window, made canvas borderless

# Version 4.3 4/25/2014
#     * Fixed Image getPixel to work with Python 3.4, TK 8.6 (tuple type handling)
#     * Added interactive keyboard input (getKey and checkKey) to GraphWin
#     * Modified setCoords to cause redraw of current objects, thus
#       changing the view. This supports scrolling around via setCoords.
#
# Version 4.2 5/26/2011
#     * Modified Image to allow multiple undraws like other GraphicsObjects
# Version 4.1 12/29/2009
#     * Merged Pixmap and Image class. Old Pixmap removed, use Image.
# Version 4.0.1 10/08/2009
#     * Modified the autoflush on GraphWin to default to True
#     * Autoflush check on close, setBackground
#     * Fixed getMouse to flush pending clicks at entry
# Version 4.0 08/2009
#     * Reverted to non-threaded version. The advantages (robustness,
#         efficiency, ability to use with other Tk code, etc.) outweigh
#         the disadvantage that interactive use with IDLE is slightly more
#         cumbersome.
#     * Modified to run in either Python 2.x or 3.x (same file).
#     * Added Image.getPixmap()
#     * Added update() -- stand alone function to cause any pending
#           graphics changes to display.
#
# Version 3.4 10/16/07
#     Fixed GraphicsError to avoid "exploded" error messages.
# Version 3.3 8/8/06
#     Added checkMouse method to GraphWin
# Version 3.2.3
#     Fixed error in Polygon init spotted by Andrew Harrington
#     Fixed improper threading in Image constructor
# Version 3.2.2 5/30/05
#     Cleaned up handling of exceptions in Tk thread. The graphics package
#     now raises an exception if attempt is made to communicate with
#     a dead Tk thread.
# Version 3.2.1 5/22/05
#     Added shutdown function for tk thread to eliminate race-condition
#        error "chatter" when main thread terminates
#     Renamed various private globals with _
# Version 3.2 5/4/05
#     Added Pixmap object for simple image manipulation.
# Version 3.1 4/13/05
#     Improved the Tk thread communication so that most Tk calls
#        do not have to wait for synchonization with the Tk thread.
#        (see _tkCall and _tkExec)
# Version 3.0 12/30/04
#     Implemented Tk event loop in separate thread. Should now work
#        interactively with IDLE. Undocumented autoflush feature is
#        no longer necessary. Its default is now False (off). It may
#        be removed in a future version.
#     Better handling of errors regarding operations on windows that
#       have been closed.
#     Addition of an isClosed method to GraphWindow class.

# Version 2.2 8/26/04
#     Fixed cloning bug reported by Joseph Oldham.
#     Now implements deep copy of config info.
# Version 2.1 1/15/04
#     Added autoflush option to GraphWin. When True (default) updates on
#        the window are done after each action. This makes some graphics
#        intensive programs sluggish. Turning off autoflush causes updates
#        to happen during idle periods or when flush is called.
# Version 2.0
#     Updated Documentation
#     Made Polygon accept a list of Points in constructor
#     Made all drawing functions call TK update for easier animations
#          and to make the overall package work better with
#          Python 2.3 and IDLE 1.0 under Windows (still some issues).
#     Removed vestigial turtle graphics.
#     Added ability to configure font for Entry objects (analogous to Text)
#     Added setTextColor for Text as an alias of setFill
#     Changed to class-style exceptions
#     Fixed cloning of Text objects

# Version 1.6
#     Fixed Entry so StringVar uses _root as master, solves weird
#            interaction with shell in Idle
#     Fixed bug in setCoords. X and Y coordinates can increase in
#           "non-intuitive" direction.
#     Tweaked wm_protocol so window is not resizable and kill box closes.

# Version 1.5
#     Fixed bug in Entry. Can now define entry before creating a
#     GraphWin. All GraphWins are now toplevel windows and share
#     a fixed root (called _root).

# Version 1.4
#     Fixed Garbage collection of Tkinter images bug.
#     Added ability to set text atttributes.
#     Added Entry boxes.

import time, os, sys

try:  # import as appropriate for 2.x vs. 3.x
   import tkinter as tk
except:
   import Tkinter as tk


##########################################################################
# Module Exceptions

class GraphicsError(Exception):
    """Generic error class for graphics module exceptions."""
    pass

OBJ_ALREADY_DRAWN = "Object currently drawn"
UNSUPPORTED_METHOD = "Object doesn't support operation"
BAD_OPTION = "Illegal option value"

##########################################################################
# global variables and funtions

_root = tk.Tk()
_root.withdraw()


_update_lasttime = time.time()

def update(rate=None):
    global _update_lasttime
    if rate:
        now = time.time()
        pauseLength = 1/rate-(now-_update_lasttime)
        if pauseLength > 0:
            time.sleep(pauseLength)
            _update_lasttime = now + pauseLength
        else:
            _update_lasttime = now

    _root.update()

############################################################################
# Graphics classes start here


        
class GraphWin(tk.Canvas):


    """A GraphWin is a toplevel window for displaying graphics."""

    def __init__(self, title="Graphics Window",
                 width=200, height=200, autoflush=True):
        assert type(title) == type(""), "Title must be a string"
        master = tk.Toplevel(_root)
        master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Canvas.__init__(self, master, width=width, height=height,
                           highlightthickness=0, bd=0)
        self.master.title(title)
        self.pack()
        master.resizable(0,0)
        self.foreground = "black"
        self.items = []
        self.mouseX = None
        self.mouseY = None
        self.bind("<Button-1>", self._onClick)
        self.bind_all("<Key>", self._onKey)
        self.height = int(height)
        self.width = int(width)
        self.autoflush = autoflush
        self._mouseCallback = None
        self.trans = None
        self.closed = False
        master.lift()
        self.lastKey = ""

        if autoflush: _root.update()

    def __repr__(self):
        if self.isClosed():
            return "<Closed GraphWin>"
        else:
            return "GraphWin('{}', {}, {})".format(self.master.title(),
                                             self.getWidth(),
                                             self.getHeight())

    def __str__(self):
        return repr(self)
     
    def __checkOpen(self):
        if self.closed:
            raise GraphicsError("window is closed")

    def _onKey(self, evnt):
        self.lastKey = evnt.keysym


    def setBackground(self, color):
        """Set background color of the window"""
        self.__checkOpen()
        self.config(bg=color)
        self.__autoflush()
        
    def setCoords(self, x1, y1, x2, y2):
        """Set coordinates of window to run from (x1,y1) in the
        lower-left corner to (x2,y2) in the upper-right corner."""
        self.trans = Transform(self.width, self.height, x1, y1, x2, y2)
        self.redraw()

    def close(self):
        """Close the window"""

        if self.closed: return
        self.closed = True
        self.master.destroy()
        self.__autoflush()


    def isClosed(self):
        return self.closed


    def isOpen(self):
        return not self.closed


    def __autoflush(self):
        if self.autoflush:
            _root.update()

    
    def plot(self, x, y, color="black"):
        """Set pixel (x,y) to the given color"""
        self.__checkOpen()
        xs,ys = self.toScreen(x,y)
        self.create_line(xs,ys,xs+1,ys, fill=color)
        self.__autoflush()
        
    def plotPixel(self, x, y, color="black"):
        """Set pixel raw (independent of window coordinates) pixel
        (x,y) to color"""
        self.__checkOpen()
        self.create_line(x,y,x+1,y, fill=color)
        self.__autoflush()
      
    def flush(self):
        """Update drawing to the window"""
        self.__checkOpen()
        self.update_idletasks()
        
    def getMouse(self):
        """Wait for mouse click and return Point object representing
        the click"""
        self.update()      # flush any prior clicks
        self.mouseX = None
        self.mouseY = None
        while self.mouseX == None or self.mouseY == None:
            self.update()
            if self.isClosed(): raise GraphicsError("getMouse in closed window")
            time.sleep(.1) # give up thread
        x,y = self.toWorld(self.mouseX, self.mouseY)
        self.mouseX = None
        self.mouseY = None
        return Point(x,y)

    def checkMouse(self):
        """Return last mouse click or None if mouse has
        not been clicked since last call"""
        if self.isClosed():
            raise GraphicsError("checkMouse in closed window")
        self.update()
        if self.mouseX != None and self.mouseY != None:
            x,y = self.toWorld(self.mouseX, self.mouseY)
            self.mouseX = None
            self.mouseY = None
            return Point(x,y)
        else:
            return None

    def getKey(self):
        """Wait for user to press a key and return it as a string."""
        self.lastKey = ""
        while self.lastKey == "":
            self.update()
            if self.isClosed(): raise GraphicsError("getKey in closed window")
            time.sleep(.1) # give up thread

        key = self.lastKey
        self.lastKey = ""
        return key

    def checkKey(self):
        """Return last key pressed or None if no key pressed since last call"""
        if self.isClosed():
            raise GraphicsError("checkKey in closed window")
        self.update()
        key = self.lastKey
        self.lastKey = ""
        return key
            
    def getHeight(self):
        """Return the height of the window"""
        return self.height
        
    def getWidth(self):
        """Return the width of the window"""
        return self.width
    
    def toScreen(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.screen(x,y)
        else:
            return x,y
                      
    def toWorld(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.world(x,y)
        else:
            return x,y
        
    def setMouseHandler(self, func):
        self._mouseCallback = func
        
    def _onClick(self, e):
        self.mouseX = e.x
        self.mouseY = e.y
        if self._mouseCallback:
            self._mouseCallback(Point(e.x, e.y))

    def addItem(self, item):
        self.items.append(item)

    def delItem(self, item):
        self.items.remove(item)

    def redraw(self):
        for item in self.items[:]:
            item.undraw()
            item.draw(self)
        self.update()
        
                      
class Transform:

    """Internal class for 2-D coordinate transformations"""
    
    def __init__(self, w, h, xlow, ylow, xhigh, yhigh):
        # w, h are width and height of window
        # (xlow,ylow) coordinates of lower-left [raw (0,h-1)]
        # (xhigh,yhigh) coordinates of upper-right [raw (w-1,0)]
        xspan = (xhigh-xlow)
        yspan = (yhigh-ylow)
        self.xbase = xlow
        self.ybase = yhigh
        self.xscale = xspan/float(w-1)
        self.yscale = yspan/float(h-1)
        
    def screen(self,x,y):
        # Returns x,y in screen (actually window) coordinates
        xs = (x-self.xbase) / self.xscale
        ys = (self.ybase-y) / self.yscale
        return int(xs+0.5),int(ys+0.5)
        
    def world(self,xs,ys):
        # Returns xs,ys in world coordinates
        x = xs*self.xscale + self.xbase
        y = self.ybase - ys*self.yscale
        return x,y


# Default values for various item configuration options. Only a subset of
#   keys may be present in the configuration dictionary for a given item
DEFAULT_CONFIG = {"fill":"",
      "outline":"black",
      "width":"1",
      "arrow":"none",
      "text":"",
      "justify":"center",
                  "font": ("helvetica", 12, "normal")}

class GraphicsObject:

    """Generic base class for all of the drawable objects"""
    # A subclass of GraphicsObject should override _draw and
    #   and _move methods.
    
    def __init__(self, options):
        # options is a list of strings indicating which options are
        # legal for this object.
        
        # When an object is drawn, canvas is set to the GraphWin(canvas)
        #    object where it is drawn and id is the TK identifier of the
        #    drawn shape.
        self.canvas = None
        self.id = None

        # config is the dictionary of configuration options for the widget.
        config = {}
        for option in options:
            config[option] = DEFAULT_CONFIG[option]
        self.config = config
        
    def setFill(self, color):
        """Set interior color to color"""
        self._reconfig("fill", color)
        
    def setOutline(self, color):
        """Set outline color to color"""
        self._reconfig("outline", color)
        
    def setWidth(self, width):
        """Set line weight to width"""
        self._reconfig("width", width)

    def draw(self, graphwin):

        """Draw the object in graphwin, which should be a GraphWin
        object.  A GraphicsObject may only be drawn into one
        window. Raises an error if attempt made to draw an object that
        is already visible."""

        if self.canvas and not self.canvas.isClosed(): raise GraphicsError(OBJ_ALREADY_DRAWN)
        if graphwin.isClosed(): raise GraphicsError("Can't draw to closed window")
        self.canvas = graphwin
        self.id = self._draw(graphwin, self.config)
        graphwin.addItem(self)
        if graphwin.autoflush:
            _root.update()
        return self

            
    def undraw(self):

        """Undraw the object (i.e. hide it). Returns silently if the
        object is not currently drawn."""
        
        if not self.canvas: return
        if not self.canvas.isClosed():
            self.canvas.delete(self.id)
            self.canvas.delItem(self)
            if self.canvas.autoflush:
                _root.update()
        self.canvas = None
        self.id = None


    def move(self, dx, dy):

        """move object dx units in x direction and dy units in y
        direction"""
        
        self._move(dx,dy)
        canvas = self.canvas
        if canvas and not canvas.isClosed():
            trans = canvas.trans
            if trans:
                x = dx/ trans.xscale 
                y = -dy / trans.yscale
            else:
                x = dx
                y = dy
            self.canvas.move(self.id, x, y)
            if canvas.autoflush:
                _root.update()
           
    def _reconfig(self, option, setting):
        # Internal method for changing configuration of the object
        # Raises an error if the option does not exist in the config
        #    dictionary for this object
        if option not in self.config:
            raise GraphicsError(UNSUPPORTED_METHOD)
        options = self.config
        options[option] = setting
        if self.canvas and not self.canvas.isClosed():
            self.canvas.itemconfig(self.id, options)
            if self.canvas.autoflush:
                _root.update()


    def _draw(self, canvas, options):
        """draws appropriate figure on canvas with options provided
        Returns Tk id of item drawn"""
        pass # must override in subclass


    def _move(self, dx, dy):
        """updates internal state of object to move it dx,dy units"""
        pass # must override in subclass

         
class Point(GraphicsObject):
    def __init__(self, x, y):
        GraphicsObject.__init__(self, ["outline", "fill"])
        self.setFill = self.setOutline
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)
        
    def _draw(self, canvas, options):
        x,y = canvas.toScreen(self.x,self.y)
        return canvas.create_rectangle(x,y,x+1,y+1,options)
        
    def _move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
        
    def clone(self):
        other = Point(self.x,self.y)
        other.config = self.config.copy()
        return other
                
    def getX(self): return self.x
    def getY(self): return self.y

class _BBox(GraphicsObject):
    # Internal base class for objects represented by bounding box
    # (opposite corners) Line segment is a degenerate case.
    
    def __init__(self, p1, p2, options=["outline","width","fill"]):
        GraphicsObject.__init__(self, options)
        self.p1 = p1.clone()
        self.p2 = p2.clone()

    def _move(self, dx, dy):
        self.p1.x = self.p1.x + dx
        self.p1.y = self.p1.y + dy
        self.p2.x = self.p2.x + dx
        self.p2.y = self.p2.y  + dy
                
    def getP1(self): return self.p1.clone()

    def getP2(self): return self.p2.clone()
    
    def getCenter(self):
        p1 = self.p1
        p2 = self.p2
        return Point((p1.x+p2.x)/2.0, (p1.y+p2.y)/2.0)

    
class Rectangle(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)

    def __repr__(self):
        return "Rectangle({}, {})".format(str(self.p1), str(self.p2))
    
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_rectangle(x1,y1,x2,y2,options)
        
    def clone(self):
        other = Rectangle(self.p1, self.p2)
        other.config = self.config.copy()
        return other


class Oval(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)

    def __repr__(self):
        return "Oval({}, {})".format(str(self.p1), str(self.p2))

        
    def clone(self):
        other = Oval(self.p1, self.p2)
        other.config = self.config.copy()
        return other
   
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_oval(x1,y1,x2,y2,options)
    
class Circle(Oval):
    
    def __init__(self, center, radius):
        p1 = Point(center.x-radius, center.y-radius)
        p2 = Point(center.x+radius, center.y+radius)
        Oval.__init__(self, p1, p2)
        self.radius = radius

    def __repr__(self):
        return "Circle({}, {})".format(str(self.getCenter()), str(self.radius))
        
    def clone(self):
        other = Circle(self.getCenter(), self.radius)
        other.config = self.config.copy()
        return other
        
    def getRadius(self):
        return self.radius

                  
class Line(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2, ["arrow","fill","width"])
        self.setFill(DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill

    def __repr__(self):
        return "Line({}, {})".format(str(self.p1), str(self.p2))

    def clone(self):
        other = Line(self.p1, self.p2)
        other.config = self.config.copy()
        return other
  
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_line(x1,y1,x2,y2,options)
        
    def setArrow(self, option):
        if not option in ["first","last","both","none"]:
            raise GraphicsError(BAD_OPTION)
        self._reconfig("arrow", option)
        

class Polygon(GraphicsObject):
    
    def __init__(self, *points):
        # if points passed as a list, extract it
        if len(points) == 1 and type(points[0]) == type([]):
            points = points[0]
        self.points = list(map(Point.clone, points))
        GraphicsObject.__init__(self, ["outline", "width", "fill"])

    def __repr__(self):
        return "Polygon"+str(tuple(p for p in self.points))
        
    def clone(self):
        other = Polygon(*self.points)
        other.config = self.config.copy()
        return other

    def getPoints(self):
        return list(map(Point.clone, self.points))

    def _move(self, dx, dy):
        for p in self.points:
            p.move(dx,dy)
   
    def _draw(self, canvas, options):
        args = [canvas]
        for p in self.points:
            x,y = canvas.toScreen(p.x,p.y)
            args.append(x)
            args.append(y)
        args.append(options)
        return GraphWin.create_polygon(*args) 

class Text(GraphicsObject):
    
    def __init__(self, p, text):
        GraphicsObject.__init__(self, ["justify","fill","text","font"])
        self.setText(text)
        self.anchor = p.clone()
        self.setFill(DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill

    def __repr__(self):
        return "Text({}, '{}')".format(self.anchor, self.getText())
    
    def _draw(self, canvas, options):
        p = self.anchor
        x,y = canvas.toScreen(p.x,p.y)
        return canvas.create_text(x,y,options)
        
    def _move(self, dx, dy):
        self.anchor.move(dx,dy)
        
    def clone(self):
        other = Text(self.anchor, self.config['text'])
        other.config = self.config.copy()
        return other

    def setText(self,text):
        self._reconfig("text", text)
        
    def getText(self):
        return self.config["text"]
            
    def getAnchor(self):
        return self.anchor.clone()

    def setFace(self, face):
        if face in ['helvetica','arial','courier','times roman']:
            f,s,b = self.config['font']
            self._reconfig("font",(face,s,b))
        else:
            raise GraphicsError(BAD_OPTION)

    def setSize(self, size):
        if 5 <= size <= 36:
            f,s,b = self.config['font']
            self._reconfig("font", (f,size,b))
        else:
            raise GraphicsError(BAD_OPTION)

    def setStyle(self, style):
        if style in ['bold','normal','italic', 'bold italic']:
            f,s,b = self.config['font']
            self._reconfig("font", (f,s,style))
        else:
            raise GraphicsError(BAD_OPTION)

    def setTextColor(self, color):
        self.setFill(color)


class Entry(GraphicsObject):

    def __init__(self, p, width):
        GraphicsObject.__init__(self, [])
        self.anchor = p.clone()
        #print self.anchor
        self.width = width
        self.text = tk.StringVar(_root)
        self.text.set("")
        self.fill = "gray"
        self.color = "black"
        self.font = DEFAULT_CONFIG['font']
        self.entry = None

    def __repr__(self):
        return "Entry({}, {})".format(self.anchor, self.width)

    def _draw(self, canvas, options):
        p = self.anchor
        x,y = canvas.toScreen(p.x,p.y)
        frm = tk.Frame(canvas.master)
        self.entry = tk.Entry(frm,
                              width=self.width,
                              textvariable=self.text,
                              bg = self.fill,
                              fg = self.color,
                              font=self.font)
        self.entry.pack()
        #self.setFill(self.fill)
        self.entry.focus_set()
        return canvas.create_window(x,y,window=frm)

    def getText(self):
        return self.text.get()

    def _move(self, dx, dy):
        self.anchor.move(dx,dy)

    def getAnchor(self):
        return self.anchor.clone()

    def clone(self):
        other = Entry(self.anchor, self.width)
        other.config = self.config.copy()
        other.text = tk.StringVar()
        other.text.set(self.text.get())
        other.fill = self.fill
        return other

    def setText(self, t):
        self.text.set(t)

            
    def setFill(self, color):
        self.fill = color
        if self.entry:
            self.entry.config(bg=color)

            
    def _setFontComponent(self, which, value):
        font = list(self.font)
        font[which] = value
        self.font = tuple(font)
        if self.entry:
            self.entry.config(font=self.font)


    def setFace(self, face):
        if face in ['helvetica','arial','courier','times roman']:
            self._setFontComponent(0, face)
        else:
            raise GraphicsError(BAD_OPTION)

    def setSize(self, size):
        if 5 <= size <= 36:
            self._setFontComponent(1,size)
        else:
            raise GraphicsError(BAD_OPTION)

    def setStyle(self, style):
        if style in ['bold','normal','italic', 'bold italic']:
            self._setFontComponent(2,style)
        else:
            raise GraphicsError(BAD_OPTION)

    def setTextColor(self, color):
        self.color=color
        if self.entry:
            self.entry.config(fg=color)


class Image(GraphicsObject):

    idCount = 0
    imageCache = {} # tk photoimages go here to avoid GC while drawn 
    
    def __init__(self, p, *pixmap):
        GraphicsObject.__init__(self, [])
        self.anchor = p.clone()
        self.imageId = Image.idCount
        Image.idCount = Image.idCount + 1
        if len(pixmap) == 1: # file name provided
            self.img = tk.PhotoImage(file=pixmap[0], master=_root)
        else: # width and height provided
            width, height = pixmap
            self.img = tk.PhotoImage(master=_root, width=width, height=height)

    def __repr__(self):
        return "Image({}, {}, {})".format(self.anchor, self.getWidth(), self.getHeight())
                
    def _draw(self, canvas, options):
        p = self.anchor
        x,y = canvas.toScreen(p.x,p.y)
        self.imageCache[self.imageId] = self.img # save a reference  
        return canvas.create_image(x,y,image=self.img)
    
    def _move(self, dx, dy):
        self.anchor.move(dx,dy)
        
    def undraw(self):
        try:
            del self.imageCache[self.imageId]  # allow gc of tk photoimage
        except KeyError:
            pass
        GraphicsObject.undraw(self)

    def getAnchor(self):
        return self.anchor.clone()
        
    def clone(self):
        other = Image(Point(0,0), 0, 0)
        other.img = self.img.copy()
        other.anchor = self.anchor.clone()
        other.config = self.config.copy()
        return other

    def getWidth(self):
        """Returns the width of the image in pixels"""
        return self.img.width() 

    def getHeight(self):
        """Returns the height of the image in pixels"""
        return self.img.height()

    def getPixel(self, x, y):
        """Returns a list [r,g,b] with the RGB color values for pixel (x,y)
        r,g,b are in range(256)

        """
        
        value = self.img.get(x,y) 
        if type(value) ==  type(0):
            return [value, value, value]
        elif type(value) == type((0,0,0)):
            return list(value)
        else:
            return list(map(int, value.split())) 

    def setPixel(self, x, y, color):
        """Sets pixel (x,y) to the given color
        
        """
        self.img.put("{" + color +"}", (x, y))
        

    def save(self, filename):
        """Saves the pixmap image to filename.
        The format for the save image is determined from the filname extension.

        """
        
        path, name = os.path.split(filename)
        ext = name.split(".")[-1]
        self.img.write( filename, format=ext)

        
def color_rgb(r,g,b):
    """r,g,b are intensities of red, green, and blue in range(256)
    Returns color specifier string for the resulting color"""
    return "#%02x%02x%02x" % (r,g,b)

def test():
    win = GraphWin()
    win.setCoords(0,0,10,10)
    t = Text(Point(5,5), "Centered Text")
    t.draw(win)
    p = Polygon(Point(1,1), Point(5,3), Point(2,7))
    p.draw(win)
    e = Entry(Point(5,6), 10)
    e.draw(win)
    win.getMouse()
    p.setFill("red")
    p.setOutline("blue")
    p.setWidth(2)
    s = ""
    for pt in p.getPoints():
        s = s + "(%0.1f,%0.1f) " % (pt.getX(), pt.getY())
    t.setText(e.getText())
    e.setFill("green")
    e.setText("Spam!")
    e.move(2,0)
    win.getMouse()
    p.move(2,3)
    s = ""
    for pt in p.getPoints():
        s = s + "(%0.1f,%0.1f) " % (pt.getX(), pt.getY())
    t.setText(s)
    win.getMouse()
    p.undraw()
    e.undraw()
    t.setStyle("bold")
    win.getMouse()
    t.setStyle("normal")
    win.getMouse()
    t.setStyle("italic")
    win.getMouse()
    t.setStyle("bold italic")
    win.getMouse()
    t.setSize(14)
    win.getMouse()
    t.setFace("arial")
    t.setSize(20)
    win.getMouse()
    win.close()

#MacOS fix 2
#tk.Toplevel(_root).destroy()

# MacOS fix 1
update()




########################################
######## BUILD FILES TO TRACK ##########
########################################
def buildtrack():
	chdir('./bin')
	ps1=open('tracking.txt','r')
	fn=[]
	dt=[]
	wttr=[]
	cptr=[]

	cou=0
	for line in ps1:
		cou=cou+1
		pss=list(line)
		#print(pss)
		if pss[0]!='#' and pss[0]!='\n':
			if pss[0]=='f':
				poo=pss[1]
				for i in range(2,len(pss)):
					if pss[i]!='\n':
						poo=poo+pss[i]
				fn.append(poo)

			if pss[0]=='w':
				poo=pss[1]
				for i in range(2,len(pss)):
					if pss[i]!='\n':
						poo=poo+pss[i]
				wttr.append(poo)

			if pss[0]=='c':
				poo=pss[1]
				for i in range(2,len(pss)):
					if pss[i]!='\n':
						poo=poo+pss[i]
				cptr.append(poo)

			if pss[0]=='d':
				poo=pss[1]
				for i in range(2,len(pss)):
					if pss[i]!='\n':
						poo=poo+pss[i]
				dt.append(poo)
				
	ps1.close()
	chdir('../')
	
	return fn, dt, wttr,cptr



########################################
############ BUILD DATE ################
########################################
def builddate(dty,dtm,dtd):
	dt=[]
	for i in range(0,len(dty)):
		dt.append(str(dtm[i])+'-'+str(dtd[i])+'-'+str(dty[i]))
		
	return dt

#########################################
#############UPDATE DATA ################
########################################
def updata(fn,dt,wttr,cptr):
	chdir('./bin')
	ps1=open('tracking.txt','w')
	ps1.write('######## TRACKING #######'+'\n')
	for i in range(0,len(fn)):
		ps1.write('f'+fn[i]+'\n')
		ps1.write('d'+dt[i]+'\n')
		ps1.write('w'+str(wttr[i])+'\n')
		ps1.write('c'+str(cptr[i])+'\n')
	
	
	
	
	ps1.close()
	chdir('../')




#########################################
############## Data Viewer ##############
#########################################
def view(title,ddt,dd):
	winv = GraphWin(title, 600, 400)
	winv.setBackground('white')
	winv.setCoords(0.0,25.0,12.0,0.0)
	
	advset=Text(Point(6,1.3),title)
	advset.setSize(25)
	advset.setStyle('bold')
	advset.setFace('courier')
	advset.setTextColor('red')
	advset.draw(winv)
	
	xaxis=Line(Point(0.5,20),Point(11.5,20))
	xaxis.draw(winv)
	
	xlab=Text(Point(.7,1),'Sec')
	xlab.draw(winv)
	
	yaxis=Line(Point(1,1.8),Point(1,20.5))
	yaxis.draw(winv)
	
	sizedata=len(ddt)
	
	dtm=[]
	dtd=[]
	dty=[]
	for i in range(0,len(ddt)):
		poo=ddt[i].split('-')
		dtm.append(int(poo[0]))
		dtd.append(int(poo[1]))
		dty.append(int(poo[2]))

			
	pimy1=[]
	for i in range(0,len(dty)):
		if dty[i] not in pimy1:
			pimy1.append(dty[i])

	pimfix=[]
	for i in range(0,len(pimy1)):
		pimfix.append([])
		
	for i in range(0,13):
		for k in range(0,len(pimy1)):
			pimfix[k].append([])
			for j in range(0,32):
				pimfix[k][i].append([])
			

			
	for i in range(0,len(dtm)):
		for m in range(0,13):
			if dtm[i]==m+1:
				for d in range(0,32):
					if dtd[i]==d+1:
						for y in range(0,len(pimy1)):
							if dty[i]==pimy1[y]:
								pimfix[y][m][d].append(i)



	makesense=[]
	for i in range(0,len(dtm)):
		makesense.append(0)

	countdrac=0
	for y in range(0,len(pimy1)):
		for m in range(0,13):
			for d in range(0,32):
				if len(pimfix[y][m][d])!=0:
					countdrac=countdrac+1
					for i in range(0,len(pimfix[y][m][d])):
						makesense[pimfix[y][m][d][i]]=countdrac
	hellno=[]
	for i in range(0,len(makesense)):
		if makesense[i] not in hellno:
			hellno.append(makesense[i])

	numpoints=len(hellno)
	scalegraphx=float(float(10.5)/(numpoints-1))

	hellyes=[]
	for i in range(0,numpoints):
		hellyes.append([])
	
	for i in range(0,len(makesense)):
		hellyes[makesense[i]-1].append(i)

		

	
	points=[]
	for i in range(0,numpoints):
	
		if len(hellyes[i])!=1:
			tot=0
			#print(type(tot))
			for j in range(0,len(hellyes[i])):
				#print(type(hellyes[i][j]))
				#print(hellyes[i][j])
				tot=tot+hellyes[i][j]
			points.append(float(tot)/len(hellyes[i]))
		else:
			points.append(float(dd[hellyes[i][0]]))

	scaley=float(15)/max(points)			
	for i in range(0,numpoints-1):
		ser=Line(Point(1+i*scalegraphx,19-(points[i]*scaley)),Point(1+(i+1)*scalegraphx,19-(points[i+1]*scaley)))
		ser.draw(winv)
	
	toppoint=19-(max(points)*scaley)
	botpoint=19-(min(points)*scaley)
	tophatL=Line(Point(1-.15,toppoint),Point(1.2,toppoint))
	tophatL.draw(winv)
	
	tophatN=Text(Point(.45,toppoint),str(int(max(points))))
	tophatN.draw(winv)
	
	bothatL=Line(Point(1-.15,botpoint),Point(1.2,botpoint))
	bothatL.draw(winv)
	
	bothatN=Text(Point(.45,botpoint),str(int(min(points))))
	bothatN.draw(winv)
	
	d1=str(dtm[hellyes[0][0]])+'-'+str(dtd[hellyes[0][0]])
	date1=Text(Point(1,21),d1)
	date1.draw(winv)
	
	d2=str(dtm[hellyes[len(hellyes)-1][0]])+'-'+str(dtd[hellyes[len(hellyes)-1][0]])
	date2=Text(Point(11,21),d2)
	date2.draw(winv)
	
	dateL=Line(Point(11,20.3),Point(11,19.6))
	dateL.draw(winv)
	
	
	#test1=Text(Point(6,6.3),scaley)
	#test1.setSize(25)
	#test1.draw(winv)
	winv.getMouse()
	
#############################################
################ EDIT TRACKING ############
#############################################
def edittracker(title,dty,dtm,dtd,fn,wttr,cptr):
	wine = GraphWin(title, 500, 600)
	wine.setBackground('white')
	wine.setCoords(0.0,25.0,12.0,0.0)
	
	advset=Text(Point(6,1.3),title)
	advset.setSize(25)
	advset.setStyle('bold')
	advset.setFace('courier')
	advset.setTextColor('red')
	advset.draw(wine)
	
	
	sets=(len(fn)/5)+1
	
	tootfn=[]
	tootdtm=[]
	tootdty=[]
	tootdtd=[]
	for i in range(0,sets):
		tootfn.append([])
		tootdtm.append([])
		tootdty.append([])
		tootdtd.append([])
		

	for i in range(0,sets):
		for j in range(0,5):
			if i*5+j<len(fn):
				tootfn[i].append(fn[i*5+j])
				tootdtm[i].append(dtm[i*5+j])
				tootdty[i].append(dty[i*5+j])
				tootdtd[i].append(dtd[i*5+j])
			
		
			
		
	weat=0

	
	file1=Text(Point(4,6),'')
	file1.draw(wine)
	file2=Text(Point(4,9),'')
	file2.draw(wine)
	file3=Text(Point(4,12),'')
	file3.draw(wine)
	file4=Text(Point(4,15),'')
	file4.draw(wine)
	file5=Text(Point(4,18),'')
	file5.draw(wine)
	
	if len(tootfn[weat])!=0:
		file1.setText(tootfn[weat][0])
	if len(tootfn[weat])>1:
		file2.setText(tootfn[weat][1])
	if len(tootfn[weat])>2:
		file3.setText(tootfn[weat][2])
	if len(tootfn[weat])>3:
		file4.setText(tootfn[weat][3])
	if len(tootfn[weat])>4:
		file5.setText(tootfn[weat][4])
	
	
	
	
	if len(tootfn[weat])!=0:
		Edtm1=Entry(Point(7,6),2)
		Edtm1.draw(wine)
	if len(tootfn[weat])>1:
		Edtm2=Entry(Point(7,9),2)
		Edtm2.draw(wine)
	if len(tootfn[weat])>2:
		Edtm3=Entry(Point(7,12),2)
		Edtm3.draw(wine)
	if len(tootfn[weat])>3:
		Edtm4=Entry(Point(7,15),2)
		Edtm4.draw(wine)
	if len(tootfn[weat])>4:
		Edtm5=Entry(Point(7,18),2)
		Edtm5.draw(wine)
		
	if len(tootfn[weat])!=0:
		Edtd1=Entry(Point(8.5,6),2)
		Edtd1.draw(wine)
	if len(tootfn[weat])>1:
		Edtd2=Entry(Point(8.5,9),2)
		Edtd2.draw(wine)
	if len(tootfn[weat])>2:
		Edtd3=Entry(Point(8.5,12),2)
		Edtd3.draw(wine)
	if len(tootfn[weat])>3:
		Edtd4=Entry(Point(8.5,15),2)
		Edtd4.draw(wine)
	if len(tootfn[weat])>4:
		Edtd5=Entry(Point(8.5,18),2)
		Edtd5.draw(wine)
		
	if len(tootfn[weat])!=0:
		Edty1=Entry(Point(10.7,6),4)
		Edty1.draw(wine)
	if len(tootfn[weat])>1:
		Edty2=Entry(Point(10.7,9),4)
		Edty2.draw(wine)
	if len(tootfn[weat])>2:
		Edty3=Entry(Point(10.7,12),4)
		Edty3.draw(wine)
	if len(tootfn[weat])>3:
		Edty4=Entry(Point(10.7,15),4)
		Edty4.draw(wine)
	if len(tootfn[weat])>4:
		Edty5=Entry(Point(10.7,18),4)
		Edty5.draw(wine)
		
		
	if len(tootfn[weat])!=0:
		Edtm1.setText(tootdtm[weat][0])
	if len(tootfn[weat])>1:
		Edtm2.setText(tootdtm[weat][1])
	if len(tootfn[weat])>2:
		Edtm3.setText(tootdtm[weat][2])
	if len(tootfn[weat])>3:
		Edtm4.setText(tootdtm[weat][3])
	if len(tootfn[weat])>4:
		Edtm5.setText(tootdtm[weat][4])
		
	if len(tootfn[weat])!=0:
		Edtd1.setText(tootdtd[weat][0])
	if len(tootfn[weat])>1:
		Edtd2.setText(tootdtd[weat][1])
	if len(tootfn[weat])>2:
		Edtd3.setText(tootdtd[weat][2])
	if len(tootfn[weat])>3:
		Edtd4.setText(tootdtd[weat][3])
	if len(tootfn[weat])>4:
		Edtd5.setText(tootdtd[weat][4])
		
		
	if len(tootfn[weat])!=0:
		Edty1.setText(tootdty[weat][0])
	if len(tootfn[weat])>1:
		Edty2.setText(tootdty[weat][1])
	if len(tootfn[weat])>2:
		Edty3.setText(tootdty[weat][2])
	if len(tootfn[weat])>3:
		Edty4.setText(tootdty[weat][3])
	if len(tootfn[weat])>4:
		Edty5.setText(tootdty[weat][4])
		
	
	############ SAVE BUTTON ########################
	exitbttn=Rectangle(Point(4.3,22.4),Point(7.8,24.3))
	exitbttn.setFill('green1')
	exitb=Text(Point(6,23.4),'Save Changes')
	exitbttn.draw(wine)
	exitb.draw(wine)
	
	
	########### NEXT BUTTON #######################
	nextbttn=Rectangle(Point(9.3,23),Point(10.8,24))
	nextbttn.setFill('yellow')
	nextbttn.draw(wine)
	nexttxt=Text(Point(10.1,23.5),'Next>>')
	nexttxt.draw(wine)
	
	ffn=Text(Point(4,3),'File Name')
	ffn.draw(wine)
	
	fdm=Text(Point(6.9,3),'Month')
	fdm.draw(wine)
	
	fdd=Text(Point(8.5,3),'Day')
	fdd.draw(wine)
	
	fdy=Text(Point(10.7,3),'Year')
	fdy.draw(wine)
	
	
	chachanges=True
	while chachanges:
	
		ch=wine.getMouse()
		
		############### Press SAVE #################
		if 4.3<=ch.getX()<=7.8 and 22.4<=ch.getY()<=24.3:
			if len(tootfn[weat])!=0 and 0<int(Edtm1.getText())<=12:
				dtm[weat]=int(Edtm1.getText())
			if len(tootfn[weat])>1 :
				dtm[weat+1]=int(Edtm2.getText())
			if len(tootfn[weat])>2 and 0<int(Edtm1.getText())<=12:
				dtm[weat+2]=int(Edtm3.getText())
			if len(tootfn[weat])>3 and 0<int(Edtm1.getText())<=12:
				dtm[weat+3]=int(Edtm4.getText())
			if len(tootfn[weat])>4 and 0<int(Edtm1.getText())<=12:
				dtm[weat+4]=int(Edtm5.getText())
				
			if len(tootfn[weat])!=0 and 2000<int(Edty1.getText()):
				dty[weat]=int(Edty1.getText())
			if len(tootfn[weat])>1 and 2000<int(Edty1.getText()):
				dty[weat+1]=int(Edty2.getText())
			if len(tootfn[weat])>2 and 2000<int(Edty1.getText()):
				dty[weat+2]=int(Edty3.getText())
			if len(tootfn[weat])>3 and 2000<int(Edty1.getText()):
				dty[weat+3]=int(Edty4.getText())
			if len(tootfn[weat])>4 and 2000<int(Edty1.getText()):
				dty[weat+4]=int(Edty5.getText())			
			
			
			if len(tootfn[weat])!=0 and 0<int(Edtd1.getText())<=31:
				dtd[weat]=int(Edtd1.getText())
			if len(tootfn[weat])>1 and 0<int(Edtd1.getText())<=31:
				dtd[weat+1]=int(Edtd2.getText())
			if len(tootfn[weat])>2 and 0<int(Edtd1.getText())<=31:
				dtd[weat+2]=int(Edtd3.getText())
			if len(tootfn[weat])>3 and 0<int(Edtd1.getText())<=31:
				dtd[weat+3]=int(Edtd4.getText())
			if len(tootfn[weat])>4 and 0<int(Edtd1.getText())<=31:
				dtd[weat+4]=int(Edtd5.getText())
				
			
			dt=builddate(dty,dtm,dtd)
			#also update!
			updata(fn,dt,wttr,cptr)
			
	
			
		
			

		
		
		############### Press Next ##################
		if 9.3<=ch.getX()<=10.8 and 23<=ch.getY()<=24:
			if len(tootfn[weat])!=0 and 0<int(Edtm1.getText())<=12:
				dtm[weat]=int(Edtm1.getText())
			if len(tootfn[weat])>1 :
				dtm[weat+1]=int(Edtm2.getText())
			if len(tootfn[weat])>2 and 0<int(Edtm1.getText())<=12:
				dtm[weat+2]=int(Edtm3.getText())
			if len(tootfn[weat])>3 and 0<int(Edtm1.getText())<=12:
				dtm[weat+3]=int(Edtm4.getText())
			if len(tootfn[weat])>4 and 0<int(Edtm1.getText())<=12:
				dtm[weat+4]=int(Edtm5.getText())
				
			if len(tootfn[weat])!=0 and 2000<int(Edty1.getText()):
				dty[weat]=int(Edty1.getText())
			if len(tootfn[weat])>1 and 2000<int(Edty1.getText()):
				dty[weat+1]=int(Edty2.getText())
			if len(tootfn[weat])>2 and 2000<int(Edty1.getText()):
				dty[weat+2]=int(Edty3.getText())
			if len(tootfn[weat])>3 and 2000<int(Edty1.getText()):
				dty[weat+3]=int(Edty4.getText())
			if len(tootfn[weat])>4 and 2000<int(Edty1.getText()):
				dty[weat+4]=int(Edty5.getText())			
			
			
			if len(tootfn[weat])!=0 and 0<int(Edtd1.getText())<=31:
				dtd[weat]=int(Edtd1.getText())
			if len(tootfn[weat])>1 and 0<int(Edtd1.getText())<=31:
				dtd[weat+1]=int(Edtd2.getText())
			if len(tootfn[weat])>2 and 0<int(Edtd1.getText())<=31:
				dtd[weat+2]=int(Edtd3.getText())
			if len(tootfn[weat])>3 and 0<int(Edtd1.getText())<=31:
				dtd[weat+3]=int(Edtd4.getText())
			if len(tootfn[weat])>4 and 0<int(Edtd1.getText())<=31:
				dtd[weat+4]=int(Edtd5.getText())
				
			
				
			
		
			
		
			weat=(weat+1)%sets
			if len(tootfn[weat])!=0:
				Edtm1.setText(tootdtm[weat][0])
			else:
				Edtm1.setText('')
			if len(tootfn[weat])>1:
				Edtm2.setText(tootdtm[weat][1])
			else:
				Edtm2.setText('')
			if len(tootfn[weat])>2:
				Edtm3.setText(tootdtm[weat][2])
			else:
				Edtm3.setText('')
			if len(tootfn[weat])>3:
				Edtm4.setText(tootdtm[weat][3])
			else:
				Edtm4.setText('')
			if len(tootfn[weat])>4:
				Edtm5.setText(tootdtm[weat][4])
			else:
				Edtm5.setText('')
		
			if len(tootfn[weat])!=0:
				Edtd1.setText(tootdtd[weat][0])
			else:
				Edtd1.setText('')
			if len(tootfn[weat])>1:
				Edtd2.setText(tootdtd[weat][1])
			else:
				Edtd2.setText('')
			if len(tootfn[weat])>2:
				Edtd3.setText(tootdtd[weat][2])
			else:
				Edtd3.setText('')
			if len(tootfn[weat])>3:
				Edtd4.setText(tootdtd[weat][3])
			else:
				Edtd4.setText('')
			if len(tootfn[weat])>4:
				Edtd5.setText(tootdtd[weat][4])
			else:
				Edtd5.setText('')
				
			if len(tootfn[weat])!=0:
				Edty1.setText(tootdty[weat][0])
			else:
				Edty1.setText('')
			if len(tootfn[weat])>1:
				Edty2.setText(tootdty[weat][1])
			else:
				Edty2.setText('')
			if len(tootfn[weat])>2:
				Edty3.setText(tootdty[weat][2])
			else:
				Edty3.setText('')
			if len(tootfn[weat])>3:
				Edty4.setText(tootdty[weat][3])
			else:
				Edty4.setText('')
			if len(tootfn[weat])>4:
				Edty5.setText(tootdty[weat][4])
			else:
				Edty5.setText('')
				
			if len(tootfn[weat])!=0:
				file1.setText(tootfn[weat][0])
			else:
				file1.setText('')
			if len(tootfn[weat])>1:
				file2.setText(tootfn[weat][1])
			else:
				file2.setText('')
			if len(tootfn[weat])>2:
				file3.setText(tootfn[weat][2])
			else:
				file3.setText('')
			if len(tootfn[weat])>3:
				file4.setText(tootfn[weat][3])
			else:
				file4.setText('')
			if len(tootfn[weat])>4:
				file5.setText(tootfn[weat][4])
			else:
				file5.setText('')
			
			
			dt=builddate(dty,dtm,dtd)
			#also update!
			updata(fn,dt,wttr,cptr)
			

	
	
	






##########################################################
###################### Tracking Main #####################
##########################################################


#############################################
################ Tracking Window ############
#############################################



def tracker():
	fn, dt, wttr,cptr=buildtrack()


	dtm=[]
	dtd=[]
	dty=[]
	for i in range(0,len(dt)):
		poo=dt[i].split('-')
		dtm.append(int(poo[0]))
		dtd.append(int(poo[1]))
		dty.append(int(poo[2]))

		
	win100 = GraphWin("Data Tracking", 400, 400)
	win100.setBackground('white')
	win100.setCoords(0.0,25.0,12.0,0.0)




	advset=Text(Point(6,1.3),'Data Tracking')
	advset.setSize(25)
	advset.setStyle('bold')
	advset.setFace('courier')
	advset.setTextColor('red')
	advset.draw(win100)


	haha=Text(Point(4.4,4.6),'View Wait Time Data:')
	haha.setStyle('bold')
	haha.draw(win100)


	haha2=Text(Point(4.4,8.6),'View Clarification Pause Data:')
	haha2.setStyle('bold')
	haha2.draw(win100)




	################ View CP DATA Button ################
	cpdbutton=Text(Point(9.3,8.6),'View')
	cpd=Rectangle(Point(9.9,9.2),Point(8.7,7.8))
	cpd.setFill('green')
	cpd.draw(win100)
	cpdbutton.draw(win100)


	################ View WT DATA Button ################
	wtdbutton=Text(Point(9.3,4.6),'View')
	wtd=Rectangle(Point(9.9,5.2),Point(8.7,3.8))
	wtd.setFill('green')
	wtd.draw(win100)
	wtdbutton.draw(win100)


	liner=Line(Point(0,13),Point(12,13))
	liner.draw(win100)

	liner2=Line(Point(0,12),Point(12,12))
	liner2.draw(win100)




	haha3=Text(Point(4.4,15.6),'Edit Saved Data:')
	haha3.setStyle('bold')
	haha3.draw(win100)


	# haha4=Text(Point(4.4,19.6),'Edit Clarification Pause Data:')
	# haha4.setStyle('bold')
	# haha4.draw(win100)


	################ Edit CP DATA Button ################
	# cpdebutton=Text(Point(9.3,19.6),'Edit')
	# cpde=Rectangle(Point(9.9,20.2),Point(8.7,18.8))
	# cpde.setFill('red')
	# cpde.draw(win100)
	# cpdebutton.draw(win100)


	################ Edit SAVED DATA Button ################
	wtdebutton=Text(Point(9.3,15.6),'Edit')
	wtde=Rectangle(Point(9.9,16.2),Point(8.7,14.8))
	wtde.setFill('red')
	wtde.draw(win100)
	wtdebutton.draw(win100)





	td=True
	while td:
		tool100=win100.getMouse()
		
		

		################ Click View WT DATA Button ################
		if 8.7<=tool100.getX()<=9.9 and 3.8<=tool100.getY()<=5.2:
			try:
				view("Wait Time Data",dt,wttr)
			except:
				pass
				
		
		################ Click View CP DATA Button ################
		if 8.7<=tool100.getX()<=9.9 and 7.8<=tool100.getY()<=9.2:
			try:
				view("Clarification Pause Data",dt,cptr)
			except:
				pass
				
		################ Click Edit SAVED DATA Button ################
		if 8.7<=tool100.getX()<=9.9 and 14.8<=tool100.getY()<=16.2:
			try:
				edittracker("Edit Saved Data",dty,dtm,dtd,fn,wttr,cptr)
			except:
				pass
				
		################ Click Edit CP DATA Button ################
		# if 8.7<=tool100.getX()<=9.9 and 18.8<=tool100.getY()<=20.2:
			# try:
				# edittracker("Clarification Pause Data",dty,dtm,dtd,fn)
			# except:
				# pass
			













######################## DECODER AND CALCULATOR #################

# The Decoder Module


def TheGame(todecode):

	Words=[]
	lattice=[]
	Start=[]
	End=[]
	DirtyWords=[]
	Prob=[]
	print(str(todecode))
	ffll=str(todecode).split('\\')
	print(ffll)
	a,sucka=ffll[len(ffll)-1].split('.')
	print(sucka)
	#chdir('./audio_files/')
	AudioSegment.converter = "D:\\ffmpeg\\ffmpeg\\bin\\ffmpeg.exe"
	if sucka=='mp3':
		myaudio=AudioSegment.from_mp3(todecode)
	else:
		myaudio = AudioSegment.from_file(todecode , sucka) 
	chunk_length_ms = 60000 # pydub calculates in millisec
	chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec



	chdir('./audio_files/temp')
	t=0
	for i, chunk in enumerate(chunks):
    		chunk_name = "chunk{0}.raw".format(i)
    		t=t+1
		vchunck=chunk.dBFS
		chng=-20.0-vchunck
		fatty=chunk.apply_gain(chng)
		fatty1=fatty.set_frame_rate(16000)
		fatty2=fatty1.set_channels(1)
    		fatty2.export(chunk_name, format="raw")
	chdir('../')
	chdir('../')
	for j in range(0,t):
		W,S,E,P, WW, LW=Doit('chunk'+str(j)+'.raw')
		for k in range(0,len(W)):
			if W[k]!='<s>' and W[k]!='</s>':
				Words.append(W[k])
		#for k in range(0,len(S)):
				Start.append(S[k]+j*chunk_length_ms)
		#for k in range(0,len(E)):
				End.append(E[k]+j*chunk_length_ms)
		#for k in range(0,len(P)):
				Prob.append(P[k])
		#for k in range(0,len(WW)):
				DirtyWords.append(WW[k])

		for i in range(0,len(LW)):
			lattice.append(LW[i])
	chdir('./audio_files/temp')
	for j in range(0,t):
		remove('chunk'+str(j)+'.raw')
	
	chdir('../')
	chdir('../')

	print(Words)

	return Words, Start, End, Prob, DirtyWords, lattice




	
	

def Doit(todecode):

	#from os import environ,path,chdir,remove

	#from pocketsphinx.pocketsphinx import *
	#from sphinxbase.sphinxbase import *

	chdir('./bin')
	loadsettings=open('prefersett.txt','r')
	settings=[]
	countest=0
	strhelper=''
	for line in loadsettings:
		countest=countest+1
		lll=list(line)
		for j in lll:
			if j!='\n' and countest<14:
				settings.append(int(j))
			if j!='\n' and countest==14:
				strhelper=strhelper+j
		if countest==14:
			settings.append(strhelper)

	chdir('../')

	# These are the locations we will look for files
	MODELDIR = './bin/model'

	if settings[12]==1:
		DICTDIR='./bin/LM_data'
	else:
		DICTDIR ='./bin/model/en-us'


	TESTDIR='./audio_files/temp'


	# Create a decoder with certain model
	config = Decoder.default_config()


	config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
	if settings[12]==1:
		config.set_string('-lm', path.join(DICTDIR, settings[13]+'.lm'))

	else:
		config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))

	if settings[12]==1:	
		config.set_string('-dict',path.join(DICTDIR, settings[13]+'.dic'))
	else:
		config.set_string('-dict',path.join(DICTDIR, 'cmudict-en-us.dict'))

	# Decode streaming data.
	decoder = Decoder(config)
	
	if settings[0]==1:
		chdir('./training_data/speech_training')
		datafile=open('data.txt','r')
		tool=[]
		for line in datafile:
			l=list(line)
			es=''
			if l[0]!='#' and l[0]!='':
				for i in range(0,len(line)):
					if l[i]!='\n':
						es=es+l[i]
			if es!='':
				tool.append(es)
		datafile.close()
		
		chdir('../')
		chdir('../')
		
		chdir('./bin/LM_data')
		filly=open('words.txt')
		wolly=[]
		for line in filly:
			ff100=line.split('\n')
			pll=ff100[0]
			wolly.append(pll)
		filly.close()

		chdir('../')
		chdir('../')
		
		chdir('./training_data/speech_training')
		
		for i in range(0,len(tool)):
			if settings[i+1]==1:
				da=open(tool[i]+'.txt','r')
				hell=[]
				for line in da:
					s=''
					l=list(line)
					for j in l:
						if j!='\n':
							s=s+j
					hell.append(s)
				kk=0
				for k in hell:
					if tool[i] not in wolly and kk==0:
						decoder.add_word(tool[i],k,True)
						kk=kk+1
					else:
						print(tool[i])
						decoder.add_word(tool[i]+'('+str(5+kk)+')',k,True)
						kk=kk+1
				da.close()
					
		chdir('../')
		chdir('../')
	

	


	decoder.start_utt()

	# The file we are decoding

	stream = open(path.join(TESTDIR, todecode), 'rb')

		
		
	# This says HEY GO DECODE YOU BLACK BOX YOU
	while True:
	  buf = stream.read(1024)
	  if buf:
		decoder.process_raw(buf, True, False)
	  else:
		break
	decoder.end_utt()





	# W will be the "washed words" and WW is be the "un-washed words" by "washed" I mean I strip the (number) at end of the word
	W=[seg.word for seg in decoder.seg()]
	WW=[seg.word for seg in decoder.seg()]

	# This "washes" the words
	for i in range(0,len(W)):
		l=list(W[i])
		ll=len(l)
		if l[ll-1]==')':
			w=''
			K=True
			t=0
			while K:
				if l[t]=='(':
					K=False
				else:
					w=w+l[t]
				t=t+1
			W[i]=w
			
	# End times:
	E=[seg.end_frame for seg in decoder.seg()]

	# Start tims:
	S=[seg.start_frame for seg in decoder.seg()]
	#print(S)

	# Probabilities:
	P=[seg.prob for seg in decoder.seg()]


	chdir('./temp')
	decoder.get_lattice().write('latticetemp.lat')
	#decoder.get_lattice().write_htk('rob_test1.htk')


	LW=[]
	infile=open('latticetemp.lat','r')
#infile2=open('rob_test1.htk','r')

	zz=0





	for i in range(0,len(S)):
		LW.append([])





	toots=0
	poops=0
	for i in infile:
		#print(i)
		T=i.split(' ')
		#print(zz)
		if len(T)>=3 and zz!=0:
			poop=int(T[2])+S[0]
		else:
			poop=''	
		if len(T)>=3 and zz!=0:
			poots=0
			for europa in range(0,len(S)):
				if poop>= S[europa]:
					poots=europa
			LW[poots].append(T[1])
		
	
		if zz!=0 and len(T)>=3 and int(T[0])==toots:
			#print('break')
			break
		if T[0]=='Nodes':
			toots=int(T[1])-1
			#print(toots)
			zz=zz+1
	
	
		#do something
	
	
	
	
#print(LW)
#print(H)
	infile.close()
	
	remove('latticetemp.lat')
	chdir('../')


	for i in range(0,len(LW)):
		l=list(LW[i])
		ll=len(l)
		if l[ll-1]==')':
			w=''
			K=True
			t=0
			while K:
				if l[t]=='(':
					K=False
				else:
					w=w+l[t]
				t=t+1
			LW[i]=w
	
	#print(W)
	# hypothesis = decoder.hyp()
	# logmath = decoder.get_logmath()
	# print ('Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", logmath.exp(hypothesis.prob))


	# Collect them all? I don't think we use this one anymore
	#A=[W, S,E,P]
	return W, S, E, P, WW, LW
	
	
	
	
	
	
	


# This associates trigger words with the appropriate silence	
def findTimes(W,SILE,SILS,SILCT,CP,WT,S,P,LW):

	#print(W)
	CPI=[[],[],[],[],[],[]]
	WTI=[[],[],[],[],[],[]]
	for i in range(0,len(W)):
		if W[i] in CP:
			#print(W[i])
			CPI[0].append(i)
			CPI[2].append(S[i])
			CPI[3].append(P[i])
			CPI[4].append(False)
			T=0
			K=True
			while K and T<len(SILE):
				if SILE[len(SILE)-T-1]<CPI[0][len(CPI[0])-1]:
					CPI[1].append(len(SILE)-T-1)
					K=False
				elif T==len(SILE)-1 and SILE[len(SILE)-T-1]>CPI[0][len(CPI[0])-1]:
					CPI[1].append('no')
					K=False
				T=T+1
		if W[i] in WT:
			WTI[0].append(i)
			WTI[2].append(S[i])
			WTI[3].append(P[i])
			WTI[4].append(False)
			T=0 
			K=True
			while K and T<len(SILS):
				if SILS[T]>WTI[0][len(WTI[0])-1]:
					WTI[1].append(T)
					K=False
				elif T==len(SILS)-1 and SILS[T]<WTI[0][len(WTI[0])-1]:
					WTI[1].append('no')
					K=False
				T=T+1
		if W[i] not in WT and W[i] not in CP and W[i]!='<s>' and W[i]!='</s>':
			for flashpoint in range(0,len(LW[i])):
				if LW[i][flashpoint] in CP:
					#print(W[i])
					CPI[0].append(i)
					CPI[2].append(S[i])
					CPI[3].append(P[i])
					CPI[4].append(True)
					T=0
					K=True
					while K and T<len(SILE):
						if SILE[len(SILE)-T-1]<CPI[0][len(CPI[0])-1]:
							CPI[1].append(T-1)
							K=False
						elif T==len(SILE)-1 and SILE[len(SILE)-T-1]>CPI[0][len(CPI[0])-1]:
							CPI[1].append('no')
							K=False
						T=T+1
				if LW[i][flashpoint] in WT:
					WTI[0].append(i)
					WTI[2].append(S[i])
					WTI[3].append(P[i])
					WTI[4].append(True)
					T=0 
					K=True
					while K and T<len(SILS):
						if SILS[T]>WTI[0][len(WTI[0])-1]:
							WTI[1].append(T)
							K=False
						elif T==len(SILS)-1 and SILS[T]<WTI[0][len(WTI[0])-1]:
							WTI[1].append('no')
							K=False
						T=T+1
	

					
	return WTI,CPI
	
	
	
	
def AverageTimes(E,S,SILCT,SILS,SILE,WTI,CPI):
	countCP=0
	countWT=0
	#calculate average times:
	ACP=0
	AWT=0
	for i in range(0,len(CPI[1])):
		#condition on too much time has passed (set now to 20 seconds)
		if CPI[1][i]!='no' and S[CPI[0][i]]-E[SILE[CPI[1][i]]]<=6120:
			#print(S[CPI[0][i]]-SILE[CPI[1][i]])
			conditionCP=True 
			countCP=countCP+1
		else:
			conditionCP=False
			#print(S[CPI[0][i]]-SILE[CPI[1][i]])
		if conditionCP and CPI[1][i]!='no':
			if CPI[4]:
				ACP=ACP+((2*SILCT[CPI[1][i]])/3)
			else:
				ACP=ACP+SILCT[CPI[1][i]]

	if countCP!=0:
		ACP=ACP/countCP
	for i in range(0,len(WTI[1])):
		#condition on too much time has passed (set now to 10 seconds)
		if WTI[1][i]!='no' and S[SILS[WTI[1][i]]]-E[WTI[0][i]]<6120:
			conditionWT=True 
			countWT=countWT+1
		else:
			conditionWT=False
		if conditionWT and WTI[1][i]!='no':
			if WTI[4]:
				AWT=AWT+((2*SILCT[WTI[1][i]])/3)
			else:
				AWT=AWT+SILCT[WTI[1][i]]

	if countWT!=0:
		AWT=AWT/countWT
		
	
	return AWT, ACP, countCP, countWT
		
		
		
		
		
		
		
		
		
# The silence preprocesser
def silence(W, E, S):
	# Pre-Process the silence 
	SIL=[]
	SILT=[]
	for i in range(0,len(W)):
		if W[i]=='<sil>' or W[i]=='[NOISE]' or W[i]=='<s>' or W[i]=='</s>':
			SIL.append(i)
			SILT.append(E[i]-S[i])
			
			


			
			
	L=[]
	SILS=[]
	SILE=[]
	SILCT=[]
	for i in range(0,len(SIL)):
		if i not in L:
			k=i
			j=i
			t=SILT[i]
			L.append(i)
			while j-k<1 and j+1<len(SIL):
				if SIL[j+1]-SIL[j]==1:
					k=j+1
					j=j+1
					t=t+SILT[j]
					L.append(j)
				else:
					j=j+1
					SILE.append(SIL[k])
					SILS.append(SIL[i])
					SILCT.append(t)
					
					
	return SILE, SILS, SILCT
	
	
	
	
	




############################################################################################

######################################## DICTIONARY TRAINER ############################

#############################################################################################

def trainer(filename,testword):

	#chdir('./audio_files')

###################### CONVERT FILE TO GOOD FILE ###############

	#a,sucka=filename.split('.')
	ffll=str(filename).split('\\')
	a, sucka=ffll[len(ffll)-1].split('.')
	tunes=AudioSegment.from_file(filename,sucka)
	volume=tunes.dBFS
	chng=-20.0-volume
	sounds=tunes.apply_gain(chng)
	sounds1=sounds.set_frame_rate(16000)
	sounds2=sounds1.set_channels(1)
	newname=a+'.raw'
	chdir('./audio_files/temp')
	sounds2.export(a+'.raw','raw')
	chdir('../')
	chdir('../')


	filename=newname


	MODELDIR = './bin/model'
	DICTDIR ='./'
	TESTDIR='./audio_files/temp'

	# Create a decoder with certain model
	config = Decoder.default_config()
	config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
	config.set_string('-allphone', path.join(MODELDIR, 'en-us/en-us-phone.lm.bin'))
	config.set_float('-lw', 2.0)
	config.set_float('-pip', 0.3)
	config.set_float('-beam', 1e-200)
	config.set_float('-pbeam', 1e-20)
	config.set_boolean('-mmap', False)

	decoder = Decoder(config)

	# Decode streaming data.
	decoder = Decoder(config)

	decoder.start_utt()
	stream=open(path.join(TESTDIR, filename),'rb')

	while True:
	  buf = stream.read(1024)
	  if buf:
		decoder.process_raw(buf, False, False)
	  else:
		break
	decoder.end_utt()



	W=[seg.word for seg in decoder.seg()]

	# End times:
	#E=[seg.end_frame for seg in decoder.seg()]

	# Start tims:
	#S=[seg.start_frame for seg in decoder.seg()]
	#print(S)
	
	# chdir('./audio_files/temp')
	# remove(a+'.raw')
	
	# chdir('../')
	# chdir('../')
	
	
	chdir('./bin')
	PHONE=[]
	infile1=open("phone.dict","r")
	for line in infile1:
		l=line.split(' ')
		for i in l:
			if i.isupper() and i!=' ' and i!='\n':
				if i not in PHONE and i+'\n' not in PHONE:
					PHONE.append(i)
					
	for i in range(0,len(PHONE)):
		l=list(PHONE[i])
		s=''
		for j in l:
			if j!='\n':
				s=s+j
		PHONE[i]=s
					
	infile1.close()
	chdir('../')

	#print(W)
	#print(PHONE)
	#infile=open("adapted-en-us.dict","r")

	R=[]
	s=''
	for i in range(0,len(W)):
		#if W[i]=='SIL':
			#print((E[i]-S[i])*0.01)
		#if W[i]=='SIL' and s!='' and (E[i]-S[i])*0.01>=0.1:
		#	L.append(s)
		#	s=''
		if W[i] in PHONE:
			s=s+' '+W[i]

	#print(L)	
	num=0 #change this
			#decoder.add_word('foobie', 'F UW B IY', False)
			#outfile.write(testword+'('+str(5+i)+') '+L[i]+'\n')
	
	#else:
		#print('Sorry but you did not leave enough silence between the words please try again!')
		#R.append('Sorry but you did not leave enough silence between the words please try again!')
		
	#print(R)
	#print(PHONE)
	#infile.close()

	chdir('./training_data/speech_training')
	fn=testword.upper()+'.txt'
	infile=open('data.txt','r')


	datasofar=[]

	for l in infile:
		zipper=list(l)
		if zipper[0]!='' and zipper[0]!='#':
			datasofar.append(l)
			#print(l)
	
	infile.close()
	outfile2=open('data.txt','a+')
	duh0=testword.upper()
	duh=duh0+'\n'
	if len(datasofar)==0:
		outfile2.write('\n')
	if duh not in datasofar:
		outfile2.write(duh)
	else:
		num=num+1

	R.append(duh0+'('+str(5+num)+')')
	R.append(s)
	#print(R)
	
	outfile2.close()
	outfile=open(fn,'a+')
		
	outfile.write(R[1]+'\n')




	outfile.close()
	chdir('../')
	chdir('../')

	chdir('./bin')
	ps=open('prefersett.txt','r')
	peep=[]
	
	cou=0
	for line in ps:
		cou=cou+1
		pss=list(line)
		if cou<14:
			peep.append(int(pss[0]))
		else:
			see=''
			for j in pss:
				if j!='\n':
					see=see+j
					#print(see)
			peep.append(see)

	ps.close()
	chdir('../')
	chdir('./training_data/speech_training')
	datafile=open('data.txt','r')

	tool=[]
	for line in datafile:
		l=list(line)
		if l[0]!='#' and l[0]!='':
			es=''
			for i in range(0,len(line)):
				if l[i]!='\n':
					es=es+l[i]
			if es!='':
				tool.append(es)
			
	print('tool=')
	print(tool)
	
	
	datafile.close()
	chdir('../')
	chdir('../')
	peep[0]=1
	coco=0
	for j in tool:
		coco=coco+1
		if j==duh0:
			peep[coco]=1
	
	
	print('peep=')
	print(peep)			

	chdir('./bin')
	upp=open('prefersett.txt','w')
	for i in range(0,len(peep)):
		upp.write(str(peep[i])+'\n')
		
	upp.close()
	chdir('../')
	
	ender=a+'.raw'
	return ender

			




			
#########################################################################################			
			
##################################### ADVANCED SETTINGS ##############################

##########################################################################################


def advanced_settings():

	

	chdir('./bin')
	ps=open('prefersett.txt','r')
	peep=[]
	cou=0
	for line in ps:
		cou=cou+1
		pss=list(line)
		if cou<14:
			peep.append(int(pss[0]))
		else:
			s=''
			for j in pss:
				if j!='\n':
					s=s+j
					#print(s)
			peep.append(s)
				

	ps.close()
	chdir('../')
	chdir('./training_data/speech_training')
	datafile=open('data.txt','r')

	tool=[]
	for line in datafile:
		l=list(line)
		if l[0]!='#' and l[0]!='':
			es=''
			for i in range(0,len(line)):
				if l[i]!='\n':
					es=es+l[i]
			if es!='':
				tool.append(es)
	datafile.close()
	chdir('../')
	chdir('../')

	
	
	
	

	
	win7 = GraphWin("Advanced Settings", 400, 400)
	win7.setBackground('white')
	win7.setCoords(0.0,25.0,12.0,0.0)
	
	
	
	
	
	
	advset=Text(Point(6,1.3),'Advanced Settings')
	advset.setSize(25)
	advset.setStyle('bold')
	advset.setFace('courier')
	advset.setTextColor('red')
	advset.draw(win7)
	
	
	haha=Text(Point(4.4,4.6),'Use Previously Trained Words:')
	haha.setStyle('bold')
	haha.draw(win7)
	
	
	
	nnoo=Text(Point(6,6.6),'No Trained Words Selected')
	nnoo.setTextColor('grey')
	nnoo.draw(win7)
	
	
	

	yee=Text(Point(6,6.6),'Click to see selected words')
	yeetan=Rectangle(Point(2.5,7.2),Point(9.5,5.8))





	trndbutton=Text(Point(9.3,4.6),'OFF')
	trnd=Rectangle(Point(9.9,5.2),Point(8.7,3.8))
	trnd.setFill('grey')
	trnd.draw(win7)
	trndbutton.draw(win7)


	if peep[0]==1:
		trndbutton.setText('ON')
		trnd.setFill('green')
		peep[0]=1
		nnoo.undraw()
		yee.draw(win7)
		yeetan.draw(win7)





	haha2=Text(Point(4.4,9),'Use Language Model:')
	haha2.setStyle('bold')
	haha2.draw(win7)
	

	lmbutton=Text(Point(9.3,9),'OFF')
	lm=Rectangle(Point(9.9,9.6),Point(8.7,8.2))
	lm.setFill('grey')
	lm.draw(win7)
	lmbutton.draw(win7)
	





	op1=Text(Point(6,11.2),'by default S.T.A.R. uses')
	op01=Text(Point(6,12.2),'the sphinx packaged language model')
	op1.setTextColor('grey')
	op01.setTextColor('grey')
	op02=Text(Point(6,18),'Warning:')
	op2=Text(Point(6,19),'Current setting has')
	op002=Text(Point(6,20), 'VERY SLOW processing speed')
	op2.setTextColor('red')
	op2.setStyle('bold')
	op2.setFace('courier')
	op02.setTextColor('red')
	op02.setStyle('bold')
	op02.setFace('courier')
	op002.setTextColor('red')
	op002.setStyle('bold')
	op002.setFace('courier')
	op1.draw(win7)
	op01.draw(win7)
	op2.draw(win7)
	op02.draw(win7)
	op002.draw(win7)
	fu2=Text(Point(2.4,17.5),'Common Phrases:')

	fudgy=Entry(Point(8,17.5),25)
	fudgy.setText('.txt')

	cm=Text(Point(6,11.4),'Current Model: '+peep[13])

	nm=Text(Point(6,15),'Compile New Model:')
	nm.setFace('courier')
	nm.setStyle('bold')


	lineup=Line(Point(0,14),Point(12,14))
	nmgo=Text(Point(6,20),'Compile')
	nmgobttn=Rectangle(Point(4.4,19.4),Point(7.8,20.6))
	nmgobttn.setFill('yellow1')
	linedown=Line(Point(0,16),Point(12,16))
	linedoubledown=Line(Point(0,21.4),Point(12,21.4))
	linedoubledown.draw(win7)


	exitbttn=Rectangle(Point(4.3,22.4),Point(7.8,24.3))
	exitbttn.setFill('red1')
	exitb=Text(Point(6,23.4),'Exit and Save')
	exitbttn.draw(win7)
	exitb.draw(win7)





	if peep[12]==1:
		lmbutton.setText('ON')
		lm.setFill('green')
		peep[12]=1
		op1.undraw()
		op01.undraw()
		op2.undraw()
		op02.undraw()
		op002.undraw()
		fu2.draw(win7)
		cm.draw(win7)
		fudgy.draw(win7)
		nm.draw(win7)
		nmgobttn.draw(win7)
		nmgo.draw(win7)
		lineup.draw(win7)
		linedown.draw(win7)
		








	paparoach=True
	while paparoach:

		peas=win7.getMouse()
		if 4.3<=peas.getX()<=7.8 and 22.4<=peas.getY()<=24.3:
			chdir('./bin')
			upp=open('prefersett.txt','w')
			for i in range(0,len(peep)):
				upp.write(str(peep[i])+'\n')
			
			upp.close()
			chdir('../')
			paparoach=False
		if peep[0]==0:
	
			if 8.7<peas.getX()<9.9 and 3.8<peas.getY()<5.2:
				trndbutton.setText('ON')
				trnd.setFill('green')
				peep[0]=1
				nnoo.undraw()
				yee.draw(win7)
				yeetan.draw(win7)
	

		else:
			if 8.7<=peas.getX()<=9.9 and 3.8<peas.getY()<=5.2:
				trndbutton.setText('OFF')
				peep[0]=0

				trnd.setFill('grey')
				peep[0]=0
				nnoo.draw(win7)
				yee.undraw()
				yeetan.undraw()

	

			if 2.5<=peas.getX()<=9.5 and 5.8<=peas.getY()<=7.2:
		


				if len(tool)<=11:
					num=3.5 +2*len(tool)+4
				else:
					num=30.5
				le=num*15
				le2=le/16
				try:
					win8 = GraphWin("Trained Words", 400, le)
					win8.setBackground('white')
					win8.setCoords(0.0,le2,12.0,0.0)
					tit=Text(Point(6,1.3),'Trained Words:')
					tit.setSize(25)
					tit.setStyle('bold')
					tit.setFace('courier')
					tit.setTextColor('red')
					tit.draw(win8)
		
					en=Text(Point(6,le2-2),'Save and Close')
					enbttn=Rectangle(Point(4.2,le2-2.6),Point(7.8,le2-1.4))
					enbttn.setFill('green')
					enbttn.draw(win8)
					en.draw(win8)


					c1=Line(Point(10.3,3.5-.6),Point(11,3.5+.6))



					c2=Line(Point(10.3,5.5-.6),Point(11,5.5+.6))


					c3=Line(Point(10.3,7.5-.6),Point(11,7.5+.6))


					c4=Line(Point(10.3,9.5-.6),Point(11,9.5+.6))


					c5=Line(Point(10.3,11.5-.6),Point(11,11.5+.6))


					c6=Line(Point(10.3,13.5-.6),Point(11,13.5+.6))


					c7=Line(Point(10.3,15.5-.6),Point(11,15.5+.6))


					c8=Line(Point(10.3,17.5-.6),Point(11,17.5+.6))


					c9=Line(Point(10.3,19.5-.6),Point(11,19.5+.6))


					c10=Line(Point(10.3,21.5-.6),Point(11,21.5+.6))


					c11=Line(Point(10.3,23.5-.6),Point(11,23.5+.6))










					for j in range(0,11):
						if j>len(tool)-1:
							break
						if j==0:
							ht=3.5

						else:
							ht=ht+2
						bht=ht+.6
						bbht=ht-.6
						Text(Point(5.1,ht),tool[j]).draw(win8)
						Rectangle(Point(10.3,bht),Point(11,bbht)).draw(win8)

						if j==0:
							if peep[1]==1:
								c1.draw(win8)

						if j==1:
							if peep[2]==1:
								c2.draw(win8)

						if j==2:
							if peep[3]==1:
								c3.draw(win8)

						if j==3 and peep[4]==1:
							
							c4.draw(win8)

						if j==4 and peep[5]==1:
							c5.draw(win8)

						if j==5 and peep[6]==1:
							c6.draw(win8)

						if j==6 and peep[7]==1:
							c7.draw(win8)

						if j==7 and peep[8]==1:
							c8.draw(win8)

			
						if j==8 and peep[9]==1:
							c9.draw(win8)
			
						if j==9 and peep[10]==1:
							c10.draw(win8)

						if j==10 and peep[11]==1:
							c11.draw(win8)

					potluck=True

					while potluck:
						carrots=win8.getMouse()
						if 10.3<=carrots.getX()<=11:
							if 3.5-.6<=carrots.getY()<=3.5+.6:
								if peep[1]==0:
									c1.draw(win8)
									peep[1]=1
								else:
									c1.undraw()
									peep[1]=0
							if 5.5-.6<=carrots.getY()<=5.5+.6:
								if peep[2]==0:
									c2.draw(win8)
									peep[2]=1
								else:
									c2.undraw()
									peep[2]=0
							if 7.5-.6<=carrots.getY()<=7.5+.6:
								if peep[3]==0:
									c3.draw(win8)
									peep[3]=1
								else:
									c3.undraw()
									peep[3]=0
							if 9.5-.6<=carrots.getY()<=9.5+.6:
								if peep[4]==0:
									c4.draw(win8)
									peep[4]=1
								else:
									c4.undraw()
									peep[4]=0
							if 11.5-.6<=carrots.getY()<=11.5+.6:
								if peep[5]==0:
									c5.draw(win8)
									peep[5]=1
								else:
									c5.undraw()
									peep[5]=0
							if 13.5-.6<=carrots.getY()<=13.5+.6:
								if peep[6]==0:
									c6.draw(win8)
									peep[6]=1
								else:
									c6.undraw()
									peep[6]=0
							if 15.5-.6<=carrots.getY()<=15.5+.6:
								if peep[7]==0:
									c7.draw(win8)
									peep[7]=1
								else:
									c7.undraw()
									peep[7]=0
							if 17.5-.6<=carrots.getY()<=17.5+.6:
								if peep[8]==0:
									c8.draw(win8)
									peep[8]=1
								else:
									c6.undraw()
									peep[8]=0
							if 19.5-.6<=carrots.getY()<=19.5+.6:
								if peep[9]==0:
									c9.draw(win8)
									peep[9]=1
								else:
									c9.undraw()
									peep[9]=0
							if 21.5-.6<=carrots.getY()<=21.5+.6:
								if peep[10]==0:
									c10.draw(win8)
									peep[10]=1
								else:
									c6.undraw()
									peep[10]=0
							if 23.5-.6<=carrots.getY()<=23.5+.6:
								if peep[11]==0:
									c11.draw(win8)
									peep[11]=1
								else:
									c11.undraw()
									peep[11]=0
						if 4.2<=carrots.getX()<=7.8 and le2-2.6<=carrots.getY()<=le2-1.4:
							potluck=False

						chdir('./bin')
						upp=open('prefersett.txt','w')
						for i in range(0,len(peep)):
							upp.write(str(peep[i])+'\n')
				
						upp.close()
						chdir('../')

					win8.close()
				except:
					pass


		if peep[12]==0:
			if peas.getY()<=9.6 and peas.getY()>=8.2 and peas.getX()<=9.9 and peas.getX()>=8.7:
				lmbutton.setText('ON')
				lm.setFill('green')
				peep[12]=1
				chdir('./bin')
				openfile=open('prefersett.txt')
				xcup=0
				for line in openfile:
					s=''
					xcup=xcup+1
					lip=list(line)
					for j in lip:
						if xcup==14:
							if j!='\n':
								s=s+j
					if xcup==14:	
						peep[13]=s
				
				openfile.close()
				chdir('../')
				cm.setText('Current Model: '+peep[13])
				op1.undraw()
				op01.undraw()
				op2.undraw()
				op02.undraw()
				op002.undraw()
				fu2.draw(win7)
				fudgy.draw(win7)
				cm.draw(win7)
				nm.draw(win7)
				nmgobttn.draw(win7)
				nmgo.draw(win7)
				lineup.draw(win7)
				linedown.draw(win7)
				




		else:
			if 19.4<=peas.getY()<=20.6 and 4.4<=peas.getX()<=7.8:
				todo=fudgy.getText()
				too,doo=todo.split('.')
				
				chdir('./training_data/language_training')

	############### CHECK IF FILE EXISTS ##################	
				xmas=True
				while xmas:
					if path.exists(todo):
						chdir('../')
						chdir('../')
						xmas=False
					else:
						win5=GraphWin('No Such File',500,150)
						win5.setBackground('white')
						win5.setCoords(0.0,11.0,6.0,0.0)
						#pluuu=Text(Point(3,6),'(This may take some time)')
						#pluuu.draw(win2)
						#hText(Point(1.4,5.5),'Class Recording:').draw(win5)
						#fudger=Entry(Point(3.55,5.5),25)
						#fudger.setText('.file-type')
						#fudger.draw(win5)
						zzzz=Text(Point(3,2.3),todo)
						zzz=Text(Point(3,4.5),'DOES NOT EXIST')
						zzz.setSize(20)
						zzz.setStyle('bold')
						zzz.setFace('courier')
						zzz.setTextColor('red')
						zzz.draw(win5)
						zzzz.setSize(25)
						zzzz.setStyle('bold')
						zzzz.setFace('courier')
						zzzz.setTextColor('red')
						zzzz.draw(win5)
						haha=Text(Point(3,6.9),'make sure your file is in the folder audio_files')
						haha2=Text(Point(3,8),'and remember to use the correct extension for example .mp3')
						haha.setStyle('bold')
						haha2.setStyle('bold')
						haha2.draw(win5)
						haha.draw(win5)
						zz2=Text(Point(3,9.9),'(click anywhere to go back!)')
						zz2.draw(win5)

						chdir('../')
						chdir('../')
						try:
							win5.getMouse()
							win5.close()
						except:
							pass
						fudgy.setText('.txt')
						break
						
				######### CHECK CORRECT FILE TYPE ###########
				xmas2=False
				if xmas==False:
					overthisshit=list(todo)
					sooverit=False
					for shit in overthisshit:
						if shit=='.':
							sooverit=True
					if sooverit:
						a, sucka=todo.split('.')
					else:
						sucka='empty'
					filetypes=['txt']
					if sucka not in filetypes:
						xmas2=True
						

					
					if xmas2:

						win5=GraphWin('No Such File',500,150)
						win5.setBackground('white')
						win5.setCoords(0.0,11.0,6.0,0.0)
						#pluuu=Text(Point(3,6),'(This may take some time)')
						#pluuu.draw(win2)
						#hText(Point(1.4,5.5),'Class Recording:').draw(win5)
						#fudger=Entry(Point(3.55,5.5),25)
						#fudger.setText('.file-type')
						#fudger.draw(win5)
						zzzz=Text(Point(3,2.3),'.'+sucka)
						zzz=Text(Point(3,4.5),'IS NOT A VALID FILE TYPE')
						zzz.setSize(20)
						zzz.setStyle('bold')
						zzz.setFace('courier')
						zzz.setTextColor('red')
						zzz.draw(win5)
						zzzz.setSize(25)
						zzzz.setStyle('bold')
						zzzz.setFace('courier')
						zzzz.setTextColor('red')
						zzzz.draw(win5)
						haha=Text(Point(3,6.8),'To make a language model')
						haha2=Text(Point(3,8),'Enter a .txt file')
						haha.setStyle('bold')
						haha2.setStyle('bold')
						haha2.draw(win5)
						haha.draw(win5)
						zz2=Text(Point(3,9.9),'(click anywhere to go back!)')
						zz2.draw(win5)

						
						try:
							win5.getMouse()
							win5.close()
						except:
							pass
						fudgy.setText('.txt')

						


					





				if xmas==False and xmas2==False:

				
					#Loading Window
					win22=GraphWin('Creating Model...',500,150)
					win22.setBackground('white')
					win22.setCoords(0.0,11.0,6.0,0.0)
					ttt2=Text(Point(3,6),'(This may take some time)')
					ttt2.draw(win22)
					tt2=Text(Point(3,3),'System Processing...')
					tt2.setSize(25)
					tt2.setStyle('bold')
					tt2.setFace('courier')
					tt2.setTextColor('red')
					tt2.draw(win22)
					tt22=Text(Point(3,9),'(This window will close when the process is done!)')
					tt22.draw(win22)

			############## MAKE NEW LANGUAGE MODEL #########
					chdir('./training_data/language_training')
			
					br=mechanize.Browser()
					br.open('http://www.speech.cs.cmu.edu/tools/lmtool-new.html')
					def select_form(form):
					  return form.attrs.get('action', None) == 'http://www.speech.cs.cmu.edu/cgi-bin/tools/lmtool/run'

					br.select_form(predicate=select_form)

					br.form.add_file(open(todo,'r'), 'text/plain', todo, name='corpus')
					res=br.submit()

					thelist=[]
					for link in br.links():
						thelist.append([link.text,link.url])
					#print(thelist)
					
					chdir('../')
					chdir('../')
					#lm name
					w2=''
					for j in thelist:
						ll=list(str(j[0]))
						if ll[len(ll)-2]=='l' and ll[len(ll)-1]=='m':
							w2=str(j[0])

					res2=br.open(w2)
					chdir('./bin/LM_data')
					fileobj=open(too+'.lm','wb')
					fileobj.write(res2.read())

					chdir('../')
					chdir('../')



					fileobj.close()


					chdir('./training_data/language_training')

					br=mechanize.Browser()
					br.open('http://www.speech.cs.cmu.edu/tools/lmtool-new.html')
					def select_form(form):
					  return form.attrs.get('action', None) == 'http://www.speech.cs.cmu.edu/cgi-bin/tools/lmtool/run'

					br.select_form(predicate=select_form)

					br.form.add_file(open(todo,'r'), 'text/plain', todo, name='corpus')
					res=br.submit()

					thelist=[]
					for link in br.links():
						thelist.append([link.text,link.url])
					#print(thelist)

					#dic name
					w1=''
					chdir('../')
					chdir('../')
					

					for j in thelist:
						ll=list(str(j[0]))
						if ll[len(ll)-3]=='d' and ll[len(ll)-2]=='i' and ll[len(ll)-1]=='c':
							w1=str(j[0])
					res2=br.open(w1)
					chdir('./bin/LM_data')
					fileobj=open(too+'.dic','wb')
					fileobj.write(res2.read())

					chdir('../')
					chdir('../')



					fileobj.close()	
					fudgy.setText('.txt')
					peep[13]=too
					cm.setText('Current Model: '+peep[13])
					win22.close()
					
					chdir('./bin/LM_data')
					#update words#
					fil=open(peep[13]+'.dic','r')

					W=[]
					for line in fil:
						#print(line)
						#print(line.split(' '))
						one=line.split(' ')
						two=str(one[0])
						three=two.split('\t')
						four=three[0].split('(')
						five=four[0]
						if five not in W:
							W.append(five)
						
							print(five)
							
					fil2=open('words.txt','w')
					for w in W:
						fil2.write(w+'\n')
						
					fil.close()
					fil2.close()
					chdir('../')
					chdir('../')
				
			



			if peas.getY()<=9.6 and peas.getY()>=8.2 and peas.getX()<=9.9 and peas.getX()>=8.7:
				lmbutton.setText('OFF')
				lm.setFill('grey')
				peep[12]=0
				op1.draw(win7)
				op01.draw(win7)
				op2.draw(win7)
				op02.draw(win7)
				op002.draw(win7)
				fu2.undraw()
				fudgy.undraw()
				cm.undraw()
				nm.undraw()
				nmgobttn.undraw()
				nmgo.undraw()
				lineup.undraw()
				linedown.undraw()
				
				
		chdir('./bin')
		upp=open('prefersett.txt','w')
		for i in range(0,len(peep)):
			upp.write(str(peep[i])+'\n')
		
		upp.close()
		chdir('../')
		
	win7.close()
	


				#Text(Point(1.4,5.5),'Class Recording:').draw(win7)
				#fudgy=Entry(Point(6.55,5.5),25)
				#fudgy.setText('.file-type')
				#fudgy.draw(win7)
		
			







################### INTERFACE PROGRAM ############################

#Define Window
win = GraphWin("S.T.A.R.", 600, 600)
win.setBackground('white')
win.setCoords(0.0,25.0,11.0,0.0)





######################### LOGO #################################

chdir('./Logos')
Image(Point(5.3,3.23),'STAR1.gif').draw(win)

#Image(Point(9.99,1.4),'CTE1.png').draw(win)

chdir('../')
# star=Polygon(Point(5.3,1),Point(4.5,2.8),Point(3.3,2.8),Point(4.3,3.5),Point(3.3,6),Point(5.3,4),Point(7.3,6),Point(6.4,3.5),Point(7.3,2.8),Point(6.1,2.8),Point(5.3,1))
# star.setFill('yellow1')
# star.draw(win)
# Text(Point(5.3,3.2),'S.T.A.R.').draw(win)







################### ADVANCED SETTINGS BUTTON ####################


ASbutton=Text(Point(1.4,0.4),'Advanced Settings')
AS=Rectangle(Point(0.1,0.1),Point(2.7,0.8))
AS.setFill('red1')
AS.draw(win)
ASbutton.draw(win)


##################### TRACKING BUTTON ###########################
Tbutton=Text(Point(10,0.4),'Tracking')
Track=Rectangle(Point(9.4,0.1),Point(10.67,0.8))
Track.setFill('green')
Track.draw(win)
Tbutton.draw(win)




################### LINES SEPERATING LOGO ######################

l3=Line(Point(0,7),Point(11,7))
l3.draw(win)

l4=Line(Point(0,6.5),Point(11,6.5))
l4.draw(win)



######################### TRAINING ENTRY #######################

# #Training Word Entry
Text(Point(3.4,8),'Training Word:').draw(win)
trw=Entry(Point(5.5,8),12)
trw.setText('')
trw.draw(win)


# #Train Data File Name Entry
Text(Point(3.4,9.5),'Training File Name:').draw(win)

# Browse to choose file button
bftbutton=Text(Point(8.5,9.5),'Browse')
bft=Rectangle(Point(7.9,9.1),Point(9.1,10.1))
bft.setFill('grey')
bft.draw(win)
bftbutton.draw(win)

bftan=Text(Point(6,9.5),'none selected')
bftan.draw(win)



# #Train Button
trnbutton=Text(Point(5.3,11.3),'Train')
trn=Rectangle(Point(4,10.5),Point(6.7,12.2))
trn.setFill('green1')
trn.draw(win)
trnbutton.draw(win)


################ LINE SEPERATING ENTRIES #######################


l1=Line(Point(0,12.7),Point(11,12.7))
l1.draw(win)

l2=Line(Point(0,13.1),Point(11,13.1))
l2.draw(win)


####################### DECODING ENTRY #########################

#Class Recording File Name Entry
Text(Point(3.4,17.1),'Class Recording:').draw(win)
#f=Entry(Point(6.5,17.1),20)
#f.setText('.file-type')
#f.draw(win)


# Browse to choose file button
bfbutton=Text(Point(8.5,17.1),'Browse')
bf=Rectangle(Point(7.9,16.7),Point(9.1,17.7))
bf.setFill('grey')
bf.draw(win)
bfbutton.draw(win)

bfan=Text(Point(6,17.1),'none selected')
bfan.draw(win)


# #Trigger Word C.P.
Text(Point(3.4,15.8),'Trigger Word C.P.').draw(win)
tcp=Entry(Point(5.8,15.8),12)
tcp.setText('')
tcp.draw(win)

# #Trigger Word W.T.
Text(Point(3.4,14.5),'Trigger Word W.T.').draw(win)
twt=Entry(Point(5.8,14.5),12)
twt.setText('')
twt.draw(win)



#Find Times Button
tmbutton=Text(Point(5.3,18.95),'Find My Times')
tm=Rectangle(Point(4,18),Point(6.7,20))
tm.setFill('yellow1')
tm.draw(win)
tmbutton.draw(win)


############## LINES SEPERATING ANSWERS ########################

l5=Line(Point(0,20.4),Point(11,20.4))
l5.draw(win)
l6=Line(Point(0,20.9),Point(11,20.9))
l6.draw(win)



########################## ANSWERS ############################

Text(Point(3.05,22.1),'Average Wait Time:').draw(win)
Text(Point(2.4,23.1),'Average Clarification Pauses:').draw(win)
#Text(Point(7.05,22.1),'Number given:').draw(win)
#Text(Point(7.05,23.1),'Number given:').draw(win)

#Text(Point(5.6,22.1),'00.00 seconds').draw(win)
#Text(Point(5.6,23.1),'00.00 seconds').draw(win)

#Text(Point(9.05,22.1),'000 times/class').draw(win)
#Text(Point(9.05,23.1),'000 times/class').draw(win)





####################### BUTTON CLICKING ########################
h=0
R=[]


todecode=''
totrain=''

while h==0:
	p1=win.getMouse()
	
	Track=Rectangle(Point(9.4,0.1),Point(10.67,0.8))
	######### PRESS TRACKING BUTTON ################
	if 9.4<=p1.getX()<=10.67 and 0.1<=p1.getY()<=0.8:
		try:
			tracker()
		except:
			pass
	
	####### PRESS BROWSE BUTTON ######
	if 7.9<=p1.getX()<=9.1:
		#### CLASS RECORDING ####
		if 16.7<=p1.getY()<=17.7:
			flipper=fileopenbox()
			fl=str(flipper).split('\\')
			bfan.setText(fl[len(fl)-1])
			todecode=flipper
			
		#### TRAINING DATA ####
		if 9.1<=p1.getY()<=10.1:
			flipp=fileopenbox()
			fll=str(flipp).split('\\')
			bftan.setText(fll[len(fll)-1])
			totrain=flipp
			
			
	
	
	
	####### PRESS ADVANCED SETTINGS BUTTON ########
	if 0.1<=p1.getX()<=2.7 and 0.1<=p1.getY()<=0.8:
		try:
			advanced_settings()
		except:
			pass
	
	
	######### PRESS TRAIN BUTTON ##########
	if 4<=p1.getX()<=6.7 and 10.5<=p1.getY()<=12.2:
		####################################
		###### UPDATE TRACKING DATA ########
		####################################
		

		
	
		######### CHECK IF FILE EXISTS ##############
		#totrain=todo
		#chdir('./audio_files')
		if totrain!='':
			fiil=str(totrain).split('\\')
		else:
			fiil=['None Selected']
		xmas1=True
		while xmas1:
			if path.exists(totrain):
				#chdir('../')
				xmas1=False
			else:
				win5=GraphWin('OOPS!',500,150)
				win5.setBackground('white')
				win5.setCoords(0.0,11.0,6.0,0.0)
				#pluuu=Text(Point(3,6),'(This may take some time)')
				#pluuu.draw(win2)
				#hText(Point(1.4,5.5),'Class Recording:').draw(win5)
				#fudger=Entry(Point(3.55,5.5),25)
				#fudger.setText('.file-type')
				#fudger.draw(win5)
				if len(fiil)!=1:
					zzzz=Text(Point(3,2.3),fiil[len(fiil)-1])
					zzz=Text(Point(3,4.5),'DOES NOT EXIST')
				else:
					zzzz=Text(Point(3,2.3),'You Forgot')
					zzz=Text(Point(3,4.5),'To Enter A File')
				zzz.setSize(20)
				zzz.setStyle('bold')
				zzz.setFace('courier')
				zzz.setTextColor('red')
				zzz.draw(win5)
				zzzz.setSize(25)
				zzzz.setStyle('bold')
				zzzz.setFace('courier')
				zzzz.setTextColor('red')
				zzzz.draw(win5)
				haha=Text(Point(3,6.9),'make sure your file is in the folder audio_files')
				haha2=Text(Point(3,8),'and remember to use the correct extension for example .mp3')
				haha.setStyle('bold')
				haha2.setStyle('bold')
				haha2.draw(win5)
				haha.draw(win5)
				zz2=Text(Point(3,9.9),'(click anywhere to go back!)')
				zz2.draw(win5)

				#chdir('../')
				try:
					win5.getMouse()
					win5.close()
				except:
					pass
				bftan.setText('none selected')
				break
				
				
######### CHECK CORRECT FILE TYPE ###########
		xmas3=False
		if xmas1==False:
			ffuu=str(totrain).split('\\')
			overthisshit=list(ffuu[len(ffuu)-1])
			sooverit=False
			for shit in overthisshit:
				if shit=='.':
					sooverit=True
			if sooverit:
				a, sucka=ffuu[len(ffuu)-1].split('.')
			else:
				sucka='empty'
			filetypes=['wav','mp3','flv','mp4']
			if sucka not in filetypes:
				xmas3=True
				

			
			if xmas3:

				win5=GraphWin('No Such File',500,150)
				win5.setBackground('white')
				win5.setCoords(0.0,11.0,6.0,0.0)
				#pluuu=Text(Point(3,6),'(This may take some time)')
				#pluuu.draw(win2)
				#hText(Point(1.4,5.5),'Class Recording:').draw(win5)
				#fudger=Entry(Point(3.55,5.5),25)
				#fudger.setText('.file-type')
				#fudger.draw(win5)
				zzzz=Text(Point(3,2.3),'.'+sucka)
				zzz=Text(Point(3,4.5),'IS NOT A VALID FILE TYPE')
				zzz.setSize(20)
				zzz.setStyle('bold')
				zzz.setFace('courier')
				zzz.setTextColor('red')
				zzz.draw(win5)
				zzzz.setSize(25)
				zzzz.setStyle('bold')
				zzzz.setFace('courier')
				zzzz.setTextColor('red')
				zzzz.draw(win5)
				haha=Text(Point(3,6.8),'S.T.A.R. only excepts files of type:')
				haha2=Text(Point(3,8),'.wav, .mp3, .flv, and .mp4')
				haha.setStyle('bold')
				haha2.setStyle('bold')
				haha2.draw(win5)
				haha.draw(win5)
				zz2=Text(Point(3,9.9),'(click anywhere to go back!)')
				zz2.draw(win5)

				
				try:
					win5.getMouse()
					win5.close()
				except:
					pass
				bftan.setText('none selected')
			
			
		if xmas1==False and xmas3==False:
			stealing=trw.getText()
			if stealing=='':
				win5=GraphWin('Forgot to write Word',500,150)
				win5.setBackground('white')
				win5.setCoords(0.0,11.0,6.0,0.0)
				zzzz=Text(Point(3,2.3),'You Forgot')
				zzz=Text(Point(3,4.5),'To Enter A Word')
				zzz.setSize(20)
				zzz.setStyle('bold')
				zzz.setFace('courier')
				zzz.setTextColor('red')
				zzz.draw(win5)
				zzzz.setSize(25)
				zzzz.setStyle('bold')
				zzzz.setFace('courier')
				zzzz.setTextColor('red')
				zzzz.draw(win5)
				haha=Text(Point(3,6.9),'The training word should be')
				haha2=Text(Point(3,8),'the word you say in the training file')
				haha.setStyle('bold')
				haha2.setStyle('bold')
				haha2.draw(win5)
				haha.draw(win5)
				zz2=Text(Point(3,9.9),'(click anywhere to go back!)')
				zz2.draw(win5)

				try:
					win5.getMouse()
					win5.close()
				except:
					pass
				trw.setText('')
			else:
				#Loading Window
				win2=GraphWin('Training...',500,150)
				win2.setBackground('white')
				win2.setCoords(0.0,11.0,6.0,0.0)
				ttt=Text(Point(3,6),'(This may take some time)')
				ttt.draw(win2)
				tt=Text(Point(3,3),'System Processing...')
				tt.setSize(25)
				tt.setStyle('bold')
				tt.setFace('courier')
				tt.setTextColor('red')
				tt.draw(win2)
				tt2=Text(Point(3,9),'(This window will close when the process is done!)')
				tt2.draw(win2)

				
				poo3=0
				#Runs the Training Program
				try:
					ender=trainer(totrain,trw.getText())
					win2.close()
					
				except:
					poo3=1
					pass
				if poo3==1:
					l123=str(totrain).split('\\')
					
					win2.close()
					win4=GraphWin('File Cannot Process',500,150)
					win4.setBackground('white')
					win4.setCoords(0.0,11.0,6.0,0.0)
					#pluuu=Text(Point(3,6),'(This may take some time)')
					#pluuu.draw(win2)
					#Text(Point(1.4,7.1),'Class Recording:').draw(win4)
					#fudge=Entry(Point(3.55,7.1),25)
					#fudge.setText('.file-type')
					#fudge.draw(win4)
					zzzz=Text(Point(3,2.7),'Something is WRONG')
					zzz=Text(Point(3,4.8),'with the file: '+l123[len(l123)-1])
					zzz.setSize(20)
					zzz.setStyle('bold')
					zzz.setFace('courier')
					zzz.setTextColor('red')
					zzz.draw(win4)
					zzzz.setSize(25)
					zzzz.setStyle('bold')
					zzzz.setFace('courier')
					zzzz.setTextColor('red')
					zzzz.draw(win4)
					Text(Point(3,8.5),'Select a different file and try again').draw(win4)
					zz2=Text(Point(3,9.9),'(click anywhere when done!)')
					zz2.draw(win4)

					try:
						win4.getMouse()
						win4.close()
					except:
						pass
				
				else:
					
						
					chdir('./audio_files/temp')
					remove(ender)
					chdir('../')
					chdir('../')
					win2.close()
					trw.setText('')
					bftan.setText('none selected')
					bftan.setText('none selected')
		
		
		
		
	
	
	
	
	##### PRESSED FIND MY TIMES BUTTON ########
	if 4<=p1.getX()<=6.7 and 18<=p1.getY()<=20:
		now=datetime.datetime.now()
		dater=str(now.month)+'-'+str(now.day)+'-'+str(now.year)
		
		
				


		############ CHECK IF FILE EXISTS #######
		#todecode=f.getText()
		ffiill=str(todecode)
		#chdir('./audio_files')
		if todecode!='':
			fffuuu=str(todecode).split('\\')
		else:
			fffuuu=['none selected']
		xmas=True
		while xmas:
			if path.exists(todecode):
				#chdir('../')
				xmas=False
			else:
				win5=GraphWin('OOPS!',500,150)
				win5.setBackground('white')
				win5.setCoords(0.0,11.0,6.0,0.0)
				#pluuu=Text(Point(3,6),'(This may take some time)')
				#pluuu.draw(win2)
				#hText(Point(1.4,5.5),'Class Recording:').draw(win5)
				#fudger=Entry(Point(3.55,5.5),25)
				#fudger.setText('.file-type')
				#fudger.draw(win5)
				if len(fffuuu)!=1:
					zzzz=Text(Point(3,2.3),fffuuu[len(fffuuu)-1])
					zzz=Text(Point(3,4.5),'DOES NOT EXIST')
				else:
					zzzz=Text(Point(3,2.3),'You Forgot')
					zzz=Text(Point(3,4.5),'To Enter A File')
				zzz.setSize(20)
				zzz.setStyle('bold')
				zzz.setFace('courier')
				zzz.setTextColor('red')
				zzz.draw(win5)
				zzzz.setSize(25)
				zzzz.setStyle('bold')
				zzzz.setFace('courier')
				zzzz.setTextColor('red')
				zzzz.draw(win5)
				haha=Text(Point(3,6.9),'make sure your file is in the folder audio_files')
				haha2=Text(Point(3,8),'and remember to use the correct extension for example .mp3')
				haha.setStyle('bold')
				haha2.setStyle('bold')
				haha2.draw(win5)
				haha.draw(win5)
				zz2=Text(Point(3,9.9),'(click anywhere to go back!)')
				zz2.draw(win5)

				#chdir('../')
				try:
					win5.getMouse()
					win5.close()
				except:
					pass
				bfan.setText('none selected')
				break
				
		######### CHECK CORRECT FILE TYPE ###########
		xmas2=False
		if xmas==False:
			overthisshit=list(todecode)
			sooverit=False
			for shit in overthisshit:
				if shit=='.':
					sooverit=True
			if sooverit:
				a, sucka=todecode.split('.')
			else:
				sucka='empty'
			filetypes=['wav','mp3','flv','mp4']
			if sucka not in filetypes:
				xmas2=True
				

			
			if xmas2:

				win5=GraphWin('Bad File Type',500,150)
				win5.setBackground('white')
				win5.setCoords(0.0,11.0,6.0,0.0)
				#pluuu=Text(Point(3,6),'(This may take some time)')
				#pluuu.draw(win2)
				#hText(Point(1.4,5.5),'Class Recording:').draw(win5)
				#fudger=Entry(Point(3.55,5.5),25)
				#fudger.setText('.file-type')
				#fudger.draw(win5)
				zzzz=Text(Point(3,2.3),'.'+sucka)
				zzz=Text(Point(3,4.5),'IS NOT A VALID FILE TYPE')
				zzz.setSize(20)
				zzz.setStyle('bold')
				zzz.setFace('courier')
				zzz.setTextColor('red')
				zzz.draw(win5)
				zzzz.setSize(25)
				zzzz.setStyle('bold')
				zzzz.setFace('courier')
				zzzz.setTextColor('red')
				zzzz.draw(win5)
				haha=Text(Point(3,6.8),'S.T.A.R. only excepts files of type:')
				haha2=Text(Point(3,8),'.wav, .mp3, .flv, and .mp4')
				haha.setStyle('bold')
				haha2.setStyle('bold')
				haha2.draw(win5)
				haha.draw(win5)
				zz2=Text(Point(3,9.9),'(click anywhere to go back!)')
				zz2.draw(win5)

				
				try:
					win5.getMouse()
					win5.close()
				except:
					pass
				bfan.setText('none selected')
				
					
				#todecode=fudger.getText()

			





		if xmas==False and xmas2==False:
			#chdir('../')
			#Loading Window
			win2=GraphWin('Calculating...',500,150)
			win2.setBackground('white')
			win2.setCoords(0.0,11.0,6.0,0.0)
			ttt=Text(Point(3,6),'(This may take some time)')
			ttt.draw(win2)
			tt=Text(Point(3,3),'System Processing...')
			tt.setSize(25)
			tt.setStyle('bold')
			tt.setFace('courier')
			tt.setTextColor('red')
			tt.draw(win2)
			tt2=Text(Point(3,9),'(This window will close when the process is done!)')
			tt2.draw(win2)

			#Runs Decoder
			pooppyy=0
			yoyoman=True
			while yoyoman:
				
				try:
					W,S,E,P,WW,LW=TheGame(todecode)
					win2.close()
				except:
					pooppyy=1
					pass
				if pooppyy==1:
					l123=str(todecode).split('\\')
					
					win2.close()
					win4=GraphWin('File Cannot Process',500,150)
					win4.setBackground('white')
					win4.setCoords(0.0,11.0,6.0,0.0)
					#pluuu=Text(Point(3,6),'(This may take some time)')
					#pluuu.draw(win2)
					#Text(Point(1.4,7.1),'Class Recording:').draw(win4)
					#fudge=Entry(Point(3.55,7.1),25)
					#fudge.setText('.file-type')
					#fudge.draw(win4)
					zzzz=Text(Point(3,2.7),'Something is WRONG')
					zzz=Text(Point(3,4.8),'with the file: '+l123[len(l123)-1])
					zzz.setSize(20)
					zzz.setStyle('bold')
					zzz.setFace('courier')
					zzz.setTextColor('red')
					zzz.draw(win4)
					zzzz.setSize(25)
					zzzz.setStyle('bold')
					zzzz.setFace('courier')
					zzzz.setTextColor('red')
					zzzz.draw(win4)
					Text(Point(3,8.5),'Select a different file and try again').draw(win4)
					zz2=Text(Point(3,9.9),'(click anywhere when done!)')
					zz2.draw(win4)

					try:
						win4.getMouse()
						win4.close()
						yoyoman=False
					except:
						yoyoman=False
						pass
				else:
					yoyoman=False


					
				

			if pooppyy==0:
				#h=1
				CP=['CLARIFICATION', 'CLARIFICATIONS','CLARIFY','QUESTION','QUESTIONS',str(tcp.getText())]
				WT=['WAIT',str(twt.getText())]


				#preprocess Silence:
				SILE,SILS,SILCT=silence(W, E, S)

				#associate trigger words to silences:
				WTI,CPI=findTimes(W,SILE,SILS,SILCT,CP,WT,S,P,LW)


				#find average times
				AWT,ACP, countCP, countWT=AverageTimes(E,S,SILCT,SILS, SILE,WTI,CPI)
				win2.close()


				AWT=AWT*0.01
				ACP=ACP*0.01
				l123=str(todecode).split('\\')
				fn, dt, wttr,cptr=buildtrack()
				dt.append(dater)
				fn.append(l123[len(l123)-1])
				wttr.append(AWT)
				cptr.append(ACP)
				updata(fn,dt,wttr,cptr)


				Text(Point(5.6,22.1),str(AWT)+' seconds').draw(win)
				Text(Point(5.6,23.1),str(ACP)+' seconds').draw(win)



				Text(Point(9.05,22.1),str(countWT)+' times/class').draw(win)
				Text(Point(9.05,23.1),str(countCP)+' times/class').draw(win)


				#tmbutton.setText('Quit')











######################## CLOSE WINDOW ##########################

g=0
while g==0:
	p2=win.getMouse() # Pause to view result

	if 4<=p2.getX()<=6.7 and 18<=p2.getY()<=20:
		win.close()    # Close window when done
		g=1







