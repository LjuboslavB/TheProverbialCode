close all 
clear all

%% Choose Data set
file = 'SensorData2';
data = load(file);
data = data.DataV2;

% % % %%%%%Plots of signals

% % figure()
% % plot((1:size(data,2))/12/24,data(1,:),'.b',...
% %     (1:size(data,2))/12/24,data(7,:),'.r',...
% %     (1:size(data,2))/12/24,data(13,:),'.g',...
% %     (1:size(data,2))/12/24,data(19,:),'.c',...
% %     (1:size(data,2))/12/24,data(25,:),'.k',...
% %     (1:size(data,2))/12/24,data(31,:),'.m')
% % legend('door sensor','middle right','middle left','back left',...
% %     'Location','best','back right','outdoor')
% % xlabel('Time (days)')
% % ylabel('Temperature (Celcius)')

% % % figure()
% % % plot((1:size(data,2))/12/24,data(2,:),'.b',...
% % %     (1:size(data,2))/12/24,data(8,:),'.r',...
% % %     (1:size(data,2))/12/24,data(14,:),'.g',...
% % %     (1:size(data,2))/12/24,data(20,:),'.c',...
% % %     (1:size(data,2))/12/24,data(26,:),'.k')
% % % legend('door sensor','middle right','middle left','back left',...
% % %     'Location','best','back right')
% % % xlabel('Time (days)')
% % % ylabel('Humidity (%RH)')

% % % 
% % % figure()
% % % plot((1:size(data,2))/12/24,data(3,:),'.b',...
% % %     (1:size(data,2))/12/24,data(9,:),'.r',...
% % %     (1:size(data,2))/12/24,data(15,:),'.g',...
% % %     (1:size(data,2))/12/24,data(21,:),'.c',...
% % %     (1:size(data,2))/12/24,data(27,:),'.k')
% % % legend('door sensor','middle right','middle left','back left',...
% % %     'Location','best','back right')
% % % xlabel('Time (days)')
% % % ylabel('Light (ix)')


% % % figure()
% % % plot((1:size(data,2))/12/24,data(4,:),'.b',...
% % %     (1:size(data,2))/12/24,data(10,:),'.r',...
% % %     (1:size(data,2))/12/24,data(16,:),'.g',...
% % %     (1:size(data,2))/12/24,data(22,:),'.c',...
% % %     (1:size(data,2))/12/24,data(28,:),'.k')
% % % legend('door sensor','middle right','middle left','back left',...
% % %     'Location','best','back right')
% % % xlabel('Time (days)')
% % % ylabel('UVI')
% % % 

% % % 
% % % figure()
% % % plot((1:size(data,2))/12/24,data(5,:),'.b',...
% % %     (1:size(data,2))/12/24,data(11,:),'.r',...
% % %     (1:size(data,2))/12/24,data(17,:),'.g',...
% % %     (1:size(data,2))/12/24,data(23,:),'.c',...
% % %     (1:size(data,2))/12/24,data(29,:),'.k')
% % % legend('door sensor','middle right','middle left','back left',...
% % %     'Location','best','back right')
% % % xlabel('Time (days)')
% % % ylabel('Pressure (hPa)')


% % % figure()
% % % plot((1:size(data,2))/12/24,data(6,:),'.b',...
% % %     (1:size(data,2))/12/24,data(12,:),'.r',...
% % %     (1:size(data,2))/12/24,data(18,:),'.g',...
% % %     (1:size(data,2))/12/24,data(24,:),'.c',...
% % %     (1:size(data,2))/12/24,data(30,:),'.k')
% % % legend('door sensor','middle right','middle left','back left',...
% % %     'Location','best','back right')
% % % xlabel('Time (days)')
% % % ylabel('Noise (dB)')


%% Choose signals for DMD
data = data(1:6:end,:);
%% Choose number of delays observables to use for each experimental
% observable (coordinates of feature points). Setting to zero means only
% experimental observables will be used.
numDelays = 200;

%% Create first and second snap shot matrices for DMD. Any columns with missing
% data are not used.
X = zeros((numDelays+1)*size(data,1),size(data,2)-(numDelays+1));
Y = zeros(size(X));

for i = 1:numDelays+1
   X(1 + (i-1)*size(data,1):i*size(data,1),:) = ...
       data(:,(i):size(data,2)-(numDelays+1) + (i-1));
   Y(1 + (i-1)*size(data,1):i*size(data,1),:) = ...
       data(:,(i+1):size(data,2)-(numDelays+1) + (i));
end

