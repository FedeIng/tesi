CREATE OR REPLACE FUNCTION guild.rental_get(
	)
    RETURNS TABLE(result jsonb[]) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
BEGIN    
RETURN QUERY (SELECT ARRAY(
	SELECT to_jsonb(t)
	FROM (SELECT gg.name as game_name,
		  	gu.name as user_name,
		  	gu.surname as user_surname,
		  	gu.nickname as user_nickname,
		 	gu.telephone as user_telephone,
		  	gu.telegram_id as user_telegram_id,
		  	gs.name as staff_name,
		  	gs.surname as staff_surname,
		  	gs.nickname as staff_nickname,
		 	gs.telephone as staff_telephone,
		  	gs.telegram_id as staff_telegram_id
		  FROM guild.users_games gug
		  INNER JOIN guild.games gg
		  	ON gg.id = gug.game_id
		  INNER JOIN guild.users gu
		  	ON gu.id = gug.user_id
		  LEFT JOIN guild.users gs
		  	ON gs.id = gug.staff_id
		  WHERE gug.restitution_ts IS NULL
		 ) t
) as result);
END;
$BODY$;

ALTER FUNCTION guild.rental_get()
    OWNER TO postgres;