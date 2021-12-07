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
| Functions for sporadic tasks within the program.                                       |
|                                                                                        |
+----------------------------------------------------------------------------------------+
"""

import os
import sys
import builtins
import _sitebuiltins
import logging


def get_absolute_path(*part_of_the_way, dir=False):
    """
    Enable directory check

    :param dir: Check if the path points to a directory
    :param part_of_the_way: part of the way
    :return: absolute path or None
    """

    if getattr(sys, 'frozen', False):
        directory = os.path.dirname(sys.executable)
    else:
        directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    path = os.path.join(directory, *part_of_the_way)

    if dir:
        status = os.path.isdir(path)
    else:
        status = os.path.isfile(path)

    return path if status else None


def set_copyright():
    """Set 'license' in builtins"""
    builtins.copyright = _sitebuiltins._Printer('copyright', 'Copyright 2021 João Vitor and listed authors')
    builtins.credits = _sitebuiltins._Printer('credits', 'João V. M. Santos')
    path = get_absolute_path('LICENSE.TXT')
    if path:
        builtins.license = _sitebuiltins._Printer('license',
                                                  'See www.github.com/...',
                                                  ['LICENSE.TXT'],
                                                  [os.path.dirname(path)])
    else:
        logging.warning('Could not find license file')


def convert_screen_dimensions_str_to_tuple_int(dimensions_str):
    try:
        end_position = dimensions_str.index('+')
        s = dimensions_str[:end_position]
        return tuple(map(int, s.split('x')))

    except ValueError:
        logging.error('Unable to convert window dimension to integers')

    return 0, 0
