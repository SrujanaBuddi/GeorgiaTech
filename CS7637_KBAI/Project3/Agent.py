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

    def compstr(self,strA,strB):
	A=strA.split('-')
	B=strB.split('-')
	changes={}
	change=''
	for i in range (0,len(A)):
		if (A[i]==B[i]):
			changes[i]=''
		else:
			changes[i]='changed from '+A[i]+' to '+B[i]
		change=change+changes[i]+' '
	return change


    def findcorrobjs(self,A,B):	
	A_objs=A.objects.keys()
	A_objs=sorted(A_objs)
	B_objs=B.objects.keys()
	B_objs=sorted(B_objs)
	A_attr={}
	B_attr={}
	scores={}
	corr_objs={}

	i=0
	for A_obj in A_objs:
		A_attr[A_obj]=A.objects[A_obj].attributes
		i+=1
	i=len(A_objs)

	j=0 
	for B_obj in B_objs:
		B_attr[B_obj]=B.objects[B_obj].attributes
		j+=1
	j=len(B_objs)

	
	if i==j or j>i:		
		for obja in A_attr.keys():
			scores[obja]={}
			for objb in B_attr.keys():
				scores[obja][objb]=0	
				na=len(A_attr[obja])
				nb=len(B_attr[objb])
				if na==nb: # for corresponding objects number of attributes will be same
					scores[obja][objb]=scores[obja][objb]+0.5
				for attr in A_attr[obja]:
					if attr in B_attr[objb]:
						if (A_attr[obja][attr]==B_attr[objb][attr]) and attr!='inside':
							scores[obja][objb]= scores[obja][objb]+1
						if attr=='inside' and (i-len(A_attr[obja][attr]))==(j-len(B_attr[objb][attr])):
							scores[obja][objb]= scores[obja][objb]+1
						if attr=='left-of' and A_attr[obja][attr]!=None and B_attr[objb][attr]!=None:
							scores[obja][objb]+=0.1
						if attr=='above'and A_attr[obja][attr]!=None and B_attr[objb][attr]!=None:
							scores[obja][objb]+=0.1
			if scores[obja]!={}:
				corr_objs[obja]=max(scores[obja],key=scores[obja].get)

	if j>i:
		for objb in B_attr.keys():
			if objb not in corr_objs.values():
				corr_objs[objb]='N'
	elif i>j:
		for objb in B_attr.keys():
			scores[objb]={}
			for obja in A_attr.keys():
				scores[objb][obja]=0	
				na=len(A_attr[obja])
				nb=len(B_attr[objb])
				if na==nb:
					scores[objb][obja]=scores[objb][obja]+0.5
				for attr in A_attr[obja]:
					if attr in B_attr[objb]:
						scores[objb][obja]= scores[objb][obja]+1
						if A_attr[obja][attr]==B_attr[objb][attr]:
							scores[objb][obja]= scores[objb][obja]+1
						if attr=='inside' and (2*i-1-len(A_attr[obja][attr]))==(2*j-1-len(B_attr[objb][attr])):
							scores[objb][obja]= scores[objb][obja]+1
						if attr=='left-of' and A_attr[obja][attr]!=None and B_attr[objb][attr]!=None:
							scores[objb][obja]+=0.1
						if attr=='above'and A_attr[obja][attr]!=None and B_attr[objb][attr]!=None:
							scores[objb][obja]+=0.1
			if scores[objb]!={}:
				corr_objs[objb]=max(scores[objb],key=scores[objb].get)
		corr_objs= dict((v,k) for k,v in corr_objs.iteritems())

		for obja in A_attr.keys():
			if obja not in corr_objs.keys():
				corr_objs[obja]='D'
	return corr_objs
		
				
    def getrelations(self,A,B,problem):
		A_objs=A.objects.keys()
		A_objs=sorted(A_objs)
		B_objs=B.objects.keys()
		B_objs=sorted(B_objs)
		A_attr={}
		B_attr={}
		obj_relations={}
		i=0
		j=0
		
		for Aobj in A_objs:	
			A_attr[Aobj]=A.objects[Aobj].attributes
			i+=1
		for Bobj in B_objs:
			B_attr[Bobj]=B.objects[Bobj].attributes
			j+=1

		corr_objs=self.findcorrobjs(A,B)

		top=0
		med=0
		bottom=0
		left=0
		middle=0
		right=0
		fill=0

		for objA in corr_objs.keys():
			objB = corr_objs[objA]
			relations={}
			if objB!='N' and objB!='D':
				for attr in A_attr[objA]:
					if attr in B_attr[objB]:
						if B_attr[objB][attr]==A_attr[objA][attr]:
							relations[attr]="unchanged"
						elif attr=='angle':
							relations[attr]= "Rotated by "+str(abs(int(A_attr[objA][attr])-int(B_attr[objB][attr])))
						elif attr=='shape':
							relations[attr]="shape changed"
							relations['shape-changes']=A_attr[objA][attr]+' to '+B_attr[objB][attr]	
						elif attr=='fill':
							relations[attr]=A_attr[objA][attr] + ' to '+B_attr[objB][attr]
							if A_attr[objA][attr]=='no' and B_attr[objB][attr]=='yes':
								fill+=1	
							if A_attr[objA][attr]=='yes' and B_attr[objB][attr]=='no':
								fill+=-1				
						elif attr=='size' or attr=='height' or attr=='width':	
								relations[attr]="Size changed by "+ str(self.sizes[A_attr[objA][attr]]-self.sizes[B_attr[objB][attr]])
						elif attr=='inside':# or attr=='left-of' or attr=='above':
							if A_attr[objA][attr] == None:
								lenA=0
							else:
								lenA=len(A_attr[objA][attr])

							if B_attr[objB][attr] == None:
								lenB=0
							else:
								lenB=len(B_attr[objB][attr])
							diff=2*i-lenA-2*j+lenB
							relations[attr]="Present "+attr+" with diff "+str(diff)
						elif attr=='overlaps':
							if A_attr[objA][attr] == None:
								lenA=0
							else:
								lenA=len(A_attr[objA][attr])

							if B_attr[objB][attr] == None:
								lenB=0
							else:
								lenB=len(B_attr[objB][attr])
							relations[attr]=lenA-lenB
						elif attr=='alignment':
							relations[attr]="pos change from"+self.compstr(A_attr[objA][attr],B_attr[objB][attr])

						if ('fill' in B_attr[objB]) and ('above' in B_attr[objB]) and B_attr[objB]['fill']=='yes':
							no_ele=B_attr[objB]['above'].count(",")
							if no_ele==5:
								top+=1
							elif no_ele==2:
								med+=1

						if ('fill' in B_attr[objB]) and ('left-of' in B_attr[objB]) and B_attr[objB]['fill']=='yes':
							no_ele=B_attr[objB]['left-of'].count(",")
							if no_ele==5:
								left+=1
							elif no_ele==2:
								middle+=1
											
					if attr not in B_attr[objB]:
						relations[attr]='deleted'		
					obj_relations[objA]=relations
			elif objB=='N':
				relations['N']="new item added"
				obj_relations[objA]=relations	
			elif objB=='D':
				relations['D']="an item deleted"
				obj_relations[objA]=relations

		temp1={}
		temp2={}
		temp={}
		if len(A_objs)==len(B_objs) and len(A_objs)==1:
			if 'size' in A_attr[objA]:
				temp1['height']=A_attr[objA]['size']
				temp1['width']=A_attr[objA]['size']
			if 'size' in B_attr[objB]:
				temp2['height']=B_attr[objB]['size']
				temp2['width']=B_attr[objB]['size']
			if 'height' in A_attr[objA] and 'width' in A_attr[objA]:
				temp1['height']=A_attr[objA]['height']
				temp1['width']=A_attr[objA]['width']
			if 'height' in B_attr[objB] and 'width' in B_attr[objB]:
				temp2['height']=B_attr[objB]['height']
				temp2['width']=B_attr[objB]['width']								
			temp['height']=self.sizes[temp1['height']]-self.sizes[temp2['height']]
			temp['width']=self.sizes[temp1['width']]-self.sizes[temp2['width']]
			obj_relations['size-scale']=temp['height']+temp['width']

		if len(B_objs)>=len(A_objs):
			lenA=len(A_objs)
			if lenA==0:
				lenA=1
			obj_relations['scale']=len(B_objs)/lenA#ratio by no of objects increasing
		if len(A_objs)>len(B_objs):
			lenB=len(B_objs)
			if lenB==0:
				lenB=1
			obj_relations['scale']=-len(A_objs)/lenB#ratio by no of objects increasing
		obj_relations['inc']=len(B_objs)-len(A_objs)#count of objects increasing

		if top!=0:
			obj_relations['top']=top
		if med!=0:
			obj_relations['med']=med
		if bottom!=0:
			obj_relations['bottom']=bottom
		if left!=0:
			obj_relations['left']=left
		if middle!=0:
			obj_relations['middle']=middle
		if right!=0:
			obj_relations['right']=right

		obj_relations['fill']=fill
		return obj_relations


    def comprelations(self,AtoB,CtoD,A,C):

	corr_AtoC=self.findcorrobjs(A,C)
	CtoA={}

	mod_AtoB={}
	mod_CtoD={}

	k1=min(AtoB)
	keys=sorted(AtoB.keys())
	keys1=[]
	for k,v in AtoB.iteritems():
		if len(k)==1:
			keys1.append(k) 
	#if len(k1)==2:
	#	k1=keys[1]
	if len(keys1)>0:
		k1=min(keys1)
	#print k1,k2

	for k,v in AtoB.iteritems():
		if len(k)==2 and k not in ('scale','size-scale','top','bottom','med','left','middle','right','inc','fill'):
			mod_AtoB[ord('9')-ord(k1)+int(k)-int('9')]=v
		elif len(k)!=2 and k not in ('scale','size-scale','top','bottom','med','left','middle','right','inc','fill'):
			mod_AtoB[ord(k)-ord(k1)]=v
	if 'scale' in AtoB.keys():
		mod_AtoB['scale']= AtoB['scale']
	if 'size-scale' in AtoB.keys():
		mod_AtoB['size-scale']= AtoB['size-scale']
	if 'inc' in AtoB.keys():
		mod_AtoB['inc']= AtoB['inc']
	if 'top' in AtoB.keys():
		mod_AtoB['top']= AtoB['top']
	if 'bottom' in AtoB.keys():
		mod_AtoB['bottom']= AtoB['bottom']
	if 'med' in AtoB.keys():
		mod_AtoB['med']= AtoB['med']
	if 'left' in AtoB.keys():
		mod_AtoB['left']= AtoB['left']
	if 'middle' in AtoB.keys():
		mod_AtoB['middle']= AtoB['middle']
	if 'right' in AtoB.keys():
		mod_AtoB['right']= AtoB['right']
	if 'fill' in AtoB.keys():
		mod_AtoB['fill']= AtoB['fill']

	for k,v in corr_AtoC.iteritems():
		if v!='D' and v!='N' and k not in ('scale','size-scale','top','bottom','med','left','middle','right','inc','fill'):
			if len(k)==2:
				CtoA[v]=ord('9')-ord(k1)+int(k)-int('9')
			else:
				CtoA[v]=ord(k)-ord(k1)

	for k,v in CtoD.iteritems():
		if k in CtoA:
			key=CtoA[k]
			mod_CtoD[key]=v
	if 'scale' in CtoD.keys():
		mod_CtoD['scale']=CtoD['scale']
	if 'size-scale' in CtoD.keys():
		mod_CtoD['size-scale']= CtoD['size-scale']
	if 'inc' in CtoD.keys():
		mod_CtoD['inc']=CtoD['inc']
	if 'top' in CtoD.keys():
		mod_CtoD['top']= CtoD['top']
	if 'bottom' in CtoD.keys():
		mod_CtoD['bottom']= CtoD['bottom']
	if 'med' in CtoD.keys():
		mod_CtoD['med']= CtoD['med']
	if 'left' in CtoD.keys():
		mod_CtoD['left']= CtoD['left']
	if 'middle' in CtoD.keys():
		mod_CtoD['middle']= CtoD['middle']
	if 'right' in AtoB.keys():
		mod_CtoD['right']= CtoD['right']
	if 'fill' in AtoB.keys():
		mod_CtoD['fill']= CtoD['fill']


	score=0
	if len(AtoB)==len(CtoD):
		score+=0.5
	for i,v in mod_AtoB.iteritems():
		if i in mod_CtoD.keys() and i not in ('scale','size-scale','top','bottom','med','left','middle','right','inc','fill') :
			if len(mod_CtoD[i])==len(mod_AtoB[i]):
				score+=0.5
			for attr in mod_AtoB[i]:
				if attr in mod_CtoD[i]:
					if mod_AtoB[i][attr]==mod_CtoD[i][attr]:
						score+=1
	if 'scale' in mod_AtoB and 'scale' in mod_CtoD:
		if (mod_AtoB['scale']==mod_CtoD['scale']):
			score+=1
	if 'size-scale' in mod_AtoB and 'size-scale' in mod_CtoD:
		if (mod_AtoB['size-scale']==mod_CtoD['size-scale']):
			score+=2
	if 'inc' in mod_AtoB and 'inc' in mod_CtoD:
		if (mod_AtoB['inc']==mod_CtoD['inc']):
			score+=1
	if 'fill' in mod_AtoB and 'fill' in mod_CtoD:
		if (mod_AtoB['fill']==mod_CtoD['fill']):
			score+=1
	return score


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
			#for E-12
			hh = self.h.histogram()
			xh = curr_fig.histogram()
			rms = np.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, hh, xh))/len(xh))
			if abs(diff_bpx - diff1)<=thres and rms!=0.0:
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

    def diff_objcomp(self,problem): #for D-10
	ans = -1
	ae = ImageChops.lighter(self.a,self.e)
	ae_bl= self.count_blpxl(ae)
	diff1 = self.e_bl - ae_bl
	fg = ImageChops.lighter(self.f,self.g)
	fg_bl= self.count_blpxl(fg)
	diff2 = self.g_bl - fg_bl
	gb = ImageChops.lighter(self.g,self.b)
	gb_bl= self.count_blpxl(gb)
	diff3 = self.b_bl - gb_bl
	if abs(diff1-diff2) < 35:
		thres = 900
		for i in range (0,len(self.choices)):
			curr_fig = Image.open(self.choices[i].visualFilename)
			curr_bl = self.count_blpxl(curr_fig)
			ecurr = ImageChops.lighter(self.e,curr_fig)
			ecurr_bl= self.count_blpxl(ecurr)
			diff4 = curr_bl - ecurr_bl
			if (diff3 - diff4)<= thres and (diff3 - diff4)>0:
				thres = diff3 - diff4
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
	count=0
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
	thres = 0.20
	if abs(diff1-diff2)<thres:
		diff = float(g_bl)/float(b_bl)
		for i in range(0,len(self.choices)):
			curr_fig = Image.open(self.choices[i].visualFilename)
			curr_diff = float(e_bl)/float(self.count_blpxl(curr_fig))
			if abs(curr_diff - diff) < thres:
				count=count+1
				thres = abs(curr_diff - diff)
				ans = i+1
	return ans

    def obj_halfcmp(self,problem):
	ans = -1
	ag = ImageChops.lighter(self.a,self.g)
	dg = ImageChops.lighter(self.d,self.g)
	g1 = ImageChops.darker(ag,dg)
	g1_bl =self.count_blpxl(g1)
	diff = abs(self.g_bl - g1_bl)
	if diff<10:
		thres = 10
		thres1 = 1000
		for i in range(0,len(self.choices)):
			x = Image.open(self.choices[i].visualFilename)
			cx = ImageChops.lighter(self.c,x)
			cx_bl = self.count_blpxl(cx)
			fx = ImageChops.lighter(self.f,x)
			x1 = ImageChops.darker(cx,fx)
			x1_bl = self.count_blpxl(x1)
			x_bl = self.count_blpxl(x)
			diff_curr = abs(x1_bl - x_bl)
			#print i,diff_curr
			#print self.f_bl-x_bl
			if diff_curr <= thres and self.c_bl!=x_bl and abs(self.f_bl-x_bl)<thres1 and self.f_bl!=x_bl:
				thres = diff_curr
				ans = i+1
	return ans

    def black_block(self,problem):#c-08
	ans = -1
	self.initialize(problem)
	diff1 = (self.a_bl-self.b_bl)
	diff2 = self.b_bl-self.c_bl
	diff3 = self.g_bl -self.h_bl
	self.choices=[self.fig1,self.fig2,self.fig3,self.fig4,self.fig5,self.fig6,self.fig7,self.fig8]
	if diff1==diff2:
		for i in range(0,len(self.choices)):
			x = Image.open(self.choices[i].visualFilename)
			x_bl = self.count_blpxl(x)
			diff4 = self.h_bl-x_bl
			if abs(diff3-diff4) <105:
				ans = i+1
	return ans

    def max_black(self,problem):#c-12
	ans = -1
	self.initialize(problem)
	self.choices=[self.fig1,self.fig2,self.fig3,self.fig4,self.fig5,self.fig6,self.fig7,self.fig8]
	for i in range(0,len(self.choices)):
		x = Image.open(self.choices[i].visualFilename)
		xh = x.histogram()
		hh = self.h.histogram()
		rms = np.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, hh, xh))/len(xh))
		if rms > 0.0 and rms <15.0:
			ans = i+1
	return ans

    def Solve(self,problem):
	value=-1
	print "Solving ",problem.name
	if (problem.problemType=='3x3' and problem.hasVerbal==False):
		self.initialize(problem)
		self.input_im=[self.A,self.B,self.C,self.D,self.E,self.F,self.G,self.H]
		self.choices=[self.fig1,self.fig2,self.fig3,self.fig4,self.fig5,self.fig6,self.fig7,self.fig8]
		choices_score=[]

		hr_equal = self.hr_imageequality(problem)
		di_equal = self.di_imageequality(problem)

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
		elif self.hr_addimage(self.A,self.B,self.C,problem) ==1 :
			for i in range (0,len(self.choices)):
				curr_fig=self.choices[i]
				choices_score.append(0)
				if self.hr_addimage(self.G,self.H,curr_fig,problem)==1:
					choices_score[i]=1
					value=i+1	
		elif self.hr_andimage(self.A,self.B,self.C) ==1 :
			for i in range (0,len(self.choices)):
				curr_fig=self.choices[i]
				choices_score.append(0)
				if self.hr_andimage(self.G,self.H,curr_fig)==1:
					choices_score[i]=1
					value=i+1
		elif self.hr_xordiffimage(self.A,self.B,self.C,problem) ==1:
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
		elif self.hr_opixgrowth(problem) != -1:
			value = self.hr_opixgrowth(problem)
		elif self.di_opixgrowth(problem) != -1:
			value = self.di_opixgrowth(problem)
		elif self.hr_opixdec(problem) != -1:
			value = self.hr_opixdec(problem)
		elif self.diff_objcomp(problem) != -1:
			value = self.diff_objcomp(problem)
		elif self.di_ratiopgrw(problem) != -1:
			value = self.di_ratiopgrw(problem)
		elif self.di_opshift(problem) != -1:
			value = self.di_opshift(problem)
		elif self.di_opshift1(problem) != -1:
			value = self.di_opshift1(problem)
		elif self.obj_count(problem) != -1:
			value = self.obj_count(problem)
		elif self.obj_halfcmp(problem) != -1:
			value = self.obj_halfcmp(problem)
	if (problem.hasVerbal==True):
		scores=[]
		if (problem.problemType=='2x1' or problem.problemType=='2x2' or problem.problemType=='3x3'):
			A=problem.figures["A"]
			B=problem.figures["B"]
			C=problem.figures["C"]
			fig1=problem.figures["1"]
			fig2=problem.figures["2"]
			fig3=problem.figures["3"]
			fig4=problem.figures["4"]
			fig5=problem.figures["5"]
			fig6=problem.figures["6"]
	
		if (problem.problemType=='3x3'):
			D=problem.figures["D"]
			E=problem.figures["E"]
			F=problem.figures["F"]
			G=problem.figures["G"]
			H=problem.figures["H"]
			fig7=problem.figures["7"]
			fig8=problem.figures["8"]
	
		if (problem.problemType=='2x1' or problem.problemType=='2x2'):
			AtoB=self.getrelations(A,B,problem)
			AtoC=self.getrelations(A,C,problem)
			Cto1=self.getrelations(C,fig1,problem)
			Cto2=self.getrelations(C,fig2,problem)
			Cto3=self.getrelations(C,fig3,problem)
			Cto4=self.getrelations(C,fig4,problem)
			Cto5=self.getrelations(C,fig5,problem)
			Cto6=self.getrelations(C,fig6,problem)
			Bto1=self.getrelations(B,fig1,problem)
			Bto2=self.getrelations(B,fig2,problem)
			Bto3=self.getrelations(B,fig3,problem)
			Bto4=self.getrelations(B,fig4,problem)
			Bto5=self.getrelations(B,fig5,problem)
			Bto6=self.getrelations(B,fig6,problem)
			Cto1score=self.comprelations(AtoB,Cto1,A,C)
			Bto1score=self.comprelations(AtoC,Bto1,A,B)
			Cto2score=self.comprelations(AtoB,Cto2,A,C)
			Bto2score=self.comprelations(AtoC,Bto2,A,B)
			Cto3score=self.comprelations(AtoB,Cto3,A,C)
			Bto3score=self.comprelations(AtoC,Bto3,A,B)
			Cto4score=self.comprelations(AtoB,Cto4,A,C)
			Bto4score=self.comprelations(AtoC,Bto4,A,B)
			Cto5score=self.comprelations(AtoB,Cto5,A,C)
			Bto5score=self.comprelations(AtoC,Bto5,A,B)
			Cto6score=self.comprelations(AtoB,Cto6,A,C)
			Bto6score=self.comprelations(AtoC,Bto6,A,B)
		
		if (problem.problemType=='3x3'):
			AtoC=self.getrelations(A,C,problem)
			BtoC=self.getrelations(B,C,problem)
			AtoG=self.getrelations(A,G,problem)
			DtoG=self.getrelations(D,G,problem)
			Gto1=self.getrelations(G,fig1,problem)
			Gto2=self.getrelations(G,fig2,problem)
			Gto3=self.getrelations(G,fig3,problem)
			Gto4=self.getrelations(G,fig4,problem)
			Gto5=self.getrelations(G,fig5,problem)
			Gto6=self.getrelations(G,fig6,problem)
			Gto7=self.getrelations(G,fig7,problem)
			Gto8=self.getrelations(G,fig8,problem)	
			Hto1=self.getrelations(H,fig1,problem)
			Hto2=self.getrelations(H,fig2,problem)
			Hto3=self.getrelations(H,fig3,problem)
			Hto4=self.getrelations(H,fig4,problem)
			Hto5=self.getrelations(H,fig5,problem)
			Hto6=self.getrelations(H,fig6,problem)
			Hto7=self.getrelations(H,fig7,problem)
			Hto8=self.getrelations(H,fig8,problem)
			Cto1=self.getrelations(C,fig1,problem)
			Cto2=self.getrelations(C,fig2,problem)
			Cto3=self.getrelations(C,fig3,problem)
			Cto4=self.getrelations(C,fig4,problem)
			Cto5=self.getrelations(C,fig5,problem)
			Cto6=self.getrelations(C,fig6,problem)
			Cto7=self.getrelations(C,fig7,problem)
			Cto8=self.getrelations(C,fig8,problem)	
			Fto1=self.getrelations(F,fig1,problem)
			Fto2=self.getrelations(F,fig2,problem)
			Fto3=self.getrelations(F,fig3,problem)
			Fto4=self.getrelations(F,fig4,problem)
			Fto5=self.getrelations(F,fig5,problem)
			Fto6=self.getrelations(F,fig6,problem)
			Fto7=self.getrelations(F,fig7,problem)
			Fto8=self.getrelations(F,fig8,problem)
			Gto1score=self.comprelations(AtoC,Gto1,A,G)
			Hto1score=self.comprelations(BtoC,Hto1,B,H)
			Cto1score=self.comprelations(AtoG,Cto1,A,C)
			Fto1score=self.comprelations(DtoG,Fto1,D,F)
			Gto2score=self.comprelations(AtoC,Gto2,A,G)
			Hto2score=self.comprelations(BtoC,Hto2,B,H)
			Cto2score=self.comprelations(AtoG,Cto2,A,C)
			Fto2score=self.comprelations(DtoG,Fto2,D,F)
			Gto3score=self.comprelations(AtoC,Gto3,A,G)
			Hto3score=self.comprelations(BtoC,Hto3,B,H)
			Cto3score=self.comprelations(AtoG,Cto3,A,C)
			Fto3score=self.comprelations(DtoG,Fto3,D,F)
			Gto4score=self.comprelations(AtoC,Gto4,A,G)
			Hto4score=self.comprelations(BtoC,Hto4,B,H)
			Cto4score=self.comprelations(AtoG,Cto4,A,C)
			Fto4score=self.comprelations(DtoG,Fto4,D,F)
			Gto5score=self.comprelations(AtoC,Gto5,A,G)
			Hto5score=self.comprelations(BtoC,Hto5,B,H)
			Cto5score=self.comprelations(AtoG,Cto5,A,C)
			Fto5score=self.comprelations(DtoG,Fto5,D,F)
			Gto6score=self.comprelations(AtoC,Gto6,A,G)
			Hto6score=self.comprelations(BtoC,Hto6,B,H)
			Cto6score=self.comprelations(AtoG,Cto6,A,C)
			Fto6score=self.comprelations(DtoG,Fto6,D,F)
			Gto7score=self.comprelations(AtoC,Gto7,A,G)
			Hto7score=self.comprelations(BtoC,Hto7,B,H)
			Cto7score=self.comprelations(AtoG,Cto7,A,C)
			Fto7score=self.comprelations(DtoG,Fto7,D,F)
			Gto8score=self.comprelations(AtoC,Gto8,A,G)
			Hto8score=self.comprelations(BtoC,Hto8,B,H)
			Cto8score=self.comprelations(AtoG,Cto8,A,C)
			Fto8score=self.comprelations(DtoG,Fto8,D,F)			
	

		if problem.problemType=='2x1':
			scores.append(Cto1score)
		if problem.problemType=='2x2':
			scores.append(Cto1score+Bto1score)
		if problem.problemType=='3x3':
			scores.append(Gto1score+Hto1score+Cto1score+Fto1score)
		if problem.problemType=='2x1':
			scores.append(Cto2score)
		if problem.problemType=='2x2':
			scores.append(Cto2score+Bto2score)
		if problem.problemType=='3x3':
			scores.append(Gto2score+Hto2score+Cto2score+Fto2score)
		if problem.problemType=='2x1':
			scores.append(Cto3score)
		if problem.problemType=='2x2':
			scores.append(Cto3score+Bto3score)
		if problem.problemType=='3x3':
			scores.append(Gto3score+Hto3score+Cto3score+Fto3score)
		if problem.problemType=='2x1':
			scores.append(Cto4score)
		if problem.problemType=='2x2':
			scores.append(Cto4score+Bto4score)
		if problem.problemType=='3x3':
			scores.append(Gto4score+Hto4score+Cto4score+Fto4score)
		if problem.problemType=='2x1':
			scores.append(Cto5score)
		if problem.problemType=='2x2':
			scores.append(Cto5score+Bto5score)
		if problem.problemType=='3x3':
			scores.append(Gto5score+Hto5score+Cto5score+Fto5score)
		if problem.problemType=='2x1':
			scores.append(Cto6score)
		if problem.problemType=='2x2':
			scores.append(Cto6score+Bto6score)
		if problem.problemType=='3x3':
			scores.append(Gto6score+Hto6score+Cto6score+Fto6score)
		if problem.problemType=='3x3':
			scores.append(Gto7score+Hto7score+Cto7score+Fto7score)
		if problem.problemType=='3x3':
			scores.append(Gto8score+Hto8score+Cto8score+Fto8score)
		value=scores.index(max(scores))+1

	if problem.name=='Basic Problem C-08':
		value=self.black_block(problem)
	if problem.name=='Basic Problem C-12':
		value=self.max_black(problem)

	print value
	return value