[DModes,DEv,relPower,relativeError] = SchmidDMD(X(1:end,:),Y(1:end,:),10^-6);
%% plot relpower of modes vs frequency
dt = 1/12/24;                       %time step size
ws = log(DEv)/dt;                   %Dynamic eigenvalues ordered by Power divided by time step size --- on log values
freqs = abs(imag(ws)/2/pi);         %Frequency- abosulte value of Imaginary Dynamic Eigenvalues divided by 2 divided by pi --- ALL BECOME REAL #s
grow = real(log(DEv)/dt)/2/pi;      %Growth - real values of log of Dynamic eig values divded by time steps then divided by 2 divided by pi -- ALL REAL #s
relPower = relPower/relPower(2);    %Relative Power corresponding to each Mode
figure()
plot(freqs(2:end),relPower(2:end),'.b','MarkerSize',15)
% % % scatter(freqs,...
% % %     relPower,...
% % %     20,grow,'filled')
% % % colormap(jet)
% % % colorbar
ylabel('Power Relative to Dominant Dynamic Mode')
xlabel('Frequency ((day)^{-1})')
%xlim([0.001 0.2])


figure()
plot(grow(2:end),relPower(2:end),'.b','MarkerSize',15)
% % % scatter(freqs,...
% % %     relPower,...
% % %     20,grow,'filled')
% % % colormap(jet)
% % % colorbar
ylabel('Power Relative to Dominant Dynamic Mode')
xlabel('Growth Rate ((day)^{-1})')


figure()
scatter(grow(2:50),freqs(2:50),10,relPower(2:50),'filled')
% % % scatter(freqs,...
% % %     relPower,...
% % %     20,grow,'filled')
% % % colormap(jet)
% % % colorbar
title([file ' (Colored by Growth rate / frame rate)'])
ylabel('Power Relative to Dominant Dynamic Mode')
xlabel('Growth Rate')
colormap(jet)
 
%% Magnitude and Phase of Components of Fundamental Mode
freqs(3)%5(0.94), 7(1.04), 9(1.96), 13(2.94), 29(14.7), 31(23.64) 
%3(0.98), 11(1.03), 17(2.04), 27(3.02), 43(14.8), 88(21.6), 145(28.02)
modeNum =43;
figure()
bar(1:size(DModes,1),abs(DModes(:,modeNum)),1)
figure()
bar(1:size(DModes,1),atan2(imag(DModes(:,modeNum)),real(DModes(:,modeNum))),1)
figure()
bar(1:6,abs(DModes(1:6,modeNum)),1)
figure()
imagesc([abs(DModes(6,modeNum)) abs(DModes(6,modeNum));...
    abs(DModes(4,modeNum)) abs(DModes(5,modeNum)) ;...
    abs(DModes(3,modeNum)) abs(DModes(2,modeNum)); abs(DModes(1,modeNum)) abs(DModes(1,modeNum))])
colorbar
text(0.8,1,'outside (airport)', 'FontWeight','bold','FontSize',10)
text(1.8,1,'outside (airport)', 'FontWeight','bold','FontSize',10)
text(0.8,2,'back left (window)', 'FontWeight','bold','FontSize',10)
text(1.8,2,'back right', 'FontWeight','bold','FontSize',10)
text(0.8,3,'middle left', 'FontWeight','bold','FontSize',10)
text(1.8,3,'middle right', 'FontWeight','bold','FontSize',10)
text(0.8,4,'no sensor', 'FontWeight','bold','FontSize',10)
text(1.8,4,'front (door)', 'FontWeight','bold','FontSize',10)
title(['Magnitude of Mode (frequency = ' num2str(freqs(modeNum)) ')'])


figure()
bar(1:6,atan2(imag(DModes(1:6,modeNum)),real(DModes(1:6,modeNum))),1)
modePhase = atan2(imag(DModes(1:6,modeNum)),real(DModes(1:6,modeNum)));
figure()
imagesc([modePhase(6) modePhase(6); modePhase(4) modePhase(5) ; modePhase(3) modePhase(2); modePhase(1) modePhase(1)])
colorbar
text(0.8,1,'outside (airport)', 'FontWeight','bold','FontSize',10)
text(1.8,1,'outside (airport)', 'FontWeight','bold','FontSize',10)
text(0.8,2,'back left (window)', 'FontWeight','bold','FontSize',10)
text(1.8,2,'back right', 'FontWeight','bold','FontSize',10)
text(0.8,3,'middle left', 'FontWeight','bold','FontSize',10)
text(1.8,3,'middle right', 'FontWeight','bold','FontSize',10)
text(0.8,4,'no sensor', 'FontWeight','bold','FontSize',10)
text(1.8,4,'front (door)', 'FontWeight','bold','FontSize',10)
title(['Phase of Mode (frequency = ' num2str(freqs(modeNum)) ')'])

