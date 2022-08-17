use Blog;
create table contacts(
sno int primary key auto_increment,
namez varchar (50),
phone_num varchar (12),
msg varchar(200),
dates varchar (30),
email varchar (50)
);
create table posts(
sno int primary key auto_increment,
title varchar (80),
slug varchar (30),
content varchar(2000),
content1 varchar(2000),
content2 varchar(2000),
content3 varchar(2000),
tagline varchar(200),
dates varchar (30),
author varchar (80),
codes varchar (2000),
video varchar (120),
fiveer varchar (2000),
img_file varchar (50),
img1 varchar (50),
img2 varchar (50),
img3 varchar (50)
);
desc posts;
desc contacts;