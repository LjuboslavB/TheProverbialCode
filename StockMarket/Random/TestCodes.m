% 
close all
clear all
clc

%Open High Low Close AdjClose Volume
m1 = dlmread('DRI.csv',',',1,1);
p1 = 100*(m1(:,4)-m1(:,1))./m1(:,1);
pup1=find(p1>=5);
candle(m1(:,1:4));hold on;plot(pup1,m1(pup1,1),'g.','markersize',20)
% m2(:,1:5)=m1(:,1:5)/max(max(m1(:,1:5)));
% p2 = 100*(m2(:,4)-m2(:,1))./m2(:,1);
% pup2=find(p2>=5);


% candle(m(:,1:4))
% hold on;
% plot(pup,m(pup,1),'g.','markersize',20)