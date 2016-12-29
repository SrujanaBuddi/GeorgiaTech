function centroid=initializecentroid(pixels,K)
centroid=zeros(K,size(pixels,2));
randidx=ceil(rand(K,1)*size(pixels,1));
centroid=pixels(randidx(1:K),:);
end