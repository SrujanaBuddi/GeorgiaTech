function prob = algorithm(q)
format shortEng
% plot and return the probability
 load('sp500');
%price_move;
n= size(price_move,1);
a= zeros(n,2);
a(1,1)=(1-q)*0.2;
a(1,2)= q*0.8;
for i = 2:n
    if price_move(i,1)==1
        a(i,1)=q*((a(i-1,1)*0.8)+(a(i-1,2)*0.2));
        a(i,2)=(1-q)*((a(i-1,1)*0.2)+(a(i-1,2)*0.8));
    end
    if price_move(i,1)== -1
        a(i,1)=(1-q)*((a(i-1,1)*0.8)+(a(i-1,2)*0.2));
        a(i,2)=q*((a(i-1,1)*0.2)+(a(i-1,2)*0.8));
    end
end
b=zeros(n,2);
b(n,1)=1;
b(n,2)=1;
for i=n-1:-1:1
    if price_move(i,1)==1
        b(i,1)= 0.8*q*b(i+1,1)+0.2*(1-q)*b(i+1,2);
        b(i,2)= 0.2*q*b(i+1,1)+0.8*(1-q)*b(i+1,2);
    end
    if price_move(i,1)==-1
        b(i,1)=0.8*(1-q)*b(i+1,1)+0.2*q*b(i+1,2);
        b(i,2)=0.2*(1-q)*b(i+1,1)+0.8*q*b(i+1,2);
    end
end
prob_all=zeros(n,1);
for i = 1:n
    prob_all(i)=a(i,1)*b(i,1)/(a(i,1)*b(i,1)+a(i,2)*b(i,2));
end
prob=prob_all(n);
figure
plot(prob_all)
hold on;
str=sprintf('For q = %.1f',q);
title(str);
xlabel('Week')
ylabel('Probability')
hold on;
end