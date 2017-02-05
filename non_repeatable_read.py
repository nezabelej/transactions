# -*- coding: utf-8 -*-

import MySQLdb as mdb
import time
import threading

def tabela(rez):
    rows = rez.fetch_row(how=1)
    while rows:
        for row in rows:
          print row
        rows = rez.fetch_row(how=1)

def tr1():
    conn1 = mdb.connect('127.0.0.1', 'root', 'root', 'tup')

    conn1.autocommit(False)
    print 'TRANSACTION 1 STARTED'
    conn1.query("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED") ######################## REŠITEV REPEATABLE READ
    
    print "Začetno stanje (Preiskava 57398)"
    conn1.query("SELECT Vrednost FROM Preiskava WHERE IdPreiskave = 57398")
    tabela(conn1.use_result())


    time.sleep(2)
    print "Non-repeatable read (Preiskava 57398)"
    conn1.query("SELECT Vrednost FROM Preiskava WHERE IdPreiskave = 57398")
    tabela(conn1.use_result())
    print 'TRANSACTION 1 COMMIT'
    conn1.query("COMMIT")


    time.sleep(8)
    print "Končno stanje (Preiskava 57398)"
    conn1.query("SELECT Vrednost FROM Preiskava WHERE IdPreiskave = 57398")
    tabela(conn1.use_result())
    conn1.query("COMMIT")
    conn1.close()
    return
    
    
def tr2():
  conn2 = mdb.connect('127.0.0.1', 'root', 'root', 'tup')

  #cu2.execute('SET TRANSACTION ISOLATION LEVEL READ COMMITTED')
  #conn2.query("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")

  time.sleep(1)
  conn2.autocommit(False)
  print 'TRANSACTION 2 STARTED'
  conn2.query("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")

  print "UPDATE Preiskava SET Vrednost = 10 WHERE IdPreiskave = 57398"
  conn2.query("UPDATE Preiskava SET Vrednost = 10 WHERE IdPreiskave = 57398")    
  print 'TRANSACTION 2 COMMIT!'
  conn2.query("COMMIT")
  conn2.close()

  return
   

t1 = threading.Thread(target=tr1)
t2 = threading.Thread(target=tr2)

t1.start()
t2.start()

while threading.activeCount() > 1:
        time.sleep(1)