-- tables of the database

CREATE TABLE IF NOT EXISTS "user" (
  id SERIAL,
  name VARCHAR(30) NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL,
  hashed_password TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS "group" (
  id SERIAL,
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS "group_member" (
  id SERIAL,
  is_creator BOOLEAN NOT NULL,
  user_id INT NOT NULL,
  group_id INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES "user" (id),
  FOREIGN KEY (group_id) REFERENCES "group" (id)
);

CREATE TABLE IF NOT EXISTS "non_group_expense" (
  id SERIAL,
  description VARCHAR(100) NOT NULL,
  amount NUMERIC(8, 2) NOT NULL,
  payor_id INT NOT NULL,
  payee_id INT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (payee_id) REFERENCES "user" (id),
  FOREIGN KEY (payor_id) REFERENCES "user" (id)
);

CREATE TABLE IF NOT EXISTS "group_expense" (
  id SERIAL,
  description VARCHAR(100) NOT NULL,
  amount NUMERIC(8, 2) NOT NULL,
  payor_id INT NOT NULL,
  group_id INT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (payor_id) REFERENCES "user" (id),
  FOREIGN KEY (group_id) REFERENCES "group" (id)
);

CREATE TABLE IF NOT EXISTS "share_of_expense" (
  id SERIAL,
  user_id INT NOT NULL,
  expense_id INT NOT NULL,
  amount NUMERIC(8, 2) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES "user" (id),
  FOREIGN KEY (expense_id) REFERENCES group_expense (id)
);

CREATE TABLE IF NOT EXISTS "payment" (
  id SERIAL,
  payor_id INT NOT NULL,
  payee_id INT NOT NULL,
  amount NUMERIC(8, 2) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (payor_id) REFERENCES "user" (id),
  FOREIGN KEY (payee_id) REFERENCES "user" (id)
);
