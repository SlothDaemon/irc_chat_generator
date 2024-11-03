# Introduction
This Python script exists to make writing "IRC chat logs" for worldbuilding purposes easier. One of my players is greatly anticipating being a hacker and exposing chat logs, so I invented this way to be able to world build and, of course, create saucy secrets for that hacker character to blackmail corpos with.

# How it works
Clears the terminal and asks the user for two optional inputs:
1. The time the IRC chat takes place in. This is to evoke the illusion
    that these chats were typed on different times. If left empty, it simply takes your current system time stamp. Readers may
    grow suspicious whenn lore dumps that supposedly occurred on different times happened right after one another, though. The timestamps of the chats are is updated live in real time, to
    also simulate the typing speed of the chat participants in accordance
    with your own typing speed.
    
    When prompted, set the timestamp with the following format: `HH:MM:SS`, or for example, `12:44:37`.

2. The list of users that are present in the chat.
    Chat logs usually concern two or more people, unless you want to write a monologue or a diary.
    During writing, you can change which user is typing by typing one of the indicators. 

    When prompted, Register the users as follows:
    ```
    DioBrando, JotaroKujo
    ```

The users are registered as participating, and the chat log begins.
You can now type chat messages as the first registered user. 
Should you wish to change users, 
you can type one of the LEFT_INDICATORS or RIGHT_INDICATORS
and send the message to type as a different user.
(Imagine that the users are sitting around a circular dinner table,
hence 'left' and 'right'.)

Example: 
```
[12:44:37] DioBrando: Oh? You're approaching me?  
[12:44:41] DioBrando: /left  
```

becomes:  
```
[12:44:37] DioBrando: Oh? You're approaching me?  
[12:44:46] JotaroKujo:  
```

Should you wish to start anew, you can clear the chat by typing a CLEAR_INDICATOR:  
```
[12:44:37] DioBrando: Oh? You're approaching me?  
[12:44:50] DioBrando: /clear  
```

Should you wish to stop and save the chat, you may type an EXIT_INDICATOR:  
```
[12:45:01] DioBrando: /exit  
```

The chat is then stored in the same folder the Python script is located in
with a unique file name consisting of the datetime you created the chat on,
and the participating users.

Alternatives for these commands are documented at the top of the script as the indicator constants.

An example IRC chat log is provided in this repository for you to peruse.

Happy typing!