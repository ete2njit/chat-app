# Set up React  
0. `git clone https://github.com/NJIT-CS490/project2-m1-ete2` 
1. Install your stuff!    
  a) `npm install`    
  b) `pip install flask-socketio`    
  c) `pip install eventlet`    
  d) `npm install -g webpack`    
  e) `npm install --save-dev webpack`    
  f) `npm install socket.io-client --save`    
  g) `pip install python-dotenv`
  h) `npm install --save-dev css-loader`
  i) `pip install requests`
  j) `npm install react-google-login`
  k) `npm install react react-dom`
  l) `pip install rfc3987`
If you see any error messages, make sure you use `sudo pip` or `sudo npm`. If it says "pip cannot be found", run `which pip` and use `sudo [path to pip from which pip] install`  
  
# Getting PSQL to work with Python  
  
1. Update yum: `sudo yum update`, and enter yes to all prompts    
2. Upgrade pip: `sudo /usr/local/bin/pip install --upgrade pip`  
3. Get psycopg2: `sudo /usr/local/bin/pip install psycopg2-binary`    
4. Get SQLAlchemy: `sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1`    
  
# Setting up PSQL  
  
1. Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`    
    Enter yes to all prompts.    
2. Initialize PSQL database: `sudo service postgresql initdb`    
3. Start PSQL: `sudo service postgresql start`    
4. Make a new superuser: `sudo -u postgres createuser --superuser $USER`    
    If you get an error saying "could not change directory", that's okay! It worked!  
5. Make a new database: `sudo -u postgres createdb $USER`    
        If you get an error saying "could not change directory", that's okay! It worked!  
6. Make sure your user shows up:    
    a) `psql`    
    b) `\du` look for ec2-user as a user    
    c) `\l` look for ec2-user as a database    
7. Make a new user:    
    a) `psql` (if you already quit out of psql)    
    ## REPLACE THE [VALUES] IN THIS COMMAND! Type this with a new (short) unique password.   
    b) I recommend 4-5 characters - it doesn't have to be very secure. Remember this password!  
        `create user [some_username_here] superuser password '[some_unique_new_password_here]';`    
    c) `\q` to quit out of sql    
8. `cd` into `project2-m2-ete2` and make a new file called `sql.env` and add `DATABASE_URL=` into it 
9. Set database_url equal to "postgresql://{username}:{password}@localhost/postgres", where {username} 
   is the username and {password} is the password from step 7b).
  
  
# Enabling read/write from SQLAlchemy  
There's a special file that you need to enable your db admin password to work for:  
1. Open the file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
If that doesn't work: `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`  
2. Replace all values of `ident` with `md5` in Vim: `:%s/ident/md5/g`  
3. After changing those lines, run `sudo service postgresql restart`  
4. Ensure that `sql.env` has the username/password of the superuser you created!  
5. Run your code!    
  a) `npm run watch`. If prompted to install webpack-cli, type "yes"    
  b) In a new terminal, `python app.py`    
  c) Preview Running Application (might have to clear your cache by doing a hard refresh)    


Technical Issues


A large issue I experienced on the previous milestone, that I only discovered at the very end, was that information was being passed 
at exponential rates. So the first time a client received a message, it receives it once. The next time twice. Then four times etc.
This was not apparent at the time because I used poor style (sorry), which I have since changed, in how I use the State Hook. I first
though that the issue might be caused by socketio.emit, but looking at posts such as this one:
    https://stackoverflow.com/questions/56278700/socket-io-emit-events-twice
Nothing seemed to be similar to the problem I had. After placing a console.log outside the socket.on call in my react components, I found
that in fact the entire component was rendering x-many times per update, with that x also doubling each update. After a while, I found on 
the slack that useEffect has a second argument, and passing a '[]' as my second argument solved my issue. I found this on the bottom of
the documentation of useEffect at 
    https://reactjs.org/docs/hooks-effect.html
Although I did look to the documentation early on, I had overlooked this part initially, as it did not seem to fix my issue due to me 
misunderstanding the actual root cause.


One issue I had occured when I changed my login from a text input to Google login. I used a hook to set the username, and I obviously
only need to call this hook while the client has no name (meaning name = ""). To circumvent unnecessary calls, I put the hook into the
same if statement that controls which screen is displayed, the chat or the login. However, this is apparently illegal, and react was very 
upset with me. The error message, that I was calling fewer hooks than expected, led me to this site:
    https://medium.com/@jonchurch/how-to-fix-react-error-rendered-fewer-hooks-than-expected-e6a378985d3c
Where I learned that react is not a fan of conditional hooks. So now I waste a call to a function that does absolutely nothing for most of 
the clients lifetime.


Another Google login issue I ran into was on heroku. While Google login worked perfectly fine, it always returned the error response of the
Google call. After looking into it a bit more, and double checking that my heroku was an allowed origin uri, I found this link:
    https://stackoverflow.com/questions/42566296/google-api-authentication-not-valid-origin-for-the-client
After finding this, I cleared my cache and Google login on heroku has consistently worked since.

Improvements:

One improvement I would make with more time would be to add more chatbots of different characters. I would store all of them within a handler, 
that I can simply pass the most recent message to, and it figures out what each of the bots respond, and which do not respond at all.

Another improvement would be to separate some of the logic, especially some of the socket stuff, into a different file. I don't personally think
it's too bad or unworkable, but I have definitely put myself into some technical debt over the course of these two milestones. I did get myself 
out of most of it, but I still have concerns about scalability and future-proofedness of, particularly, my backend.