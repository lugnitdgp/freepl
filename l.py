"""
For converting xls to json fixture
"""

import xlrd
import json 

# Open the workbook and define the worksheet
book = xlrd.open_workbook("cricketplayer.xls")
sheet = book.sheet_by_name("playerlist")

l=[]
for r in range(1, sheet.nrows):
      d = {}
      d["pk"] = r
      d["model"] = "freepl.players"	
      
      fields = {}
      fields["firstname"] = sheet.cell(r,0).value
      fields["lastname"] = sheet.cell(r,1).value
      fields["country"] = int(sheet.cell(r,2).value)
      fields["netperformance"] = int(sheet.cell(r,3).value)
      fields["role"] = sheet.cell(r,4).value
      fields["price"] = int(sheet.cell(r,5).value)
      
      d["fields"] = fields
      l.append(d)
      # Assign values from each row
countries = ["AUS","IND","RSA","WI","SL","NZ","ENG","BAN"]
cnt=1
for i in xrange(1,len(countries)+1):
    d = {}
    d["pk"]=i
    d["model"] = "freepl.teams"
    fields = {"country":countries[i-1]}
    d["fields"] = fields
    l.append(d)
    
f = open('players.json',"w+")
f.write(json.dumps(l))
f.close()