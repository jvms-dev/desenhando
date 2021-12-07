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
| Implement some tkinter widget customizations.                                          |
|                                                                                        |
+----------------------------------------------------------------------------------------+
"""
from tkinter import *
from tkinter import ttk


class NumericalSpinBox(ttk.Spinbox):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        function = (self.register(lambda value: len(value) == 0 or value.isdecimal()), '%P')
        self['to'] = 10000
        self['from_'] = 1
        self['validate'] = 'key'
        self['validatecommand'] = function
        self.set(1)


class AutoHideScrollbar(ttk.Scrollbar):
    """
    A scrollbar that is automatically hidden when not needed.
    Only the grid geometry manager is supported ttk.
    """

    def set(self, lo, hi):
        if float(lo) > 0.0 or float(hi) < 1.0:
            self.grid()
        else:
            self.grid_remove()
        super().set(lo, hi)

    def pack(self, **kwargs):
        raise TclError(f'{self.__class__.__name__} does not support "pack"')

    def place(self, **kwargs):
        raise TclError(f'{self.__class__.__name__} does not support "place"')


class NumericalComboBox(ttk.Combobox):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        function = (self.register(self.validate_input), '%P')
        self['values'] = self.default_values
        self['validate'] = 'key'
        self['validatecommand'] = function

    def validate_input(self, value):
        return len(value) == 0 or value.isdecimal()
