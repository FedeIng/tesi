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
		FROM guild.users gu
        INNER JOIN guild.users_roles gur ON gu.id = gur.user_id
        INNER JOIN guild.roles gr ON gur.role_id = gr.id
	    WHERE gu.telegram_id = v_telegram_id and gr.name = 'STAFF')
as result);
END;
$BODY$;

ALTER FUNCTION guild.telegram_id_staff_get()
    OWNER TO postgres;