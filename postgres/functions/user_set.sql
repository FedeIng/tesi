CREATE OR REPLACE FUNCTION guild.user_set(
	v_telegram_id bigint,
	v_name character varying,
	v_surname character varying,
	v_nickname character varying)
    RETURNS TABLE(result boolean) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
t_user int;
BEGIN
select count(*) into t_user
from guild.users gu
where gu.telegram_id = v_telegram_id;
CASE
	WHEN t_user = 0 THEN
		INSERT INTO guild.users (telegram_id,name,surname,nickname)
		VALUES (v_telegram_id,v_name,v_surname,v_nickname);
	WHEN t_user = 1 THEN
		UPDATE guild.users
		SET name=v_name,surname=v_surname,nickname=v_nickname
		WHERE telegram_id = v_telegram_id;
	ELSE
END CASE;
RETURN QUERY (SELECT count(*) = 1
				from guild.users gu
				where gu.telegram_id = v_telegram_id
			);
END;
$BODY$;

ALTER FUNCTION guild.user_set(bigint, character varying, character varying, character varying)
    OWNER TO postgres;