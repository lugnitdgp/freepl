import requests
from BeautifulSoup import BeautifulSoup
import urllib
import json 

def crawl(url):
	while True:
		try:
			print "trying to get URL... ",
			r=requests.get(url)
			print "Got URL!"
			return r.content
		except Exception as e:
			print e
			sleep(2)
			print "Retrying!!"

def give_country_fixture(name,countryid):
    d = {}
    d["pk"] = countryid
    d["model"] = "freepl.teams"
    fields = {"country":name,"flag":"/countries/c"+str(countryid)+".jpg"}
    d["fields"] = fields
    return d

def give_player_fixture(firstname,lastname,countryid,playerid):
    d={}
    d["pk"] = playerid
    d["model"] = "freepl.players"	  
    fields = {}
    fields["firstname"] = firstname
    fields["lastname"] = lastname
    fields["country"] = countryid
    fields["netperformance"] = 0
    fields["role"] = 'allround'
    fields["price"] = 0
    d["fields"] = fields
    return d

l = []
playerid = 1
countryid = 1
player_list=[]
i=1
BASE_URL = 'http://www.espncricinfo.com/'
mother_url = 'http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/series/509587.html'
url_list = []

all_teams_soup = BeautifulSoup(crawl(mother_url))

#print all_teams_soup.find("a",{"href":"/icc-cricket-world-cup-2015/content/squad?object=509587"}).findNext("div")
urls_for_teams = all_teams_soup.find("a",{"href":"/icc-cricket-world-cup-2015/content/squad?object=509587"}).findNext("div").findAll("li",{"class":"sub_nav_item"})

urls_for_teams = urls_for_teams[10:]
for url in urls_for_teams:
    #Adding the country!
    countryname = url.find("a").text
    l.append(give_country_fixture(countryname,countryid))
    squad_url = BASE_URL+url.find("a")["href"]
    parsed_squad = BeautifulSoup(crawl(squad_url))
    #print parsed_squad
    allplayers = parsed_squad.find("div",{"role":"main"}).findAll("li")

    #Adding the players!
    for player in allplayers:
	name = player.find("h3").find("a").text
	tm = name.split(" ")
	try:
	    image = player.find("img")
	    image_fetch_url = BASE_URL+image["src"]
	    urllib.urlretrieve(image_fetch_url,"pics/"+str(str(playerid)+".jpg"))
	except:
	    print "Could not fetch image for ",tm

	if len(tm)==1:
	    tm.append("")
	l.append(give_player_fixture(tm[0],tm[1],countryid,playerid))
	print playerid,tm[0],tm[1],countryname
	playerid+=1
    countryid+=1

#Converting the dict l into json!
f = open('data.json',"w+")
f.write(json.dumps(l))
f.close()
"""
	file.write(str(pid))
		file.write(",")
		#pid+=1
		#nametext=name.find('a').text
		lst=name.split(' ')
		print lst
		file.write(str(str(lst[0])+","))
		if(1<len(lst)):
			file.write(str(lst[1]))
		file.write(str(","+str(i)+"\n"))
		file.write("\n")
		urllib.urlretrieve(image_fetch_url,"media/playerimages/"+str(str(pid)+"jpg"))
		pid+=1
	file.close()
    #Adding in all the players!
    for 
url_list=["http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/814789.html","http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/819741.html","http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/816431.html","http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/812413.html","http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/817409.html","http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/816765.html","http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/818117.html","http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/817901.html","http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/818887.html","http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/817889.html","http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/817899.html","http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/819825.html","http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/819743.html","http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/817903.html"]

countryid = 1
playerid = 1
for url in url_list:
	
	html = crawl(url)
	print "Page crawled."
	parsed_html = BeautifulSoup(html)
	#pics=parsed_html.findAll("div",{ "class" : "large-7 medium-7 small-7 columns" })
	allplayers = parsed_html.find("div",{"role":"main"}).findAll("li")
	file=open("player1.csv","a")
	for player in allplayers:
		image = player.find("img")
		base_url="http://www.espncricinfo.com/"
		image_fetch_url = base_url+image["src"]
		name = player.find("h3").find("a").text
		
		print image
		
		left="src=\""
		right="\" alt="
		arg = re.search('%s(.*)%s' % (left, right), image)
		imgsrc=urlify(base_url,arg)
		print imgsrc
		
		file.write(str(pid))
		file.write(",")
		#pid+=1
		#nametext=name.find('a').text
		lst=name.split(' ')
		print lst
		file.write(str(str(lst[0])+","))
		if(1<len(lst)):
			file.write(str(lst[1]))
		file.write(str(","+str(i)+"\n"))
		file.write("\n")
		urllib.urlretrieve(image_fetch_url,str(str(pid)+"jpg"))
		pid+=1
	file.close()
	i+=1
"""