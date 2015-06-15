# -*- coding: utf-8 -*-

"""
    This module provides several utility functions
"""

import os
import re
import sys
import fnmatch
import traceback


from radish.terrain import world


class Failure(object):  # pylint: disable=too-few-public-methods
    """
        Represents the fail reason for a step
    """
    def __init__(self, exception):
        """
            Initalizes the Step failure with a given Exception

            :param Exception exception: the exception shrown in the step
        """
        self.exception = exception
        self.reason = unicode(str(exception), "utf-8")
        self.traceback = traceback.format_exc()
        self.name = exception.__class__.__name__
        traceback_info = traceback.extract_tb(sys.exc_info()[2])[-1]
        self.filename = traceback_info[0]
        self.line = int(traceback_info[1])


def console_write(text):
    """
        Writes the given text to the console

        If the --no-colors flag is given all colors are removed from the text
    """
    if world.config.no_ansi:
        text = re.sub(r"\x1b[^m]*m", "", text)

    print(text)


def expandpath(path):
    """
        Expands a path

        :param string path: the path to expand
    """
    return os.path.expanduser(os.path.expandvars(path))


def recursive_glob(root, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(root):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches


def get_debugger():
    """
        Returns a debugger instance
    """
    try:
        from IPython.core.debugger import Pdb
        pdb = Pdb()
    except ImportError:
        try:
            from IPython.Debugger import Pdb
            from IPython.Shell import IPShell

            IPShell(argv=[""])
            pdb = Pdb()
        except ImportError:
            import pdb

    return pdb


def datetime_to_str(datetime):
    """
        Returns the datetime object in a defined human readable format.

        :param Datetime datetime: the datetime object
    """
    if not datetime:
        return ""

    return datetime.strftime("%Y-%m-%dT%H:%M:%S")


def get_width(data):
    """
        Returns the needed width for a data column

        :param list data: a column with data
    """
    return max(len(x) for x in data)
