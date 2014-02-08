class mainscore:
	def __init__(self):
		print "recvd for score eval"

	def do(self,runsmade,wickets,ballsfaced,fours,sixes,oversbowled,maidenovers,\
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
			
