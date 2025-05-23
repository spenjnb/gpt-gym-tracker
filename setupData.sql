-- USERS
INSERT INTO users (username, email, creation_date) VALUES
  ('alice', 'alice@example.com', '2025-01-10'),
  ('bob',   'bob@example.net',   '2025-02-14'),
  ('carol', 'carol@fitness.io',  '2025-03-01'),
  ('dave', 'dave@nowhere.com', '2025-05-10');

-- LOCATIONS
INSERT INTO location (gym_name, address) VALUES
  ('Peak Performance', '123 Summit Ave'),
  ('Downtown Gym',     '456 City Blvd'),
  ('Fitness Factory',  '789 Industrial Rd'),
  ('Health Hub',      '101 Wellness Way'),
  ('Active Life',     '202 Vitality St');

-- WORKOUTS
INSERT INTO workout (workout_date, duration_minutes, location_id, user_id) VALUES
  ('2025-05-01', 60, 1, 1),
  ('2025-05-03', 45, 2, 2),
  ('2025-05-05', 30, NULL, 3),
  ('2025-05-06', 50, 1, 1),
  ('2025-05-07', 40, 2, 1),
  ('2025-04-01', 60, 1, 2),
  ('2025-05-08', 30, 2, 2);

-- EXERCISE TYPES
INSERT INTO exercise_type (name, muscle_group) VALUES
  ('Bench Press', 'Chest'),
  ('Squat',       'Legs'),
  ('Deadlift',    'Back'),
  ('Pull-up',     'Back'),
  ('Push-up',     'Chest'),
  ('Lunge',       'Legs'),
  ('Plank',       'Core'),
  ('Bicep Curl',  'Arms');

-- EXERCISES
INSERT INTO exercise (workout_id, type_id, sets, reps, weight) VALUES
  (1, 1, 3, 10,  135.0),
  (1, 2, 3, 8,   185.0),
  (2, 3, 4, 6,   225.0),
  (3, 2, 2, 12,  155.0);

-- PROGRAMS
INSERT INTO program (name, description) VALUES
  ('Strength Builder', '4-week linear strength progression'),
  ('Cardio Blast',    'High-intensity interval training');

-- WORKOUT ↔ PROGRAM
INSERT INTO workout_program (workout_id, program_id) VALUES
  (1, 1),
  (2, 1),
  (3, 2);

-- PROGRESS METRICS
INSERT INTO progress_metric (user_id, weight_body, body_fat, metric_date) VALUES
  (1,  155.5, 18.2, '2025-04-01'),
  (2,  180.0, 22.5, '2025-04-15'),
  (2, 182.0, 23.0, '2025-05-10'),
  (3,  140.2, 16.8, '2025-05-01');