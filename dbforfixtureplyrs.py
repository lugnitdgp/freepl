import xlrd
import MySQLdb
import sys
#fgff
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
query = """INSERT INTO freepl_cricketplayer (playerid, firstname, lastname, country, role, netperformance, price) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
#print query

# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for r in range(1, sheet.nrows):
      playerid  = sheet.cell(r,0).value
      firstname = sheet.cell(r,1).value
      lastname  = sheet.cell(r,2).value
      country   = sheet.cell(r,3).value
      netperformance  = sheet.cell(r,4).value
      role  = sheet.cell(r,5).value
      price = sheet.cell(r,6).value

      # Assign values from each row
      values = (playerid, firstname, lastname, country, role, netperformance, price)

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


