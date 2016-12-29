clear; 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SPECTRAL CLUSTERING ALGORITHM
% ==============================
% 
% Type of Algorithm:
% -------------------
% Un-normalized Laplacian: L = D - A
% 
% DATASET:
% ---------
%
% Generated by the program. Data points are clustered into two circles -
% inner and outer ring using coordinate system.
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

%% Data Generation 

% Generate random angles between [0, 2pi]
n = 800; 
rangle = 2 * pi * rand(n, 1); 

% Generate random radius for the first circle; 
e = 0.2;
rr = 1.9 + e * rand(n, 1); 

rx = rr .* sin(rangle); 
ry = rr .* cos(rangle); 

x = rx; 
y = ry; 

% Generate random radius for the second circle; 
rr2 = 1.2 + e * rand(n, 1); 

rx2 = rr2 .* sin(rangle); 
ry2 = rr2 .* cos(rangle); 

x = [x; rx2]; 
y = [y; ry2]; 

% Generate points for inducing connectivity between two circles.
rx3 = 1.4 + (1.9 - 1.4) * rand(10, 1); 
ry3 = e * rand(10, 1); 

% % uncomment this to connect the two rings; 
% x = [x; rx3]; 
% y = [y; ry3]; 

%%
% Original data figure
data = [x, y]; 
figure; 
plot(x, y, 'k.'); 
hold on; 
title('original data'); 

input('press any key to continue ...'); 

% run kmeans on the original coordinates; 
K = 3; 
idx = kmeans([x, y], K, 'Replicates', 10); 

% Cluster visualization for k-means
figure; 
cstr='rbgcm'; 
for i = 1:K
    plot(x(idx==i), y(idx==i), [cstr(i), '.']); 
    hold on; 
end
title('K-means'); 

input('press any key to continue ...');

% Distance between two points
distmat = squareform(pdist(data)).^2; 

% A(A<0.99) = 0; 
% Distance threshold to cluster points within distmat distance of each other
A = double(distmat < 0.1);  

% figure; 
% spy(A); 
% hold on; 
% title('adjacency matrix'); 

%% Spectral clustering Algorithm

D = diag(sum(A,2)); % Step to go from adjacency matrix A to degree matrix D
L = D - A; % unnormalized Laplacian

[V, S] = eig(L); % S contains eigenvalues for L and V is matrix whose 
                 % columns are the corresponding right eigenvectors
% K = 3;  % change cluster numbers here to experiment 
idx = kmeans(V(:,1:K), K, 'Replicates', 10); % Returns clusters based on L

% Cluster visualization for spectral algorithm
figure; 
figure; 
cstr='rbgcm'; 
for i = 1:K
    plot(x(idx==i), y(idx==i), [cstr(i), '.']); 
    hold on; 
end
title('Spectral Clustering'); 








