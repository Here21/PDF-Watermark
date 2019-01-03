from tkinter import *
import tkinter.messagebox as messagebox
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PyPDF2 import PdfFileReader, PdfFileWriter


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        w = 800;
        h = 500;
        # 计算 x, y 位置
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.pack()
        self.createWidgets()

    def createWidgets(self):
        # 输入框
        self.lable1 = Label(self, text="输入水印文字（最好15个字）")
        self.entry = Entry(self)
        # self.lable1.grid(row=0)
        # self.entry.grid(row=0, column=1)
        self.lable1.pack()
        self.entry.pack()
        # # button
        self.generButton = Button(self, text='生成', command=self.create_watermark)
        self.generButton.pack()


        # list box
        self.lable2 = Label(self, text="当前目录所有的 PDF 文件")
        self.lable2.pack()

        self.listBox = Listbox(self, height = 10, width = 80)

        self.files = self.list_all_files('./')
        for item in self.files:  # 第一个小部件插入数据
            self.listBox.insert(0, item)

        self.listBox.pack()
        # button
        self.startButton = Button(self, text='开始', command=self.addWatermark)
        # self.startButton.pack(side = BOTTOM)

    def hello(self):
        name = self.nameInput.get() or 'world'
        messagebox.showinfo('Message', 'Hello, %s' % name)

    def list_all_files(self, rootdir):
        _files = []
        # 列出文件夹下所有的目录与文件
        list = os.listdir(rootdir)
        for i in range(0, len(list)):
               path = os.path.join(rootdir, list[i])
               if os.path.isdir(path):
                  _files.extend(self.list_all_files(path))
               if os.path.isfile(path):
                   if os.path.splitext(path)[-1][1:] == "pdf":
                        _files.append(path)
        return _files

    def create_watermark(self):
        content = self.entry.get();

        # 默认大小为21cm*29.7cm
        c = canvas.Canvas("mark.pdf", pagesize=(21 * cm, 29.7 * cm))
        # 移动坐标原点(坐标系左下为(0,0))
        c.translate(1 * cm, 1 * cm)

        # 设置字体
        c.setFont("Helvetica", 80)
        # 指定描边的颜色
        c.setStrokeColorRGB(0, 1, 0)
        # # 指定填充颜色
        # c.setFillColorRGB(0, 1, 0)
        # # 画一个矩形
        # c.rect(cm, cm, 7 * cm, 17 * cm, fill=1)

        # 旋转45度，坐标系被旋转
        c.rotate(45)
        # 指定填充颜色
        # c.setFillColorRGB(0.6, 0, 0)
        # 设置透明度，1为不透明
        c.setFillAlpha(0.2)
        # 画几个文本，注意坐标系旋转的影响
        c.drawString(3 * cm, 0 * cm, content)
        c.setFillAlpha(0.4)
        c.drawString(6 * cm, 3 * cm, content)
        c.setFillAlpha(0.6)
        c.drawString(9 * cm, 6 * cm, content)

        # 关闭并保存pdf文件
        print('maker 制作完成')
        c.save()
        messagebox.showinfo("提示", "生成水印成功，请继续执行")
        self.generButton.forget()
        self.startButton.pack(side = BOTTOM)



    def addWatermark(self):
        self.startButton.Enable(False)
        for file in self.files:
            print("执行文件 ->", file)
            # 获取一个 PdfFileReader 对象
            pdfReader = PdfFileReader(open(file, 'rb'))
            # 获取 PDF 的页数
            pageCount = pdfReader.getNumPages()

            # 获取一个 PdfFileWriter 对象
            pdfWriter = PdfFileWriter()

            pdf_watermark = PdfFileReader(open('./mark.pdf', 'rb'))

            # 给每一页打水印
            for i in range(pageCount):
                page = pdfReader.getPage(i)
                page.mergePage(pdf_watermark.getPage(0))
                page.compressContentStreams()  # 压缩内容
                pdfWriter.addPage(page)

            # 将一个 PageObject 加入到 PdfFileWriter 中
            # pdfWriter.addPage(page)
            #
            # # 输出到文件中
            pdfWriter.write(open(file, 'wb'))

        self.startButton.Enable(True)
        messagebox.showinfo('提示', "转化完成")


app = Application()
# 设置窗口标题:
app.master.title('PDF加水印批处理程序')
# 主消息循环:
app.mainloop()