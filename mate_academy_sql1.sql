-- скрипт використовує мову SQL Oracle
-- можна запускати на платформі https://livesql.oracle.com/next/
with users as
(select 35 as id, 'jsmith@example.com' as email, 'John' as first_name, 'Smith' as last_name, '(123) 456-7890' as phone, 1 as domain_id, 1 as language_id from dual
 union all
 select 47 as id, 'ldoe@example.com' as email, 'Laura' as first_name, 'Doe' as last_name, '(987) 654-3210' as phone, 1 as domain_id, 1 as language_id from dual
 union all
 select 51 as id, 'mbrown@example.com' as email, 'Michael' as first_name, 'Brown' as last_name, '(555) 123-4567' as phone, 4 as domain_id, 5 as language_id from dual
),
leads as (
 select 10 id, 35 user_id, 25 course_id, 
    TO_UTC_TIMESTAMP_TZ('2024-01-14T11:17:29.664+00') created_at, 
    TO_UTC_TIMESTAMP_TZ('2024-02-26T17:28:13.647+00') updated_at, 'LOST' status, 'NO_CONTACT' lost_reason from dual
 union all
 select 16 id, 35 user_id, 38 course_id, 
    TO_UTC_TIMESTAMP_TZ('2024-01-13T18:42:38.671+00') created_at, 
    TO_UTC_TIMESTAMP_TZ('2024-01-30T12:01:44.473+00') updated_at, 'WON' status, null lost_reason from dual
 union all
 select 45 id, 62 user_id, 27 course_id, 
    TO_UTC_TIMESTAMP_TZ('2024-01-12T16:49:15.082+00') created_at, 
    TO_UTC_TIMESTAMP_TZ('2024-02-13T09:13:07.151+00') updated_at, 'NEW' status, null lost_reason from dual
),
domains as (
select 1 id, 'ua' slug, 'Ukraine' country_name, '2023-07-27 09:31:22.147845+00' created_at, '2024-02-26 10:21:53.046+00' updated_at, 't' active from dual
union all
select 3 id, 'pl' slug, 'Poland' country_name, '2023-12-21 09:14:32.8806+00' created_at, '2024-02-15 11:24:51.941+00' updated_at, 'f' active from dual
),
courses as (
select 12 id, 'python_basics' slug, 'MODULE' type, 1 language_id, 3 sort from dual
union all
select 25 id, 'frontend' slug, 'FULL_TIME' type, 1 language_id, 5 sort from dual
union all
select 27 id, 'devops' slug, 'FLEX' type, 1 language_id, 1 sort from dual
)
--Prepare SQL queries to select the next data:
--1.1. The number of created leads per week grouped by course type
/*в таблиці leads немає записів про курс з course_id = 12 тож у підсумку MODULE = 0, 
а в таблиці courses немає запису про курс з id = 38, що є в таблиці leads тож в отриманому результаті для такого модуля немає типу
*/ 
select 
to_char(trunc(l.created_at, 'IW'),'IW') week_num 
,trunc(l.created_at, 'IW') week_day 
,c.type
,count(l.created_at) created_leads
from courses c
full join leads l 
on l.course_id = c.id
group by c.type, to_char(trunc(l.created_at, 'IW'), 'IW'), trunc(l.created_at, 'IW')
order by 1,2;