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
|                                                                                        |
|                                                                                        |
+----------------------------------------------------------------------------------------+
"""

from tkinter import *
from tkinter import ttk


from core import Help, Files, Editions, DrawingArea, Toolbox, Properties


class DesenhandoBase(ttk.Frame):

    menu_specs = ['file', 'edit', 'help']

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid(column=0, row=0, sticky=(N, S, E, W), padx=5, pady=5)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.root = parent

        # Menu bar settings
        self.root.option_add('*tearOff', FALSE)  # Prevents mine from separating from the menu bar
        self.menu_bar = menu_bar = Menu(parent)
        parent['menu'] = menu_bar
        self.menus = {}
        self._configure_the_menu_bar()

        # Components menu
        self.file = Files.SalveAs(self)
        self.help = Help.About(self)
        self.editions = Editions.PageSize(self)

        # Components
        self.drawing_area = DrawingArea.DrawingArea(self, column=0, row=2, sticky=(N, S, E, W))
        self.tool_box = Toolbox.Toolbox(self, self.root, self.drawing_area)
        self.tool_box.grid(column=0, row=0, sticky=(E, W))
        ttk.Separator(self, orient=HORIZONTAL).grid(column=0, row=1, pady=5, sticky=(E, W))
        self.properties = Properties.Properties(parent=self, draw_area=self.drawing_area.drawing_area,
                                                column=1, row=0, rowspan=3, padx=5, sticky=(N, S))

    def _configure_the_menu_bar(self):
        for name in self.menu_specs:
            formatted_name = name.capitalize()
            menu = Menu(self.menu_bar)
            self.menu_bar.add_cascade(menu=menu, label=formatted_name)
            self.menus[name] = menu
