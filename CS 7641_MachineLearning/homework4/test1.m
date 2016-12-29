
function prob = algorithm(q)

% plot and return the probability
A = [0.8 0.2;0.2,0.8];
B = [q,1-q;1-q,q];
pi = [0.2,0.8];

load 'sp500';
T = size(price_move,1);

P = zeros(1,T);
alpha = zeros(2,T);
beta = zeros(2,T);
for t=1:T
    y = -0.5*(price_move(t))+1.5;
    if t==1
       alpha(:,t)=pi.*B(:,y)';
       beta(:,T+1-t) = 1;
    else      
        alpha(1,t) = B(1,y)*(A(1,:)*alpha(:,t-1));
        alpha(2,t) = B(2,y)*(A(2,:)*alpha(:,t-1));
        i = T+1-t;
        yNext = -0.5*(price_move(i+1))+1.5;
        beta(1,i) = sum(beta(:,i+1).*A(:,1).*B(:,yNext));
        beta(2,i) = sum(beta(:,i+1).*A(:,2).*B(:,yNext));
%     P(t)=(alpha(i,t)*beta(i,t))/(denom);
    end  
end

for t=1:T
   denom = alpha(:,t)'*beta(:,t);
   P(1,t)=(alpha(1,t)*beta(1,t))/denom ;
%    P(2,t)=(alpha(2,t)*beta(2,t))/denom ;
end
P(39)
plot(2:39,P(2:end));
title('P(X=good|Y) vs week')
xlabel('Week') % x-axis label
ylabel('P(X=good|Y)') % y-axis label
end