create table students(
  ID varchar(50),
  first varchar(50) not null,
  last varchar(50) not null,
  year numeric(4,0) not null,
  note varchar(50000),
  primary key(ID)
);

create table visits(
  ID varchar(50),
  visit_date date, --YYYY-MM-DD
  visit_start varchar(50), --HH:MM
  show varchar(3) not null, --If the student shows | yes / no
  topic varchar(100) not null,
  note varchar(10000),
  comments varchar(50000), --student comments
  observations varchar(50000), --observations
  recommendations varchar(50000), --reccomendation
  primary key(ID, visit_date, visit_start),
  foreign key(ID) references students
);
