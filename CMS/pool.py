import pymysql as MYSQL
def ConnectionPooling():
    db=MYSQL.connect(host="localhost",port=3306,user="root",password="123@root",db="cms")
    cmd=db.cursor()
    return db,cmd