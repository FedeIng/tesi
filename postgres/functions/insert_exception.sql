CREATE OR REPLACE FUNCTION guild.insert_exception(
	v_chat_id bigint,
	v_exception_name character varying,
	v_exception_desc character varying,
	v_exception_code bigint)
    RETURNS TABLE(result boolean) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
	t_count bigint;
BEGIN    
SELECT COUNT(*) INTO t_count
FROM guild.exceptions
WHERE chat_id = v_chat_id and name = v_exception_name and description = v_exception_desc and code = v_exception_code;
INSERT INTO guild.exceptions(chat_id, name, description, code)
	VALUES (v_chat_id, v_exception_name, v_exception_desc, v_exception_code);
RETURN QUERY (
	SELECT COUNT(*) = t_count + 1
	FROM guild.exceptions
	WHERE chat_id = v_chat_id and name = v_exception_name and description = v_exception_desc and code = v_exception_code
);
END;
$BODY$;

ALTER FUNCTION guild.insert_exception(bigint, character varying, character varying, bigint)
    OWNER TO postgres;