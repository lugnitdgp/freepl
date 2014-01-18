class mainscore:
	def __init__():
		print "recvd for score eval"
	def do(runsmade,wickets,ballsfaced,fours,sixes,oversbowled,maidenovers,\
	runsgiven,catches,stumpings,runouts,dotsbowled,mom,dnb):
		s1=runsmade
		s2=2*sixes
		if (runsmade==0 and not dnb):
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
		fieldscore=catch*10+stumpings*15+runouts*10
		return (batscore+fieldscore+bowlscore+25*mom)
			
