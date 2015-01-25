"""
module with some custom tests to be used in the views.py
"""
class istheteamvalid:
	teamAcount=0
	teamBcount=0
	powp=""
	totalprice=0
	plrcount={"bat":0,"bowl":0,"wk":0,"allround":0}
	def __init__(self,ply,rivals,powp):
		self.plrcount["bat"]=0
		self.plrcount["bowl"]=0
		self.plrcount["wk"]=0
		self.plrcount["allround"]=0
		for i in range(0,len(ply)):
			self.totalprice+=ply[i].price
			if ply[i].role=="wk":
				print ply[i].playerid
			self.plrcount[ply[i].role]+=1
			if ply[i].country==rivals[0]:
				self.teamAcount+=1
			if ply[i].country==rivals[1]:
				self.teamBcount+=1
		self.powp=powp

	def evaluate(self):
		print str(self.plrcount["wk"])+"wk"
		if(self.teamAcount+self.teamBcount!=11):
			return "Players don't belong to the countries in the fixture!"
		if(self.teamAcount>6 or self.teamBcount>6):
			return "Maximum players from a single team exceeded!"
		if(self.plrcount["wk"]!=1):
			return "You must keep only one wicketkeeper!"		
		if(self.plrcount["bat"]<4):
			return "Batsmen insufficient!"
		if(self.plrcount["bowl"]<2):
			return "Bowlers insufficient!"
		if(self.plrcount["allround"]<2):
			return "Allrounders insufficient!"
		if self.powp=="":
			return "Power player missing"
		if self.totalprice>850:
			return "Total Budget Exceeded!"
		return "yes"
