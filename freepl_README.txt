The site at present is not styled, but ready with manual entering 
features.

TODO::Styling, putting in certain portions in the template, and then 
automating the manual entering as far as possible.

For Admins:
1. Create a database named 'freepl' in your mysql database.

2. Create a file secrets.py in mysite folder, and add DB_USER, DB_PASSWORD,
   DB_NAME, LOCKDOWN_PASSWORD, APP_SECRET.
   Note: App secret can be generated, or create a dummy django project, and
	 copy the app secret here.
   e.g.
   DB_NAME = 'xyz'
   DB_USER = 'me'
   LOCKDOWN_PASSWORD = 'pass'
   APP_SECRET = 'sjfhsfjksdfsdfsdf'
   DB_PASSWORD = 'password'

3. Now do, 'python manage.py syncdb', this will create the necessary tables 
   in the database from the django models.
   
   You would be prompted to add an admin user, this would be your username
   and password, for administering. DO NOT DISCLOSE IT to anyone.

4. Create an .xls file as given in the repo, and place it at the same place,
   for the player list.

5. Now, edit the countries list as given in the make_json.py file, if needed,
   and MAINTAIN uniformity while entering the country names.

6. Now run 'python make_json.py'.

7. Then run 'python manage.py loaddata data.json'. This will add the initial
   player database.

8. Now, log in to the admin panel, by going to the url <your_domain>/admin/.

9. Create the fixtures.

   There are 4 possible states for a fixture.

   State 1 -> locked - False, active - False => The fixture won't be visible to anyone.
   State 2 -> locked - False, active - True => The fixture would be active and the users,
                                               can form their teams.
   State 3 -> locked - True, active - False => The match is on, and users cannot be made.
   State 4 -> locked - True, active - False => The match is over and the scores need will be published.
   
   I. Administering a particular fixture (Follow the steps in order).
      i. Create a fixture.
      ii. Put the fixture to State 2, when you want to allow the users to form their teams.
      iii. Put the fixture to State 3, when you want to stop the users from making any team.
      iv. Put the fixture to State 4, when the match is over.
	  a. Manually enter the stats of each player in the 'Playerstats' model one by one.
	  b. Run the filter, on the right hand side to display the stats for the particular fixture.
	  c. Select all Playerstats, after the filtering and run the action 'Playerstatsupdate'. This will evaluate the 
	     'funscore' or the fantasy points, for each player for the particular fixture.
	  d. Go to 'Fixtureteams' model. Run the filter as you did in step (b.) and then Select all the filtered
	     Fixtureteams, and run the action 'Fixtureteamsscoreupdate', this will update the fantasy points, for each
	     team made by the users.
	  e. Now, Go to Users model in the freepl section( Not the Auth section). Select all players on each page, and
	     run the action 'Cumulativescoreupdate'. This will update the cumulative score of each user over the fixtures.
	  f. Sit back and chill, and prepare for the next fixture.

Note: Admin cannot play the game with the superuser created in step 3, create a normal user by registering
      yourself :P.

Note: The rules for score calculation, is in the function calculate_fun_score, in freepl/admin.py


Ping me if you find any bugs, or face any problems in setting up.
