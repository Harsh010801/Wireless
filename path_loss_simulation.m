% =========================================================================
% Course: 21CSE458T — Wireless and Mobile Communication (B.Tech CSE, 7th Sem)
% Project: Comparative Analysis of Wireless Signal Propagation Models 
%          Classical VHF/UHF vs. 5G/6G 3GPP TR 38.901 & Close-In mmWave
% 
% Team Members:
% 1. Harsh Yadav (RA2311003011546)
% 2. Utkarsh Dabas (RA2311003011550)
% 3. Tamanna Singh (RA2311003011570)
% =========================================================================

clc;
clear;
close all;

%% =========================================================================
%% PART 1: CLASSICAL MODELS (GSM 900 MHz Band, Macrocell 1 - 20 km)
%% =========================================================================
d_km = 1:20;            % Distance range from 1 km to 20 km
f_mhz = 900;            % Carrier frequency in MHz (Standard GSM band)
h_te = 30;              % Base station / tower antenna height in meters
h_re = 1.5;             % Mobile station antenna height in meters

% Model A: Free Space Path Loss (FSPL)
% Formula: L_fspl = 20*log10(d) + 20*log10(f) + 32.44
fspl = 20 * log10(d_km) + 20 * log10(f_mhz) + 32.44;

% Model B: Okumura-Hata Urban Model
a_hre = (1.1 * log10(f_mhz) - 0.7) * h_re - (1.56 * log10(f_mhz) - 0.8);
hata_urban = 69.55 + 26.16 * log10(f_mhz) - 13.82 * log10(h_te) - a_hre ...
             + (44.9 - 6.55 * log10(h_te)) .* log10(d_km);

% Model C: Okumura Model (Open Area via empirical correction)
correction = -4.78 * (log10(f_mhz)^2) + 18.33 * log10(f_mhz) - 40.94;
okumura = hata_urban + correction;

fprintf('=================================================================\n');
fprintf('  PART 1: CLASSICAL MODELS NUMERICAL RESULTS (f = %d MHz)\n', f_mhz);
fprintf('  Tower Height = %d m | Mobile Height = %.1f m\n', h_te, h_re);
fprintf('=================================================================\n');
fprintf('%-15s | %-16s | %-14s | %-14s\n', 'Distance (km)', 'Free Space (dB)', 'Okumura (dB)', 'Hata Urban (dB)');
fprintf('-----------------------------------------------------------------\n');
for i = 1:5:length(d_km)
    fprintf('%-15d | %-16.2f | %-14.2f | %-14.2f\n', d_km(i), fspl(i), okumura(i), hata_urban(i));
end
fprintf('%-15d | %-16.2f | %-14.2f | %-14.2f\n', d_km(end), fspl(end), okumura(end), hata_urban(end));
fprintf('=================================================================\n\n');


%% =========================================================================
%% PART 2: 5G / 6G MILLIMETER-WAVE MODELS (3GPP TR 38.901 & CI at 28 GHz)
%% =========================================================================
fc_ghz = 28.0;          % mmWave carrier frequency in GHz
c = 299792458;          % Speed of light in m/s
h_bs = 10.0;            % Microcell BS height (meters)
h_ut = 1.5;             % User terminal height (meters)
h_e = 1.0;              % Effective environment height (m) for UMi
h_bs_p = h_bs - h_e;    % 9.0 m
h_ut_p = h_ut - h_e;    % 0.5 m

% Distance vector for mmWave microcell: 10 m to 1000 m
d_m = logspace(1, 3, 100);   % 10 m to 1000 m
d_3d = sqrt(d_m.^2 + (h_bs - h_ut)^2);

% Breakpoint distance d'BP = 4 * h'BS * h'UT * fc / c
d_bp_prime = 4 * h_bs_p * h_ut_p * (fc_ghz * 1e9) / c;  % ~ 1681.16 m

% 1. 3GPP TR 38.901 UMi LoS
pl1_umi_los = 32.4 + 21.0 * log10(d_3d) + 20.0 * log10(fc_ghz);
pl2_umi_los = 32.4 + 40.0 * log10(d_3d) + 20.0 * log10(fc_ghz) ...
              - 9.5 * log10(d_bp_prime^2 + (h_bs - h_ut)^2);
umi_los = zeros(size(d_m));
for i = 1:length(d_m)
    if d_m(i) <= d_bp_prime
        umi_los(i) = pl1_umi_los(i);
    else
        umi_los(i) = pl2_umi_los(i);
    end
end

% 2. 3GPP TR 38.901 UMi NLoS
pl_nlos_prime = 35.3 * log10(d_3d) + 22.4 + 21.3 * log10(fc_ghz) - 0.3 * (h_ut - 1.5);
umi_nlos = max(umi_los, pl_nlos_prime);

% 3. Close-In (CI) Model with 1m Free Space Reference (n = 3.19 for NLoS)
fspl_1m = 20 * log10(4 * pi * 1.0 * (fc_ghz * 1e9) / c); % 61.38 dB
n_ci = 3.19;
ci_model = fspl_1m + 10 * n_ci * log10(max(d_m, 1.0));

