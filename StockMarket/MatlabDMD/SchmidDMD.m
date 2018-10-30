function [DModes,DEv,relPower,relativeError] = SchmidDMDROBOT(X,Y,relTol)
% Dynamic Mode Decomposition as presented by 
% "Dynamic Mode Decomposition of numerical and experimental data" by Peter
% J. Schmid, Journal of Fluid Mechanics, 2010

% inputs : X and Y data matricies and a relative tolerance 

% outputs: 
% 1 - DModes - Dynamic Modes: The rows of this matrix are in one-to-one
% correspondence with the rows of Data. The columns of this matrix are 
% normalized with respect to the 2-norm and are the 
% DMD modes ordered by Power (see below).

% 2- DEv - Dynamic Eigenvalues: A column matrix of DMD eigenvalues
% whose entries are ordered by Power and 
% in a one-to-one correspondence with the columns of DModes.

% 3- relPower - A column matrix in one-to-one correspondence with
% the columns of DModes which contains the relative
% "power" contribution of each mode
% as described in "Extracting Spatial-Temporal Coherent Patterns in
% Large-Scale Neural Recordings Using Dynamic Mode Decomposition," by B.
% Brunton et. al., Journal of Neuroscience Methods, 2016. This column
% matrix is in descending order.

[U,S,V] = svd(X,0);
r = find(diag(S)>S(1,1)*relTol,1,'last');
%disp(['DMD subspace dimension:',num2str(r)])

U = U(:,1:r);
S = S(1:r,1:r);
V = V(:,1:r);

Ahat = (S^-.5)*(U'*(Y*V))*(S^-.5);
[what,lambda]=eig(Ahat);
w = (S^.5)*what;

%DModes = U*w;
DModes = Y*V*S^-1*w;
DEv = diag(lambda);

normsSquared = zeros(size(DModes,2),1);
for i = 1:size(DModes,2)
    normsSquared(i) = norm(DModes(:,i))^2;
end

%%%%%%%%% Power spectrum part of code  %%%%%%%%%%%%%%
[Power,Index]=sort(normsSquared,'descend');
DEv = DEv(Index);
DModes = DModes(:,Index);
DModes = DModes./repmat(sqrt(Power'),size(DModes,1),1);
%%disp('modes sorted based on power contribution to Data matrix')
relPower = Power/sum(Power);

Q = DModes*diag(DEv)*pinv(DModes)*X;   
   
relativeError = norm(Q-Y,'fro')/norm(Y,'fro');

%%disp(['time to compute DMD:',num2str(toc)])

end


%=========================================================================%
% Ljuboslav Boskic 
% Mezic research group
% UC Santa Barbara
% lboskic@ucsb.edu
%=========================================================================%

