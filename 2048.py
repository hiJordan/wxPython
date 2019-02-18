import wx
import os
import random
import copy


class Frame(wx.Frame):
    def __init__(self, title):
        super().__init__(None, -1, title=title, style=wx.DEFAULT_FRAME_STYLE^
                         wx.MAXIMIZE_BOX^wx.RESIZE_BORDER)
        self.colors = {0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200),
                       8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95),
                       64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 207, 114),
                       512: (237, 207, 114), 1024: (237, 207, 114), 2048: (237, 207, 114),
                       4096: (237, 207, 114), 8192: (237, 207, 114), 16384: (237, 207, 114),
                       32768: (237, 207, 114), 65536: (237, 207, 114), 131072: (237, 207, 114),
                       262144: (237, 207, 114), 524288: (237, 207, 114), 1048576: (237, 207, 114),
                       2097152: (237, 207, 114), 4194304: (237, 207, 114),
                       8388608: (237, 207, 114), 16777216: (237, 207, 114),
                       33554432: (237, 207, 114), 67108864: (237, 207, 114),
                       134217728: (237, 207, 114), 268435456: (237, 207, 114),
                       536870912: (237, 207, 114), 1073741824: (237, 207, 114),
                       2147483648: (237, 207, 114), 4294967296: (237, 207, 114),
                       8589934592: (237, 207, 114), 17179869184: (237, 207, 114),
                       34359738368: (237, 207, 114), 68719476736: (237, 207, 114),
                       137438953472: (237, 207, 114), 274877906944: (237, 207, 114),
                       549755813888: (237, 207, 114), 1099511627776: (237, 207, 114),
                       2199023255552: (237, 207, 114), 4398046511104: (237, 207, 114),
                       8796093022208: (237, 207, 114), 17592186044416: (237, 207, 114),
                       35184372088832: (237, 207, 114), 70368744177664: (237, 207, 114),
                       140737488355328: (237, 207, 114), 281474976710656: (237, 207, 114),
                       562949953421312: (237, 207, 114), 1125899906842624: (237, 207, 114),
                       2251799813685248: (237, 207, 114), 4503599627370496: (237, 207, 114),
                       9007199254740992: (237, 207, 114), 18014398509481984: (237, 207, 114),
                       36028797018963968: (237, 207, 114), 72057594037927936: (237, 207, 114)}
        self.setIcon()
        self.initGame()

        panel = wx.Panel(self)
        panel.SetFocus()
        panel.Bind(wx.EVT_CHAR_HOOK, self.onKeyDown)

        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.SetClientSize((505, 600))

        self.Center()
        self.Show()

    def setIcon(self):
        icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

    def initGame(self):
        'Font参数：尺寸，指定的字体，是否倾斜，醒目程度, faceName指定字体名'
        self.bgFont = wx.Font(40, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.scFont = wx.Font(36, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.smFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.curScore = 0
        self.bstScore = 0
        self.loadScore()
        self.data = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
        count = 0

        while count < 2:
            row = random.randint(0, len(self.data)-1)
            col = random.randint(0, len(self.data[0])-1)
            if self.data[row][col] != 0:
                continue
            self.data[row][col] = 2 if random.randint(0, 1) else 4
            count += 1

    def onKeyDown(self, event):
        '与按键事件中得到对应的键码'
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_UP:
            self.doMove(*self.slideUpDown(True))
        elif keyCode == wx.WXK_DOWN:
            self.doMove(*self.slideUpDown(False))
        elif keyCode == wx.WXK_LEFT:
            self.doMove(*self.slideLeftRight(True))
        elif keyCode == wx.WXK_RIGHT:
            self.doMove(*self.slideLeftRight(False))

    def onSize(self, event):
        self.initBuffer()
        self.drawAll()

    def onPaint(self, event):
        '缓存一套绘画命令，直到命令完整并准备在屏幕上绘画'
        dc = wx.BufferedPaintDC(self, self.buffer)

    def onClose(self, event):
        self.saveScore()
        self.Destroy()

    def saveScore(self):
        ff = open('bestScore.ini', 'w')
        ff.write(str(self.bstScore))
        ff.close()

    def loadScore(self):
        if os.path.exists('bestScore.ini'):
            ff = open('bestScore.ini')
            self.bstScore = int(ff.read())
            ff.close()

    def initBuffer(self):
        '客户区大小指主窗体（不包括边框、标题栏）的区域(505,600)'
        w, h = self.GetClientSize()
        self.buffer = wx.Bitmap(w, h)


    def drawAll(self):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.drawBg(dc)
        self.drawLogo(dc)
        self.drawLabel(dc)
        self.drawScore(dc)
        self.drawTiles(dc)

    def drawChange(self, score):
        '缓冲可将绘画命令单独发送到缓冲区，然后一次性的绘制到屏幕。'
        '缓存绘画指令，命令完整时一次性的绘制，防止闪烁，clientDC指窗口的' \
        '主区域也称客户区(不包括边框、装饰、标题栏)。第一个参数指要绘制到的设备上下文，' \
        '第二个参数则是一个位图，被作为一个临时的缓冲'
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        if score:
            self.curScore += score
            if self.curScore > self.bstScore:
                self.bstScore = self.curScore
            self.drawScore(dc)
        self.drawTiles(dc)

    def drawBg(self, dc):
        '背景画刷当Clear被调用时使用'
        dc.SetBackground(wx.Brush((250, 248, 239)))
        dc.Clear()
        '用于填充绘制于设备上下文的形状，是一个wx.Brush对象'
        dc.SetBrush(wx.Brush((187, 173, 160)))
        '画笔是一个wx.Pen对象，用于所有绘制线条的操作'
        dc.SetPen(wx.Pen((187, 173, 160)))
        '圆角，x,y,w,h,r，r为正值，以像素为单位半径，反之矩形较小边的比例'
        dc.DrawRoundedRectangle(15, 110, 475, 475, 5)

    def drawLogo(self, dc):
        '文本的绘制'
        dc.SetFont(self.bgFont)
        '字体前景色'
        dc.SetTextForeground((119, 110, 101))
        '绘制的文本内容,开始绘制的坐标(x,y)，使用当前的字体前景背景色'
        dc.DrawText('2048', 15, 10)

    def drawLabel(self, dc):
        dc.SetFont(self.smFont)
        dc.SetTextForeground((119, 110, 101))
        dc.DrawText('合并相同数字，得2048', 15, 70)

    def drawScore(self, dc):
        dc.SetFont(self.smFont)
        '得到字符串将占用的矩形范围的尺寸，以元组的方式返回'
        scoreLabelSize = dc.GetTextExtent('SCORE')
        bestLabelSize = dc.GetTextExtent('BEST')
        '预先重设容纳字符的两个矩形的宽'
        curScoreBoardMinW = 15 * 2 + scoreLabelSize[0]
        bstScoreBoardMinW = 15 * 2 + bestLabelSize[0]
        '获取实际可变内容的尺寸'
        curScoreSize = dc.GetTextExtent(str(self.curScore))
        bstScoreSize = dc.GetTextExtent(str(self.bstScore))
        '预先重设可变内容的宽度'
        curScoreBoardNedW = 10 + curScoreSize[0]
        bstScoreBoardNedW = 10 + bstScoreSize[0]
        '以矩形与可变内容的比较，获取最大值'
        curScoreBoardW = max(curScoreBoardMinW, curScoreBoardNedW)
        bstScoreBoardW = max(bstScoreBoardMinW, bstScoreBoardNedW)

        dc.SetBrush(wx.Brush((187, 173, 160)))
        dc.SetPen(wx.Pen((187, 173, 160)))
        '绘制两个圆角矩形'
        dc.DrawRoundedRectangle(505 - 15 - bstScoreBoardW, 40,
                                bstScoreBoardW, 50, 3)
        dc.DrawRoundedRectangle(505 - 15 - bstScoreBoardW - 5 - curScoreBoardW,
                                40, curScoreBoardW, 50, 3)
        dc.SetTextForeground((238, 228, 218))
        '绘制字符串'
        dc.DrawText('BEST', 505 - 15 - bstScoreBoardW + (bstScoreBoardW -
                                                         bestLabelSize[0]) / 2, 48)
        dc.DrawText("SCORE", 505 - 15 - bstScoreBoardW - 5 - curScoreBoardW +
                    (curScoreBoardW - scoreLabelSize[0]) / 2, 48)
        dc.SetTextForeground((255, 255, 255))
        '绘制可变内容字符串'
        dc.DrawText(str(self.bstScore), 505 - 15 - bstScoreBoardW +
                    (bstScoreBoardW - bstScoreSize[0]) / 2, 68)
        dc.DrawText(str(self.curScore), 505 - 15 - bstScoreBoardW - 5 - curScoreBoardW
                    + (curScoreBoardW - curScoreSize[0]) / 2, 68)

    def drawTiles(self, dc):
        dc.SetFont(self.scFont)
        for row in range(4):
            for col in range(4):
                value = self.data[row][col]
                color = self.colors[value]
                '若值为2或4则字体的颜色为棕色反之为白色'
                if value == 2 or value == 4:
                    dc.SetTextForeground((119, 110, 101))
                else:
                    dc.SetTextForeground((255, 255, 255))

                '绘制小方块'
                dc.SetBrush(wx.Brush(color))
                dc.SetPen(wx.Pen(color))
                dc.DrawRoundedRectangle(30 + col * 115, 125 + row * 115, 100, 100, 2)
                size = dc.GetTextExtent(str(value))

                '绘制方块中的数字，若数字的尺寸大于70像素(将要超过方块的尺寸)则重设数字字体的大小'
                while size[0] > 100 - 15 * 2:
                    self.scFont = wx.Font(self.scFont.GetPointSize() * 4 / 5, wx.SWISS,
                                          wx.NORMAL, wx.BOLD)
                    dc.SetFont(self.scFont)
                    size = dc.GetTextExtent(str(value))
                if value != 0:
                    dc.DrawText(str(value), 30 + col * 115 + (100 - size[0]) / 2,
                                125 + row * 115 + (100 - size[1]) / 2)


    def doMove(self, move, score):
        if move:
            '每移动一次则生成一个2或4'
            self.putTile()
            self.drawChange(score)
            if self.isGameOver():
                if wx.MessageBox('游戏结束，是否重新开始?', '(*^▽^*)',
                                 wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
                    bstScore = self.bstScore
                    self.initGame()
                    self.bstScore = bstScore
                    self.drawAll()

    def slideUpDown(self, up):
        score = 0
        numCols = len(self.data[0])
        numRows = len(self.data)
        '复制列表中的所有结构与数据'
        oldData = copy.deepcopy(self.data)

        for col in range(numCols):
            '得以列值为序且不为0([0][0],[1][0],[2][0],[3][0])的列表'
            cvl = [self.data[row][col] for row in range(numRows) if
                   self.data[row][col] != 0]
            '改变score以及对列中的值进行合并，删除cvl中合并前可合并的两个数中的一个，另一个翻倍改变'
            if len(cvl) >= 2:
                score += self.update(cvl, up)
            '通过cvl中的个数来添加或是插入0值，保持cvl中列表个数为4个'
            for i in range(numRows - len(cvl)):
                if up:
                    cvl.append(0)
                else:
                    cvl.insert(0, 0)
            '将改变后的数据放入原始变量中'
            for row in range(numRows):
                self.data[row][col] = cvl[row]

        '比较当前数据与原始数据是否发生变化'
        return oldData != self.data, score



    def slideLeftRight(self, left):
        score = 0
        numRows = len(self.data)
        numCols = len(self.data[0])
        oldData = copy.deepcopy(self.data)

        for row in range(numRows):
            rvl = [self.data[row][col] for col in range(numCols) if
                   self.data[row][col] != 0]
            if len(rvl) >= 2:
                score += self.update(rvl, left)
            for i in range(numCols - len(rvl)):
                if left:
                    rvl.append(0)
                else:
                    rvl.insert(0, 0)
            for col in range(numCols):
                self.data[row][col] = rvl[col]
        return oldData != self.data, score


    def update(self, vlist, direct):
        score = 0
        '向up或left移动则执行'
        if direct:
            i = 1
            '最多判断执行一次'
            while i < len(vlist):
                if vlist[i-1] == vlist[i]:
                    del vlist[i]
                    vlist[i-1] *= 2
                    score += vlist[i-1]
                    i += 1
                i += 1
        else:
            i = len(vlist) - 1
            while i > 0:
                if vlist[i-1] == vlist[i]:
                    del vlist[i]
                    vlist[i-1] *= 2
                    score += vlist[i-1]
                    i -= 1
                i -= 1

        return score

    def putTile(self):
        '存储二元列表中为零的下标(元组)'
        available = []
        for row in range(len(self.data)):
            for col in range(len(self.data[0])):
                if self.data[row][col] == 0:
                    available.append((row, col))
        if available:
            '随机在一个为零的下标位置中生成2或4'
            row, col = available[random.randint(0, len(available) - 1)]
            self.data[row][col] = 2 if random.randint(0, 1) else 4
            return True

        return False

    def isGameOver(self):
        copyData = copy.deepcopy(self.data)
        flag = False
        '判断不同方向是否可移动'
        if not self.slideUpDown(True)[0] and not self.slideUpDown(False)[0] and \
           not self.slideLeftRight(True)[0] and not self.slideLeftRight(False)[0]:
            flag = True
        if not flag:
            self.data = copyData

        return flag


if __name__ == '__main__':
    app = wx.App()
    Frame('2048')
    app.MainLoop()
