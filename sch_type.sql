drop table ohschools.ode_type_ref;
CREATE TABLE ohschools.ode_type_ref(
   Typology        VARCHAR(39) NOT NULL PRIMARY KEY
  ,SchType         INTEGER  NOT NULL
  ,RegionType      VARCHAR(9) NOT NULL
  ,StudentPoverty  VARCHAR(10) NOT NULL
);
INSERT INTO ohschools.ode_type_ref(Typology,SchType,RegionType,StudentPoverty) VALUES ('1 - Rural - High Student Poverty',1,'Rural','High');
INSERT INTO ohschools.ode_type_ref(Typology,SchType,RegionType,StudentPoverty) VALUES ('2 - Rural - Average Student Poverty',2,'Rural','Average');
INSERT INTO ohschools.ode_type_ref(Typology,SchType,RegionType,StudentPoverty) VALUES ('3 - Small Town - Low Student Poverty',3,'SmallTown','Low');
INSERT INTO ohschools.ode_type_ref(Typology,SchType,RegionType,StudentPoverty) VALUES ('4 - Small Town - High Student Poverty',4,'SmallTown','High');
INSERT INTO ohschools.ode_type_ref(Typology,SchType,RegionType,StudentPoverty) VALUES ('5 - Suburban - Low Student Poverty',5,'Suburban','Low');
INSERT INTO ohschools.ode_type_ref(Typology,SchType,RegionType,StudentPoverty) VALUES ('6 - Suburban - Very Low Student Poverty',6,'Suburban','Very Low');
INSERT INTO ohschools.ode_type_ref(Typology,SchType,RegionType,StudentPoverty) VALUES ('7 - Urban - High Student Poverty',7,'Urban','High');
INSERT INTO ohschools.ode_type_ref(Typology,SchType,RegionType,StudentPoverty) VALUES ('8 - Urban - Very High Student Poverty',8,'Urban','Very High');
;