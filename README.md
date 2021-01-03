# NewHackNewYear Hackathon
This is a hackathon project made for the MLH New Year New Hack Hackathon (Jan 1 - 3, 2021). Our project is called the HackerGames.

---

Hi and welcome to the HackerGames 

HackerGames is a minipack of games similar to Jackbox. From 1 friend to 100, you 
can bond with folks over this game. 
# Installing and Running the App Info!
To be able to play hangman, you need to install randomwords. In your terminal,
type: pip install RandomWords
Once it's installed, hangman will work. 
TO RUN THIS PROJECT: application.py is the main file that you will run to access
the games as a whole package/project! You do need to have cmu-112-graphics.py in 
the same folder level though. 
Included in this application are 5 games:
1. Snake, charged.
    - AI mode (singleplayer)
2. War, declared.
    - A singleplayer terminal game for those who laptops and computers can't
    handle running intense graphics
3. Pong, deflected.
    - AI mode (singleplayer)
4. Hangman, escaped.
    - A single player graphics game where the computer comes up with a word and 
    you have to try to guess it! 
5. Agario, networked.
    - multiplayer (on same local network)
    The classic Agario game, revisited. We all hate how crowded public servers are.
    There always seems to be a monopoly among the top 3 players and there lacks a time-respecting objective to the game. 
    Play our Agario game where you can connect with those on your local network (you can get a "small-server" experience) and also get put on a 5-minute timer to exercise your mind.
    Can you strategize growth? Note: Do not hit the giant black blobs! If you get too close, it will freeze the game and embarrass you in front of all your friends.  
    
    # Info on running Agario!
    There should be an easy way to connect clients on separate networks, but the most secure way is through creating a Linux server, which we didn't have time to explore this weekend. 
    Those living close to you are special, too! Here are the instructions to running Agario on your local network:
    1. One person needs to run server.py (I ran it using command prompt and I recommend it!). 
    They should see this show up:
    [SERVER] Server Started with local ip "XXX.XXX.X.XXX" (your ip is different)
    [GAME] Setting up level
    [SERVER] Waiting for connections
    2. Have all clients (those who want to play the game. the person running the server can play too) open client.py on Spyder or any IDE and change self.host = "192.168.0.133" to the IP address that showed up in step 1. Save your changes to the client.py file.
    3. Run game.py. I ran it on Spyder. 
    
Connection to New Year Theme: 
    It's finally 2021!!!! After the brutal year that was 2020, we are all 
    excited to turn over a new leaf and go back to normal. But... even if we
    want to pretend like 2020 is behind us, we need to remember that we are 
    still in the middle of a pandemic. A sobering though in this time of fresh
    starts, but important nonetheless. We still have to social distance, but
    social distancing doesn't mean we have to be isolated from our friends! Our 
    application is a whole host of party games that lets you play with multiple
    people (or if they're all busy then you can play against the AI)
