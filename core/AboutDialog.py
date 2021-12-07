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
| About Dialog for Desenhando.                                                           |
|                                                                                        |
+----------------------------------------------------------------------------------------+
"""

import os

from tkinter import *
from tkinter import ttk

from lib.tools import get_absolute_path
from lib.text_view import view_text


class AboutDialog(Toplevel):
    """
    Modal about dialog for idle
    """

    def __init__(self, parent, **kwargs):
        """
        Create popup, do not return until tk widget destroyed.

        :param parent: top level window
        :param kwargs: toplevel default parameters
        """

        super().__init__(parent, **kwargs)
        self.configure(borderwidth=5)
        self.geometry('+%d+%d' % (parent.winfo_rootx() + 30, parent.winfo_rooty() + 30))
        self.resizable(height=False, width=False)
        self.title(f"Sobre Desenhando {os.environ['DS_VERSION']}")
        self.transient(parent)
        self.grab_set()
        self.protocol('WM_DELETE_WINDOW', self.ok)
        self.parent = parent
        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.ok)
        self.bg = '#bbbbbb'
        self.fg = '#000000'
        self.create_widget()

    def create_widget(self):
        frame = Frame(self, borderwidth=2, relief=SUNKEN)
        frame_buttons = Frame(self)
        frame.pack(side=TOP, expand=True, fill=BOTH)
        frame_buttons.pack(side=BOTTOM, fill=X)
        ttk.Button(frame_buttons, text='Fechar', command=self.ok).pack(padx=5, pady=5)

        frame_background = Frame(frame, bg=self.bg)
        frame_background.pack(expand=True, fill=BOTH)

        header = Label(frame_background, text='Desenhando', fg=self.fg,
                       bg=self.bg, font=('courier', 24, 'bold'))
        header.grid(row=0, column=0, sticky=E, padx=10, pady=10)

        tk_patch_level = self.tk.call('info', 'patchlevel')
        ext = '.png' if tk_patch_level >= '8.6' else '.gif'
        icon = get_absolute_path('icons', f'desenhando_48{ext}')
        self.icon_image = PhotoImage(file=icon)
        logo = Label(frame_background, image=self.icon_image, bg=self.bg)
        logo.grid(row=0, column=0, sticky=W, rowspan=2, padx=10, pady=10)

        byline_text = 'Um simples programa para desenho' + 5 * '\n'
        byline = Label(frame_background, text=byline_text, justify=LEFT,
                       fg=self.fg, bg=self.bg)
        byline.grid(row=2, column=0, sticky=W, columnspan=3, padx=10, pady=5)

        version = Label(frame_background, text='Desenhando version:  ' + os.environ['DS_VERSION'],
                        fg=self.fg, bg=self.bg)
        version.grid(row=9, column=0, sticky=W, padx=10, pady=0)

        button_container = Frame(frame_background, bg=self.bg)
        button_container.grid(row=10, column=0, columnspan=2, sticky=NSEW)
        Button(button_container, text='License', width=8, highlightbackground=self.bg,
               command=self.show_py_license).pack(side=LEFT, padx=10, pady=10)
        Button(button_container, text='Copyright', width=8, highlightbackground=self.bg,
               command=self.show_py_copyright).pack(side=LEFT, padx=10, pady=10)
        Button(button_container, text='Credits', width=8, highlightbackground=self.bg,
               command=self.show_py_credits).pack(side=LEFT, padx=10, pady=10)

    def show_py_license(self):
        """
        Handle License button event.

        :return: None
        """

        self.display_printer_text('About - License', license)

    def show_py_copyright(self):
        """
        Handle Copyright button event.

        :return: None
        """

        self.display_printer_text('About - Copyright', copyright)

    def show_py_credits(self):
        """
        Handle Credits button event.

        :return: None
        """

        self.display_printer_text('About - Python Credits', credits)

    def display_printer_text(self, title, printer):
        """
        Create textview for built-in constants.
        Built-in constants have type _sitebuiltins._Printer.  The
        text is extracted from the built-in and then sent to a text
        viewer with self as the parent and title as the title of
        the popup.
        
        :param title: 
        :param printer: 
        :return: None
        """
        printer._Printer__setup()
        text = '\n'.join(printer._Printer__lines)
        self._current_textview = view_text(self, title, text,)

    def ok(self, event=None):
        """
        Dismiss help_about dialog.

        :param event:
        :return: None
        """
        self.grab_release()
        self.destroy()
