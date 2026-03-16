-- Copied from https://stackoverflow.com/a/45079738/4849865
CREATE OR REPLACE FUNCTION notify_person_updated()
RETURNS TRIGGER LANGUAGE plpgsql as $$
declare
    payload text;
begin
    payload:= (SELECT COUNT(*) FROM person)::int;
    perform pg_notify('person_updated', payload);
    return null;
end $$;


CREATE TRIGGER person_table_insert
    AFTER INSERT ON person
    EXECUTE PROCEDURE notify_person_updated();

CREATE TRIGGER person_table_update
    AFTER UPDATE ON person
    EXECUTE PROCEDURE notify_person_updated();

CREATE TRIGGER person_table_delete
    AFTER DELETE ON person
    EXECUTE PROCEDURE notify_person_updated();

CREATE TRIGGER person_table_truncate
    AFTER TRUNCATE ON person
    EXECUTE PROCEDURE notify_person_updated();