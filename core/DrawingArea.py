"""
+----------------------------------------------------------------------------------------+
|                                 This file is part of:                                  |
|                                      DESENHANDO                                        |
|                                 www.github.com/...                                     |
+----------------------------------------------------------------------------------------+
|     Copyright (c) 2021 João Vitor, ...                                                 |
|                                                                                        |
|     Permission is hereby granted, free of charge, to any person obtaining a copy       |
|     of this software and associated documentation files (the "Software"), to deal      |
|     in the Software without restriction, including without limitation the rights       |
|     to use, copy, modify, merge, publish, distribute, sublicense, and/or sell          |
|     copies of the Software, and to permit persons to whom the Software is              |
|     furnished to do so, subject to the following conditions:                           |
|                                                                                        |
|     The above copyright notice and this permission notice shall be included in         |
|     all copies or substantial portions of the Software.                                |
|                                                                                        |
|     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR         |
|     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,           |
|     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE        |
|     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER             |
|     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,      |
|     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN          |
|     THE SOFTWARE.                                                                      |
|                                                                                        |
+----------------------------------------------------------------------------------------+
|                                         ABSTRACT                                       |
+----------------------------------------------------------------------------------------+
| Implement some dialog screens.                                                         |
|                                                                                        |
+----------------------------------------------------------------------------------------+
"""

from tkinter import *
from tkinter import ttk

from .CustomComponents import AutoHideScrollbar
from .Tools import PencilTool  # test


class StatusBar(ttk.Frame):

    format_position = '{:04.0f}, {:04.0f}'
    format_page_size = '({}x{})px'
    zoom_default_values = ['100%', '50%', '150%', '200%']

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.mouse_position = ttk.Label(self, text=self.format_position.format(0, 0))
        self.mouse_position.grid(column=0, row=0, padx=10)

        ttk.Separator(self, orient=VERTICAL).grid(column=1, row=0, padx=10, sticky=(N, S))

        self.page_size = ttk.Label(self, text=self.format_page_size.format(1024, 720))
        self.page_size.grid(column=2, row=0)

        ttk.Separator(self, orient=VERTICAL).grid(column=3, row=0, padx=50, sticky=(N, S))

        self.zoom = ttk.Combobox(self, values=self.zoom_default_values)
        self.zoom.bind('<<ComboboxSelected>>', self.set_zoom)
        self.zoom.bind('<Return>', self.set_zoom)
        self.zoom.grid(column=4, row=0)

    def set_zoom(self, event=None):
        s = self.zoom.get()
        s = s.replace('%', '')
        try:
            value = int(s)
            self.zoom.set('{}%'.format(value))
        except ValueError:
            pass

    def _format_input(self, value):
        return int(value.replace('%', ''))

    def set_position(self, x, y):
        self.mouse_position['text'] = self.format_position.format(x, y)

    def set_page_size(self, x, y):
        self.page_size['text'] = self.format_page_size.format(x, y)


class DrawingArea:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, parent, **kwargs):
        self.parent = parent

        self.frame = frame = ttk.Frame(parent)
        frame.grid(**kwargs)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        self.drawing_area = drawing_area = Canvas(frame, background='#ffffff')
        self.drawing_area.grid(column=0, row=0)

        self.scroll_x = AutoHideScrollbar(frame,
                                          orient=HORIZONTAL,
                                          takefocus=False,
                                          command=drawing_area.xview)
        self.scroll_x.grid(column=0, row=1, sticky=(E, W))
        drawing_area['xscrollcommand'] = self.scroll_x.set

        self.scroll_y = AutoHideScrollbar(frame,
                                          orient=VERTICAL,
                                          takefocus=False,
                                          command=drawing_area.yview)
        self.scroll_y.grid(column=1, row=0, sticky=(N, S))
        drawing_area['yscrollcommand'] = self.scroll_y.set

        ttk.Separator(frame, orient=HORIZONTAL).grid(column=0, row=2, pady=10, sticky=(E, W), columnspan=2)

        # Create a status bar and update the mouse position as it moves within the drawing area
        self.status_bar = StatusBar(frame)
        self.status_bar.grid(column=0, row=3, sticky=(E, W))

        self.drawing_area.bind('<Motion>', self.update_mouse_position)
        self.drawing_area.bind('<Button-1>', self.start_drawing)
        self.drawing_area.bind('<B1-Motion>', self.update_drawing)
        self.drawing_area.bind('<B1-ButtonRelease>', self.finish_drawing)

        self.update_workspace_size(1024, 720)
        self.tool = None

    def update_mouse_position(self, event=None):
        x = self.drawing_area.canvasx(event.x)
        y = self.drawing_area.canvasy(event.y)
        self.status_bar.set_position(x, y)

    def update_workspace_size(self, width, height):
        self.drawing_area.configure(width=width,
                                    height=height,
                                    scrollregion=(0, 0, width, height))
        self.status_bar.set_page_size(width, height)

    def get_canvas_size(self):
        return self.drawing_area.winfo_width(), self.drawing_area.winfo_height()

    def start_drawing(self, event):
        if hasattr(self.tool, 'start'):
            self.tool.start(event)
        self.update_mouse_position(event)

    def update_drawing(self, event):
        if hasattr(self.tool, 'update'):
            self.tool.update(event)
        self.update_mouse_position(event)

    def finish_drawing(self, event):
        if hasattr(self.tool, 'finish'):
            self.tool.finish(event)
        self.update_mouse_position(event)

    @classmethod
    def get_instance_of_drawing_area(cls):
        if hasattr(cls, 'instance'):
            return cls.instance
        else:
            raise AttributeError('function object has no attribute instance')
