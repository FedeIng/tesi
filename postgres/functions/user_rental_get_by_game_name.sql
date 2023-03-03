CREATE OR REPLACE FUNCTION guild.user_rental_get_by_game_name(
	v_game_name character varying)
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
	FROM (SELECT DISTINCT gu.name as name,
		  	gu.surname as surname,
		  	gu.nickname as nickname,
		    gu.telegram_id as telegram_id,
		    gu.telephone as telephone
		  FROM guild.users_games gug
		  INNER JOIN guild.games gg
		  	ON gg.id = gug.game_id
		  INNER JOIN guild.users gu
		  	ON gu.id = gug.user_id
		  WHERE gg.name=v_game_name and gug.restitution_ts IS NULL
		 ) t
) as result);
END;
$BODY$;

ALTER FUNCTION guild.user_rental_get_by_game_name(character varying)
    OWNER TO postgres;