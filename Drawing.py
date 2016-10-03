# This module is designed to hide all the tkinter details

import ActiveGame
import Globals
import Constants
import tkinter as tk
import io
from tkinter import messagebox

_frame_rate = 16  # 60 fps
DEBUG_DISPLAY_BOUNDING_BOXES = False

class tkRect:
    def __init__(self, list):
        self.left = list[0]
        self.top = list[1]
        self.right=list[2]
        self.bottom=list[3]

    @staticmethod
    def fromCoord(l, t, r, b):
        return tkRect((l,t,r,b))

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top

    def inflate(self, rect):
        self.left = min(self.left, rect.left)
        self.top= min(self.top, rect.top)
        self.right= max(self.right, rect.right)
        self.bottom= max(self.bottom, rect.bottom)


def InitializeGameWindow(width, height):
    Globals.g_tk_root_window = tk.Tk()
    window = Globals.g_tk_root_window
    window.title = Constants.APPLICATION_TITLE
    Globals.g_main_canvas = tk.Canvas(window, width=width, height=height)
    Globals.g_main_canvas.configure(background='grey')
    if DEBUG_DISPLAY_BOUNDING_BOXES:
        Globals.g_main_canvas.create_rectangle(0,0,width,height,fill=None, outline=Constants.COLOR_BORDER, width=4)
    Globals.g_main_canvas.pack(fill=tk.BOTH, expand=1)
    window.update()

# Helper functions
def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents

# display a text object on the canvas and return it's bounding rect
def _canvas_print_at(canvas, left, top, text, *args, **kwargs):
    s = text.format(*args, **kwargs)
    color = Constants.DEFAULT_TEXT_COLOR
    if 'fill' in kwargs:
        color = kwargs['fill']
    id = canvas.create_text(left, top,
                       font=(Constants.MONOSPACE_FONT_FAMILY, Constants.BIG_FONT_SIZE),
                       text=s, fill=color,
                       anchor='nw')

    if DEBUG_DISPLAY_BOUNDING_BOXES:
        r=canvas.create_rectangle(canvas.bbox(id),fill="white")
        canvas.tag_lower(r,id)
    return tkRect(canvas.bbox(id))


def _clear_canvas(canvas):
    canvas.delete(tk.ALL)

def _foo(textFrame):
    entryWidget = tk.Entry(textFrame)
    entryWidget["width"] = 50
    entryWidget.pack(side=tk.LEFT)


# exports
def clear_display():
    _clear_canvas(Globals.g_main_canvas)

def rectangle(left, top, right, bottom, fill, outline):
    r = Globals.g_main_canvas.create_rectangle(Constants.DISPLAY_MARGIN_LEFT +left,
                                               Constants.DISPLAY_MARGIN_TOP + top,
                                               Constants.DISPLAY_MARGIN_LEFT +right,
                                               Constants.DISPLAY_MARGIN_TOP + bottom, fill=fill, outline=outline)
    if DEBUG_DISPLAY_BOUNDING_BOXES:
        Globals.g_main_canvas.lower(r)
    return r

def print_at(left, top, text, *args, **kwargs):
    return _canvas_print_at(Globals.g_main_canvas,
                            Constants.DISPLAY_MARGIN_LEFT + left,
                            Constants.DISPLAY_MARGIN_TOP + top, text, *args, **kwargs)


def draw_current_sector(game: ActiveGame):
    rect = print_at(0, 0, 'Current Sector: {0}', game.player.galaxy_coord)
    bbox = game.galaxy[game.player.galaxy_coord].print_sector(0, rect.bottom+1)
    game.player.display(bbox.right + 5, rect.bottom + 1)
    # print('Current Sector: ', game.player.galaxy_coord)


def frame_ready(nextframe):
    Globals.g_tk_root_window.after(_frame_rate, nextframe)


# class that turns a bunch of line-based output into a vertical raster in our
# display space
class Lineator:
    def __init__(self, left, top):
        self.orig_top = top
        self.orig_left = left
        self.left = left
        self.top = top
        self.bbox = tkRect.fromCoord(left, top, left, top)

    def print(self, *args, **kwargs):
        text = print_to_string(*args, **kwargs)

        rect = print_at(self.left, self.top, '{0}', text)
        self.left += rect.width()
        self.bbox.inflate(rect)

        if text[-1:] == '\n':
            self.top += rect.height()
            self.left = self.orig_left

    def drawBoundingRect(self, fill=None, outline='Black'):
        rectangle(self.bbox.left, self.bbox.top, self.bbox.right, self.bbox.bottom, fill=fill, outline = outline )

