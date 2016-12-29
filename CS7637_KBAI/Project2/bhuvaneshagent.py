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
from copy import deepcopy
from Utilities import Transformation , Attribute , Conversion

class Agent:
.
    def __init__(self):
        self.problem_number = 0
        self.TwoX2ChoiceCount = 6
        self.ThreeX3ChoiceCount = 8
        self.answerChoices = []


    def Solve(self,problem):
        self.problem_number += 1
        print("Solving "+str(self.problem_number))
        self.Initialize()
        #2x2 solving (Assuming A,B,C and D only in rpm)
        A = problem.figures['A']
        B = problem.figures['B']
        C = problem.figures['C']
        for i in range(1,self.TwoX2ChoiceCount+1):
            self.answerChoices.append(problem.figures[str(i)])
        #Correspondence finding
        rowPairs = self.FindCorrespondingObjects(A,B)
        colPairs = self.FindCorrespondingObjects(A,C)
        #Horizontal Transformation List (Transformation to right - Tr)
        Tr = self.GetTransformationList(A,B,rowPairs)
        #Vertical Transformation List (Transformation to bottom - Tc)
        Tc = self.GetTransformationList(A,C,colPairs)
        #Generate and Test
        Dr = self.Generate(Tr,C,colPairs) #generated object for col wise transformation. colPairs are passed to know which object's transformation from A is to be applied to C
        Dc = self.Generate(Tc,B,rowPairs)
        D = self.Combine(Dr,Dc)
        result = self.Test(D)
        print("Answer: "+str(result))
        return result

    def Initialize(self):
        self.answerChoices = []

    def GetTransformationList(self, A, B, pairs):
        tr = {}
        for k in sorted(A.objects.keys()):
            pair = pairs[k]
            if pair != "none":
                tr[k] = self.FindTransformation(A.objects[k],B.objects[pair])
            else:
                tr[k] = self.FindTransformation(A.objects[k])
        return tr

    def FindTransformation(self, a, b="none"):
        trans = []
        if b != "none":
            if Attribute.shape.name in a.attributes and Attribute.shape.name in b.attributes:
                if b.attributes[Attribute.shape.name] != a.attributes[Attribute.shape.name]:
                    conversion = Conversion(Transformation.ShapeChange,a.attributes[Attribute.shape.name],b.attributes[Attribute.shape.name])
                    trans.append(conversion)
            if Attribute.angle.name in a.attributes and Attribute.angle.name in b.attributes:
                if b.attributes[Attribute.angle.name] != a.attributes[Attribute.angle.name]:
                    bAngle = int(b.attributes[Attribute.angle.name])
                    aAngle = int(a.attributes[Attribute.angle.name])
                    if bAngle - aAngle == 90 or bAngle - aAngle == 270:
                        conversion = Conversion(Transformation.Reflect,a.attributes[Attribute.angle.name],b.attributes[Attribute.angle.name])
                    else:
                        conversion = Conversion(Transformation.Rotate,a.attributes[Attribute.angle.name],b.attributes[Attribute.angle.name])
                    trans.append(conversion)
            if Attribute.fill.name in a.attributes and Attribute.fill.name in b.attributes:
                if b.attributes[Attribute.fill.name] != a.attributes[Attribute.fill.name]:
                    conversion = Conversion(Transformation.Fill,a.attributes[Attribute.fill.name],b.attributes[Attribute.fill.name])
                    trans.append(conversion)
            if Attribute.size.name in a.attributes and Attribute.size.name in b.attributes:
                if b.attributes[Attribute.size.name] != a.attributes[Attribute.size.name]:
                    conversion = Conversion(Transformation.Scale,a.attributes[Attribute.size.name],b.attributes[Attribute.size.name])
                    trans.append(conversion)
            if Attribute.alignment.name in a.attributes and Attribute.alignment.name in b.attributes:
                if b.attributes[Attribute.alignment.name] != a.attributes[Attribute.alignment.name]:
                    conversion = Conversion(Transformation.Translate,a.attributes[Attribute.alignment.name],b.attributes[Attribute.alignment.name])
                    trans.append(conversion)
        else:
            conversion = Conversion(Transformation.Delete,"none","none")
            trans.append(conversion)
        if trans == []:
            conversion = Conversion(Transformation.NoChange,"none","none")
            trans.append(conversion)
        return trans

    def FindCorrespondingObjects(self, A, B):
        pairs = {}
        difference = {}
        toDecidePairs = {}
        availableA = list(A.objects.keys())
        availableB = list(B.objects.keys())
        for objAKey,objAValue in A.objects.items():
            difference[objAKey] = {}
            for objBKey,objBValue in B.objects.items():
                difference[objAKey][objBKey] = self.GetDifference(objAValue,objBValue)
        for k1,v1 in difference.items():
            max = 100
            foundk2 = ""
            foundv2 = ""
            for k2,v2 in v1.items():
                if v2 < max:
                    foundk2 = k2
                    foundv2 = v2
                    max = v2
            if foundv2 == 0:
                pairs[k1] = foundk2
                availableB.remove(foundk2)
                availableA.remove(k1)
            else:
                toDecidePairs[k1] = foundk2
        for k,v in toDecidePairs.items():
            if v in availableB:
                pairs[k] = v
                availableB.remove(v)
                availableA.remove(k)
            else:
                pairs[k] = "none"
        return pairs

    def GetDifference(self, aObj, bObj):
        diff = 0
        if Attribute.shape.name in aObj.attributes and Attribute.shape.name in bObj.attributes:
            if bObj.attributes[Attribute.shape.name] != aObj.attributes[Attribute.shape.name]:
                diff += Attribute.shape.value
        if Attribute.size.name in aObj.attributes and Attribute.size.name in bObj.attributes:
            if bObj.attributes[Attribute.size.name] != aObj.attributes[Attribute.size.name]:
                diff += Attribute.size.value
        if Attribute.fill.name in aObj.attributes and Attribute.fill.name in bObj.attributes:
            if bObj.attributes[Attribute.fill.name] != aObj.attributes[Attribute.fill.name]:
                diff += Attribute.fill.value
        if Attribute.angle.name in aObj.attributes and Attribute.angle.name in bObj.attributes:
            if bObj.attributes[Attribute.angle.name] != aObj.attributes[Attribute.angle.name]:
                diff += Attribute.angle.value
        if Attribute.alignment.name in aObj.attributes and Attribute.alignment.name in bObj.attributes:
            if bObj.attributes[Attribute.alignment.name] != aObj.attributes[Attribute.alignment.name]:
                diff += Attribute.alignment.value
        if Attribute.above.name in aObj.attributes and Attribute.above.name not in bObj.attributes:
            diff += Attribute.above.value
        elif Attribute.above.name not in aObj.attributes and Attribute.above.name in bObj.attributes:
            diff += Attribute.above.value
        #have ot add inside attribute if needed
        return diff

    def Generate(self,Trans, Fig, Pairs):
        finalFig = deepcopy(Fig)
        #this works for A to C since Pairs contains obj of A only. what to do if more pairs are added for 3x3?
        for k,v in Pairs.items():
            if v != "none":
                curObject = finalFig.objects[v]
                for item in Trans[k]:
                    if item.TransformationType == Transformation.Delete:
                        del finalFig.objects[v]
                        break
                    elif item.TransformationType != Transformation.NoChange:
                        if Attribute.shape.name in curObject.attributes:
                            if item.TransformationType == Transformation.ShapeChange:
                                curObject.attributes[Attribute.shape.name] = item.getConvertedValue()
                        if Attribute.angle.name in curObject.attributes:
                            if item.TransformationType == Transformation.Reflect:
                                curObject.attributes[Attribute.angle.name] = item.getConvertedValue(curObject.attributes[Attribute.angle.name])
                        if Attribute.size.name in curObject.attributes:
                            if item.TransformationType == Transformation.Scale:
                                curObject.attributes[Attribute.size.name] = item.getConvertedValue()
                        if Attribute.angle.name in curObject.attributes:
                            if item.TransformationType == Transformation.Rotate:
                                curObject.attributes[Attribute.angle.name] = item.getConvertedValue(curObject.attributes[Attribute.angle.name])
                        if Attribute.fill.name in curObject.attributes:
                            if item.TransformationType == Transformation.Fill:
                                curObject.attributes[Attribute.fill.name] = item.getConvertedValue()
                        if Attribute.alignment.name in curObject.attributes:
                            if item.TransformationType == Transformation.Translate:
                                curObject.attributes[Attribute.alignment.name] = item.getConvertedValue(curObject.attributes[Attribute.alignment.name])
        return finalFig

    def Test(self,Fig):
        matchPercentage = 0
        matchChoiceNumber = 1
        for choice in self.answerChoices:
            pairs,availableInFig,availableInChoice = self.FindMatchingObjects(Fig,choice)
            if len(availableInFig) == 0 and len(availableInChoice) == 0:
                return int(choice.name)
            else:
                percentage = (1/(len(availableInFig)+len(availableInChoice)+1))*100
                if percentage >= matchPercentage:
                    matchPercentage = percentage
                    matchChoiceNumber = int(choice.name)
        return matchChoiceNumber

    def IsEqualObjects(self,a,b):
        if Attribute.shape.name in a.attributes and Attribute.shape.name in b.attributes:
            if b.attributes[Attribute.shape.name] != a.attributes[Attribute.shape.name]:
                return False
        if Attribute.fill.name in a.attributes and Attribute.fill.name in b.attributes:
            if b.attributes[Attribute.fill.name] != a.attributes[Attribute.fill.name]:
                return False
        if Attribute.size.name in a.attributes and Attribute.size.name in b.attributes:
            if b.attributes[Attribute.size.name] != a.attributes[Attribute.size.name]:
                return False
        if Attribute.angle.name in a.attributes and Attribute.angle.name in b.attributes:
            if b.attributes[Attribute.angle.name] != a.attributes[Attribute.angle.name]:
                return False
        if Attribute.alignment.name in a.attributes and Attribute.alignment.name in b.attributes:
            if b.attributes[Attribute.alignment.name] != a.attributes[Attribute.alignment.name]:
                return False
        return True

    def Combine(self, fig1, fig2):
        pairs,availableInFig1,availableInFig2 = self.FindMatchingObjects(fig1, fig2)
        if len(availableInFig1) == 0 and len(availableInFig2) == 0:
            return fig1
        elif len(availableInFig1) > 0:
            fig = deepcopy(fig2)
            #add to fig2 and return
            for objName in availableInFig1:
                fig.objects[objName] = deepcopy(fig1.objects[objName])
            return fig
        elif len(availableInFig2) > 0:
            fig = deepcopy(fig1)
            #add to fig1 and return
            for objName in availableInFig2:
                fig.objects[objName] = deepcopy(fig2.objects[objName])
            return fig
        pass

    def FindMatchingObjects(self, A, B):
        pairs = {}
        difference = {}
        availableA = list(A.objects.keys())
        availableB = list(B.objects.keys())
        for objAKey,objAValue in A.objects.items():
            difference[objAKey] = {}
            for objBKey,objBValue in B.objects.items():
                difference[objAKey][objBKey] = self.GetDifference(objAValue,objBValue)
        for k1,v1 in difference.items():
            max = 100
            foundk2 = ""
            foundv2 = ""
            for k2,v2 in v1.items():
                if v2 < max:
                    foundk2 = k2
                    foundv2 = v2
                    max = v2
            if foundv2 == 0:
                pairs[k1] = foundk2
                availableB.remove(foundk2)
                availableA.remove(k1)
        return pairs,availableA,availableB

    #def PrintValue(self,transList):
     #   for k,a in transList.items():
      #      print(" "+k+":")
       #     for b in a:
        #        print("  "+b.toString())

    #def PrintPairs(self,pairs):
     #   for k,v in pairs.items():
      #      print(" "+k+":"+v+",")

    #def PrintObject(self,fig):
     #   for k1 in sorted(fig.objects.keys()):
      #      print(" "+k1+":")
       #     for k,v in fig.objects[k1].attributes.items():
#print(" "+k+":"+v)
