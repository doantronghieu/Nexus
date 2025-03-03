# Databases

[← Back to Main Documentation](../../../../README.md)

## SQL

PostgreSQL

```sql
-- Car Assistant Database Schema

-- Table: Actions
CREATE TABLE Actions (
    action_id INT PRIMARY KEY AUTO_INCREMENT,
    action_name VARCHAR(50) NOT NULL UNIQUE
);

-- Comprehensive list of potential action_name values:
-- 'open', 'close', 'lock', 'unlock', 'turn_on', 'turn_off', 'increase', 'decrease',
-- 'set', 'adjust', 'start', 'stop', 'activate', 'deactivate', 'play', 'pause',
-- 'resume', 'skip', 'rewind', 'fast_forward', 'mute', 'unmute', 'call', 'end_call',
-- 'navigate_to', 'cancel_navigation', 'check', 'report', 'schedule', 'cancel',
-- 'find', 'locate', 'pair', 'unpair', 'connect', 'disconnect', 'enable', 'disable',
-- 'fold', 'unfold', 'tilt', 'park', 'honk', 'defog', 'defrost', 'heat', 'cool',
-- 'vent', 'recirculate', 'sync', 'unsync', 'read', 'send', 'accept', 'reject'

-- Table: Parts
CREATE TABLE Parts (
    part_id INT PRIMARY KEY AUTO_INCREMENT,
    part_name VARCHAR(50) NOT NULL UNIQUE
);

-- Comprehensive list of potential part_name values:
-- 'window', 'door', 'trunk', 'hood', 'sunroof', 'moonroof', 'air_conditioner',
-- 'heater', 'fan', 'radio', 'media_player', 'navigation_system', 'headlights',
-- 'taillights', 'fog_lights', 'hazard_lights', 'turn_signal', 'windshield_wipers',
-- 'rear_wiper', 'side_mirrors', 'rear_view_mirror', 'seats', 'steering_wheel',
-- 'cruise_control', 'parking_brake', 'gear_shifter', 'horn', 'fuel_cap',
-- 'charging_port', 'battery', 'engine', 'tire_pressure_system', 'climate_control',
-- 'defrost', 'seat_belt', 'airbag', 'dashboard', 'instrument_cluster',
-- 'infotainment_system', 'bluetooth', 'wifi', 'usb_port', 'auxiliary_input',
-- 'cigarette_lighter', 'power_outlet', 'cup_holder', 'glove_compartment',
-- 'center_console', 'armrest', 'roof_rack', 'tow_hitch', 'suspension', 'brakes',
-- 'accelerator', 'clutch', 'transmission', 'exhaust_system', 'muffler', 'catalytic_converter',
-- 'radiator', 'alternator', 'starter_motor', 'fuel_pump', 'oil_filter', 'air_filter',
-- 'cabin_filter', 'spark_plugs', 'ignition_system', 'coolant_system', 'power_steering',
-- 'shock_absorbers', 'struts', 'axles', 'differential', 'driveshaft', 'fuel_injector',
-- 'throttle_body', 'oxygen_sensor', 'mass_airflow_sensor', 'camshaft', 'timing_belt',
-- 'serpentine_belt', 'thermostat', 'water_pump', 'head_gasket', 'valve_cover',
-- 'piston', 'connecting_rod', 'crankshaft', 'flywheel', 'clutch_plate', 'pressure_plate',
-- 'transmission_fluid', 'brake_fluid', 'power_steering_fluid', 'windshield_washer_fluid',
-- 'antifreeze', 'motor_oil', 'rear_differential_fluid', 'transfer_case_fluid',
-- 'transmission_cooler', 'intercooler', 'turbocharger', 'supercharger', 'car_alarm',
-- 'keyless_entry', 'remote_start', 'backup_camera', 'parking_sensors', 'blind_spot_monitor',
-- 'lane_departure_warning', 'forward_collision_warning', 'adaptive_cruise_control',
-- 'traction_control', 'stability_control', 'anti_lock_braking_system', 'tire_pressure_monitor',
-- 'heads_up_display', 'night_vision', 'rain_sensor', 'ambient_lighting', 'dome_light',
-- 'reading_light', 'license_plate_light', 'door_handle', 'door_lock', 'window_switch',
-- 'power_window_motor', 'windshield', 'rear_window', 'side_window', 'quarter_panel',
-- 'fender', 'bumper', 'grille', 'spoiler', 'antenna', 'roof', 'floor_mats',
-- 'cargo_area', 'spare_tire', 'jack', 'lug_wrench', 'first_aid_kit', 'emergency_kit',
-- 'fire_extinguisher', 'child_safety_lock', 'lumbar_support', 'seat_heater', 'seat_cooler',
-- 'seat_massage', 'steering_wheel_heater', 'paddle_shifters', 'drive_mode_selector'

-- Table: Commands
CREATE TABLE Commands (
    command_id INT PRIMARY KEY AUTO_INCREMENT,
    action_id INT,
    part_id INT,
    command_text VARCHAR(255) NOT NULL,
    voice_trigger VARCHAR(255),
    category VARCHAR(50),
    FOREIGN KEY (action_id) REFERENCES Actions(action_id),
    FOREIGN KEY (part_id) REFERENCES Parts(part_id)
);

-- Potential category values:
-- 'climate_control', 'audio', 'navigation', 'lighting', 'security',
-- 'engine', 'windows_and_doors', 'wipers', 'mirrors', 'seats',
-- 'driving_assistance', 'maintenance', 'connectivity', 'comfort',
-- 'safety', 'performance', 'entertainment', 'communication'

-- Table: Parameters
CREATE TABLE Parameters (
    parameter_id INT PRIMARY KEY AUTO_INCREMENT,
    command_id INT,
    parameter_name VARCHAR(50) NOT NULL,
    parameter_type ENUM('numeric', 'text', 'boolean') NOT NULL,
    parameter_value VARCHAR(255),
    FOREIGN KEY (command_id) REFERENCES Commands(command_id)
);

-- Comprehensive list of potential parameter_name and parameter_type combinations:
-- 'temperature' - numeric (for climate control)
-- 'fan_speed' - numeric (for climate control)
-- 'volume' - numeric (for audio)
-- 'balance' - numeric (for audio)
-- 'fade' - numeric (for audio)
-- 'bass' - numeric (for audio)
-- 'treble' - numeric (for audio)
-- 'equalizer' - text (for audio)
-- 'station' - numeric (for radio)
-- 'frequency' - numeric (for radio)
-- 'track_number' - numeric (for media player)
-- 'playlist' - text (for media player)
-- 'artist' - text (for media player)
-- 'album' - text (for media player)
-- 'genre' - text (for media player)
-- 'brightness' - numeric (for lights or displays)
-- 'color' - text (for ambient lighting)
-- 'intensity' - numeric (for lights)
-- 'speed' - numeric (for cruise control, wipers)
-- 'distance' - numeric (for adaptive cruise control)
-- 'destination' - text (for navigation)
-- 'route_preference' - text (for navigation, e.g., 'fastest', 'shortest', 'avoid_tolls')
-- 'contact_name' - text (for phone calls)
-- 'phone_number' - text (for phone calls)
-- 'message_content' - text (for sending messages)
-- 'recipient' - text (for sending messages)
-- 'timer_duration' - numeric (for setting timers)
-- 'reminder_text' - text (for setting reminders)
-- 'alarm_time' - text (for setting alarms)
-- 'seat_position' - text (for seat adjustment, e.g., 'forward', 'backward', 'up', 'down')
-- 'lumbar_support' - numeric (for seat adjustment)
-- 'mirror_position' - text (for mirror adjustment, e.g., 'left', 'right', 'up', 'down')
-- 'steering_wheel_position' - text (for steering wheel adjustment)
-- 'air_distribution' - text (for climate control, e.g., 'face', 'feet', 'defrost')
-- 'recirculation' - boolean (for climate control)
-- 'ac_power' - boolean (for air conditioning)
-- 'heated_seats' - boolean (for seat controls)
-- 'seat_temperature' - numeric (for heated/cooled seats)
-- 'massage_intensity' - numeric (for massage seats)
-- 'cruise_control_speed' - numeric (for cruise control)
-- 'lane_departure_warning' - boolean (for driving assistance)
-- 'blind_spot_monitor' - boolean (for driving assistance)
-- 'parking_assist' - boolean (for driving assistance)
-- 'traction_control' - boolean (for driving assistance)
-- 'stability_control' - boolean (for driving assistance)
-- 'drive_mode' - text (for performance, e.g., 'eco', 'sport', 'comfort')
-- 'gear' - text (for transmission)
-- 'regenerative_braking' - numeric (for electric vehicles)
-- 'battery_limit' - numeric (for electric vehicles)
-- 'charge_mode' - text (for electric vehicles, e.g., 'standard', 'fast')
-- 'defrost_level' - numeric (for defrosting)
-- 'window_position' - numeric (for power windows)
-- 'sunroof_position' - numeric (for sunroof)
-- 'trunk_position' - numeric (for power trunk)
-- 'hood_position' - numeric (for power hood)
-- 'door_lock_status' - boolean (for door locks)
-- 'child_lock_status' - boolean (for child safety locks)
-- 'bluetooth_device' - text (for connectivity)
-- 'wifi_network' - text (for connectivity)
-- 'phone_pairing' - boolean (for phone connectivity)
-- 'voice_command_language' - text (for voice control settings)
-- 'display_brightness' - numeric (for infotainment display)
-- 'display_mode' - text (for infotainment display, e.g., 'day', 'night', 'auto')
-- 'navigation_zoom' - numeric (for navigation display)
-- 'navigation_view' - text (for navigation display, e.g., '2D', '3D')
-- 'backup_camera_guidelines' - boolean (for backup camera)
-- 'tire_pressure' - numeric (for tire pressure monitoring)
-- 'oil_life' - numeric (for maintenance monitoring)
-- 'wiper_speed' - numeric (for windshield wipers)
-- 'horn_duration' - numeric (for horn control)
-- 'alarm_sensitivity' - numeric (for car alarm)
-- 'remote_start_duration' - numeric (for remote start)
-- 'climate_preconditioning' - boolean (for remote climate control)
-- 'fuel_type' - text (for refueling reminders)
-- 'parking_location' - text (for location services)
-- 'valet_mode' - boolean (for valet parking)
-- 'teen_driver_mode' - boolean (for driver monitoring)
-- 'speed_limit' - numeric (for speed limiting)
-- 'geofence' - text (for location-based alerts)
-- 'diagnostics_check' - text (for vehicle diagnostics)

-- Table: Vehicles
CREATE TABLE Vehicles (
    vehicle_id INT PRIMARY KEY AUTO_INCREMENT,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    vin VARCHAR(17) UNIQUE,
    license_plate VARCHAR(20),
    color VARCHAR(30),
    fuel_type ENUM('Gasoline', 'Diesel', 'Electric', 'Hybrid', 'Hydrogen') DEFAULT 'Gasoline'
);

-- Table: Users
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20),
    preferred_language VARCHAR(10) DEFAULT 'en',
    timezone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: UserVehicles (for multi-vehicle users)
CREATE TABLE UserVehicles (
    user_id INT,
    vehicle_id INT,
    is_primary BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (user_id, vehicle_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
);

-- Table: CommandHistory
CREATE TABLE CommandHistory (
    history_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    vehicle_id INT,
    command_id INT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN,
    error_message TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id),
    FOREIGN KEY (command_id) REFERENCES Commands(command_id)
);

-- Table: Locations
CREATE TABLE Locations (
    location_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    is_favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Table: Schedules
CREATE TABLE Schedules (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    vehicle_id INT,
    name VARCHAR(100) NOT NULL,
    command_id INT,
    start_time TIME,
    end_time TIME,
    days_of_week SET('Mon','Tue','Wed','Thu','Fri','Sat','Sun'),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id),
    FOREIGN KEY (command_id) REFERENCES Commands(command_id)
);

-- Stored Procedure: Generate Command Text
DELIMITER //

CREATE PROCEDURE GenerateCommandText(IN p_command_id INT)
BEGIN
    DECLARE v_action_name VARCHAR(50);
    DECLARE v_part_name VARCHAR(50);
    DECLARE v_parameter_name VARCHAR(50);
    DECLARE v_parameter_value VARCHAR(255);
    DECLARE v_command_text VARCHAR(255);

    -- Get action_name and part_name
    SELECT a.action_name, p.part_name
    INTO v_action_name, v_part_name
    FROM Commands c
    JOIN Actions a ON c.action_id = a.action_id
    JOIN Parts p ON c.part_id = p.part_id
    WHERE c.command_id = p_command_id;

    -- Start building the command_text
    SET v_command_text = CONCAT(v_action_name, '_', v_part_name);

    -- Check if there's a parameter for this command
    SELECT parameter_name, parameter_value
    INTO v_parameter_name, v_parameter_value
    FROM Parameters
    WHERE command_id = p_command_id
    LIMIT 1;

    -- If there's a parameter, add it to the command_text
    IF v_parameter_name IS NOT NULL THEN
        SET v_command_text = CONCAT(v_command_text, '_', v_parameter_name, '_', v_parameter_value);
    END IF;

    -- Update the command_text in the Commands table
    UPDATE Commands
    SET command_text = v_command_text
    WHERE command_id = p_command_id;
END //

DELIMITER ;

-- Sample data insertions

-- Insert sample actions
INSERT INTO Actions (action_name) VALUES 
('turn_on'), ('turn_off'), ('increase'), ('decrease'), ('set'), ('open'), ('close');

-- Insert sample parts
INSERT INTO Parts (part_name) VALUES 
('headlights'), ('air_conditioner'), ('radio'), ('windows'), ('sunroof');

-- Insert sample commands
INSERT INTO Commands (action_id, part_id, category) VALUES 
(1, 1, 'lighting'), -- turn_on headlights
(2, 1, 'lighting'), -- turn_off headlights
(1, 2, 'climate_control'), -- turn_on air_conditioner
(5, 2, 'climate_control'), -- set air_conditioner
(3, 3, 'audio'), -- increase radio
(6, 4, 'windows_and_doors'), -- open windows
(7, 4, 'windows_and_doors'), -- close windows
(6, 5, 'windows_and_doors'), -- open sunroof
(7, 5, 'windows_and_doors'); -- close sunroof

-- Insert sample parameters
INSERT INTO Parameters (command_id, parameter_name, parameter_type, parameter_value) VALUES 
(4, 'temperature', 'numeric', '72'), -- for 'set air_conditioner'
(5, 'volume', 'numeric', '8'), -- for 'increase radio'
(6, 'position', 'numeric', '100'), -- for 'open windows'
(8, 'position', 'numeric', '50'); -- for 'open sunroof'

-- Generate command_text for all commands
DELIMITER //
CREATE PROCEDURE GenerateAllCommandTexts()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE cmd_id INT;
    DECLARE cur CURSOR FOR SELECT command_id FROM Commands;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO cmd_id;
        IF done THEN
            LEAVE read_loop;
        END IF;
        CALL GenerateCommandText(cmd_id);
    END LOOP;

    CLOSE cur;
END //
DELIMITER ;

-- Call the procedure to generate all command texts
CALL GenerateAllCommandTexts();

-- Insert sample vehicles
INSERT INTO Vehicles (make, model, year, vin, license_plate, color, fuel_type) VALUES 
('Toyota', 'Camry', 2022, '4T1BF1FK5CU123456', 'ABC1234', 'Silver', 'Gasoline'),
('Tesla', 'Model 3', 2023, '5YJ3E1EA1PF123456', 'XYZ9876', 'Red', 'Electric');

-- Insert sample users
INSERT INTO Users (username, password_hash, first_name, last_name, email, phone_number, preferred_language, timezone) VALUES 
('john_doe', 'hashed_password_here', 'John', 'Doe', 'john.doe@example.com', '1234567890', 'en', 'America/New_York'),
('jane_smith', 'another_hashed_password', 'Jane', 'Smith', 'jane.smith@example.com', '9876543210', 'es', 'America/Los_Angeles');

-- Link users to vehicles
INSERT INTO UserVehicles (user_id, vehicle_id, is_primary) VALUES 
(1, 1, TRUE),  -- John Doe's primary vehicle (Toyota Camry)
(1, 2, FALSE), -- John Doe's secondary vehicle (Tesla Model 3)
(2, 2, TRUE);  -- Jane Smith's primary vehicle (Tesla Model 3)

-- Insert sample command history
INSERT INTO CommandHistory (user_id, vehicle_id, command_id, executed_at, success) VALUES 
(1, 1, 1, '2023-05-15 08:30:00', TRUE),  -- John turned on headlights in Camry
(1, 1, 4, '2023-05-15 08:35:00', TRUE),  -- John set AC temperature in Camry
(2, 2, 6, '2023-05-15 09:00:00', TRUE);  -- Jane opened windows in Tesla

-- Insert sample locations
INSERT INTO Locations (user_id, name, address, latitude, longitude, is_favorite) VALUES 
(1, 'Home', '123 Main St, Anytown, USA', 40.7128, -74.0060, TRUE),
(1, 'Work', '456 Office Blvd, Businessville, USA', 40.7589, -73.9851, TRUE),
(2, 'Gym', '789 Fitness Ave, Healthytown, USA', 34.0522, -118.2437, FALSE);

-- Insert sample schedules
INSERT INTO Schedules (user_id, vehicle_id, name, command_id, start_time, days_of_week, is_active) VALUES 
(1, 1, 'Morning Warm-up', 3, '07:30:00', 'Mon,Tue,Wed,Thu,Fri', TRUE),
(2, 2, 'Evening Cool-down', 4, '18:00:00', 'Mon,Tue,Wed,Thu,Fri', TRUE);

-- Example queries

-- Get all commands for a specific vehicle
SELECT c.command_text, c.category
FROM Commands c
JOIN UserVehicles uv ON uv.vehicle_id = 1  -- Change this to the desired vehicle_id
JOIN Actions a ON c.action_id = a.action_id
JOIN Parts p ON c.part_id = p.part_id;

-- Get command history for a specific user
SELECT ch.executed_at, c.command_text, v.make, v.model
FROM CommandHistory ch
JOIN Commands c ON ch.command_id = c.command_id
JOIN Vehicles v ON ch.vehicle_id = v.vehicle_id
WHERE ch.user_id = 1  -- Change this to the desired user_id
ORDER BY ch.executed_at DESC;

-- Get active schedules for a specific user
SELECT s.name, c.command_text, v.make, v.model, s.start_time, s.days_of_week
FROM Schedules s
JOIN Commands c ON s.command_id = c.command_id
JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
WHERE s.user_id = 1 AND s.is_active = TRUE;  -- Change this to the desired user_id
```

## NoSQL

## VectorDB