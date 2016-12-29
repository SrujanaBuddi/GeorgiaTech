function class=ClosestCenter(pixels,centroids)
p=size(pixels,1);
class=zeros(p,1);
K=size(centroids,1);

for i=1:p
    min_dis=inf;
    for j=1:K
        dis=sqrt(sum(((pixels(i,:)-centroids(j,:)).^2)));
            if dis<min_dis
                class(i)=j;
                min_dis=dis;
            end
    end
end
end



