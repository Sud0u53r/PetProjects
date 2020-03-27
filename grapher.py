import turtle, tkinter
from math import *
from time import sleep

N = 40

axes = turtle.Turtle(); axes.speed(0); axes.hideturtle()

for x in [1,0,0,1]:
	for _ in range(10):
		axes.fd(N)
		axes.rt(90) if x else axes.lt(90)
		axes.fd(N/3); axes.bk(N/3)
		axes.lt(90) if x else axes.rt(90)
	axes.fd(N); axes.stamp(); axes.setpos((0,0)); axes.lt(90)

class Graph:
	def __init__(self, equation, color):
		self.pointer = turtle.Turtle()
		self.pointer.hideturtle()
		self.pointer.color(color)
		self.pointer.width(1.5)
		self.pointer.speed(0)
		self.pointer.up()
		self.eq = equation

class GraphCartesian(Graph):
	def __init__(self, equation, color = 'black'):
		super().__init__(equation, color)

	def drawGraph(self):
		for x in range(-N*10, N*10):
			x /= N
			try:
				y = eval(self.eq)*N
			except ZeroDivisionError:
				continue
			x *= N
			if -N*10 <= y <= N*10:
				self.pointer.goto((x,y)); self.pointer.down()
			else:
				self.pointer.up()

class GraphPolar(Graph):
	def __init__(self, equation, color = 'black'):
		super().__init__(equation, color)

	def drawGraph(self):
		for deg in range(360):
			x = (deg/180)*pi
			try:
				y = eval(self.eq)*N
			except ZeroDivisionError:
				continue
			if -N*10 <= y <= N*10:
				target = (y*cos(x), y*sin(x))
				self.pointer.goto(target); self.pointer.down()
			else:
				self.pointer.up()

# GraphPolar('5*cos(x)', 'blue').drawGraph()
# GraphPolar('5*sin(x)', 'red').drawGraph()
# GraphPolar('5 - (5*cos(x))', 'green').drawGraph()

GraphCartesian('x', 'violet').drawGraph()
GraphCartesian('x**2', 'indigo').drawGraph()
GraphCartesian('x**3', 'blue').drawGraph()
GraphCartesian('x**4', 'green').drawGraph()
GraphCartesian('x**5', 'yellow').drawGraph()
GraphCartesian('x**6', 'orange').drawGraph()
GraphCartesian('x**7', 'red').drawGraph()

GraphCartesian('sin(x)', 'violet').drawGraph()
GraphCartesian('cos(x)', 'indigo').drawGraph()
GraphCartesian('tan(x)', 'blue').drawGraph()
GraphCartesian('1/sin(x)', 'green').drawGraph()
GraphCartesian('1/cos(x)', 'orange').drawGraph()
GraphCartesian('1/tan(x)', 'red').drawGraph()

turtle.done()