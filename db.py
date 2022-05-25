from utils.config import *
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

def create_db():
    #Cambiar formatos (featuring Engineering)
    df1 = pd.read_csv("data/dataset.csv", index_col=0).reset_index().rename(columns={"index":"consec"})
    df1["consec"] = df1["consec"] + 1
    print(df1.info())
    
    df2 = pd.read_csv("data/respuestas.csv", index_col=0)
    print(df2.info())
    #Conectar AWS RDS
    db = pymysql.connect(host = host,
                        user = username,
                        password = password,
                        cursorclass = pymysql.cursors.DictCursor
    )
    cursor = db.cursor()

    #Eliminar DATABASE
    drop_db = '''DROP DATABASE respuestas_openai'''
    try:
        cursor.execute(drop_db)
    except Exception as e:
        print(e)

    #Crear DATABASE
    create_db = f'''CREATE DATABASE respuestas_openai'''
    cursor.execute(create_db)

    #Usar DATABASE
    cursor.connection.commit()
    use_db = '''USE respuestas_openai'''
    cursor.execute(use_db)

    #Crear tabla DATABASE
    create_table1 = "CREATE TABLE RESPUESTAS (etiqueta int PRIMARY KEY AUTO_INCREMENT, respuesta varchar(400))"
    cursor.execute(create_table1)   
    
    

    #Insertar df a la Base de Datos
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(user = username, pw = password, host = host, db = 'respuestas_openai'))
    df2.to_sql(name='RESPUESTAS', con=engine, if_exists= 'append', index=False)
    
    create_table2 = "CREATE TABLE OPENAI (consec int PRIMARY KEY AUTO_INCREMENT, texto varchar(300), etiqueta int, FOREIGN KEY(etiqueta) REFERENCES RESPUESTAS(etiqueta))"
    cursor.execute(create_table2) 
    df1.to_sql(name='OPENAI', con=engine, if_exists= 'append', index=False)
    

    sql1 = '''SELECT * FROM RESPUESTAS '''
    sql2 = '''SELECT * FROM OPENAI'''
    cursor.execute(sql1)    
    mi_lista1 = cursor.fetchall()
    cursor.execute(sql2)
    mi_lista2 = cursor.fetchall()
    print(mi_lista1, mi_lista2)
    db.commit()
    db.close()
    
    return "DB Creada"

create_db()
def sql_query(table_name): 
    query = f'''
    SELECT * 
    FROM {table_name}
    '''
    db = pymysql.connect(host = host,
                        user = username,
                        password = password,
                        cursorclass = pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    
    cursor.connection.commit()
    use_db = '''USE respuestas_openai'''
    cursor.execute(use_db)
        
    # Ejecuta la query
    cursor.execute(query)

    # Almacena los datos de la query 
    ans = cursor.fetchall()

    # Obtenemos los nombres de las columnas de la tabla
    names = [description[0] for description in cursor.description]
    db.close()
    return pd.DataFrame(ans,columns=names)

print(sql_query("RESPUESTAS"))
print(sql_query("OPENAI"))