#!/usr/bin/python3
from tkinter.filedialog import *
from tkinter import *
from tkinter.ttk import * 
from tkinter import colorchooser
import os
import io
root = Tk()
root.title("Генератор интеллект-карт")
root.wm_minsize(400, 400)
root.wm_maxsize(1920, 1080)
#Фрейм
frame = Frame(root)
frame.pack(fill=BOTH)
scrollregion = (0, 0, 5000, 5000)
#Холст
canv = Canvas(root, bg="white", width=3000, height=3000, scrollregion=scrollregion)
#Полоса прокрутки
xscroll = Scrollbar(root, orient='horizontal', command=canv.xview)
canv.configure(xscrollcommand=xscroll.set)
xscroll.pack(side=BOTTOM, fill=X)
yscroll = Scrollbar(root, orient='vertical', command=canv.yview)
canv.configure(yscrollcommand=yscroll.set)
yscroll.pack(side=RIGHT, fill=Y)
canv.pack(side=TOP, fill=BOTH)
#Меню
#Функции меню
#Сохранить как изображение
def save_image():
	hen = filedialog.asksaveasfilename(defaultextension = '.ps')
	canv.postscript(file=hen, colormode='color')
#Помощь
def help():
	win = Toplevel(root)
	lab = Label(win,text="Создание текстового поля - двойной щелчок левой кнопкой мыши \nПеретаскивание текстового поля - левая кнопка мыши \nСоздание линии - правая кнопка мыши\n Удаление линии - двойной щелчок правой кнопкой мыши")
	lab.grid() 
#О программе
def about():
	win = Toplevel(root)
	lab = Label(win,text="Генератор интеллект-карт \n Автор: Абрашин Даниил \n Все права защищены(наверное)")
	lab.grid() 
#Выход
def close_win():
	root.destroy()	
#Пункты меню
m = Menu(root)
root.config(menu=m)
#Файл
am = Menu(m)
m.add_cascade(label="Файл",menu=am)
am.add_command(label="Сохранить как изображение", command=save_image)
#Помощь
m.add_command(label="Помощь",command=help)
#О программе
m.add_command(label="О программе",command=about)
#Выход
m.add_command(label="Выход", command=close_win)

#Рисование
class Drawing():
	def __init__(self, root):
		self.lines = []
		self.lastX = None
		self.lastY = None
		self.redLine = None
		self.canvas = canv
		self.canvas.bind("<Double-Button-1>",self.click1)
		self.canvas.bind("<Button-3>",self.click3)
		self.canvas.bind('<B1-Motion>', self.move)
		self.canvas.bind("<Motion>",self.mouseMoved)
		self.canvas.bind("<Double-Button-3>",self.rightClicked)
		self.canvas.pack()

#Текстовое поле
	def click1(self, event):
		x = event.x + xscroll.get()[0] * scrollregion[2]
		y = event.y + yscroll.get()[0] * scrollregion[3]
		colors = colorchooser.askcolor(title="Выбор цвета")
		canv.text = Text(bg = colors[1], width=18, height = 3, bd=3)
		canv.create_window((x, y), anchor="nw", window=canv.text)


#Перемещение текстового поля
	def move(self, event):
		x = event.x + xscroll.get()[0] * scrollregion[2]
		y = event.y + yscroll.get()[0] * scrollregion[3]
		canv.create_window((x, y), anchor="nw", window=canv.text)

		canv.text.tag_config("center", justify='center')
		canv.text.tag_add("center", 1.0, "end")

#Рисование линии 
	def click3(self, event):
		if self.lastX != None:
			x = event.x + xscroll.get()[0] * scrollregion[2]
			y = event.y + yscroll.get()[0] * scrollregion[3]
			l = self.canvas.create_line(self.lastX,self.lastY,x,y)
			self.lines.append(l)

		x = event.x + xscroll.get()[0] * scrollregion[2]
		y = event.y + yscroll.get()[0] * scrollregion[3]
		self.lastX = x
		self.lastY = y
		pass
#Удаление линии
	def rightClicked(self,event):
		self.lastX = None
		self.lastY = None
		if (len( self.lines) > 0):
			self.canvas.delete( self.lines[-1])
			del self.lines[-1]

		if self.redLine != None:
			self.canvas.delete(self.redLine)
			self.redLine = None
#Зеленые линии
	def mouseMoved(self, event):
		if self.lastX != None:
			if self.redLine != None:
				self.canvas.delete(self.redLine);
			x = event.x + xscroll.get()[0] * scrollregion[2]
			y = event.y + yscroll.get()[0] * scrollregion[3]
			self.redLine = self.canvas.create_line(self.lastX, self.lastY,x, y, fill="green")




Drawing(root)

root.mainloop()