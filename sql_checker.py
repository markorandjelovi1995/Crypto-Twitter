from mysql.connector import connect



def check_db():
    command = "CREATE TABLE keyword_research(user_id CHAR(255) NOT NULL,keyword CHAR(255) NOT NULL, email CHAR(255) NOT NULL)"
    with connect(host='127.0.0.1',user='root',password='511g3HzXwkcu') as connection:
        print(connection)
        show_db_query = "SHOW DATABASES"
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(show_db_query)
            for db in cursor:
                 print(db)
            cursor.execute("USE linzsky")
            cursor.execute(command)

def check_table():

    with connect(host='hellofreelancerbd.mysql.pythonanywhere-services.com',user='hellofreelancerb',password='llllllll') as connection:
        com = "SHOW tables;"
        with connection.cursor(buffered=True) as cursor:
            cursor.execute("USE linzsky")
            cursor.execute(com)
            tb = cursor.fetchall()

            for i in tb:
                print(i)

def show_data():
    with connect(host='',user='root',password='511g3HzXwkcu') as connection:
        com = "SELECT * FROM keyword_research"
        with connection.cursor(buffered=True) as cursor:
            cursor.execute("USE linzsky")
            cursor.execute(com)
            tb = cursor.fetchall()

            for i in tb:
                print(i)

def insert_data():
    with connect(host='127.0.0.1',user='root',password='511g3HzXwkcu') as connection:
        com = "INSERT INTO keyword_research(user_id,keyword,user_email,user_details) VALUES(999,'programmer','example@gmail.com','Null')"
        with connection.cursor(buffered=True) as cursor:
            cursor.execute("USE linzsky")
            cursor.execute(com)
            connection.commit()

def show_columns():
    with connect(host='127.0.0.1',user='root',password='511g3HzXwkcu') as connection:
        com = "SHOW columns FROM keyword_research"
        with connection.cursor(buffered=True) as cursor:
            cursor.execute("USE linzsky")
            cursor.execute(com)
            tb = cursor.fetchall()

            for i in tb:
                print(i)

def delete_columns():
    with connect(host='127.0.0.1',user='root',password='pyking') as connection:
        com = "DELETE FROM keyword_research Where user_id = 999 ;"
        with connection.cursor(buffered=True) as cursor:
            cursor.execute("USE linzsky")
            cursor.execute(com)


#delete_columns()
# #show_columns()
check_table()
# insert_data()
# show_data()
