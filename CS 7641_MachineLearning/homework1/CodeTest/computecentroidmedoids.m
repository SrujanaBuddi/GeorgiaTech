function centroid=computecentroidmedoids(pixels,K,class)
centroid=zeros(K,size(pixels,2));
centroids=zeros(K,size(pixels,2));
for i=1:K
    pos=find(class==i);
    for j=1:length(pos)
            id=pos(j);
            centroids(i,:)=centroids(i,:)+pixels(id,:);
    end
    if ~isempty(pos)
    centroids(i,:)=centroids(i,:)/length(pos);
    end
    
    for i=1:K
    pos=find(class==i);
    min_dis=inf;
    for j=1:length(pos)
            id=pos(j);
            dist_centre=sqrt(sum(((pixels(id,:)-centroids(K,:)).^2)));
            if dist_centre<min_dis
                min_dis=dist_centre;
                centroid(i,:)=pixels(id,:);
            end
    end
end
%centroid=centroids;
end