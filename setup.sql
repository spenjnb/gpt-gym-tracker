CREATE TABLE users (
  user_id       INTEGER PRIMARY KEY,
  username      TEXT    NOT NULL,
  email         TEXT    NOT NULL,
  creation_date DATE    NOT NULL
);

CREATE TABLE location (
  location_id INTEGER PRIMARY KEY,
  gym_name    TEXT    NOT NULL,
  address     TEXT
);

CREATE TABLE workout (
  workout_id       INTEGER PRIMARY KEY,
  workout_date     DATE    NOT NULL,
  duration_minutes INTEGER NOT NULL,
  location_id      INTEGER,
  user_id          INTEGER NOT NULL,
  FOREIGN KEY(location_id) 
    REFERENCES location(location_id) 
    ON DELETE SET NULL,
  FOREIGN KEY(user_id )    
    REFERENCES users(user_id)     
    ON DELETE CASCADE
);

CREATE TABLE exercise_type (
  type_id      INTEGER PRIMARY KEY,
  name         TEXT    NOT NULL UNIQUE,
  muscle_group TEXT    NOT NULL
);

CREATE TABLE exercise (
  exercise_id INTEGER PRIMARY KEY,
  workout_id  INTEGER NOT NULL,
  type_id     INTEGER NOT NULL,
  sets        INTEGER NOT NULL,
  reps        INTEGER NOT NULL,
  weight      NUMERIC,
  FOREIGN KEY(type_id)    
    REFERENCES exercise_type(type_id) 
    ON DELETE RESTRICT,
  FOREIGN KEY(workout_id) 
    REFERENCES workout(workout_id)     
    ON DELETE CASCADE
);

CREATE TABLE program (
  program_id  INTEGER PRIMARY KEY,
  name        TEXT    NOT NULL,
  description TEXT
);

CREATE TABLE workout_program (
  workout_id INTEGER NOT NULL,
  program_id INTEGER NOT NULL,
  PRIMARY KEY(workout_id, program_id),
  FOREIGN KEY(workout_id) 
    REFERENCES workout(workout_id) 
    ON DELETE CASCADE,
  FOREIGN KEY(program_id) 
    REFERENCES program(program_id) 
    ON DELETE CASCADE
);

CREATE TABLE progress_metric (
  progress_id  INTEGER PRIMARY KEY,
  user_id      INTEGER NOT NULL,
  weight_body  NUMERIC,
  body_fat     NUMERIC,
  metric_date  DATE    NOT NULL,
  FOREIGN KEY(user_id) 
    REFERENCES users(user_id) 
    ON DELETE CASCADE
);