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
| Builds a window for viewing text.                                                      |
|                                                                                        |
+----------------------------------------------------------------------------------------+
"""

from tkinter import *

from core.CustomComponents import AutoHideScrollbar


class ScrollableTextFrame(Frame):
    """
    Display text with scrollbar(s).
    """

    def __init__(self, master, wrap=NONE, **kwargs):
        """
        Create a frame for Textview.
        The Text widget is accessible via the 'text' attribute.
        Note: Changing the wrapping mode of the text widget after
        instantiation is not supported.

        :param master: master widget for this frame
        :param wrap: type of text wrapping to use ('word', 'char' or 'none')
        :param kwargs: All parameters except for 'wrap' are passed to Frame.__init__()
        """
        super().__init__(master, **kwargs)

        text = self.text = Text(self, wrap=wrap)
        text.grid(row=0, column=0, sticky=NSEW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # vertical scrollbar
        self.yscroll = AutoHideScrollbar(self, orient=VERTICAL,
                                         takefocus=False,
                                         command=text.yview)
        self.yscroll.grid(row=0, column=1, sticky=NS)
        text['yscrollcommand'] = self.yscroll.set

        # horizontal scrollbar - only when wrap is set to NONE
        if wrap == NONE:
            self.xscroll = AutoHideScrollbar(self, orient=HORIZONTAL,
                                             takefocus=False,
                                             command=text.xview)
            self.xscroll.grid(row=1, column=0, sticky=EW)
            text['xscrollcommand'] = self.xscroll.set
        else:
            self.xscroll = None


class ViewFrame(Frame):
    """
    Display TextFrame and Close button.
    """

    def __init__(self, parent, contents, wrap='word'):
        """
        Create a frame for viewing text with a "Close" button.

        The Text widget is accessible via the 'text' attribute.
        :param parent: parent widget for this frame
        :param contents: text to display
        :param wrap: type of text wrapping to use ('word', 'char' or 'none')
        """
        super().__init__(parent)
        self.parent = parent
        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.ok)
        self.text_frame = ScrollableTextFrame(self, relief=SUNKEN, height=700)

        text = self.text = self.text_frame.text
        text.insert('1.0', contents)
        text.configure(wrap=wrap, highlightthickness=0, state='disabled')
        text.focus_set()

        self.button_ok = button_ok = Button(self, text='Close', command=self.ok, takefocus=False)
        self.text_frame.pack(side='top', expand=True, fill='both')
        button_ok.pack(side='bottom')

    def ok(self, event=None):
        """
        Dismiss text viewer dialog.

        :param event:
        :return: None
        """
        self.parent.destroy()


class ViewWindow(Toplevel):
    """
    A simple text viewer dialog for IDLE.
    """

    def __init__(self, parent, title, contents, modal=True, wrap=WORD, _htest=False, _utest=False):
        """
        Show the given text in a scrollable window with a 'close' button.
        If modal is left True, users cannot interact with other windows
        until the textview window is closed.

        :param parent: parent of this dialog
        :param title: string which is title of popup dialog
        :param contents: text to display in dialog
        :param modal: text to display in dialog
        :param wrap: type of text wrapping to use ('word', 'char' or 'none')
        :param _htest: change box location when running htest.
        :param _utest: don't wait_window when running unittest.
        """
        super().__init__(parent)
        self['borderwidth'] = 5
        # Place dialog below parent if running htest.
        x = parent.winfo_rootx() + 10
        y = parent.winfo_rooty() + (10 if not _htest else 100)
        self.geometry(f'=750x500+{x}+{y}')

        self.title(title)
        self.viewframe = ViewFrame(self, contents, wrap=wrap)
        self.protocol("WM_DELETE_WINDOW", self.ok)
        self.button_ok = button_ok = Button(self, text='Close', command=self.ok, takefocus=False)
        self.viewframe.pack(side='top', expand=True, fill='both')

        self.is_modal = modal
        if self.is_modal:
            self.transient(parent)
            self.grab_set()
            if not _utest:
                self.wait_window()

    def ok(self, event=None):
        """
        Dismiss text viewer dialog.

        :param event:
        :return:
        """

        if self.is_modal:
            self.grab_release()
        self.destroy()


def view_text(parent, title, contents, modal=True, wrap='word', _utest=False):
    """
    Create text viewer for given text.

    :param parent: parent of this dialog
    :param title: string which is the title of popup dialog
    :param contents: text to display in this dialog
    :param modal: type of text wrapping to use ('word', 'char' or 'none')
    :param wrap: controls if users can interact with other windows while this dialog is displayed
    :param _utest: controls wait_window on unittest
    :return: ViewWindow
    """

    return ViewWindow(parent, title, contents, modal, wrap=wrap, _utest=_utest)
