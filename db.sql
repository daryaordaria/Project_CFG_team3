CREATE DATABASE Sherfood;

USE Sherfood;

CREATE TABLE users (
  userID INT auto_increment PRIMARY KEY,
  username VARCHAR(45) NOT NULL,
  user_password VARCHAR (15) NOT NULL,
  email VARCHAR(45) NOT NULL);
  
  CREATE TABLE annoucements (
  annoucementID INT auto_increment PRIMARY KEY,
  userID INT NOT NULL,
  address VARCHAR(45) NOT NULL,
  latitude Decimal(8,6) NULL,
  longitude Decimal(9,6) NULL,
  pick_up_details VARCHAR (500) NOT NULL, 
  expiration_date DATE NOT NULL,
  vegan INT NULL,
  vegetarian INT NULL,
  kosher INT NULL,
  halal INT NULL,
  glutenfree INT NULL,
  lactosefree INT NULL,
  product_name VARCHAR (30) NOT NULL,
  description VARCHAR (500) NOT NULL,
  INDEX coords (latitude, longitude));
  

-- test records:
INSERT INTO annoucements
VALUES (1,1, "Manchester", 53.480, -2.2426,"Available at 17:00, pick up from store Melcia", "2029-11-19", 1,0,0,0,0,0, "Vegan Wine", "Pinot noir from France");

INSERT INTO users
VALUES (1, 'test_user','password', 'email@email.com');