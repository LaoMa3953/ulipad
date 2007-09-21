#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2006 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   UliPad is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#   $Id: Debug.py 1504 2006-09-02 04:08:43Z limodou $

DEBUG = True
import types
import sys
import traceback
import time
import os.path

class Debug:
    def __init__(self, filename=os.path.abspath('debug.txt'), debug=None):
        self.filename = filename
        self.reset(filename)
        self.debug = debug

    def log(self, *args):
        self.output(*args)

    def info(self, *args):
        self.output('[ INFO] -- ', *args)

    def warn(self, *args):
        self.output('[ WARN] -- ', *args)

    def error(self, *args):
        self.output('[ERROR] -- ', *args)

    def debug(self, *args):
        self.output('[DEBUG] -- ', *args)

    def traceback(self):
        message = traceback.format_exception(*sys.exc_info())
        self.output('[Traceback]', ''.join(message))

    def time(self, *args):
        self.output('[%s] -- ' % time.ctime(time.time()), *args)

    def output(self, *args):
        if self.is_debug():
            #encoding = locale.getdefaultlocale()[1]
            encoding = 'utf-8'
            out = open(self.filename, 'a')
            for i in args:
                if not type(i) in [types.UnicodeType, types.StringTypes, types.StringType]:
                    s= repr(i)
                else:
                    s = i
                if type(s) == type(u''):
                    out.write(s.encode(encoding))
                else:
                    out.write(s)
            out.write("\n")
            out.close()

    def reset(self, filename):
        if self.is_debug():
            open(filename, 'w')
            self.filename = filename

    def is_debug(self):
        if not DEBUG:
            return False
        if self.debug is None:
            return DEBUG
        else:
            return self.debug

debug = None
error = None

if __name__ == '__main__':
    debug = Debug()
    error = Debug(os.path.abspath('error.txt'))
    debug.log('log')
    debug.info('info')
    debug.warn('warn')
    debug.error('error')
    debug.debug('debug')