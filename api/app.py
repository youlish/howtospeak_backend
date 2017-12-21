from flask import Flask
import MySQLdb


def connectDb():
    db = MySQLdb.connect(host='127.0.0.1'
                         , user='root'
                         , passwd=''
                         , db='howtospeak'
                         , charset='utf8'
                         , use_unicode=True)
    return db
def connectCursor(db):

    cursor = db.cursor()
    return cursor

def getDataTable(table,columns, where, groupBy, having, orderBy):
    # open connect Database
    db = connectDb()

    # use method cursor()
    cursor = connectCursor(db)
    sql = """SELECT %(columns)s FROM %(table)s
                    %(where)s
                    %(groupBy)s
                    %(having)s
                    %(orderBy)s""" % \
          {'columns': columns,
           'table': table,
           'where': where,
           'groupBy': groupBy,
           'having': having,
           'orderBy': orderBy
           }
    #print sql
    # print sql
    try:
        # Thuc thi lenh SQL
        cursor.execute(sql)
        rows = cursor.fetchall()
        #print rows
        # Commit cac thay doi vao trong Database
        db.commit()
    except:
        # Rollback trong tinh huong co bat ky error nao
        db.rollback()

    # ngat ket noi voi server
    db.close()
    return rows

app = Flask(__name__)
