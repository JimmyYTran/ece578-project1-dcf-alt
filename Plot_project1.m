
X = [100, 200, 300, 500, 800, 1000];
%for sender A trnsmission
Y1 = [1200000,2402400,3603600,4117200,4250400,4140000];
Y2 = [1191600, 1444800,	1842000,	1758000,	2088000,	1339200];
Y3 = [1198800,	2396400,	3596400,	4208400,	4380000,	4417200];
Y4 = [1198800,	2397600,	3602400,	5635200,	6260400,	5017200];

%for sender B transmission
Y5 = [1201200,	2398800,	3600000,	4166400,	3992400,	4113600];
Y6 = [1198800,	1708800,	1453200,	1524000,	1279200,	2004000];
Y7 = [1200000,	2397600,	3601200,	4348800,	4183200,	4147200];
Y8 = [1198800,	2398800,	3601200,	2859600,	2269200,	3514800];

%for sender A  collision
Y9 =  [1,	8,	18,	758,	791,	782];
Y10 = [1412,	3296,	3410,	3354,	3518,	3154];
Y11 = [2,	5,	7,	828,	777,	809];
Y12 = [22,	73,	1469,	359,	303,	274];

%for sender B collision
Y13 =  [1,	8,	18,	758,	791,	782];
Y14 = [1413,	3414,	3236,	3262,	3151,	3443];
Y15 = [2,	5,	7,	828,	777,	809];
Y16 = [27,	64,	1432,	343,	299,	276];

%fairness Index

top1 = (Y1+Y5).^2;
top2 = (Y2+Y6).^2;
top3 = (Y3+Y7).^2;
top4 = (Y4+Y8).^2;

bot1 = 2 .* (Y1.^(2) + Y5.^(2));
bot2 = 2 .* (Y2.^(2) + Y6.^(2));
bot3 = 2 .* (Y3.^(2) + Y7.^(2));
bot4 = 2 .* (Y4.^(2) + Y8.^(2));

FI1 = top1./bot1;
FI2 = top2./bot2;
FI3 = top3./bot3;
FI4 = top4./bot4;


close all; % closes all open figure windows
set(0,'defaulttextinterpreter','latex'); % allows you to use latex math
set(0,'defaultlinelinewidth',2); % line width is set to 2
set(0,'DefaultLineMarkerSize',10); % marker size is set to 10
set(0,'DefaultTextFontSize', 16); % Font size is set to 16
set(0,'DefaultAxesFontSize',16); % font size for the axes is set to 16
figure(1)
% plot(X, Y13,  X, Y14,  X,  Y15, X,  Y16); % plottinge curves  for the same X
plot(X, FI1,  X, FI2,  X,  FI3, X,  FI4); % plottinge curves  for the same X
grid on; % grid lines on the plot
xlim([0 1050])
ylim([0.8 1.05])
legend('Shared Collision Domain (No VCS)', 'Hidden Terminals (No VCS)','Shared Collision Domain (VCS Enabled)','Hidden Terminals (VCS Enabled)');
% ylabel('$T$ (bps)');
% ylabel('number of collision');
ylabel('Fairness Index');
xlabel('$\lambda$ (frames/sec)');












