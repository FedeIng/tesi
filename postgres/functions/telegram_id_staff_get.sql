CREATE OR REPLACE FUNCTION guild.telegram_id_staff_get(
	)
    RETURNS TABLE(result bigint[]) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
BEGIN    
RETURN QUERY (SELECT ARRAY(
	SELECT telegram_id
	FROM guild.users
	WHERE is_staff = TRUE and telegram_id IS NOT NULL
) as result);
END;
$BODY$;

ALTER FUNCTION guild.telegram_id_staff_get()
    OWNER TO postgres;