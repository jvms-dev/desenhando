#!/usr/bin/env python3

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
| This file starts the Desenhando python application.                                    |
|                                                                                        |
+----------------------------------------------------------------------------------------+
"""

import sys

try:
    from tkinter import *
except ImportError:
    print("** Desenhando can't import Tkinter.\n"
          "Your Python may not be configured for Tk. **", file=sys.__stderr__)

from tkinter import messagebox

if TkVersion < 8.5:
    root_ = Tk()
    root_.withdraw()
    messagebox.showerror("Desenhando Cannot Start",
                         f"Desenhando requires tcl/tk 8.5+, not {TkVersion}.")
    raise SystemError(1)

import os
from platform import system
import logging

from core import DesenhandoBase
from lib.tools import set_copyright

__version__ = '1.4.0'
release = False

__status__ = "Production" if release else "Development"


def get_version_digits_str():
    """
    String representation of the version number only (no additional info)
    """
    return __version__


def is_release():
    """
    True when release version, False for nightly (dev) build
    """
    return release


def is_build():
    """
    Determine whether the app is frozen using pyinstaller/py2app.
    Returns True when this is a release or nightly build (eg. it is build as a
    distributable package), returns False if it is a source checkout.
    """
    return getattr(sys, 'frozen', False)


def get_version():
    """
    Comparable version as list of ints
    """
    return __version__.split('.')


def get_cwd():
    """
    Retrieve the folder where desenhando.py or desenhando.exe is located.
    This is not necessarily the CWD (current working directory), but it is what
    the CWD should be.
    """
    if is_build():
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.realpath(__file__))


def set_sys_path():
    """
    Append local module folders to python search path.
    """
    if not sys.platform.startswith('darwin'):  # Causes issues with py2app builds on MAC
        os.chdir(get_cwd())
    syspath = ["./", "./lib", "./core"]
    syspath.extend(sys.path)
    sys.path = syspath

    if is_build():
        # Make sure we load packaged DLLs instead of those present on the system
        os.environ["PATH"] = '.' + os.path.pathsep + get_cwd() + os.path.pathsep + os.environ["PATH"]


def init_logging(debug=True):
    """
    Configure the format of log messages

    :param debug: enable debug (Default=True)
    :return: None
    """
    debug = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=debug)


def parse_arguments():
    if len(sys.argv) < 2:
        return dict()

    import argparse  # requires python >= 2.7
    parser = argparse.ArgumentParser()

    # optional arguments
    parser.add_argument('-v', '--version', action='version', version=get_version_digits_str())
    parser.add_argument('-d', '--debug', help='enable debug', action='store_true')
    parser.add_argument("--license", action="store_true", help="Show full copyright notice and software license")

    if not is_release():
        parser.add_argument('-t', '--runtests', action='store_true', help='run test suite (for developers)')

    arg_options = vars(parser.parse_args())

    if arg_options.get('license', False):
        print("\n" + license() + "\n")
        sys.exit(0)

    return arg_options


def set_application_icon(root):
    icondir = os.path.join(get_cwd(), 'icons')

    if system() == 'Windows':
        icon_file = os.path.join(icondir, 'desenhando.ico')
        root.wm_iconbitmap(default=icon_file)
    else:
        if TkVersion >= 8.6:
            ext = '.png'
            sizes = (16, 32, 48, 256)
        else:
            ext = '.gif'
            sizes = (16, 32, 48)
        icon_files = [os.path.join(icondir, 'desenhando_%d%s' % (size, ext))
                      for size in sizes]
        icons = [PhotoImage(master=root, file=icon_file)
                 for icon_file in icon_files]
        root.wm_iconphoto(True, *icons)


def main():

    try:
        set_copyright()
        set_sys_path()
        os.environ['DS_VERSION'] = get_version_digits_str()
        args = parse_arguments()
        init_logging(args.get('debug', False))
        print(copyright())

    except Exception as e:
        print('ERROR: ' + format(str(e)), file=sys.stderr)
        import traceback
        bt = traceback.format_exc()
        print(bt, file=sys.stderr)
        return

    # Pass release info to debug dump using environment variables
    os.environ['DS_FROZEN'] = 'Yes' if is_build() else 'No'
    os.environ['DS_RELEASE'] = 'Yes' if is_release() else 'No'

    root = Tk(className='Desenhando')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    set_application_icon(root)
    base = DesenhandoBase.DesenhandoBase(root)

    root.mainloop()


if __name__ == '__main__':
    main()
