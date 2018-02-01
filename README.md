# chatbot

This project intends to use facebook messenger platform to build a chatbot.
The contorl of chatbot is in bot.py. Run python bot.py for starting the chatbot server.
You would need a file entitled 'password.txt', with first line to be username and second line to be password.

The log is stored in mongoDB. db is chatbot and collections are user and user_history.
user stores user_id 
user_history stores all interaction between user and chatbot in terms of 
(bot_id, current_id, ab_test_id, situation, what user said, timestamp)

current_id is the id shows the index of chatbot(with bot_id)'s question.
