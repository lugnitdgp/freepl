def do(runsmade,wickets,ballsfaced,fours,sixes,oversbowled,maidenovers,\
runsgiven,catches,stumpings,runouts,dotsbowled,mom,dnb):
	s1=runsmade
	print "runs score",s1
	s2=2*sixes
	print "sixes points",s2
	s3=int(runsmade/25)*10
	print "milestone bonus",s3
	s4=runsmade-ballsfaced
	print "bat pace bonus",s4
	batscore=s1+s2+s3+s4
	if (runsmade==0 and not dnb):
		batscore-=5
	print batscore
	
	s1=20*wickets
	print "wickets",s1
	s2=dotsbowled
	s3=0
	if wickets>0:
		s3=10*(wickets-1)
	print "wickets extra",s3
	ballsbowled=int(oversbowled)*6+(oversbowled-int(oversbowled))*10
	s4=ballsbowled-runsgiven
	if s4>0:
		s4*=2
	print "bowlpace bonus",s4
	bowlscore=s1+s2+s3+s4
	print "bowlscore",bowlscore
	fieldscore=catches*10+stumpings*15+runouts*10
	return int(batscore+fieldscore+bowlscore+25*mom)

import xlrd
import MySQLdb
import sys

filename=sys.argv[1]
filen=filename.split('.')
# Open the workbook and define the worksheet
try:
	book = xlrd.open_workbook(sys.argv[1])
except:
	print "Invalid scoreboard filename, or the file does not exist."
sheet = book.sheet_by_name("Sheet1")

# Establish a MySQL connection
database = MySQLdb.connect (host="localhost", user = "root", passwd = "123456", db = "mydja")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Create the INSERT INTO sql query
query = """INSERT INTO freepl_fixturecricketplayers (fixtureid, playerid, firstname, lastname, runsmade, wickets, ballsfaced, fours, sixes, oversbowled, maidenovers, runsgiven, catches, stumpings, runouts, dotsbowled, mom, funscore, dnb) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#print query

# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
pids=["p31","p33","p34","p41","p42","p45","p46","p52","p57","p60","p61"]
fixtureid=str(filen[0])
for r in range(1, sheet.nrows):
      playerid  = (sheet.cell(r,1).value)
      firstname =(sheet.cell(r,2).value)
      lastname  =(sheet.cell(r,3).value)
      dnb= (sheet.cell(r,4).value)
      runsmade= (sheet.cell(r,5).value)
      ballsfaced= (sheet.cell(r,6).value)
      fours=(sheet.cell(r,7).value)
      sixes=(sheet.cell(r,8).value)
      oversbowled=( sheet.cell(r,9).value)
      maidenovers= (sheet.cell(r,10).value)
      runsgiven= (sheet.cell(r,11).value)
      wickets= (sheet.cell(r,12).value)
      catches= (sheet.cell(r,13).value)
      stumpings= (sheet.cell(r,14).value)
      runouts= (sheet.cell(r,15).value)
      dotsbowled=(sheet.cell(r,16).value)
      mom=(sheet.cell(r,17).value)
      print runsmade,wickets,ballsfaced,fours,sixes,oversbowled,maidenovers,\
      runsgiven,catches,stumpings,runouts,dotsbowled,mom
      funscore=do(runsmade,wickets,ballsfaced,fours,sixes,oversbowled,maidenovers,\
      runsgiven,catches,stumpings,runouts,dotsbowled,mom,dnb)
      # Assign values from each row
      print firstname,lastname,funscore
      print ""
      print ""
      values = (fixtureid,playerid, firstname, lastname,runsmade,wickets,\
      ballsfaced,fours,sixes,oversbowled,maidenovers,runsgiven,catches,\
      stumpings,runouts,dotsbowled,mom,funscore,dnb)

      # Execute sql Query
      cursor.execute(query, values)

# Close the cursor
cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()

# Print results
print ""
print "All Done! Bye, for now."
print ""
#columns = str(sheet.ncols)
#rows = str(sheet.nrows)
#print "I ust imported " %2B columns %2B " columns and " %2B rows %2B " rows to MySQL!"


