CREATE OR REPLACE FUNCTION guild.game_name_rental_get(
	)
    RETURNS TABLE(result character varying[]) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
BEGIN    
RETURN QUERY (SELECT ARRAY(
		SELECT DISTINCT gg.name as game_name
		  FROM guild.users_games gug
		  INNER JOIN guild.games gg
		  	ON gg.id = gug.game_id AND gug.restitution_ts IS NULL
) as result);
END;
$BODY$;

ALTER FUNCTION guild.game_name_rental_get()
    OWNER TO postgres;
