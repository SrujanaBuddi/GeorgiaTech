# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
#problem.figures['A'].object('a').attributes
# problem.name - string containing the name of the problem
# problem.problemType - string containing the type of problem
# problem.hasVisual - boolean on if pictures 
# problem.hasVerbal - boolean on if text included
# problem.figures - dictionary for figures & solutions	
from PIL import Image
import numpy
import math
import pdb
import string

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.


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
		#print change
		return change

    def findcorrobjs(self,A,B):	
		A_objs=A.objects.keys()
		A_objs=sorted(A_objs)
		B_objs=B.objects.keys()
		B_objs=sorted(B_objs)
		A_attr={}
		B_attr={}
		corr_objs={}
		i=0
		for A_obj in A_objs:
			A_attr[i]=A.objects[A_obj].attributes
			i+=1 #no of objects in A
		j=0
		for B_obj in B_objs:
			B_attr[j]=B.objects[B_obj].attributes
			j+=1 #no of objects in B

		for i in A_attr.keys():
			if i in B_attr.keys():
				corr_objs[i]=i

		for obja in A_attr.keys():
			na_obja=len(A_attr[obja])#number of attributes for the particular object
			scores={}
			for objb in B_attr.keys():
				na_objb=len(B_attr[objb])
				if na_obja==na_objb:	
					scores[objb]=1
					for attr in A_attr[obja]:
						if attr in B_attr[objb] and len(A_attr[obja][attr])==len(B_attr[objb][attr]):
							scores[objb]= scores[objb]+1
			if scores!={}:
				corr_objs[obja]=max(scores,scores.get).keys()[0]

		if j>i:
			for objb in B_attr.keys():
				if objb not in corr_objs.values():
					corr_objs['add']=objb
		elif i>j:
			for bobj in B_attr.keys():
				na_bobj=len(B_attr[bobj])
				scores={}
				for aobj in A_attr.keys():
					na_aobj=len(A_attr[aobj])
					if na_obja==na_objb:	
						scores[aobj]=1
						for attr in A_attr[aobj]:
							if attr in B_attr[bobj] and len(A_attr[aobj][attr])==len(B_attr[bobj][attr]):
								scores[aobj]= scores[aobj]+1
				if scores!={}:
					#print scores
					obja=max(scores,scores.get).keys()[0]
					corr_objs[obja]=bobj
			
			for a in A_attr.keys():
				if a not in corr_objs.keys():
					corr_objs[a]='del'		

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
			A_attr[i]=A.objects[Aobj].attributes
			i+=1
		for Bobj in B_objs:
			B_attr[j]=B.objects[Bobj].attributes
			j+=1

		corr_objs=self.findcorrobjs(A,B)
		#if problem.name=='Basic Problem B-12':
		#	print corr_objs
		
		for objA in corr_objs.keys():
			objB = corr_objs[objA]
			relations={}
			if objA!='add' and objB!='del':
				for attr in A_attr[objA]:
					#if objB!='add' and objB!='del':
					if attr in B_attr[objB]:
						if B_attr[objB][attr]==A_attr[objA][attr]:
							relations[attr]="unchanged"
						elif attr=='angle':
							relations[attr]= "Rotated by "+ str(abs(int(A_attr[objA][attr])-int(B_attr[objB][attr])))	
						elif attr=='shape':
							relations[attr]="shape changed"
						elif attr=='fill':
							relations[attr]=A_attr[objA][attr] + ' to '+B_attr[objB][attr]
						elif attr=='size':	
							relations[attr]="Size changed from "+A_attr[objA][attr]+" to "+B_attr[objB][attr]	
						elif attr=='inside':
							if A_attr[objA][attr] is not None and B_attr[objB][attr] is not None:
								relations[attr]="Present inside"
						elif attr=='alignment':
							relations[attr]="position changed from"+self.compstr(A_attr[objA][attr],B_attr[objB][attr])		
					obj_relations[objA]=relations
			elif objA=='add':
				relations['new']="new item added"
				obj_relations[objA]=relations	
			elif objB=='del':
				relations[objB]="an item deleted"
				obj_relations[objA]=relations
		return obj_relations


    def comprelations(self,AtoB,CtoD):
		score=0
		for i in AtoB.keys():
			if i in CtoD.keys():
				for attr in AtoB[i]:
					if attr in CtoD[i]:
						if AtoB[i][attr]==CtoD[i][attr]:
							score+=1
		return score


    def Solve(self,problem):
	#print "Solving ", problem.name
	print problem
	scores=[]
	value=-1#value that is to be returned. Default it to pass value
	#read images
	A=problem.figures["A"]
	B=problem.figures["B"]
	C=problem.figures["C"]
	fig1=problem.figures["1"]
	fig2=problem.figures["2"]
	fig3=problem.figures["3"]
	fig4=problem.figures["4"]
	fig5=problem.figures["5"]
	fig6=problem.figures["6"]
	
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

	
	Cto1score=self.comprelations(AtoB,Cto1)
	Bto1score=self.comprelations(AtoC,Bto1)
	scores.append(Cto1score+Bto1score)
	Cto2score=self.comprelations(AtoB,Cto2)
	Bto2score=self.comprelations(AtoC,Bto2)
	scores.append(Cto2score+Bto2score)
	Cto3score=self.comprelations(AtoB,Cto3)
	Bto3score=self.comprelations(AtoC,Bto3)
	scores.append(Cto3score+Bto3score)
	Cto4score=self.comprelations(AtoB,Cto4)
	Bto4score=self.comprelations(AtoC,Bto4)
	scores.append(Cto4score+Bto4score)
	Cto5score=self.comprelations(AtoB,Cto5)
	Bto5score=self.comprelations(AtoC,Bto5)
	scores.append(Cto5score+Bto5score)
	Cto6score=self.comprelations(AtoB,Cto6)
	Bto6score=self.comprelations(AtoC,Bto6)
	scores.append(Cto6score+Bto6score)
	value=scores.index(max(scores))+1
	print scores
        return value
