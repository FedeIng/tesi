CREATE OR REPLACE FUNCTION guild.user_rental_set(
	v_telegram_id bigint,
	v_game_name character varying)
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
select gg.id into t_id_game
from guild.games gg
where gg.name = v_game_name
LIMIT 1;
select gu.id into t_id_user
from guild.users gu
where gu.telegram_id = v_telegram_id
LIMIT 1;
select count(*) into t_rental
from guild.users_games gug
where gug.user_id = t_id_user and gug.restitution_ts IS null;
CASE
	WHEN t_rental = 0 and t_id_user IS NOT null AND t_id_game IS NOT null THEN
		INSERT INTO guild.users_games (user_id,game_id)
		VALUES (t_id_user,t_id_game);
	ELSE
END CASE;
RETURN QUERY (SELECT count(*) = 1 and t_rental = 0
				from guild.users_games gug
				where gug.user_id = t_id_user and gug.game_id = t_id_game and gug.restitution_ts IS null
			);
END;
$BODY$;

ALTER FUNCTION guild.user_rental_set(bigint, character varying)
    OWNER TO postgres;
