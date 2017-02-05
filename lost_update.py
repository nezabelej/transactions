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
    time.sleep(1)
    conn1 = mdb.connect('127.0.0.1', 'root', 'root', 'test')
    
    print "Start transaction 1"
    conn1.autocommit(False)
    conn1.query("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ") ########################  REŠITEV SERIALIZABLE + FOR UPDATE 

    time.sleep(1)
    print "Začetno stanje (Preiskava 57398)"
    conn1.query("SELECT Vrednost FROM Preiskava WHERE IdPreiskave = 57398")
    vrednost = conn1.use_result().fetch_row(how=1)[0]['Vrednost']
    print "Vrednost " + str(vrednost) 

    time.sleep(1)
    print "TR1: UPDATE Preiskava SET Vrednost = Vrednost + 10 WHERE IdPreiskave = 57398"
    conn1.query("UPDATE Preiskava SET Vrednost = %d WHERE IdPreiskave = 57398" % (vrednost + 10))
    
    time.sleep(1)
    conn1.query("COMMIT")
    print 'TRANSACTION 1 COMMITED!' 
    conn1.query("SELECT Vrednost FROM Preiskava WHERE IdPreiskave = 57398")
    vrednost = conn1.use_result().fetch_row(how=1)[0]['Vrednost']
    print "Vrednost " + str(vrednost) 
    conn1.close()
    return
    
    
def tr2():
  conn2 = mdb.connect('127.0.0.1', 'root', 'root', 'test')
  #conn2.query("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")

  print "Start transaction 2"
  conn2.autocommit(False)
  conn2.query("SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE")

  time.sleep(1)

  conn2.query("SELECT Vrednost FROM Preiskava WHERE IdPreiskave = 57398") ########################  REŠITEV SERIALIZABLE + FOR UPDATE 
  vrednost = conn2.use_result().fetch_row(how=1)[0]['Vrednost']

  time.sleep(1)
  print "TR2: UPDATE Preiskava SET Vrednost = Vrednost + 50 WHERE IdPreiskave = 57398"
  conn2.query("UPDATE Preiskava SET Vrednost = %d WHERE IdPreiskave = 57398" % (vrednost + 50)) 
  time.sleep(1)

  conn2.query("COMMIT")
  print 'TRANSACTION 2 COMMITED!'
  conn2.query("SELECT Vrednost FROM Preiskava WHERE IdPreiskave = 57398")
  vrednost = conn2.use_result().fetch_row(how=1)[0]['Vrednost']
  print "Vrednost " + str(vrednost) 
  conn2.close()

  return
   

t1 = threading.Thread(target=tr1)
t2 = threading.Thread(target=tr2)

t1.start()
t2.start()

while threading.activeCount() > 1:
        time.sleep(1)