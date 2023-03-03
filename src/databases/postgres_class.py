import datetime
import json

import psycopg2
import psycopg2.extras

from library import send_logs

class PostgresDb:
    class Singleton:

        def __init__(self,host,database,username,password,port,schema):
            self.host=host
            self.database=database
            self.username=username
            self.password=password
            self.port=port
            self.schema=schema

        def run_function(self,name, *params, recursive=True):
            res=None
            conn=None
            try:
                with psycopg2.connect(
                    host=self.host,
                    dbname=self.database,
                    user=self.username,
                    password=self.password,
                    port=self.port) as conn:
                    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                        table_name = '{self.schema}.{name}({",".join([item for item in params])})'
                        cur.execute('select result from %s', (table_name, ))
                        res=cur.fetchone()['result']
            except Exception as error:
                if recursive:
                    self.run_function("insert_exception",str(0),f"'{type(error)}'",f"'{error}'",str(5),recursive=False)
                    send_logs("ERROR",error,0,recursive=True)
            finally:
                if conn is not None:
                    conn.close()
            return res
    
    instance = None
    def __new__(cls,host,database,username,password,port,schema): # __new__ always a classmethod
        if not PostgresDb.instance:
            PostgresDb.instance = PostgresDb.Singleton(host,database,username,password,port,schema)
        return PostgresDb.instance