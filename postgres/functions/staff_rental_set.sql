CREATE OR REPLACE FUNCTION guild.staff_rental_set(
	v_staff_telegram_id bigint,
	v_game_name character varying,
	v_name character varying,
	v_surname character varying,
	v_nickname character varying,
	v_telephone character varying)
    RETURNS TABLE(result boolean) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
 t_id_game bigint;
 t_count_user_rental int;
 t_bool_free_game boolean;
 t_number_of_rental_games int;
 t_id_staff bigint;
 t_id_user bigint;
 t_game_number int;
BEGIN  
SELECT id INTO t_id_game
FROM guild.games gg
WHERE gg.name = v_game_name
LIMIT 1;
SELECT id INTO t_id_staff
FROM guild.users gu
WHERE gu.telegram_id = v_staff_telegram_id
LIMIT 1;
SELECT id INTO t_id_user
FROM guild.users gu
WHERE gu.telephone = v_telephone
LIMIT 1;
CASE
	WHEN t_id_user IS NULL THEN
		INSERT INTO guild.users(name, surname, nickname, telephone)
		VALUES (v_name, v_surname, v_nickname, v_telephone);
	ELSE
		UPDATE guild.users
		SET name = COALESCE(v_name,name), surname = COALESCE(v_surname,surname), nickname = COALESCE(nickname,v_nickname)
		WHERE telephone = v_telephone;
END CASE;
SELECT COUNT(*) INTO t_number_of_rental_games
FROM guild.games gg
INNER JOIN guild.users_games gug on gg.id = gug.game_id
WHERE gg.name = v_game_name and gug.restitution_ts IS NULL;
SELECT SUM(gg.number) > t_number_of_rental_games INTO t_bool_free_game
FROM guild.games gg
WHERE name = v_game_name;
SELECT id INTO t_id_user
FROM guild.users gu
WHERE gu.telephone = v_telephone
LIMIT 1;
SELECT COUNT(*) INTO t_count_user_rental
FROM guild.users_games gug
WHERE gug.user_id = t_id_user and gug.restitution_ts IS NULL;
CASE
	WHEN t_bool_free_game and t_count_user_rental = 0 THEN
		INSERT INTO guild.users_games(user_id,game_id,staff_id)
		VALUES(t_id_user,t_id_game,t_id_staff);
	ELSE
END CASE;
RETURN QUERY (
	SELECT count(*) = 1 and t_bool_free_game and t_count_user_rental = 0
	FROM guild.users_games gug
	WHERE gug.user_id = t_id_user and gug.staff_id = t_id_staff and gug.game_id = t_id_game and restitution_ts IS NULL
);
END;
$BODY$;

ALTER FUNCTION guild.staff_rental_set(bigint, character varying, character varying, character varying, character varying, character varying)
    OWNER TO postgres;
