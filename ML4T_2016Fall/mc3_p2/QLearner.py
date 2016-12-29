import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.num_actions = num_actions
        self.s = 0
        self.a = 0
        self.Q= np.random.uniform(-1,1,size=(num_states,num_actions))
        if dyna!=0:
                self.T1=0.0000001*np.ones((num_states,num_actions,num_states))
                self.T=self.T1/(self.T1.sum(axis=2,keepdims=True))
                self.R=-1*np.ones((num_states,num_actions))

    def qlearner_dyna(self):
        states=np.random.randint(0,self.num_states,self.dyna)
        actions=np.random.randint(0,self.num_actions,self.dyna)
        for i in range (self.dyna):
                st=states[i]
                ac=actions[i]
                s_prime=np.argmax(np.random.multinomial(1,self.T[st,ac,:]))
                r=self.R[st,ac]
                self.Q[st,ac]=(1-self.alpha)*self.Q[st,ac]+self.alpha*(r+self.gamma*np.max(self.Q[s_prime,:]))


    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        'action = rand.randint(0, self.num_actions-1)'
        ran=np.random.random()
        if ran< self.rar:
                action = rand.randint(0, self.num_actions-1)
        else:
                action=np.argmax(self.Q[s,:])
        #self.rar=self.rar*self.radr
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        #action = rand.randint(0, self.num_actions-1)
        self.Q[self.s,self.a]=((1-self.alpha)*self.Q[self.s,self.a])+self.alpha*(r+self.gamma*self.Q[s_prime,np.argmax(self.Q[s_prime,:])])
        if self.dyna!=0:
                self.T1[self.s,self.a,s_prime]+=1
                self.T[self.s,self.a,:]=self.T1[self.s,self.a,:]/self.T1[self.s,self.a,:].sum()
                self.R[self.s,self.a]=((1-self.alpha)*self.R[self.s,self.a])+r*self.alpha
                self.qlearner_dyna()
        self.s=s_prime
        self.a=self.querysetstate(self.s)
        self.rar=self.rar*self.radr
        if self.verbose: print "s =", s_prime,"a =",self.a,"r =",r
        return self.a

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
                                                                 

