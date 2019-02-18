import wx
import math


class ClacFrame(wx.Frame):
    def __init__(self, title):
        super().__init__(None, title=title, size=(300, 260))
        self.InitUI()
        self.Center()
        self.Show()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.textprint = wx.TextCtrl(self, -1, '', style=wx.TE_RIGHT|wx.TE_READONLY)
        self.equation = ''
        self.textprint.SetValue(self.equation)
        vbox.Add(self.textprint, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=5)

        gridBox = wx.GridSizer(5, 4, 5, 5)
        labels=['AC', 'DEL', 'PI', 'CLOSE', '7', '8', '9', '/',
                '4', '5', '6', '*', '1', '2', '3', '-', '0', '.',
                '=', '+']
        for label in labels:
            buttonItem = wx.Button(self, label=label)
            self.createHandler(buttonItem, label)
            gridBox.Add(buttonItem, 1, wx.EXPAND)
        vbox.Add(gridBox, 1, flag=wx.EXPAND)
        self.SetSizer(vbox)

    def createHandler(self, button, labels):
        item = 'DEL AC = PI CLOSE'
        if labels not in item:
            self.Bind(wx.EVT_BUTTON, self.OnAppend, button)
        elif labels == 'DEL':
            self.Bind(wx.EVT_BUTTON, self.OnDel, button)
        elif labels == 'AC':
            self.Bind(wx.EVT_BUTTON, self.OnAc, button)
        elif labels == '=':
            self.Bind(wx.EVT_BUTTON, self.OnTarget, button)
        elif labels == 'PI':
            self.Bind(wx.EVT_BUTTON, self.OnPi, button)
        elif labels == 'CLOSE':
            self.Bind(wx.EVT_BUTTON, self.OnClose, button)

    def OnAppend(self, event):
        eventButton = event.GetEventObject()
        label = eventButton.GetLabel()
        self.equation += label
        self.textprint.SetValue(self.equation)

    def OnDel(self, event):
        self.equation = self.equation[:-1]
        self.textprint.SetValue(self.equation)

    def OnAc(self, event):
        self.textprint.Clear()
        self.equation = ''

    def OnTarget(self, event):
        try:
            self.equation = str(eval(self.equation))
            self.textprint.SetValue(self.equation)
        except SyntaxError:
            dlg = wx.MessageDialog(self, '格式错误', '警告', wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def OnPi(self, event):
        if self.equation == '':
            self.equation = str(math.pi)
        elif self.equation == str(math.pi):
            self.textprint.Clear()
        else:
            self.equation += str(math.pi)
        self.textprint.SetValue(self.equation)

    def OnClose(self, event):
        self.Close()


if __name__ == '__main__':
    app = wx.App()
    ClacFrame(title='Claculator')
    app.MainLoop()