% 4. Floating-Intercept / ABG Model (UMi Street Canyon NLoS Preset)
alpha = 3.53; beta = 22.4; gamma = 2.13;
abg_model = 10 * alpha * log10(d_m) + beta + 10 * gamma * log10(fc_ghz);

% 5. LoS Probability (3GPP UMi Street Canyon)
p_los = zeros(size(d_m));
for i = 1:length(d_m)
    if d_m(i) <= 18
        p_los(i) = 1.0;
    else
        p_los(i) = (18 / d_m(i)) + exp(-d_m(i)/36) * (1 - 18 / d_m(i));
    end
end
pl_trans_mean = p_los .* umi_los + (1 - p_los) .* umi_nlos;

% Free Space baseline at 28 GHz
fspl_28 = 20 * log10(d_m) + 20 * log10(fc_ghz * 1000) + 32.44;

fprintf('=================================================================\n');
fprintf('  PART 2: 5G/6G mmWAVE 28 GHz NUMERICAL RESULTS (d = 100 m)\n');
fprintf('  hBS = %.1f m | hUT = %.1f m | fc = %.1f GHz\n', h_bs, h_ut, fc_ghz);
fprintf('=================================================================\n');
idx_100m = find(d_m >= 100, 1);
fprintf('• FSPL at 100 m                : %.2f dB\n', fspl_28(idx_100m));
fprintf('• 3GPP UMi LoS at 100 m        : %.2f dB (Expected: ~103.3 dB)\n', umi_los(idx_100m));
fprintf('• 3GPP UMi NLoS at 100 m       : %.2f dB (Expected: ~123.8 dB)\n', umi_nlos(idx_100m));
fprintf('• Close-In CI (n=3.19) at 100m : %.2f dB (Expected: ~125.2 dB)\n', ci_model(idx_100m));
fprintf('• Floating-Intercept ABG       : %.2f dB\n', abg_model(idx_100m));
fprintf('• LoS-NLoS Transition Mean     : %.2f dB (P_LoS = %.3f)\n', pl_trans_mean(idx_100m), p_los(idx_100m));
fprintf('=================================================================\n\n');


%% =========================================================================
%% 3. VISUALIZATION: PUBLICATION FIGURE WITH BOTH BANDS
%% =========================================================================
figure('Color', [1 1 1], 'Position', [100, 100, 1050, 520]);

% Subplot 1: Classical 900 MHz Cellular Models
subplot(1, 2, 1);
plot(d_km, fspl, 'b-o', 'LineWidth', 1.8, 'MarkerSize', 5, 'DisplayName', 'Free Space (Friis)');
hold on;
plot(d_km, okumura, 'g--s', 'LineWidth', 1.8, 'MarkerSize', 5, 'DisplayName', 'Okumura (Open Area)');
plot(d_km, hata_urban, 'r-.^', 'LineWidth', 1.8, 'MarkerSize', 5, 'DisplayName', 'Hata (Urban)');
hold off;
title('Classical Models (f = 900 MHz)', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('Distance (km)', 'FontSize', 11, 'FontWeight', 'bold');
ylabel('Path Loss (dB)', 'FontSize', 11, 'FontWeight', 'bold');
xlim([1 20]);
grid on;
set(gca, 'GridLineStyle', ':', 'GridAlpha', 0.6);
legend('Location', 'southeast', 'FontSize', 9);

% Subplot 2: 5G/6G mmWave 28 GHz Models
subplot(1, 2, 2);
semilogx(d_m, fspl_28, 'b:', 'LineWidth', 1.5, 'DisplayName', 'Free Space (28 GHz)');
hold on;
semilogx(d_m, umi_los, 'c-', 'LineWidth', 2.0, 'DisplayName', '3GPP UMi LoS');
semilogx(d_m, umi_nlos, 'm--', 'LineWidth', 2.0, 'DisplayName', '3GPP UMi NLoS');
semilogx(d_m, ci_model, 'Color', [0.8 0.5 0], 'LineStyle', '-.', 'LineWidth', 1.8, 'DisplayName', 'Close-In CI (n=3.19)');
semilogx(d_m, pl_trans_mean, 'Color', [0.3 0.7 0.1], 'LineWidth', 2.2, 'DisplayName', 'LoS-NLoS Trans. Mean');
hold off;
title('5G/6G mmWave (fc = 28 GHz, 3GPP TR 38.901)', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('Distance (m, Log Scale)', 'FontSize', 11, 'FontWeight', 'bold');
ylabel('Path Loss (dB)', 'FontSize', 11, 'FontWeight', 'bold');
xlim([10 1000]);
grid on;
set(gca, 'GridLineStyle', ':', 'GridAlpha', 0.6);
legend('Location', 'northwest', 'FontSize', 9);

% Save dual-panel graph
saveas(gcf, 'path_loss_graph_matlab.png');
fprintf('[+] Combined MATLAB Plot saved as path_loss_graph_matlab.png\n');
