import wx
from math import *


class CalcFrame(wx.Frame):

    def __init__(self, title):
        super().__init__(None, title=title, size=(300, 250))
        self.InitUI()
        self.Center()
        self.Show()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        'self代表此控件的父窗体，-1参数可自动创建一个唯一的标识'
        self.textprint = wx.TextCtrl(self, -1, '', style=wx.TE_RIGHT|wx.TE_READONLY)
        self.equation=''
        self.textprint.SetValue(self.equation)
        'flag指定尺寸、边框、对齐，当指定边框后，border则指定边框的尺寸'
        vbox.Add(self.textprint, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=5)

        gridBox = wx.GridSizer(5, 4, 5, 5)
        labels=['AC', 'DEL', 'PI', 'CLOSE', '7', '8', '9', '/',
                '4', '5', '6', '*', '1', '2', '3', '-', '0', '.',
                '=', '+']
        for label in labels:
            buttonItem = wx.Button(self, label=label)
            self.createHandler(buttonItem, label)
            gridBox.Add(buttonItem, 1, wx.EXPAND)

        vbox.Add(gridBox, proportion=1, flag=wx.EXPAND)
        self.SetSizer(vbox)

    def createHandler(self, button, labels):
        item = 'DEL AC = CLOSE PI'
        if labels not in item:
            self.Bind(wx.EVT_BUTTON, self.OnAppend, button)
        elif labels == 'DEL':
            self.Bind(wx.EVT_BUTTON, self.OnDel, button)
        elif labels == 'AC':
            self.Bind(wx.EVT_BUTTON, self.OnAc, button)
        elif labels == '=':
            self.Bind(wx.EVT_BUTTON, self.OnTarget, button)
        elif labels == 'CLOSE':
            self.Bind(wx.EVT_BUTTON, self.OnExit, button)
        elif labels == 'PI':
            self.Bind(wx.EVT_BUTTON, self.OnPI, button)

    def OnAppend(self, event):
        eventbutton = event.GetEventObject()
        label = eventbutton.GetLabel()
        self.equation += label
        self.textprint.SetValue(self.equation)

    def OnDel(self, event):
        self.equation = self.equation[:-1]
        self.textprint.SetValue(self.equation)

    def OnAc(self, event):
        self.textprint.Clear()
        self.equation = ''

    def OnTarget(self, event):
        string = self.equation
        try:
            target = eval(string)
            self.equation = str(target)
            self.textprint.SetValue(self.equation)
        except SyntaxError:
            dlg = wx.MessageDialog(self, 'Error Format', 'Warning', wx.OK|
                                   wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def OnExit(self, event):
        self.Close()

    def OnPI(self, event):
        if self.equation == '':
            self.equation = str(pi)
        else:
            self.equation += str(pi)
        self.textprint.SetValue(self.equation)


if __name__ == '__main__':
    app = wx.App()
    CalcFrame(title='Calculator')
    app.MainLoop()
