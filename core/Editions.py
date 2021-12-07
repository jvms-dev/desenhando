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
| Brings together classes related to the file menu.                                      |
|                                                                                        |
+----------------------------------------------------------------------------------------+
"""

import logging

from tkinter import *
from tkinter import ttk

from .Dialogs import PageSizeDialog


class PageSize:

    def __init__(self, parent):

        self.parent = parent
        self.root = parent.root
        # self.page_size_dialog = None
        self.add_option_to_menu()

    def add_option_to_menu(self):
        if hasattr(self.parent, 'menus') and 'edit' in self.parent.menus:
            self.parent.menus['edit'].add_command(label='Drawing area', command=self.show_dialog_for_page_size)

        else:
            logging.error("It was not possible to add the SalveAs function to the "
                          "file menu. Attribute 'menu' not found in self.parent.")

    def show_dialog_for_page_size(self, event=None):
        PageSizeDialog(self.root)
