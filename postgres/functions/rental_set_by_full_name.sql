CREATE OR REPLACE FUNCTION guild.rental_set_by_full_name(
	v_game_name character varying,
	v_full_name character varying)
    RETURNS TABLE(result boolean) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
	t_id_game bigint;
	t_id_user bigint;
	t_rental int;
BEGIN 
SELECT COUNT(*) INTO t_rental
FROM guild.users_games gug
INNER JOIN guild.users gu ON gug.user_id = gu.id
INNER JOIN guild.games gg ON gug.game_id = gg.id
WHERE gu.name || ' ' || gu.surname || '(' || gu.nickname || ')' = v_full_name and gg.name = v_game_name and gug.restitution_ts IS NULL;
SELECT gg.id, gu.id INTO t_id_game, t_id_user
FROM guild.users_games gug
INNER JOIN guild.users gu ON gug.user_id = gu.id
INNER JOIN guild.games gg ON gug.game_id = gg.id
WHERE gu.name || ' ' || gu.surname || '(' || gu.nickname || ')' = v_full_name and gg.name = v_game_name and gug.restitution_ts IS NULL
LIMIT 1;
CASE
	WHEN t_rental = 1 THEN
		UPDATE guild.users_games
		SET restitution_ts = NOW()
		WHERE game_id = t_id_game and user_id = t_id_user;
	ELSE
END CASE;
RETURN QUERY (
	SELECT COUNT(*) = 0 and t_rental = 1
	FROM guild.users_games gug
	INNER JOIN guild.users gu ON gug.user_id = gu.id
	INNER JOIN guild.games gg ON gug.game_id = gg.id
	WHERE gu.name || ' ' || gu.surname || '(' || gu.nickname || ')' = v_full_name and gg.name = v_game_name and gug.restitution_ts IS NULL
);
END;
$BODY$;

ALTER FUNCTION guild.rental_set_by_full_name(character varying, character varying)
    OWNER TO postgres;
