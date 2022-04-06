import psycopg2

def db_connection():
    conn = psycopg2.connect(
        host = 'localhost',
        port = 5432,
        database = 'db_blog',
        user = 'pdt',
        password = 'pdt'
    )
    
    return conn