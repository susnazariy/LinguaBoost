create or replace function check_duplicate_application()
returns trigger as $$
begin
    if exists (
        select 1 from student_applications
        where course_id = new.course_id
          and student_id = new.student_id
          and application_status in ('Підтверджено', 'В обробці')
    ) then
        raise exception 'Помилка: студент вже має заявку на цей курс зі статусом підтверджено або в обробці';
    end if;
    return new;
end;
$$ language plpgsql;

create trigger prevent_duplicate_application
before insert on student_applications
for each row
execute function check_duplicate_application();
