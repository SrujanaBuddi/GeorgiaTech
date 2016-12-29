function [ class ] = mycluster_soorya( bow, K )
    rn = random('Uniform',0,1,K,1);
    cs = sum(rn, 1);
    pi_c = rn./cs;
    nw = size(bow, 2);
    nd = size(bow, 1);
    rn = random('Uniform',0,1,nw,K);
    cs = sum(rn, 1);
    mu_jc = rn/cs;
    tau_dc = zeros(nd, K);
    tau_dc_old = ones(nd, K);
    
    while(true)
        
        for i = 1:nd
            for j = 1:K
                product = prod(mu_jc(:, :).^(bow(i,:)'))';
                tau_dc(i,j) = (pi_c(j) * product(j))/ sum(pi_c .* product);
            end
        end
        
        tf = abs(tau_dc-tau_dc_old)<0.0001;
        if(all(tf(:)))
            break;
        end
            
        for i = 1:nw
            for j = 1:K
                num = sum(tau_dc(:, j) .* bow(:, i));
                a = repmat(tau_dc(:, j), 1, nw);
                den = sum(sum(a.*bow),2);
                mu_jc(i, j) = num/den;
            end
        end

        pi_c = (sum(tau_dc,1) / nd)';
        tau_dc_old = tau_dc;
    end

    
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

% YOUR IMPLEMENTATION SHOULD START HERE!

    [~,class] = max(tau_dc,[],2);
end

