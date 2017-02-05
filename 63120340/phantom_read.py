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
    conn1.query("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED") ######################## REŠITEV SEARIALIZABLE (AMPAK TUDI REPEATABLE READ V VEČINI PRIMEROV DELA)
    
    print "Začetno stanje ( Preiskave KZZ 57398)"
    conn1.query("SELECT * FROM Preiskava WHERE KZZ = 500587")
    tabela(conn1.use_result())


    time.sleep(8)
    print "Phantom read (Preiskave KZZ 57398)"
    conn1.query("SELECT * FROM Preiskava WHERE KZZ = 500587")
    tabela(conn1.use_result())
    print 'TRANSACTION 1 COMMIT'
    conn1.query("COMMIT")

    return
    
    
def tr2():
  conn2 = mdb.connect('127.0.0.1', 'root', 'root', 'tup')

  #cu2.execute('SET TRANSACTION ISOLATION LEVEL READ COMMITTED')
  #conn2.query("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")

  time.sleep(4)
  conn2.autocommit(False)
  print 'TRANSACTION 2 STARTED'
  conn2.query("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")

  print "INSERT INTO Preiskava ..."
  conn2.query("INSERT INTO Preiskava (IdPreiskave, IdObravnave, SifraPredmetaPreiskave, IdOddelka, KZZ, ZacetekPreiskave, Vrednost) VALUES (9999999, 16044, 'S-CK-MB, aktivnost', 2304, 500587, '2017-01-01 12:00:00', 0)")  
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