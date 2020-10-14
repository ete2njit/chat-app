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
8. `cd` into `project2-m1-ete2` and make a new file called `sql.env` and add `DATABASE_URL=` into it 
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







Known Problems: 

Currently, I distinguish users by their names only. I already have the database set up to store a third element, some kind of key, but for the sake of time I decided
against using this key to distinguish users better. As such, any set of people in the chat with the same name (which can happen, I did not set a check for this as
I should ultimately have better user identification once OAuth comes in) will see all messages from individuals with the same name on the right of the screen, as those messages
are interpreted to be their own due to the names being the same. If I had more time, I could have already used the third element in my database to set a key based on 
the socketID or a combination of name and socketID to make user identification unique. This will have the issue of no persistence, however, as a user logging back in
(probably) has a different sid than the sessions before.

Another issue currently is in the chatbot. At the moment, the chat bot can only return one message per call, which is an issue in the 'joke' api call, and is generally not scalable.
With more time, I would rewrite the chatbot to not return a message, but instead return an array of message objects, which my app.py uses to socketio.emit. Currently, my app.py 
just gets a single string from my chatbot and packs it into a message itself. I would like to rewrite this, in the future, so the chatbot packages the message itself.

A third, fairly simple issue is in the chatwindow. I have it defaulted to 15 messages, which, for one-liner messages and a screen with the size of my own, is not a problem to display. 
Once the chatlogs height becomes too large, or the chat window too small, however, a scrollbar comes up. That scrollbar does not start fully at the bottom, so the default shown chat logs
are not the most recent. I tried to fix this using something I found here: https://stackoverflow.com/questions/18614301/keep-overflow-div-scrolled-to-bottom-unless-user-scrolls-up
specifically this answer: The trick is to use display: flex; and flex-direction: column-reverse;, but this resulted in my entire chatflow being upside down, and the most recent 
messages being at the top. So instead of flipping the scrollbar, it flipped my chat, which was not exactly what I wanted to accomplish.

A large issue that I found far too close to the deadline to deal with it is components seemingly being mounted multiple times. Whenever I send an emit from my server to update the chat, the
amount of times that update is received on a client is double. So when they join, they receive the chatlog once. When a message is sent, they receive the message twice. If another
message is sent, they will receive that 4 times etc exponentially rising. Obviously, this becomes a problem very quickly and makes it impossible to use the chatroom after a few messages. 
I have tried git checkout to a previous build, but even builds from long ago had similar issues, where the number of calls would rise linearly at best. Due to the server having its own debug
output, I can reasonably assume the server does only send the update once, but the clients have an exponentially rising number of socket listeners.


Tech Issues:

I had an issue with my React files not using my CSS at all, and I found the fix for it on stackoverflow: https://stackoverflow.com/questions/42196583/webpack-cant-resolve-style
Following the steps laid out in 'https://webpack.js.org/loaders/css-loader/', I edited the webpack.config.js file, and installed the css-loader, and added the command for it to
the README as seen in 1h) npm install --save-dev css-loader.

One big problem I had was figuring out how to send a message to only a single client, specifically the one who sent the request. This one was really painful to solve, because the
solution, request.sid, is not part of the flask_socket library, even though that is the direct usecase. As a result, I spent a lot of time searching through the flask socketio 
docs, as well as socketio docs in other implementations, until I stumbled upon this post on stackoverflow: https://stackoverflow.com/questions/39423646/flask-socketio-emit-to-specific-user
where I found that the command I was looking for was 'request.sid', at which point finding out it came from flask.request became very simple.

I also ran into some trouble when trying to send only one message to all of the clients, so as to not resend the entire chatlog on every new message. I did not know what the sql iteration
returned exactly, so I figured it was an array of python tuples. When I sent just one of these tuples to my clients, however, they crashed. After some trial and error, I found that the 
reason behind this was the javascript 'concat' function not working like 'append' does, and instead needing an array element. I currently create this array of a single tuple on the server,
but will most likely shift that to clientside.