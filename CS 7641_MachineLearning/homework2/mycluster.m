function [ class ] = mycluster( bow, K )
%
% Your goal of this assignment is implementing your own text clustering algo.
%
% Input:
%     bow: data set. Bag of words representation of text document as
%     described in the assignment.
%
%     K: the number of desired topics/clusters. 
%
% Output:
%     class: the assignment of each topic. The
%     assignment should be 1, 2, 3, etc. 
%
% For submission, you need to code your own implementation without using
% any existing libraries
%bow is docs x words
%mu is words x clusters
%gamma is docs x clusters

% YOUR IMPLEMENTATION SHOULD START HERE!

%pi=(1/K)*ones(K,1);%initializing clusters probablilities
docs=size(bow,1);
words=size(bow,2);
clusters=K;

%random initialization of mu
%mu=(1/K)*ones(size(bow,2),K)%prob of a word in cluster c
mu=rand(words,K);
h_sum=repmat(sum(mu,2),1,K);
mu=mu./h_sum;
%random initialization of mu ends here

%using K-Means to initialize pi
%pi=rand(K,1);
%pi=pi/sum(pi);
pi=zeros(K,1);
idx=kmeans(bow,K);
for i=1:K
    pos=find(idx==i);
    pi(i)=length(pos)/docs;
end
%k-means initialization ends here

prev_mu=zeros(size(bow,2),K);
gamma=zeros(docs,K);%prob of doc in cluster in c
prev_pi=zeros(K,1);
iter=1;

while (~(isequal(mu,prev_mu)&& isequal(pi,prev_pi)) || iter<300)
  % fprintf('Number of iterations: %d\n',iter)
   iter=iter+1;
    %update gamma, Expectation step  
    for c=1:K
        for i=1:docs        
            gamma(i,c)=pi(c)*prod(mu(:,c)'.^bow(i,:));
        end
    end
    gamma=gamma./repmat(sum(gamma,2),1,K);
    
    %maximization step
    prev_mu=mu;
    prev_pi=pi;
     pi= (1/docs)*sum(gamma,1);
     pi=pi';
     for i=1:words%words   
         for j=1:K%clusters
                 clus=repmat(gamma(:,j),1,words);
                 sum1=sum(sum(clus.*bow),2);
                 mu(i,j)=sum(gamma(:,j).*bow(:,i))/sum1;
         end
     end
end
class=zeros(docs,1);
[mx,class]=max(gamma,[],2);
end

