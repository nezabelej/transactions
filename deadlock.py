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
    conn1 = mdb.connect('127.0.0.1', 'root', 'root', 'test')

    print 'TRANSACTION 1 STARTED'
    conn1.autocommit(False)
    conn1.query("LOCK TABLE Preiskava WRITE")
    ############################################################################### REŠITEV 

    conn1.query("SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE")
    #conn1.query("LOCK TABLE Preiskava WRITE")

    conn1.query("SELECT Vrednost FROM Preiskava WHERE IdPreiskave = 57398")
    print "TR1: read(PR_57398) -> " + str(conn1.use_result().fetch_row(how=1)[0]['Vrednost'])

    time.sleep(5)
    print "TR1: write(PR_57398, vrednost + 1)"
    conn1.query("UPDATE Preiskava SET Vrednost = Vrednost + 1 WHERE IdPreiskave = 57398") 

    time.sleep(6)
    print 'TRANSACTION 1 COMMITED!'
    conn1.query("COMMIT")
    conn1.query("SELECT Vrednost FROM Preiskava WHERE IdPreiskave = 57398")
    print "TR1: read(PR_57398) -> " + str(conn1.use_result().fetch_row(how=1)[0]['Vrednost'])
    conn1.close()
    return
    
    
def tr2():
  time.sleep(0.2)
  conn2 = mdb.connect('127.0.0.1', 'root', 'root', 'test')
  #conn2.query("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
  print 'TRANSACTION 2 STARTED'
  conn2.autocommit(False)
  conn2.query("SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE")

  time.sleep(2)


  conn2.query("UPDATE Preiskava SET Vrednost = Vrednost + 1 WHERE IdPreiskave = 57398") 
  print "TR2: write(PR_57398, Vrednost + 1)"
  #print "TR2: updated!"

  time.sleep(2)
  print 'TRANSACTION 2 COMMITED!'
  conn2.query("COMMIT")
  conn2.query("SELECT Vrednost FROM Preiskava WHERE IdPreiskave = 57398")
  print "TR2: read(PR_57398) -> " + str(conn2.use_result().fetch_row(how=1)[0]['Vrednost'])
  conn2.close()

  return
   

t1 = threading.Thread(target=tr1)
t2 = threading.Thread(target=tr2)

t1.start()
t2.start()

while threading.activeCount() > 1:
        time.sleep(1)