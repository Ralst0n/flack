# Flack

## Project from Web Programming with Python and JavaScript

Flack is a basic slack clone using Flask and Javascript. A user is prompted to create a display name, which is saved across sessions. This allows the user to create chat channels as long as a channel of that name doesn't already exist as well as enter existing channels to chat in real time with others in the channel thanks to socketio

## Technical information

**application.py** provides:
    *Display name page
    *Channels list page
    *Individual chat channels
    *Create route that redirects to the individual channel page
    *Uses user sessions to keep users identified on the app as well as remember the last channel they were in and takes them right back to it on reopening of the application
    *Implements Flask flash to alert users when they try to go to a page for a channel that doesn't exist, or try to create a channel that already exist.
    *Also provides routes activated on socketio emits for new messages, user entering a chat and user leaving a chat

**main.js**
    Uses web socket emits to communicate real time action with the server and update the users ui with that action. Be it messages submitted into the chat, users joining the chat channel or users leaving the chat channel.


