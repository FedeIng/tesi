CREATE OR REPLACE FUNCTION guild.free_games_get(
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
	SELECT name
	FROM guild.games gg
	WHERE gg.number > (
		SELECT COUNT(*)
		FROM guild.users_games gug
		WHERE gg.id = gug.game_id and gug.restitution_ts IS NULL
	)
) as result);
END;
$BODY$;

ALTER FUNCTION guild.free_games_get()
    OWNER TO postgres;