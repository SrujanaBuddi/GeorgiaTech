function class=ClosestCentermedoids(pixels,centroids)

p=size(pixels,1);
class=zeros(p,1);
K=size(centroids,1);

for i=1:p
    min_dis=inf;%distance between clusters
    %calculating complete linkage
    for j=1:K
        max_dis=0;
        %for x=1:size(pixels,2)
               dis=max(abs(pixels(i,:)-centroids(j,:)));
               %if dis>max_dis
                   %max_dis=dis;
               %end
            if dis<min_dis
                class(i)=j;
                min_dis=dis;
            end
    end
end
end