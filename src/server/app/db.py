import MySQLdb


def connectDb():
    db = MySQLdb.connect(
        host='mysql',
        user='root',
        passwd='hinhct',
        db='howtospeak',
        charset='utf8',
        use_unicode=True)
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
    print(sql)
    rows = []
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()
    return rows


def get_first_data_table(table,columns, where, groupBy, having, orderBy):
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
    print(sql)
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        print(row)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return None
    finally:
        db.close()
    return row



# DELETE FROM table_name WHERE condition;

def delete(table, condition):
    db = connectDb()
    cursor = connectCursor(db)
    sql = "DELETE FROM %s WHERE %s" % (table, condition)
    print (sql)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return False
    finally:
        db.close()
    return True


def truncated(table):
    db = connectDb()
    cursor = connectCursor(db)
    sql = "TRUNCATE TABLE %s" % table
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return False
    finally:
        db.close()
    return True
