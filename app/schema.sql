CREATE TABLE IF NOT EXISTS lecture
(
  shortcut string primary key not null,
  name     string             not null,
  ects     integer default 0
);

CREATE TABLE IF NOT EXISTS execution
(
  shortcut string not null references lecture (shortcut),
  semester integer default 1,
  lecturer string,
  primary key (shortcut, semester)
);

CREATE TABLE IF NOT EXISTS exam
(
  shortcut string not null,
  semester integer default 1,
  n_tries  integer default 1,
  mark     integer,
  degree   string  default 'b' check (degree = 'b' or degree = 'm'),
  kind     integer default 0 check (kind >= 0 and kind < 2),
  primary key (shortcut, semester, n_tries),
  foreign key (shortcut, semester) references execution (shortcut, semester)

);