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

from .CustomComponents import NumericalSpinBox
from .DrawingArea import DrawingArea


class LoadingDialog(Toplevel):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.title('Loading...')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.ok)
        self.transient(parent)
        self.grab_set()
        self.frame = ttk.Frame(self)
        self.frame.grid(column=0, row=0, sticky=(N, S, E, W), padx=5, pady=5)

        self.progress_bar = ttk.Progressbar(self.frame, orient=HORIZONTAL, mode='indeterminate')
        self.progress_bar.grid(column=0, row=0, sticky=(N, S, E, W), padx=5, pady=5)
        self.progress_bar.start()

    def ok(self, event=None):
        pass


class PageSizeDialog(Toplevel):

    models = {'': (0, 0),
              'A4': (2480, 3508),
              '1280x720 (HD 720p)': (1280, 720),
              '1920x1080 (FULL HD 1080p)': (1920, 1080)
              }

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.title('Window')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.ok)
        self.transient(parent)
        self.grab_set()
        self.draw_area = DrawingArea.get_instance_of_drawing_area()

        self.frame = frame = ttk.Frame(self)
        self.frame.grid(column=0, row=0, sticky=(N, S, E, W), padx=5, pady=5)

        ttk.Label(frame, text='Model ').grid(column=0, row=0)
        self.model = ttk.Combobox(frame, values=list(self.models.keys()))
        self.model.grid(column=1, row=0, sticky=(E, W))
        self.model.state(["readonly"])
        self.model.bind('<<ComboboxSelected>>', self.change_size)

        ttk.Separator(frame, orient=HORIZONTAL).grid(column=0, row=1, pady=10, sticky=(E, W), columnspan=2)

        ttk.Label(frame, text='Page size (px)').grid(column=0, row=2, pady=5, columnspan=2)
        ttk.Label(frame, text='Width ').grid(column=0, row=3, pady=2)
        self.size_x = NumericalSpinBox(frame)
        self.size_x.grid(column=1, row=3, sticky=(E, W), pady=2)
        ttk.Label(frame, text='Height ').grid(column=0, row=4, pady=2)
        self.size_y = NumericalSpinBox(frame)
        self.size_y.grid(column=1, row=4, sticky=(E, W), pady=2)

        self.apply = ttk.Button(frame, text='Apply', command=self.apply_settings)
        self.apply.grid(column=0, row=5, columnspan=2, pady=10)

        self.set_default_values()

    def set_default_values(self):
        """
        When starting this method it gets the current size of the painting area.

        :return: None
        """
        x, y = self.draw_area.get_canvas_size()
        self.size_x.set(x)
        self.size_y.set(y)

    def ok(self, event=None):
        self.grab_release()
        self.destroy()

    def change_size(self, event=None):
        if self.model.get():
            x, y = self.models[self.model.get()]
            self.size_x.set(x)
            self.size_y.set(y)

    def apply_settings(self, event=None):
        x = self.size_x.get()
        y = self.size_y.get()
        self.draw_area.update_workspace_size(x, y)
