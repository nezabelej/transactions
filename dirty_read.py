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

    print 'TRANSACTION 1 STARTED'
    conn1.autocommit(False)
    conn1.query("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED") ###################### REŠITEV  READ COMMITED

    print "tr1: read(PR_57398)"
    conn1.query("SELECT Vrednost FROM Preiskava WHERE IdPreiskave = 57398")
    tabela(conn1.use_result())


    time.sleep(2)
    print "tr1: read(PR_57398) ... Dirty read"
    conn1.query("SELECT Vrednost FROM Preiskava WHERE IdPreiskave = 57398")
    vrednost = conn1.use_result().fetch_row(how=1)[0]['Vrednost']

    time.sleep(8)
    print "Zapis z nepotrjeno vrednostjo"
    conn1.query("UPDATE Preiskava SET Vrednost = %d WHERE IdPreiskave = 57398" % (vrednost + 5)) 
    conn1.query("COMMIT")
    conn1.query("SELECT Vrednost FROM Preiskava WHERE IdPreiskave = 57398")
    tabela(conn1.use_result())
    conn1.close()
    return
    
    
def tr2():
  conn2 = mdb.connect('127.0.0.1', 'root', 'root', 'tup')

  #cu2.execute('SET TRANSACTION ISOLATION LEVEL READ COMMITTED')
  #conn2.query("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")

  time.sleep(1)
  print 'TRANSACTION 2 STARTED'
  conn2.autocommit(False)
  conn2.query("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")

  print "UPDATE Preiskava SET Vrednost = 10 WHERE IdPreiskave = 57398"
  conn2.query("UPDATE Preiskava SET Vrednost = 10 WHERE IdPreiskave = 57398") 
  time.sleep(3)
   
  print 'ROLLBACK!'
  conn2.query("ROLLBACK")
  conn2.close()

  return
   

t1 = threading.Thread(target=tr1)
t2 = threading.Thread(target=tr2)

t1.start()
t2.start()

while threading.activeCount() > 1:
        time.sleep(1)