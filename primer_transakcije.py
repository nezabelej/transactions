# -*- coding: utf-8 -*-

import MySQLdb as mdb
import time
import threading

def novaDiagnoza():
  conn1 = mdb.connect('127.0.0.1', 'root', 'root', 'test')

  conn1.autocommit(False)

  print "Zapis diagnoze (brez stevilke obravnave)"
  conn1.query("INSERT INTO Diagnoza (IdObravnave, StevilkaDiagnoze, CasDiagnoze, ICD, ICD_SI) VALUES (10000, NULL, NOW(), 'R70', 'R70')")
  idDiagnoze = conn1.insert_id()
  conn1.commit()

  conn1.query("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
  print "Izracun naslednje stevilke obravnave"
  conn1.query("SELECT (MAX(StevilkaDiagnoze) + 1) as naslednjaStevilka FROM Diagnoza WHERE IdObravnave = 10000 FOR UPDATE")
  row = conn1.use_result().fetch_row(how=1)

  stevilkaObravnave = row[0]['naslednjaStevilka']

  time.sleep(5)
  conn1.query("UPDATE Diagnoza SET StevilkaDiagnoze = " + str(stevilkaObravnave) + " WHERE IdDiagnoze = " + str(idDiagnoze))
  print "Posodobitev prej zapisane diagnoze"
  conn1.commit()

  return

def novaDiagnozaFantomskoBranje():
  conn1 = mdb.connect('127.0.0.1', 'root', 'root', 'test')

  conn1.autocommit(False)

  print "Zapis diagnoze (brez stevilke obravnave)"
  conn1.query("INSERT INTO Diagnoza (IdObravnave, StevilkaDiagnoze, CasDiagnoze, ICD, ICD_SI) VALUES (10000, NULL, NOW(), 'R73', 'R73')")
  idDiagnoze = conn1.insert_id()
  conn1.commit()

  conn1.query("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
  print "Izracun naslednje stevilke obravnave"
  conn1.query("SELECT (MAX(StevilkaDiagnoze) + 1) as naslednjaStevilka FROM Diagnoza WHERE IdObravnave = 10000 FOR UPDATE")
  row = conn1.use_result().fetch_row(how=1)

  stevilkaObravnave = row[0]['naslednjaStevilka']

  time.sleep(5)
  conn1.query("UPDATE Diagnoza SET StevilkaDiagnoze = " + str(stevilkaObravnave) + " WHERE IdDiagnoze = " + str(idDiagnoze))
  print "Posodobitev prej zapisane diagnoze"
  conn1.commit()

  return


t1 = threading.Thread(target=novaDiagnoza)
t2 = threading.Thread(target=novaDiagnozaFantomskoBranje)

t1.start()
t2.start()

while threading.activeCount() > 1:
        time.sleep(1)





