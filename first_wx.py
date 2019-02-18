'''
import wx

app = wx.App()

frame = wx.Frame(None, -1, title='what.py', pos=(400,230), size=(200,146))
frame.Show()

app.MainLoop()
'''

'''
import wx


class Example(wx.Frame):
    def __init__(self, title):
        super().__init__(None, title=title, size=(600, 350))
        self.Center()
        self.Show()


if __name__ == '__main__':
    app = wx.App()
    Example("Shape")
    app.MainLoop()
'''


import wx


class Example(wx.Frame):
    def __init__(self, title):
        super().__init__(None, title=title, size=(250, 150))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Center()
        self.Show()

    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        dc.DrawLines(((40, 50), (90, 50), (90, 100), (40, 100), (40, 50)))


if __name__ == "__main__":
    app = wx.App()
    Example('Line')
    app.MainLoop()
