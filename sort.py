import tkinter as tk
import time
import random

width, height = 1100, 700
buttonW, buttonH = .1, .05
size = 20
vals = [None] * size
bars = [None] * size
sortSpeed = 200
interrupt = False
sorting = False
defaultColor = 'RoyalBlue'
selectColor = 'magenta2'

root = tk.Tk()
root.title("Sorting Visualiztion")

canvas = tk.Canvas(root, height = height, width = width, bg = 'pale green')
canvas.pack()


def drawRect(i, color):
	barWidth = (width * 0.9) / size
	startX = width * 0.05
	endY = height * 0.885

	x1 = startX + i * barWidth
	y1 = endY - (vals[i] / size) * (.8 * height)
	x2 = x1 + barWidth
	bars[i] = canvas.create_rectangle(x1, y1, x2, endY, fill = color, outline = color, tag = 'rect')

def swap(index1, index2):
	vals[index1], vals[index2] = vals[index2], vals[index1]

def changeColor(index, color):
	canvas.itemconfig(bars[index], fill = color, outline = color)

def quick():
	return

def mergeCombine(left, right, ):
	global interrupt, sorting
	if interrupt: # terminates when finished or when interrupted by scale
		interrupt = False
		sorting = False
		return
	combined = []
	while left and right:
		if left[0] < right[0]:
			combined.append(left[0])
			left = left[1:]
		else:
			combined.append(right[0])
			right = right[1:]
	if left:
		combined += left
	elif right:
		combined += right
	return combined

def merge(lst = None, newSort = True):
	global sorting, vals
	if sorting and newSort: # prevents another sort from being called while running
		return
	sorting = True
	lst = vals if not lst else lst

	# ALGORITHM #
	length = len(lst)
	if length == 1:
		return lst
	middle = length // 2 if length % 2 == 0 else length // 2 + 1
	left = merge(lst[: middle], False)
	right = merge(lst[middle:], False)
	lst = mergeCombine(left, right)
	if len(lst) == len(vals):
		vals = lst
		updateScreen()
	return lst

def heap():
	return

def insertion(start = 1, iteration = 0, newSort = True, prev = False):
	global interrupt, sorting
	changeColor(prev, defaultColor) if type(prev) == int else None
	if sorting and newSort: # prevents another sort from being called while running
		return
	if start == size or interrupt: # terminates when finished or when interrupted by scale
		interrupt = False
		sorting = False
		return
	sorting = True

	# ALGORITHM # (allows for brief pauses to display selection highlight)
	if iteration % 2 == 0: 
		changeColor(start, selectColor)
		root.after(sortSpeed, lambda: insertion(start, iteration + 1, False)) 
		# pause after initial start selection
	else:
		lowest = 1
		for i in range(start, 0, -1):
			if vals[i] < vals[i - 1]:
				swap(i, i - 1)
				lowest = i - 1
			else:
				lowest = i
				break
		clearRectangles(range(lowest, start + 1))
		for k in range(lowest, start + 1):
			drawRect(k, defaultColor)
		changeColor(lowest, selectColor)
		root.after(sortSpeed, lambda: insertion(start + 1, 0, False, lowest))  
		# pause after start item is swapped as long as it can go

def selection(start = 0, newSort = True, iteration = 0, currMin = float('inf'), minIdx = None):
	global interrupt, sorting
	if sorting and newSort: # prevents another sort from being called while running
		return
	if start == size or interrupt: # terminates when finished or when interrupted by scale
		changeColor(start - 1, defaultColor)
		interrupt = False
		sorting = False
		return
	sorting = True

	# ALGORITHM # (allows for brief pauses to display selection highlight)
	if iteration % 2 == 0: 
		changeColor(start - 1, defaultColor) if start != 0 else None
		for i in range(start, size):
			if vals[i] < currMin:
				currMin = vals[i]
				minIdx = i
		changeColor(minIdx, selectColor)
		root.after(sortSpeed, lambda: selection(start, False, iteration + 1, currMin, minIdx))
		# pause after minimum item is found in unsorted section
	else:
		clearRectangles([minIdx, start])
		swap(start, minIdx)
		drawRect(start, selectColor)
		drawRect(minIdx, defaultColor)
		root.after(sortSpeed, lambda: selection(start + 1, False))
		# pause after minimum item is swapped with leftmost of unsorted section


def clearRectangles(lst):
	if not lst:
		canvas.delete('rect')
	else:
		for index in lst:
			canvas.delete(bars[index])

def updateScreen():
	global bars
	clearRectangles(None)
	bars = [None] * size
	for i in range(size):
		drawRect(i, defaultColor)

def randomVals():
	global vals
	random.seed(time.time())
	vals = [None] * size
	for i in range(size):
		vals[i] = random.randint(0, size)
	updateScreen()

def changeSize(newSize):
	global size, interrupt
	interrupt = True if sorting else False
	size = int(newSize)
	randomVals()


def slow():
	global sortSpeed
	sortSpeed = 200

def medium():
	global sortSpeed
	sortSpeed = 50

def fast():
	global sortSpeed
	sortSpeed = 1


sorts = ["Quick Sort", "Merge Sort", "Heap Sort", "Insertion Sort", "Selection Sort"]
funcs = [quick, merge, heap, insertion, selection]
modes = ["Slow", "Medium", "Fast"]
speeds = [slow, medium, fast]

for i in range(len(sorts)): # button for sorts
	quick = tk.Button(canvas, text = sorts[i], command = funcs[i])
	quick.place(relx = 0.005 * (i + 1) + buttonW * i, rely = 0.005, relwidth = buttonW, relheight = buttonH)

inputSize = tk.Scale(canvas, from_ = 10, to = 1000, tickinterval = 90, orient = tk.HORIZONTAL, bg = 'light blue', command = changeSize)
inputSize.place(relx = 0.5 - buttonW * 4.5, rely = 1 - buttonH * 2.1, relwidth = buttonW * 6, relheight = buttonH * 2)
inputSize.set(size)

randomize = tk.Button(canvas, text = 'Random Values', command = lambda: changeSize(size))
randomize.place(relx = 1 - buttonW * 1.1, rely = 0.005, relwidth = buttonW, relheight = buttonH)

for i in range(3): # buttons for sort speed
	quick = tk.Button(canvas, text = modes[i], command = speeds[i])
	quick.place(relx = 0.5 + 1.75 * buttonW + buttonW * i, rely = 1 - buttonH * 1.55, relwidth = buttonW, relheight = buttonH)

randomVals()
root.mainloop()
