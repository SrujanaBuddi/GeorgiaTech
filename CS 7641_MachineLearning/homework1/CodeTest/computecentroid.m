function centroid=computecentroid(pixels,K,class)
centroid=zeros(K,size(pixels,2));
for i=1:K
    pos=find(class==i);
    for j=1:length(pos)
            id=pos(j);
            centroid(i,:)=centroid(i,:)+pixels(id,:);
    end
    if ~isempty(pos)
    centroid(i,:)=centroid(i,:)/length(pos);
    end
end
end