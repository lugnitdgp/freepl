def do(runsmade,wickets,ballsfaced,fours,sixes,oversbowled,maidenovers,\
runsgiven,catches,stumpings,runouts,dotsbowled,mom):
	s1=runsmade
	s2=2*sixes
	if (runsmade==0):
		s2-=5
	s3=(runsmade/25)*10
	s4=runsmade-ballsfaced
	batscore=s1+s2+s3+s4
	s1=20*wickets
	s2=dotsbowled
	s3=10*(wickets-1)
	s4=1.5*(10*oversbowled-9*int(oversbowled))-runsgiven
	if s4>0:
		s4*=2
	bowlscore=s1+s2+s3+s4
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
query = """INSERT INTO freepl_fixturecricketplayers (fixtureid, playerid, firstname, lastname, runsmade, wickets, ballsfaced, fours, sixes, oversbowled, maidenovers, runsgiven, catches, stumpings, runouts, dotsbowled, mom, funscore) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#print query

# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
fixtureid=str(filen[0])
for r in range(1, sheet.nrows):
      playerid  = (sheet.cell(r,1).value)
      firstname =(sheet.cell(r,2).value)
      lastname  =(sheet.cell(r,3).value)
      runsmade= (sheet.cell(r,4).value)
      wickets= (sheet.cell(r,5).value)
      ballsfaced= (sheet.cell(r,6).value)
      fours=(sheet.cell(r,7).value)
      sixes=(sheet.cell(r,8).value)
      oversbowled=( sheet.cell(r,9).value)
      maidenovers= (sheet.cell(r,10).value)
      runsgiven= (sheet.cell(r,11).value)
      catches= (sheet.cell(r,12).value)
      stumpings= (sheet.cell(r,13).value)
      runouts= (sheet.cell(r,14).value)
      dotsbowled= (sheet.cell(r,15).value)
      mom=(sheet.cell(r,16).value)
      print runsmade,wickets,ballsfaced,fours,sixes,oversbowled,maidenovers,\
      runsgiven,catches,stumpings,runouts,dotsbowled,mom
      funscore=do(runsmade,wickets,ballsfaced,fours,sixes,oversbowled,maidenovers,\
      runsgiven,catches,stumpings,runouts,dotsbowled,mom)
      # Assign values from each row
      values = (fixtureid,playerid, firstname, lastname,runsmade,wickets,\
      ballsfaced,fours,sixes,oversbowled,maidenovers,runsgiven,catches,\
      stumpings,runouts,dotsbowled,mom,funscore)

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


