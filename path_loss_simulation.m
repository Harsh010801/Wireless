% =========================================================================
% Course: 21CSE458T — Wireless and Mobile Communication (B.Tech CSE, 7th Sem)
% Project: Comparative Analysis of Wireless Signal Propagation Models 
%          (Free Space, Okumura and Hata) using MATLAB
% 
% Team Members:
% 1. Harsh Yadav (RA2311003011546)
% 2. Utkarsh Dabas (RA2311003011550)
% 3. Tamanna Singh (RA2311003011570)
% =========================================================================

clc;
clear;
close all;

%% 1. Simulation Parameters
d = 1:20;               % Distance range from 1 km to 20 km
f = 900;                % Carrier frequency in MHz (Standard GSM band)
h_te = 30;              % Base station / tower antenna height in meters
h_re = 1.5;             % Mobile station antenna height in meters

%% 2. Propagation Model Formulations

% Model A: Free Space Path Loss (FSPL)
% Formula: L_fspl = 20*log10(d) + 20*log10(f) + 32.44
fspl = 20 * log10(d) + 20 * log10(f) + 32.44;

% Model B: Okumura-Hata Urban Model
% Mobile antenna height correction factor a(h_re)
a_hre = (1.1 * log10(f) - 0.7) * h_re - (1.56 * log10(f) - 0.8);

% Standard Urban Path Loss Equation
hata_urban = 69.55 + 26.16 * log10(f) - 13.82 * log10(h_te) - a_hre ...
             + (44.9 - 6.55 * log10(h_te)) .* log10(d);

% Model C: Okumura Model (Open Area via standard Hata correction)
% Standard empirical correction factor for open/rural terrain
correction = -4.78 * (log10(f)^2) + 18.33 * log10(f) - 40.94;
okumura = hata_urban + correction;

%% 3. Display Numerical Results Table to Console
fprintf('=================================================================\n');
fprintf('  WIRELESS PROPAGATION MODELS: NUMERICAL SIMULATION RESULTS\n');
fprintf('  Frequency = %d MHz | Tower Height = %d m | Mobile Height = %.1f m\n', f, h_te, h_re);
fprintf('=================================================================\n');
fprintf('%-15s | %-16s | %-14s | %-14s\n', 'Distance (km)', 'Free Space (dB)', 'Okumura (dB)', 'Hata Urban (dB)');
fprintf('-----------------------------------------------------------------\n');
for i = 1:length(d)
    fprintf('%-15d | %-16.2f | %-14.2f | %-14.2f\n', d(i), fspl(i), okumura(i), hata_urban(i));
end
fprintf('=================================================================\n\n');

fprintf('Benchmark Readings:\n');
fprintf('• At 1 km  -> Free Space: %.2f dB | Okumura: %.2f dB | Hata: %.2f dB\n', fspl(1), okumura(1), hata_urban(1));
fprintf('• At 20 km -> Free Space: %.2f dB | Okumura: %.2f dB | Hata: %.2f dB\n', fspl(end), okumura(end), hata_urban(end));

%% 4. Graphical Visualization
figure('Color', [1 1 1], 'Position', [150, 150, 850, 550]);

plot(d, fspl, 'b-o', 'LineWidth', 2.0, 'MarkerSize', 6, 'DisplayName', 'Free Space Path Loss (FSPL)');
hold on;
plot(d, okumura, 'g--s', 'LineWidth', 2.0, 'MarkerSize', 6, 'DisplayName', 'Okumura Model (Open Area)');
plot(d, hata_urban, 'r-.^', 'LineWidth', 2.0, 'MarkerSize', 6, 'DisplayName', 'Hata Model (Urban)');
hold off;

title('Path Loss vs Distance (f=900 MHz)', 'FontSize', 14, 'FontWeight', 'bold');
xlabel('Distance (km)', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('Path Loss (dB)', 'FontSize', 12, 'FontWeight', 'bold');
xlim([1 20]);
xticks(1:1:20);
grid on;
set(gca, 'GridLineStyle', ':', 'GridAlpha', 0.6, 'FontSize', 11);
legend('Location', 'southeast', 'FontSize', 11);

% Save graph as high-resolution PNG
saveas(gcf, 'path_loss_graph_matlab.png');
fprintf('\n[+] MATLAB Plot saved as path_loss_graph_matlab.png\n');

