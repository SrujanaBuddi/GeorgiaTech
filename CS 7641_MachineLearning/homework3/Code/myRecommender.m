function [ U, V ] = myRecommender( rateMatrix, lowRank )
    % Please type your name here:
    name = 'Sai Srujana, Buddi';
    disp(name); % Do not delete this line.
   
    maxIter = 300; 
    learningRate = 5e-04; 
    regularizer =1.0 ; 
    % Random initialization:
    [n1, n2] = size(rateMatrix);
    U = rand(n1, lowRank) / lowRank;
    V = rand(n2, lowRank) / lowRank;
        
    iters=1;  
    e=100000000000000;
    %rmse=trace((rateMatrix-U*V' .* (rateMatrix > 0))*(rateMatrix-U*V' .* (rateMatrix > 0))')+regularizer*trace(U'*U)+regularizer*trace(V'*V);
    rmse=sumsqr((rateMatrix-U*V') .* (rateMatrix > 0))+regularizer*sumsqr(U)+regularizer*sumsqr(V);
    threshold=30;
    while(iters<maxIter&e-rmse>threshold)
        e=rmse;
        u_upd=U+2*learningRate*((rateMatrix-U*V' .* (rateMatrix > 0))*V-regularizer*U);
        v_upd=V+2*learningRate*((rateMatrix-U*V' .* (rateMatrix > 0))'*U-regularizer*V);
        U=u_upd;
        V=v_upd;
        rmse=sumsqr((rateMatrix-U*V') .* (rateMatrix > 0))+regularizer*sumsqr(U)+regularizer*sumsqr(V);
        iters=iters+1;
    end
    disp(iters)
end