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
from tkinter import filedialog
from tkinter import messagebox

from .Dialogs import LoadingDialog
from lib.SaveImage import SaveImage


class SalveAs:

    def __init__(self, parent):

        self.parent = parent
        self.root = parent.root
        self.loading_dialog = None
        self.add_option_to_menu()

        # Events triggered when the image is saved or an error occurs when saving
        self.root.bind('<<SavedFile>>', self.notify_that_the_file_has_been_saved)
        self.root.bind('<<ErrorSavingFile>>', self.warn_that_there_was_an_error_saving_the_image)

    def add_option_to_menu(self):
        if hasattr(self.parent, 'menus') and 'file' in self.parent.menus:
            self.parent.menus['file'].add_command(label='Salve as...', command=self.save_vector_as_image)

        else:
            logging.error("It was not possible to add the SalveAs function to the "
                          "file menu. Attribute 'menu' not found in self.parent.")

    def save_vector_as_image(self):
        """
        Gets the current drawing and saves as an image.

        :return: None
        """
        path = filedialog.asksaveasfilename(defaultextension='.png', parent=self.root)
        t = SaveImage('nome', self.root)
        t.start()
        self.loading_dialog = LoadingDialog(self.root)

    def notify_that_the_file_has_been_saved(self, event=None):
        self.loading_dialog.grab_release()
        self.loading_dialog.destroy()
        messagebox.showinfo(title='Salvo!', message='Imagem salva com sucesso!')

    def warn_that_there_was_an_error_saving_the_image(self, event=None):
        self.loading_dialog.grab_release()
        self.loading_dialog.destroy()
        messagebox.showerror(title='Error', message='Ocorreu um erro ao salvar a imagem.')
