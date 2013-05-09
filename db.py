import psycopg2, psycopg2.extras


connection_string = ''' dbname=lt user=twisterius password=lister '''
conn = psycopg2.connect(connection_string)
cur=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
