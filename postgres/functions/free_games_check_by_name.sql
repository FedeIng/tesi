CREATE OR REPLACE FUNCTION guild.free_games_check_by_name(
	v_game_name character varying)
    RETURNS TABLE(result bigint) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
BEGIN    
RETURN QUERY (
	SELECT SUM(gg.number)
	FROM guild.games gg
	WHERE gg.name = v_game_name and gg.number > (
		SELECT COUNT(*)
		FROM guild.users_games gug
		WHERE gg.id = gug.game_id and gug.restitution_ts IS NULL
));
END;
$BODY$;

ALTER FUNCTION guild.free_games_check_by_name(character varying)
    OWNER TO postgres;