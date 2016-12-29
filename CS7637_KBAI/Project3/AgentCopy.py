# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

from PIL import Image
from PIL import ImageChops
import numpy as np, operator
import math
import pdb
import string

class Agent:

    def __init__(self):
	self.choices=[]
	self.input_im=[]
	self.sizes={'very small':0,'small':1,'medium':2,'large':3,'very large':4,'huge':5}
        pass

    def initialize(self,problem):
	if (problem.problemType=='3x3'):
		self.A=problem.figures["A"]
		self.B=problem.figures["B"]
		self.C=problem.figures["C"]
		self.fig1=problem.figures["1"]
		self.fig2=problem.figures["2"]
		self.fig3=problem.figures["3"]
		self.fig4=problem.figures["4"]
		self.fig5=problem.figures["5"]
		self.fig6=problem.figures["6"]
		self.D=problem.figures["D"]
		self.E=problem.figures["E"]
		self.F=problem.figures["F"]
		self.G=problem.figures["G"]
		self.H=problem.figures["H"]
		self.fig7=problem.figures["7"]
		self.fig8=problem.figures["8"]
		self.a = Image.open(self.A.visualFilename)
		self.b = Image.open(self.B.visualFilename)
		self.c = Image.open(self.C.visualFilename)
		self.d = Image.open(self.D.visualFilename)
		self.e = Image.open(self.E.visualFilename)
		self.f = Image.open(self.F.visualFilename)
		self.g = Image.open(self.G.visualFilename)
		self.h = Image.open(self.H.visualFilename)
		self.a_bl = self.count_blpxl(self.a)
		self.b_bl = self.count_blpxl(self.b)
		self.c_bl = self.count_blpxl(self.c)
		self.d_bl = self.count_blpxl(self.d)
		self.e_bl = self.count_blpxl(self.e)
		self.f_bl = self.count_blpxl(self.f)
		self.g_bl = self.count_blpxl(self.g)
		self.h_bl = self.count_blpxl(self.h)

    def getdiff(self,A,B):
	a = Image.open(A.visualFilename).histogram()
	b = Image.open(B.visualFilename).histogram()
	rms = np.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, a, b))/len(a))
	value1=-1
	if rms<25.0:
		value1=0.0
	return value1

    def hr_imageequality(self,problem):
	A=self.A
	B=self.B
	C=self.C
	G=self.G
	H=self.H
	diffAB=self.getdiff(A,B)
	transforms=[]
	transforms.append(diffAB)
	diffBC=self.getdiff(B,C)
	transforms.append(diffBC)
	diffGH=self.getdiff(G,H)
	transforms.append(diffGH)	
	return transforms

    def di_imageequality(self,problem):
	B=self.B
	F=self.F
	G=self.G
	A=self.A
	E=self.E
	diffBF=self.getdiff(B,F)
	transforms=[]
	transforms.append(diffBF)
	diffFG=self.getdiff(F,G)
	transforms.append(diffFG)
	diffAE =self.getdiff(A,E)
	transforms.append(diffAE)	
	return transforms

    def hr_addimage(self,A,B,C,problem):
	a = ImageChops.invert(Image.open(A.visualFilename))
	b = ImageChops.invert(Image.open(B.visualFilename))
	c = Image.open(C.visualFilename)
	c1 = ImageChops.invert(ImageChops.add(a,b))
	ch = c.histogram()
	c1h = c1.histogram()
	rms = np.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, ch, c1h))/len(ch))
	if rms<=15.0:
		return 1
	else:
		return 0

    def hr_subimage(self,A,B,C,problem):
	a = ImageChops.invert(Image.open(A.visualFilename))
	b = ImageChops.invert(Image.open(B.visualFilename))
	c = Image.open(C.visualFilename)
	c1 = ImageChops.invert(ImageChops.add(a,b))
	ch = c.histogram()
	c1h = c1.histogram()
	rms = np.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, ch, c1h))/len(ch))
	if rms<=15.0:
		return 1
	else:
		return 0

    def count_blpxl(self,im):
	black = 0
	for pixel in im.getdata():
		if pixel==(0,0,0,255):
			black+=1
	return black

    def hr_opixgrowth(self,problem):
	ans = -1
	a_bl = self.a_bl
	c_bl = self.c_bl
	d_bl = self.d_bl
	f_bl = self.f_bl
	g_bl = self.g_bl
	diff1 = a_bl - c_bl
	diff2 = d_bl - f_bl
	thres=10
	if abs(diff1-diff2)<=thres:
		for i in range (0,len(self.choices)):
			curr_fig = Image.open(self.choices[i].visualFilename)
			diff_bpx = self.g_bl - self.count_blpxl(curr_fig)
			if abs(diff_bpx - diff1)<=thres:
				thres=abs(diff_bpx - diff1)
				ans = i+1
	return ans

    def hr_opixdec(self,problem):
	ans = -1
	a_bl = self.a_bl
	b_bl = self.b_bl
	c_bl = self.c_bl
	d_bl = self.d_bl
	e_bl = self.e_bl
	f_bl = self.f_bl
	g_bl = self.g_bl
	h_bl = self.h_bl
	diff1 = a_bl - b_bl - c_bl
	diff2 = d_bl - e_bl - f_bl
	thres = 10
	if abs(diff1-diff2)<=thres:
		for i in range (0,len(self.choices)):
			curr_fig = Image.open(self.choices[i].visualFilename)
			diff_bpx = g_bl - h_bl - self.count_blpxl(curr_fig)
			if abs(diff_bpx - diff1)<=thres:
				thres = abs(diff_bpx - diff1)
				ans = i+1
	return ans

    def di_opixgrowth(self,problem):
	ans = -1
	b_bl = self.b_bl
	c_bl = self.c_bl
	h_bl = self.h_bl
	a_bl = self.a_bl
	g_bl = self.g_bl
	diff1 = b_bl - g_bl
	diff2 = c_bl - h_bl
	thres = 25
	if abs(diff1-diff2)<=thres:
		for i in range (0,len(self.choices)):
			curr_fig = Image.open(self.choices[i].visualFilename)
			diff_bpx = self.a_bl - self.count_blpxl(curr_fig)
			if abs(diff_bpx - diff1)<= thres:
				thres = abs(diff_bpx - diff1)
				ans = i+1
	return ans

    def di_ratiopgrw(self,problem):#for D-07
	ans = -1
	e_bl = self.e_bl
	a_bl = self.a_bl
	f_bl = self.f_bl
	g_bl = self.g_bl
	b_bl = self.b_bl
	diff1 = abs(f_bl - g_bl)
	diff2 = abs(a_bl - e_bl)
	diff = abs(b_bl - g_bl)
        if problem.name =='Basic Problem D-10':
		print diff1,diff2,diff
		t = ImageChops.lighter(self.a,self.e)
		t.show()
	thres = 25
	if abs(diff1-diff2)<=10:
		for i in range (0,len(self.choices)):
			curr_fig = Image.open(self.choices[i].visualFilename)
			diff_bpx = abs(e_bl - self.count_blpxl(curr_fig))
			if abs(diff_bpx - diff)<=thres:
				thres = abs(diff_bpx - diff)
				ans = i+1
	return ans

    def di_opshift(self,problem):#for D-08
	ans = -1
	e_bl = self.e_bl
	a_bl = self.a_bl
	f_bl = self.f_bl
	g_bl = self.g_bl
	b_bl = self.b_bl
	c_bl = self.c_bl
	h_bl = self.h_bl
	diff1 = c_bl /(g_bl + e_bl)
	diff2 = h_bl /(f_bl + a_bl)
	if diff1 == diff2==1:
		for i in range(0,len(self.choices)):
			curr_fig = Image.open(self.choices[i].visualFilename)
			diff_bpx = self.d_bl/(b_bl+self.count_blpxl(curr_fig))
			if diff1==diff_bpx:
				ans = i+1
	return ans

    def di_opshift1(self,problem):#for D-09
	ans = -1
	a = ImageChops.invert(Image.open(self.A.visualFilename))
	f = ImageChops.invert(Image.open(self.F.visualFilename))
	h1 = ImageChops.invert(ImageChops.add(a,f))
	h = Image.open(self.H.visualFilename)	
	hh = h.histogram()
	h1h = h1.histogram()
	rms = np.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, hh, h1h))/len(hh))
	thres = 30.0
	if rms<=thres:
		d = Image.open(self.D.visualFilename)
		b = ImageChops.invert(Image.open(self.B.visualFilename))
		for i in range(0,len(self.choices)):
			curr_fig = ImageChops.invert(Image.open(self.choices[i].visualFilename))
			d1 = ImageChops.invert(ImageChops.add(b,curr_fig))
			dh = d.histogram()
			d1h = d1.histogram()
			rms1 = np.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, dh, d1h))/len(dh))
			if rms1<=thres:
				thres = rms1
				ans = i+1
	return ans

    def hr_andimage(self,A,B,C):
	a = Image.open(A.visualFilename)
	b = Image.open(B.visualFilename)
	c = Image.open(C.visualFilename)
	c1 = ImageChops.add(a,b)
	ch = c.histogram()
	c1h = c1.histogram()
	rms = np.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, ch, c1h))/len(ch))
	if rms<=15.0:
		return 1
	else:
		return 0

    def hr_xordiffimage(self,A,B,C,problem):
	a = Image.open(A.visualFilename)
	b = Image.open(B.visualFilename)
	c = Image.open(C.visualFilename)
	c11 = ImageChops.difference(a,b)
	c1 = ImageChops.invert(c11)
	ch = c.histogram()
	c1h = c1.histogram()
	rms = np.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, ch, c1h))/len(ch))
	if rms<=28.0:
		return 1
	else:
		return 0

    def obj_count(self,problem):
	ans = -1
	a_bl=self.a_bl
	b_bl=self.b_bl
	c_bl=self.c_bl
	d_bl=self.d_bl
	e_bl=self.e_bl
	f_bl=self.f_bl	
	g_bl=self.g_bl
	h_bl=self.h_bl
	diff1 = float(f_bl)/float(g_bl)
	diff2 = float(a_bl)/float(e_bl)
	#if problem.name=='Basic Problem D-10':
	#	print diff1,diff2
	thres = 0.20
	if abs(diff1-diff2)<thres:
		diff = float(g_bl)/float(b_bl)
		for i in range(0,len(self.choices)):
			curr_fig = Image.open(self.choices[i].visualFilename)
			curr_diff = float(e_bl)/float(self.count_blpxl(curr_fig))
			#if problem.name=='Basic Problem D-10':
			#	print curr_diff
			if abs(curr_diff - diff) < thres:
				thres = abs(curr_diff - diff)
				ans = i+1
	return ans	

    def Solve(self,problem):
	value=-1
	self.initialize(problem)
	print "Solving ",problem.name
	if (problem.problemType=='3x3'):
		self.input_im=[self.A,self.B,self.C,self.D,self.E,self.F,self.G,self.H]
		self.choices=[self.fig1,self.fig2,self.fig3,self.fig4,self.fig5,self.fig6,self.fig7,self.fig8]
		choices_score=[]

		hr_equal = self.hr_imageequality(problem)
		im_add=self.hr_addimage(self.A,self.B,self.C,problem)
		im_and=self.hr_andimage(self.A,self.B,self.C)
		xor_diff = self.hr_xordiffimage(self.A,self.B,self.C,problem)
		di_equal = self.di_imageequality(problem)
		hr_opxgrowth = self.hr_opixgrowth(problem)
		di_opxgrowth = self.di_opixgrowth(problem)
		hr_opxdec = self.hr_opixdec(problem)
		di_ratiopgrw = self.di_ratiopgrw(problem)
		di_opshift = self.di_opshift(problem)
		di_opshift1= self.di_opshift1(problem)
		obj_count = self.obj_count(problem)

		if sum(hr_equal)==0.0:
			for i in range (0,len(self.choices)-1):
				curr_fig=self.choices[i]
				choices_score.append(0)
				if self.getdiff(self.G,curr_fig)==0.0:
					choices_score[i]=1
					value=i+1
		elif sum(di_equal)==0.0:
			for i in range (0,len(self.choices)-1):
				curr_fig=self.choices[i]
				choices_score.append(0)
				if self.getdiff(self.A,curr_fig)==0.0:
					choices_score[i]=1
					value=i+1
		elif im_add ==1 :
			for i in range (0,len(self.choices)):
				curr_fig=self.choices[i]
				choices_score.append(0)
				if self.hr_addimage(self.G,self.H,curr_fig,problem)==1:
					choices_score[i]=1
					value=i+1	
		elif im_and ==1 :
			for i in range (0,len(self.choices)):
				curr_fig=self.choices[i]
				choices_score.append(0)
				if self.hr_andimage(self.G,self.H,curr_fig)==1:
					choices_score[i]=1
					value=i+1
		elif xor_diff ==1:
			for i in range (0,len(self.choices)):
				curr_fig=self.choices[i]
				choices_score.append(0)
				if self.hr_xordiffimage(self.G,self.H,curr_fig,problem)==1:
					choices_score[i]=1
					value=i+1
			if value == -1:
				g = Image.open(self.G.visualFilename)
				g_bl = self.g_bl
				h = Image.open(self.H.visualFilename)
				im1 = ImageChops.darker(g,h)
				h1 = self.count_blpxl(im1)
				for i in range (0,len(self.choices)):
					curr_fig= Image.open(self.choices[i].visualFilename)
					choices_score.append(0)
					im2 = ImageChops.darker(g,curr_fig)
					h2 = self.count_blpxl(im2)
					if abs(h1-h2)<10.0:
						value = i+1
		elif hr_opxgrowth != -1:
			value = hr_opxgrowth
		elif di_opxgrowth != -1:
			value = di_opxgrowth
		elif hr_opxdec != -1:
			value = hr_opxdec
		elif di_ratiopgrw != -1:
			value = di_ratiopgrw
		elif di_opshift != -1:
			value = di_opshift
		elif di_opshift1 != -1:
			value = di_opshift1
		elif obj_count != -1:
			value = obj_count				
	print value
	return value

