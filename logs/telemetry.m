main = readtable("main_telemetry.csv");
ascending = readtable("ascending_state.csv");

close all

yyaxis left
plot(main.T, main.mean_altitude)
grid on
hold on
plot([main.T(1), main.T(end)],  [ascending.target_altitude(1), ascending.target_altitude(1)])
plot(ascending.T,  ascending.target_altitude - ascending.apoapsis_error)
yyaxis right
plot(main.T, main.vertical_speed)