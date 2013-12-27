The site at present is not styled, but ready with manual entering 
features.

TODO::Styling, putting in certain portions in the template, and then 
automating the manual entering as far as possible.

For Admins:
1. First you need to create a superuser, which is simple.
cd to the ../mysite and then "python manage.py createsuperuser <username>"
Then enter in the password and you are done.

2. Now go to localhost:8000/admin in the web browser, and enter in the 
superuser credentials you just created, you will see a list of tables
for the Freepl app.

	**CAUTION**
	a. Cricket players - This is the table for keeping the player data
	with country, role, name etc. which 	
	
	This database needs to be updated first and foremost, without which 
	the app may throw unexpected behaviour, as the error handling is not 
	done, so try not to proceed without updating this.
	
	Manual:- Just serially enter/delete the player details, you need
	not worry about the playerid, that is handled internally.
	
	
	Using a Script:- If you wish to create the database table itself,
	then make sure its of the name "freepl_cricketplayer" has all the columns
	and you need to make sure that player id is of the form "p<integer>".
	The integer should be strictly in increasing order with difference of 1
	at each stage, ie 1,2,3,....
	Also for entering in the "country" details, be sure to maintain uniformity
	it should not be, "Australia" for some and "auSTRalia" for others. 
	This is case sensitive, and 

TODO:: try to make this case-insensitive, and scrape it using a script, automatically
	   from some site like cricinfo. 

	b. Fixturess
	Here you decide the fixtures. Please be careful, that while you choose the
	countries teamA and teamB to be the same as used in the table (a.)
	and don't forget to check the isactive box once you want this to be active 
	in the main site, and leave it thatway after throughout. Dont change it
	any further.
	isover is to be checked in when you are going in for score evaluation.
	Only after checking in for a particular fixture should u proceed to step (b.)

	b. Fixture cricket playerss 	
	Here we enter the performance, of each player either through a script,
	or manually. Calculation of the scores can then be done by choosing
	the action "Update scores of cricket plys" from the admin UI itself.
	
	c. Fixture teamss 	
	Here we update the scores of the teams formed by the users of the 
	fantasy league. This is again simple, just choose the action, 
	"Update scores of fixture teams" from the admin UI. 
	
	e. Fpl users 
	Here you can monitor the scores of all users in freepl, and keep a check
	on those who you think are doing something unfair, though chances are highly 
	low.
	
	To avoid any unexpected results, one must follow, all steps a to e in
	sequence.
	
TODO:: Make the steps a. to e. automated.

I have tried to be as explicit as possible, yet I maybe unclear. Sorry for
any mistakes. Am all ears to suggestions, and bug reports.
