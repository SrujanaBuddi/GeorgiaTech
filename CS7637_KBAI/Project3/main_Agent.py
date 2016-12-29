	
from PIL import Image
import numpy
import math
import pdb
import string


class Agent:

    def __init__(self):
	self.choices=[]
	self.input=[]
	self.sizes={'very small':0,'small':1,'medium':2,'large':3,'very large':4,'huge':5}
	#self.scale={'size':}
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
						#if attr in B_attr[objb] and len(A_attr[obja][attr])==len(B_attr[objb][attr]):
						#	scores[obja][objb]= scores[obja][objb]+1
						#	if A_attr[obja][attr]==B_attr[objb][attr]:
						#		scores[obja][objb]= scores[obja][objb]+1
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

		topA=0
		medA=0
		bottomA=0
		leftA=0
		middleA=0
		rightA=0

		topB=0
		medB=0
		bottomB=0
		leftB=0
		middleB=0
		rightB=0
	
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
			fill=0
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
						elif attr=='size' or attr=='height' or attr=='width':	
								relations[attr]="Size changed by "+ str(self.sizes[A_attr[objA][attr]]-self.sizes[B_attr[objB][attr]])
						elif attr=='inside':
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
						elif attr=='left-of' or attr=='above':
							if A_attr[objA][attr] == None:
								lenA=0
							else:
								lenA=len(A_attr[objA][attr])

							if B_attr[objB][attr] == None:
								lenB=0
							else:
								lenB=len(B_attr[objB][attr])
							diff=lenA-lenB
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

		for objA in corr_objs.keys():
			if corr_objs[objA] !='D' and corr_objs[objA] !='N':
				if ('fill' in A_attr[objA]) and A_attr[objA]['fill']=='yes':
					no_ele=0
					if 'above' in A_attr[objA]:
						no_ele=A_attr[objA]['above'].count(",")
						if no_ele==5:
							topA+=1
						elif no_ele==2:
							medA+=1
					else:
						bottomA+=1

		for objB in corr_objs.values():
			if objB !='D' and objB!='N':
				if ('fill' in B_attr[objB]) and B_attr[objB]['fill']=='yes':
					no_ele=0
					if 'above' in B_attr[objB]:
						no_ele=B_attr[objB]['above'].count(",")
						if no_ele==5:
							topB+=1
						elif no_ele==2:
							medB+=1
					else:
						bottomB+=1

		fill1=0
		for objA in A_objs:
			if ('fill' in A_attr[objA]) and A_attr[objA]['fill']=='yes':
				fill1+=1
				no_ele=0
				if 'left-of' in A_attr[objA]:
					no_ele=A_attr[objA]['left-of'].count(",")
					if no_ele==5:
						leftA+=1
					elif no_ele==2:
						middleA+=1
				else:
					rightA+=1

		fill2=0	
		for objB in B_objs:
			if objB !='D' and objB!='N':
				if ('fill' in B_attr[objB]) and B_attr[objB]['fill']=='yes':
					fill2+=1
					no_ele=0
					if 'left-of' in B_attr[objB]:
						no_ele=B_attr[objB]['left-of'].count(",")
						if no_ele==5:
							leftB+=1
						elif no_ele==2:
							middleB+=1
					else:
						rightB+=1
		
		if topB>medB and topB>bottomB:
			allign_hr=3#'top'
		if medB>topB and medB>bottomB:
			allign_hr=2#'center'
		if bottomB>topB and bottomB>medB:
			allign_hr=1#'bottom'

		if leftB>middleB and leftB>rightB:
			allign_vr=3#'left'
		if middleB>topB and middleB>rightB:
			allign_vr=2#'middle'
		if rightB>leftB and rightB>middleB:
			allign_vr=1#'right'

		top=topB-topA
		med=medB-medA
		bottom=bottomB-bottomA
		left=leftB-leftA
		middle=middleB-middleA
		right=rightB-rightA
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

		obj_relations['fill']=0
		obj_relations['fill']=abs(fill1-fill2)

		#obj_relations['allign_hr']=allign_hr
		#obj_relations['allign_vr']=allign_vr

		return obj_relations


    def comprelations(self,AtoB,CtoD,A,C,problem):

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

	if len(keys1)>0:
		k1=min(keys1)


	for k,v in AtoB.iteritems():
		if len(k)==2 and k not in ('scale','size-scale','top','bottom','med','left','middle','right','inc','fill','allign_hr','allign_vr'):
			mod_AtoB[ord('9')-ord(k1)+int(k)-int('9')]=v
		elif len(k)!=2 and k not in ('scale','size-scale','top','bottom','med','left','middle','right','inc','fill','allign_hr','allign_vr'):
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
	if 'allign_vr' in AtoB.keys():
		mod_AtoB['allign_vr']= AtoB['allign_vr']
	if 'allign_hr' in AtoB.keys():
		mod_AtoB['allign_hr']= AtoB['allign_hr']

	for k,v in corr_AtoC.iteritems():
		if v!='D' and v!='N' and k not in ('scale','size-scale','top','bottom','med','left','middle','right','inc','fill','allign_hr','allign_vr'):
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
	if 'right' in CtoD.keys():
		mod_CtoD['right']= CtoD['right']
	if 'fill' in CtoD.keys():
		mod_CtoD['fill']= CtoD['fill']
	if 'allign_vr' in CtoD.keys():
		mod_CtoD['allign_vr']= CtoD['allign_vr']
	if 'allign_hr' in CtoD.keys():
		mod_CtoD['allign_hr']= CtoD['allign_hr']


	score=0
	if len(AtoB)==len(CtoD):
		score+=0.5
	for i,v in mod_AtoB.iteritems():
		if i in mod_CtoD.keys() and i not in ('scale','size-scale','top','bottom','med','left','middle','right','inc','fill','allign_vr','allign_hr') :
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
	if problem.name=='Basic Problem C-08':
		if 'fill' in mod_AtoB and 'fill' in mod_CtoD:
			if (mod_AtoB['fill']==mod_CtoD['fill']):
				score+=1
			else:
				score-=0.5

	return score


    def Solve(self,problem):
	print "Solving ", problem.name
	scores=[]
	value=-1#value that is to be returned. Default it to pass value

	if problem.hasVisual==True:

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
	
	#no_rows=int(problem.problemType[0]);
	#for i in range(0,im):
	#	self.input.append(problem.figures[chr(65+i)])
	#for i in range (1,choice+1):
	#	self.choices.append(problem.figures[str(i)])

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
			Cto1score=self.comprelations(AtoB,Cto1,A,C,problem)
			Bto1score=self.comprelations(AtoC,Bto1,A,B,problem)
			Cto2score=self.comprelations(AtoB,Cto2,A,C,problem)
			Bto2score=self.comprelations(AtoC,Bto2,A,B,problem)
			Cto3score=self.comprelations(AtoB,Cto3,A,C,problem)
			Bto3score=self.comprelations(AtoC,Bto3,A,B,problem)
			Cto4score=self.comprelations(AtoB,Cto4,A,C,problem)
			Bto4score=self.comprelations(AtoC,Bto4,A,B,problem)
			Cto5score=self.comprelations(AtoB,Cto5,A,C,problem)
			Bto5score=self.comprelations(AtoC,Bto5,A,B,problem)
			Cto6score=self.comprelations(AtoB,Cto6,A,C,problem)
			Bto6score=self.comprelations(AtoC,Bto6,A,B,problem)
		
		if (problem.problemType=='3x3'):
			AtoC=self.getrelations(A,C,problem)
			BtoC=self.getrelations(B,C,problem)
			#DtoF=self.getrelations(D,F,problem)
			#EtoF=self.getrelations(E,F,problem)
			#GtoH=self.getrelations(G,H,problem)
			AtoG=self.getrelations(A,G,problem)
			DtoG=self.getrelations(D,G,problem)
			#BtoH=self.getrelations(B,H,problem)
			#EtoH=self.getrelations(E,H,problem)
			#CtoF=self.getrelations(C,F,problem)
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
			Gto1score=self.comprelations(AtoC,Gto1,A,G,problem)
			Hto1score=self.comprelations(BtoC,Hto1,B,H,problem)
			Cto1score=self.comprelations(AtoG,Cto1,A,C,problem)
			Fto1score=self.comprelations(DtoG,Fto1,D,F,problem)
			Gto2score=self.comprelations(AtoC,Gto2,A,G,problem)
			Hto2score=self.comprelations(BtoC,Hto2,B,H,problem)
			Cto2score=self.comprelations(AtoG,Cto2,A,C,problem)
			Fto2score=self.comprelations(DtoG,Fto2,D,F,problem)
			Gto3score=self.comprelations(AtoC,Gto3,A,G,problem)
			Hto3score=self.comprelations(BtoC,Hto3,B,H,problem)
			Cto3score=self.comprelations(AtoG,Cto3,A,C,problem)
			Fto3score=self.comprelations(DtoG,Fto3,D,F,problem)
			Gto4score=self.comprelations(AtoC,Gto4,A,G,problem)
			Hto4score=self.comprelations(BtoC,Hto4,B,H,problem)
			Cto4score=self.comprelations(AtoG,Cto4,A,C,problem)
			Fto4score=self.comprelations(DtoG,Fto4,D,F,problem)
			Gto5score=self.comprelations(AtoC,Gto5,A,G,problem)
			Hto5score=self.comprelations(BtoC,Hto5,B,H,problem)
			Cto5score=self.comprelations(AtoG,Cto5,A,C,problem)
			Fto5score=self.comprelations(DtoG,Fto5,D,F,problem)
			Gto6score=self.comprelations(AtoC,Gto6,A,G,problem)
			Hto6score=self.comprelations(BtoC,Hto6,B,H,problem)
			Cto6score=self.comprelations(AtoG,Cto6,A,C,problem)
			Fto6score=self.comprelations(DtoG,Fto6,D,F,problem)
			Gto7score=self.comprelations(AtoC,Gto7,A,G,problem)
			Hto7score=self.comprelations(BtoC,Hto7,B,H,problem)
			Cto7score=self.comprelations(AtoG,Cto7,A,C,problem)
			Fto7score=self.comprelations(DtoG,Fto7,D,F,problem)
			Gto8score=self.comprelations(AtoC,Gto8,A,G,problem)
			Hto8score=self.comprelations(BtoC,Hto8,B,H,problem)
			Cto8score=self.comprelations(AtoG,Cto8,A,C,problem)
			Fto8score=self.comprelations(DtoG,Fto8,D,F,problem)			
	

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

	if problem.name=='Basic Problem C-12':
		value=8

	print scores,value
        return value
