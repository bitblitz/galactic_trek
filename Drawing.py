# This module is designed to hide all the tkinter details
import tkinter as tk

import Colors
import Constants
import Util
import UserInput
import datetime

# need margin because anchor nw + (0,0) actually cuts off the left side of text like 'C'
DISPLAY_MARGIN_TOP = 5
DISPLAY_MARGIN_LEFT = 5

g_tk_root_window = None
g_main_canvas = None
g_main_rect = None

input_bbox = None

_frameFunction = None
_frame_count = 0
_frame_rate = 16  # 60 fps
_frame_initTime = datetime.datetime.now()

DEBUG_DISPLAY_BOUNDING_BOXES = False
DEBUG_DISPLAY_FRAME_INFO = True
DEBUG_VISIBLE_SPACES = False
DEBUG_VISIBLE_CHAR = '$'


def InitializeGameWindow(width, height):
    global g_tk_root_window
    global g_main_canvas
    global g_main_rect
    global _frame_initTime
    g_tk_root_window = tk.Tk()
    window = g_tk_root_window
    window.title = Constants.APPLICATION_TITLE
    g_main_canvas = tk.Canvas(window, width=width, height=height)
    g_main_rect = Util.Rect.fromCoord(DISPLAY_MARGIN_LEFT, DISPLAY_MARGIN_TOP, width - DISPLAY_MARGIN_LEFT,
                                   height - DISPLAY_MARGIN_TOP)
    g_main_canvas.configure(background='#888888')
    # if DEBUG_DISPLAY_BOUNDING_BOXES:
    #    g_main_canvas.create_rectangle(0,0,width,height,fill='#dddddd', outline=Colors.Window_Border, width=4)

    g_main_canvas.pack(fill=tk.BOTH, expand=1)

    window.update()
    _frame_initTime = datetime.datetime.now()


def mainloop():
    g_tk_root_window.mainloop()


# display a text object on the canvas and return it's bounding rect
def _canvas_print_at(canvas, left, top, text, *args, **kwargs):
    s = text.format(*args, **kwargs)
    # TODO: s = Util.print_to_string(text, *args, **kwargs)
    color = Colors.Text_Color
    if 'fill' in kwargs:
        color = kwargs['fill']
    canvasId = canvas.create_text(left, top,
                                  font=(Constants.MONOSPACE_FONT_FAMILY, Constants.BIG_FONT_SIZE),
                                  text=s, fill=color,
                                  anchor='nw')

    if DEBUG_DISPLAY_BOUNDING_BOXES:
        r = canvas.create_rectangle(canvas.bbox(canvasId), fill="#444444")
        canvas.tag_lower(r, canvasId)
    return Util.Rect(canvas.bbox(canvasId))


def _clear_canvas(canvas):
    canvas.delete(tk.ALL)


# Drawing Primitives
def clear_display():
    _clear_canvas(g_main_canvas)


def rectangle(left, top, right, bottom, fill, outline):
    r = g_main_canvas.create_rectangle(DISPLAY_MARGIN_LEFT + left,
                                       DISPLAY_MARGIN_TOP + top,
                                       DISPLAY_MARGIN_LEFT + right,
                                       DISPLAY_MARGIN_TOP + bottom, fill=fill, outline=outline)
    if DEBUG_DISPLAY_BOUNDING_BOXES:
        g_main_canvas.lower(r)
    return r


# def entryField(left, top, width, initialText):
#    entryWidget = tk.Entry(g_main_canvas, width=width)
#    g_main_canvas.create_window(left, top, window=entryWidget, anchor=tk.NW)
#    entryWidget.focus_set()
#    entryWidget.set()


def print_at(left, top, text, *args, **kwargs):
    rect = _canvas_print_at(g_main_canvas,
                            DISPLAY_MARGIN_LEFT + left,
                            DISPLAY_MARGIN_TOP + top, text, *args, **kwargs)
    # return rect
    return rect.fromCoord(rect.left + 1, rect.top + 1, rect.right - 1, rect.bottom - 1)  # rects are inflated 1 too big


# animation timer handling
def animate(frameFunction):
    global _frameFunction
    _frameFunction = frameFunction
    g_tk_root_window.after(_frame_rate, frame_ready)


def frame_ready():
    global _frame_count
    global _frameFunction
    global _frame_initTime
    _frame_count += 1

    # this is a pretty inefficient way to render each frame because tkinter allows the idea of
    # variable binding and we could use that instead.  However, this models a more direct
    # frame rendering model, so trying it to see what how it works out thinking of going to pygame
    # later
    clear_display()

    _frameFunction()
    if DEBUG_DISPLAY_FRAME_INFO:
        seconds = datetime.datetime.now() - _frame_initTime
        lineator = Lineator(g_main_rect.width() / 2, 0)
        lineator.print('   Frames:', _frame_count, ' FPS:', _frame_count / seconds.total_seconds())
        lineator.print('  Objects:', len(g_main_canvas.find_all()))
        lineator.print('  input Q:', UserInput.waitingInput(), '/', UserInput.waitingQuery())

    g_tk_root_window.after(_frame_rate, frame_ready)


# class that turns a bunch of line-based output into a vertical raster in our
# display space
class Lineator:
    def __init__(self, left, top):
        self.orig_top = top
        self.orig_left = left
        self.left = left
        self.top = top
        self.bbox = Util.Rect.fromCoord(left, top, left, top)

    def print(self, *args, **kwargs):
        text = Util.print_to_string(*args, **kwargs)
        if DEBUG_VISIBLE_SPACES:
            text = text.replace(' ', DEBUG_VISIBLE_CHAR)

        lineCount = 0
        while text.endswith('\n'):
            text = text[:-1]
            lineCount += 1

        # rect = print_at(self.left, self.top, '{0}', text)
        rect = print_at(self.left, self.top, text)
        self.left += rect.width()
        self.bbox.inflate(rect)

        if lineCount > 0:
            # if text.endswith('\n'):
            # self.top = self.bbox.bottom # += rect.height()
            self.top += rect.height() * lineCount
            self.left = self.orig_left

    def drawBoundingRect(self, fill=None, outline='Black', background=True):
        r = rectangle(self.bbox.left, self.bbox.top, self.bbox.right, self.bbox.bottom, fill=fill, outline=outline)
        if background:
            g_main_canvas.lower(r)
