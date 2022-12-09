CREATE OR REPLACE FUNCTION guild.restitution_set(
	v_telephone character varying,
	v_telegram_id bigint)
    RETURNS TABLE(result boolean) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
 t_rental int;
 t_id_rental bigint;
BEGIN  
SELECT COUNT(*) INTO t_rental
FROM guild.users_games gug
INNER JOIN guild.users gu ON gu.id = gug.user_id
WHERE ((gu.telegram_id = v_telegram_id and gu.telephone IS NULL) or (gu.telephone = v_telephone and gu.telegram_id IS NULL)) and gug.restitution_ts IS NULL;
CASE
	WHEN t_rental = 1 THEN
		SELECT gug.id INTO t_id_rental
		FROM guild.users_games gug
		INNER JOIN guild.users gu ON gu.id = gug.user_id
		WHERE ((gu.telegram_id = v_telegram_id and gu.telephone IS NULL) or (gu.telephone = v_telephone and gu.telegram_id IS NULL)) and restitution_ts IS NULL
		LIMIT 1;
		
		UPDATE guild.users_games
		SET restitution_ts = NOW()
		WHERE id = t_id_rental;
	ELSE END CASE;
RETURN QUERY (
	SELECT count(*) = 0 and t_rental = 1
	FROM guild.users_games gug
	INNER JOIN guild.users gu ON gu.id = gug.user_id
	WHERE ((gu.telegram_id = v_telegram_id and gu.telephone IS NULL) or (gu.telephone = v_telephone and gu.telegram_id IS NULL)) and restitution_ts IS NULL
);
END;
$BODY$;

ALTER FUNCTION guild.restitution_set(character varying, bigint)
    OWNER TO postgres;