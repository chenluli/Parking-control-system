#user:root, password:password
create database testdasd;
use testdasd;
create table client(client_id int(11), token int(11), i int auto_increment primary key);#客户端信息
create table beacon(pubkey varchar(255), beacon_id int(11), i int auto_increment primary key);#beacon信息
create table result(client_id int(11), result varchar(6));#客户端信息
#存储停车位信息
drop table if exists parking;
create table parking(client_id text,parking_space int,i int auto_increment primary key);
delimiter //
drop procedure if exists wk;
create procedure wk()
begin
declare num int;
set num=1;
while num<4 do
insert into parking(client_id,parking_space) values(null,num);
set num=num+1;
end while;
end //

delimiter ;
call wk();
exit;

