drop table if exists posts;
create table posts (
  id integer primary key autoincrement,
  'text' text not null
);