clc;
clear;
close all;
data = csvread('D:\2016 Spring\349 Machine Learning\Project\data3.csv');

for i = 1 : 277
    X(i,1) = data(i,1)+0.25*(data(i,2)-1)/3;
    Y(i,1) = data(i,3);
end
% figure('color','white');
% plot(X(:,1),X(:,2),'.','color','b');
% 
% hold on
% co=[-318,530,4067,634,634,4699,6025,3229,234,511,516,506,745,3977,7311,747,1938,1944,-3209,521,529,7063,2290,645,649,2938]/10000;
% % co = [ -0.0318 ,0.53,0.4067,0.0634,0.0634,0.4699,0.6025,0.3229,0.0234,0.0511,0.0516,0.0506,0.0745, 0.3977, 0.7311,0.0747,0.1938,0.1944,-0.3209,0.0521,0.0529,0.7063,0.229,0.0645,0.0649,0.2938];
% i = 1 : 189;
% plot(data(i,1),co(1)+co(2)*data(i,2)+co(3)*data(i,3)+co(4)*data(i,4)+co(5)*data(i,5)+co(6)*data(i,6)+co(7)*data(i,7)+co(8)*data(i,8)+co(9)*data(i,9)+co(10)*data(i,10)+co(11)*data(i,11)+co(12)*data(i,12)+co(13)*data(i,13)+co(14)*data(i,14)+co(15)*data(i,15)+co(16)*data(i,16)+co(17)*data(i,17)+co(18)*data(i,18)+co(19)*data(i,19)+co(20)*data(i,20)+co(21)*data(i,21)+co(22)*data(i,22)+co(23)*data(i,23)+co(24)*data(i,24)+co(25)*data(i,25)+co(26)*data(i,26),'-','color','r','LineWidth',2);
% 
% 

figure('color','white');%%µã
plot(X,Y,'x','color','r','markersize',5);
hold on

% cop5=[-1.45e-05, 0.142,-555.9,1.088e+06,-1.064e+09,4.165e+11];
% i = 1 : 277;
% plot(X(i), cop5(1)*X(i).^5 + cop5(2)*X(i).^4 + cop5(3)*X(i).^3 + cop5(4)*X(i).^2 + cop5(5)*X(i) + cop5(6),'-','color','k','LineWidth',2);
% hold on

cof2=[8420 , -1532 , 1.199e+04 , -3312 , -1615 , 0.03167];
i = 1947 : 2016;
plot(i, cof2(1) + cof2(2)*cos(cof2(6)*i) + cof2(3)*sin(cof2(6)*i) + cof2(4)*cos(2*cof2(6)*i) + cof2(5)*sin(2*cof2(6)*i),'-','color',[0 0 1],'LineWidth',1);
hold on

cog1=[2.182e+04 , 2033 , 36.07];
plot(i, cog1(1) * exp(-((i-cog1(2))/cog1(3)).^2),'-','color','m','LineWidth',1);
hold on

xu = [mean(X),std(X)];
O = ones(277,1);
X1 = (X(:,1) - xu(1)*O)/(xu(2)*O);
X1 = X1(:,1);
p1 = [-36.55 , -277.5 , 174.2 , 2872 , 4981 , 3075];
plot(X,polyval(p1,X1),'k-','LineWidth',1);
xlabel('year');
ylabel('GDP(Billion of Dollars)');
legend('Data','Fourier Fitting','Gaussian Fitting', 'Polynomial Fitting','location','northwest');
title('American GDP Data and Training Results');














