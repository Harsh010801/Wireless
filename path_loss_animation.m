% =========================================================================
% Course: 21CSE458T — Wireless and Mobile Communication (B.Tech CSE, 7th Sem)
% Project: Comparative Analysis of Wireless Signal Propagation Models 
%          (Free Space, Okumura and Hata)
% File: path_loss_animation.m (Interactive Animated Curve Tracing in MATLAB)
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
d_fine = linspace(1, 20, 200);   % Fine distance vector for smooth animation
f = 900;                         % Carrier frequency in MHz (GSM-900)
h_te = 30;                       % Tower height in meters
h_re = 1.5;                      % Mobile station height in meters

%% 2. Propagation Formulations
% Model A: Free Space Path Loss
fspl = 20 * log10(d_fine) + 20 * log10(f) + 32.44;

% Model B: Hata Urban Model
a_hre = (1.1 * log10(f) - 0.7) * h_re - (1.56 * log10(f) - 0.8);
hata_urban = 69.55 + 26.16 * log10(f) - 13.82 * log10(h_te) - a_hre ...
             + (44.9 - 6.55 * log10(h_te)) .* log10(d_fine);

% Model C: Okumura Model (Open Area)
correction = -4.78 * (log10(f)^2) + 18.33 * log10(f) - 40.94;
okumura = hata_urban + correction;

%% 3. Setup Animated Figure Window
fig = figure('Name', 'Wireless Propagation Animation - MATLAB', ...
             'Color', [0.06 0.09 0.16], ...       % Dark slate aesthetic
             'Position', [100, 100, 1000, 600]);

ax = axes('Parent', fig, 'Color', [0.12 0.16 0.23]);
hold(ax, 'on');
grid(ax, 'on');
set(ax, 'GridColor', [0.25 0.32 0.44], 'GridAlpha', 0.5, 'GridLineStyle', ':');
set(ax, 'XColor', [0.7 0.75 0.85], 'YColor', [0.7 0.75 0.85], 'FontSize', 11);

xlim(ax, [1 20]);
ylim(ax, [85 180]);
xlabel(ax, 'Distance d (km)', 'FontSize', 12, 'FontWeight', 'bold', 'Color', [0.9 0.95 1]);
ylabel(ax, 'Path Loss PL (dB)', 'FontSize', 12, 'FontWeight', 'bold', 'Color', [0.9 0.95 1]);
title(ax, 'Live Animated Path Loss Tracing (f = 900 MHz, h_{te} = 30m, h_{re} = 1.5m)', ...
      'FontSize', 13, 'FontWeight', 'bold', 'Color', [1 1 1]);

% Initialize animated lines
h_fspl = animatedline(ax, 'Color', [0.22 0.74 0.97], 'LineWidth', 2.5, 'DisplayName', 'Free Space (FSPL)');
h_oku  = animatedline(ax, 'Color', [0.29 0.87 0.50], 'LineWidth', 2.5, 'LineStyle', '--', 'DisplayName', 'Okumura (Open Area)');
h_hata = animatedline(ax, 'Color', [0.97 0.44 0.44], 'LineWidth', 2.5, 'LineStyle', '-.', 'DisplayName', 'Hata (Urban Model)');

% Moving tip markers
p_fspl = plot(ax, NaN, NaN, 'o', 'MarkerFaceColor', [0.22 0.74 0.97], 'MarkerEdgeColor', 'w', 'MarkerSize', 8);
p_oku  = plot(ax, NaN, NaN, 's', 'MarkerFaceColor', [0.29 0.87 0.50], 'MarkerEdgeColor', 'w', 'MarkerSize', 8);
p_hata = plot(ax, NaN, NaN, '^', 'MarkerFaceColor', [0.97 0.44 0.44], 'MarkerEdgeColor', 'w', 'MarkerSize', 8);

leg = legend(ax, [h_fspl, h_oku, h_hata], 'Location', 'northwest', 'FontSize', 11, ...
             'TextColor', [1 1 1], 'Color', [0.06 0.09 0.16], 'EdgeColor', [0.3 0.4 0.5]);

% Dynamic information text box in figure
info_box = text(ax, 11.5, 95, '', 'FontSize', 11, 'FontName', 'Courier', ...
                'Color', [0.9 0.95 1], 'BackgroundColor', [0.06 0.09 0.16], ...
                'EdgeColor', [0.22 0.74 0.97], 'Margin', 8);

% Team watermark
text(ax, 0.98, 0.03, sprintf('Harsh Yadav (RA2311003011546)\nUtkarsh Dabas (RA2311003011550)\nTamanna Singh (RA2311003011570)\n21CSE458T — Wireless & Mobile Comm'), ...
     'Units', 'normalized', 'HorizontalAlignment', 'right', 'VerticalAlignment', 'bottom', ...
     'FontSize', 9, 'Color', [0.5 0.58 0.7]);

fprintf('Streaming animated MATLAB path loss simulation...\n');

%% 4. Animation Loop
for k = 1:length(d_fine)
    % Add points to lines
    addpoints(h_fspl, d_fine(k), fspl(k));
    addpoints(h_oku,  d_fine(k), okumura(k));
    addpoints(h_hata, d_fine(k), hata_urban(k));
    
    % Update tip markers
    set(p_fspl, 'XData', d_fine(k), 'YData', fspl(k));
    set(p_oku,  'XData', d_fine(k), 'YData', okumura(k));
    set(p_hata, 'XData', d_fine(k), 'YData', hata_urban(k));
    
    % Update live metric box
    curr_d = d_fine(k);
    str_info = sprintf(['Distance: %4.1f km\n' ...
                        'FSPL:     %5.1f dB\n' ...
                        'Okumura:  %5.1f dB\n' ...
                        'Hata:     %5.1f dB\n' ...
                        'Delta:   +%5.1f dB'], ...
                        curr_d, fspl(k), okumura(k), hata_urban(k), hata_urban(k) - fspl(k));
    set(info_box, 'String', str_info);
    
    drawnow limitrate;
    pause(0.02); % Adjust animation speed
end

fprintf('[+] Animation complete! All curves traced to 20 km.\n');

