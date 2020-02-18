create table sketch.model_evaluation(
id SERIAL PRIMARY KEY,
model_name VARCHAR not null,
time_stamp TIMESTAMP not null,
user_name VARCHAR not null,
metric VARCHAR not null,
value FLOAT not null);

CREATE SEQUENCE sketch.model_sequence
  start 1
  increment 1;
