#   Programmer:     limodou
#   E-mail:         limodou@gmail.com
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
#   $Id: mRun.py 1858 2007-01-25 14:15:57Z limodou $

import os
import wx
import locale
import types
from modules import Mixin
from modules import common


def message_init(win):
    wx.EVT_IDLE(win, win.OnIdle)
    wx.EVT_END_PROCESS(win.mainframe, -1, win.mainframe.OnProcessEnded)
    wx.EVT_KEY_DOWN(win, win.OnKeyDown)
    wx.EVT_KEY_UP(win, win.OnKeyUp)
    wx.EVT_UPDATE_UI(win, win.GetId(),  win.RunCheck)

    win.MAX_PROMPT_COMMANDS = 25

    win.process = None
    win.pid = -1

    win.CommandArray = []
    win.CommandArrayPos = -1

    win.editpoint = 0
    win.writeposition = 0
Mixin.setPlugin('messagewindow', 'init', message_init)

def RunCommand(win, command, redirect=True, hide=False, input_decorator=None):
    """replace $file = current document filename"""
    global input_appendtext
    if input_decorator:
        input_appendtext = input_decorator(appendtext)
    else:
        input_appendtext = appendtext
    if redirect:
        win.createMessageWindow()
        win.panel.showPage(tr('Message'))
        win.callplugin('start_run', win, win.messagewindow)
        win.messagewindow.SetReadOnly(0)
        appendtext(win.messagewindow, '> ' + command + '\n')
        
        win.messagewindow.editpoint = 0
        win.messagewindow.writeposition = 0
        win.SetStatusText(tr("Running "), 0)
        try:
            win.messagewindow.process = wx.Process(win)
            win.messagewindow.process.Redirect()
            if wx.Platform == '__WXMSW__':
                if hide == False:
                    win.messagewindow.pid = wx.Execute(command, wx.EXEC_ASYNC|wx.EXEC_NOHIDE, win.messagewindow.process)
                else:
                    win.messagewindow.pid = wx.Execute(command, wx.EXEC_ASYNC, win.messagewindow.process)
            else:
                win.messagewindow.pid = wx.Execute(command, wx.EXEC_ASYNC|wx.EXEC_MAKE_GROUP_LEADER, win.messagewindow.process)
            if hasattr(win.messagewindow, 'inputstream') and win.messagewindow.inputstream:
                win.messagewindow.inputstream.close()
            win.messagewindow.inputstream = win.messagewindow.process.GetInputStream()
            win.messagewindow.outputstream = win.messagewindow.process.GetOutputStream()
            win.messagewindow.errorstream = win.messagewindow.process.GetErrorStream()
        except:
            win.messagewindow.process = None
            dlg = wx.MessageDialog(win, tr("There are some problems when running the program!\nPlease run it in shell.") ,
                "Stop running", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
    else:
        wx.Execute(command, wx.EXEC_ASYNC)
Mixin.setMixin('mainframe', 'RunCommand', RunCommand)

def OnIdle(win, event):
    if win.process is not None:
        if win.inputstream:
            if win.inputstream.CanRead():
                text = win.inputstream.read()
                input_appendtext(win, text)
                win.writeposition = win.GetLength()
                win.editpoint = win.GetLength()
        if win.errorstream:
            if win.errorstream.CanRead():
                text = win.errorstream.read()
                input_appendtext(win, text)
                win.writeposition = win.GetLength()
                win.editpoint = win.GetLength()
Mixin.setMixin('messagewindow', 'OnIdle', OnIdle)

def OnKeyDown(win, event):
    keycode = event.GetKeyCode()
    pos = win.GetCurrentPos()
    if win.pid > -1:
        if (pos >= win.editpoint) and (keycode == wx.WXK_RETURN):
            text = win.GetTextRange(win.writeposition, win.GetLength())
            l = len(win.CommandArray)
            if (l < win.MAX_PROMPT_COMMANDS):
                win.CommandArray.insert(0, text)
                win.CommandArrayPos = -1
            else:
                win.CommandArray.pop()
                win.CommandArray.insert(0, text)
                win.CommandArrayPos = -1

            if isinstance(text, types.UnicodeType):
                text = text.encode(locale.getdefaultlocale()[1])
            win.outputstream.write(text + os.linesep)
            win.GotoPos(win.GetLength())
        if keycode == wx.WXK_UP:
            l = len(win.CommandArray)
            if (len(win.CommandArray) > 0):
                if (win.CommandArrayPos + 1) < l:
                    win.GotoPos(win.editpoint)
                    win.SetTargetStart(win.editpoint)
                    win.SetTargetEnd(win.GetLength())
                    win.CommandArrayPos = win.CommandArrayPos + 1
                    win.ReplaceTarget(win.CommandArray[win.CommandArrayPos])

        elif keycode == wx.WXK_DOWN:
            if len(win.CommandArray) > 0:
                win.GotoPos(win.editpoint)
                win.SetTargetStart(win.editpoint)
                win.SetTargetEnd(win.GetLength())
                if (win.CommandArrayPos - 1) > -1:
                    win.CommandArrayPos = win.CommandArrayPos - 1
                    win.ReplaceTarget(win.CommandArray[win.CommandArrayPos])
                else:
                    if (win.CommandArrayPos - 1) > -2:
                        win.CommandArrayPos = win.CommandArrayPos - 1
                    win.ReplaceTarget("")
    if ((pos > win.editpoint) and (not keycode == wx.WXK_UP)) or ((not keycode == wx.WXK_BACK) and (not keycode == wx.WXK_LEFT) and (not keycode == wx.WXK_UP) and (not keycode == wx.WXK_DOWN)):
        if (pos < win.editpoint):
            if (not keycode == wx.WXK_RIGHT):
                event.Skip()
        else:
            event.Skip()
Mixin.setMixin('messagewindow', 'OnKeyDown', OnKeyDown)

def OnKeyUp(win, event):
    keycode = event.GetKeyCode()
    #franz: pos was not used
    if keycode == wx.WXK_HOME:
        if (win.GetCurrentPos() < win.editpoint):
            win.GotoPos(win.editpoint)
        return
    elif keycode == wx.WXK_PRIOR:
        if (win.GetCurrentPos() < win.editpoint):
            win.GotoPos(win.editpoint)
        return
    event.Skip()
Mixin.setMixin('messagewindow', 'OnKeyUp', OnKeyUp)

def OnProcessEnded(win, event):
    if win.messagewindow.inputstream.CanRead():
        text = win.messagewindow.inputstream.read()
        input_appendtext(win.messagewindow, text)
    if win.messagewindow.errorstream.CanRead():
        text = win.messagewindow.errorstream.read()
        input_appendtext(win.messagewindow, text)

    if win.messagewindow.process:
        win.messagewindow.process.Destroy()
        win.messagewindow.process = None
        win.messagewindow.inputstream.close()
        win.messagewindow.inputstream = None
        win.messagewindow.outputstream = None
        win.messagewindow.errorstream = None
        win.messagewindow.pid = -1
        win.SetStatusText(tr("Finished! "), 0)
#        common.note(tr("Finished!"))
Mixin.setMixin('mainframe', 'OnProcessEnded', OnProcessEnded)

def appendtext(win, text):
    win.GotoPos(win.GetLength())
    if not isinstance(text, types.UnicodeType):
        text = unicode(text, locale.getdefaultlocale()[1])
    win.AddText(text)
    win.GotoPos(win.GetLength())
    win.EmptyUndoBuffer()
input_appendtext = appendtext

def RunCheck(win, event):
    if (win.GetCurrentPos() < win.editpoint) or (win.pid == -1):
        win.SetReadOnly(1)
    else:
        win.SetReadOnly(0)
Mixin.setMixin('messagewindow', 'RunCheck', RunCheck)