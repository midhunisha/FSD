/*create database fsd_assign;
use fsd_assign;
create table movies(movie_id int primary key, title varchar(50), release_year int, director_id int, foreign key(director_id) references directors(id));
create table directors(id int primary key, director_name varchar(50));
create table genres(id int primary key, genre_name varchar(50));
alter table movies rename column movie_id to id;
create table movie_genres(movie_id int, genre_id int, foreign key(movie_id) references movies(id), foreign key(genre_id) references genres(id));
insert into movies values(1, "RRR", 2022, 1), (2, "ismart shankar", 2019, 2), (3, "bahubali 2", 2017, 1), (4, "custody", 2023, 3), (5, "acharya", 2022, 4);
insert into directors values(1, "rajamouli"), (2, "puri jagannadh"), (3, "rajamouli"), (4, "koratala siva");
insert into genres values(1, "action"), (2, "romance"), (3, "adventure"), (4, "drama"), (5, "fantasy");
select * from movies;
select * from directors;
select * from genres;
select * from movie_genres;
update directors set  director_name = "venkat prabhu" where id = 3;*/
/* query 1 */ 
select movies.title as movie, directors.director_name from movies join directors on movies.director_id = directors.id;
/* query 2 */
select movies.title as movie, movies.release_year, directors.director_name from movies join directors on movies.director_id = directors.id;
/* query 3 */
select directors.director_name, movies.title as movie from directors left join movies on directors.id = movies.director_id;
/* query 4 */
select directors.director_name, movies.title as movie, movies.release_year from movies right join directors on directors.id = movies.director_id;
/* query 5 */
select movies.title, genres.genre_name from movies join movie_genres on movies.id = movie_genres.movie_id left join genres on movie_genres.movie_id = genres.id ;
/*insert into movie_genres values(1,4), (2,2), (3,5), (4,1), (5,3);
select * from movie_genres;*/
