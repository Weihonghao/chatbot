# -*- coding: UTF-8 -*-

from collections import *
from utils import Params, Config, Topics, Reply

import random


def get_text_from_db():
	params = Params()
	config = Config()
	topics = Topics()

	openning = [["Hi {name}, I\'m {bot_name}.", "I\'m here to help you deal with your stress.", "Can you tell me a little bit about a recent event that makes you stressed?"],
				["Hi {name}, I\'m {bot_name}.", "I\'m here to help you deal with your stress.", "What\'s stressing you out right now?"],
				["Hi {name}, I\'m {bot_name}.", "I\'m here to help you deal with your stress.", "What\'s on your mind?"],
				["Hi {name}, I\'m {bot_name}.", "I\'m here to help you deal with your stress.", "Could you share something that\'s on your mind?"]]
	closing = [["Thank you for sharing with me. I hope I\'ve been able to help.", "Have a nice day!"]]

	dk_check_at_begining = [["Do you want me to come back later?"]]

	bot_texts = defaultdict(dict)
	for i in range(params.BOT_NUM):
		bot_texts[i][config.START_INDEX] = Reply(bot_id=i, in_group_id=config.START_INDEX, texts={topics.GENERAL:[["START_OF_CONVERSATION"]]}, next_id=-1)
		bot_texts[i][config.OPENNING_INDEX] = Reply(bot_id=i, in_group_id=config.OPENNING_INDEX, texts={topics.GENERAL:openning}, next_id=0)
		bot_texts[i][config.CLOSING_INDEX] = Reply(bot_id=i, in_group_id=config.CLOSING_INDEX, texts={topics.GENERAL:closing}, next_id=None)
		bot_texts[i][config.DK_INDEX] = Reply(bot_id=i, in_group_id=config.DK_INDEX, texts={topics.GENERAL:dk_check_at_begining}, next_id=[(config.DEFAULT_DK, config.DK_INDEX), (config.DEFAULT_NO, config.CLOSING_INDEX), (config.DEFAULT_OTHERS, config.CLOSING_INDEX)])


	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Can you share with me more details about this {problem}?"], ["Why is {problem} stressing you out?"]]
	# tmp_text[topics.TRAFFIC] = [["Traffic can really suck.", "How bad is it out there today?"]]
	# tmp_text[topics.TIRED] = [["I see that you seem tired.", "Do you feel you got enough sleep last night?"]]
	# tmp_text[topics.LATE] = [["Sorry to hear that you are late.", "How bad is it?"]]
	# tmp_text[topics.DRIVER] = [["Yeah, there are a lot of aggressive drivers on the road.", "Can you give me more detail why it\'s stressing you out?"]]
	# tmp_text[topics.VEHICLE] = [["Can you give me more details on how your vehicle isn\'t responding?"]]
	bot_texts[0][0] = Reply(bot_id=0, in_group_id=0, texts=tmp_text, next_id=1)
	del tmp_text


	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Hmm I see…", "What are you most worried about happening due to this {problem}?"], ["Sorry to hear that.", "What are you most afraid might happen as a result?"]]
	# tmp_text[topics.TRAFFIC] = [["That\'s unfortunate.", "What do you think the worst possible outcome of this traffic is for you?"]]
	# tmp_text[topics.TIRED] = [["That could be a possible fix.", "What\'s the worst possible outcome of you being tired?"]]
	# tmp_text[topics.LATE] = [["Sorry to hear that.", "Let me ask you something, what is the worst possible outcome of your lateness?"]]
	# tmp_text[topics.DRIVER] = [["Hmm I see…", "What are most afraid might happen as a result of these other drivers?"]]
	# tmp_text[topics.VEHICLE] = [["That\'s unfortunate.", "What\'s the worst possible outcome of this malfunction?"]]
	bot_texts[0][1] = Reply(bot_id=0, in_group_id=1, texts=tmp_text, next_id=[(config.DEFAULT_DK, 7), (config.DEFAULT_OTHERS, 2)])
	del tmp_text

	bot_texts[0][2] = Reply(bot_id=0, in_group_id=2, texts={topics.GENERAL:[["Ok, on a scale of 1 to 10, with 1 being almost impossible, how likely is this scenario?"], ["Alright, on a scale of 1 to 10 (1 impossible, 10 certain), how likely is this scenario?"]]}, next_id= [(('5','6','7', 'five', 'six','seven', '8','9','10', 'eight', 'nine', 'ten', 'likely', 'certain'), 3), (('1','2','3','4','one','two','three','four', 'unlikely', 'impossible'), 4), ((config.DEFAULT_OTHERS, ), 10)])


	bot_texts[0][3] = Reply(bot_id=0, in_group_id=3, texts={topics.GENERAL:[["Alright, in the case that this happens, what could you do to get back on track?"]]}, next_id=[(config.DEFAULT_DK, 6), (config.DEFAULT_NO, 7), (config.DEFAULT_OTHERS, 8)])
	bot_texts[0][4] = Reply(bot_id=0, in_group_id=4, texts={topics.GENERAL:[["So would you agree that this scenario is unlikely?"]]}, next_id=[(config.DEFAULT_YES, 9), (config.DEFAULT_NO, 3), (config.DEFAULT_OTHERS, 8)])
	#bot_texts[0][5] = Reply(bot_id=0, in_group_id=5, texts={topics.GENERAL:[["So would you agree that the worst case situation is unlikely?"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, 9)])

	bot_texts[0][6] = Reply(bot_id=0, in_group_id=6, texts={topics.GENERAL:[["That\'s ok. Could you try and think of a solution?"], ["Is there anything you could do to improve the situation?"]]}, next_id= [(config.DEFAULT_NO, 7), (config.DEFAULT_OTHERS, 8)])
	

	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Maybe spend some time thinking about your problem and possible ways to approach it."]]
	tmp_text[topics.TRAFFIC] = [["Maybe taking a different route or leaving earlier or later could solve your problem?", "Spending some time planning your travel may help you come up with a solution."]]
	tmp_text[topics.TIRED] = [["The easiest solution would be to just go to sleep.", "But if this doesn\'t work for you,", "spend some time thinking of ways to re-organize your schedule to accommodate a good night\'s rest."]]
	tmp_text[topics.LATE] = [["Everyone\'s late once in awhile.", "However, if it is a common occurence maybe think about leaving earlier or taking a quicker route to make your scheduled events on time."]]
	tmp_text[topics.DRIVER] = [["If aggressive driving is a frequent issue, then perhaps taking a different route could solve your problem."]]
	tmp_text[topics.VEHICLE] = [["Taking your vehicle to the dealership or mechanic is usually a good solution", "as they can pinpoint the exact problem with your vehicle and offer you a solution."]]
	bot_texts[0][7] = Reply(bot_id=0, in_group_id=7, texts=tmp_text, next_id=config.CLOSING_INDEX)
	del tmp_text



	bot_texts[0][8] = Reply(bot_id=0, in_group_id=8, texts={topics.GENERAL:[["It seems like you have a plan B", "Just remember even though you cannot control everything, there is a way to get back on your feet."]]}, next_id=config.CLOSING_INDEX)


	tmp_text = {}
	# tmp_text[topics.GENERAL] = [["Glad to hear that.", "Seems like you have things in perspective."],["Glad to hear that.", "Sounds like you have things in perspective."]]
	# tmp_text[topics.TRAFFIC] = [["Glad to hear that.", "Traffic is a nuisance but getting too stressed out by it is often more trouble than it\'s worth."]]
	# tmp_text[topics.TIRED] = [["Seems like you have things in perspective.", "Often, we just need a good night\'s rest or even  a short nap to feel refreshed."]]
	# tmp_text[topics.LATE] = [["Even the best prepared are sometimes late.", "It\'s usually more trouble than it\'s worth to get too worked up about it."]]
	# tmp_text[topics.DRIVER] = [["Sounds like you have things in perspective.", "Aggressive drivers can often be scary to share the road with, but as long as you are driving safely it will usually work out."]]
	# tmp_text[topics.VEHICLE] = [["Glad to hear that.", "Oftentimes, vehicle malfunctions are quick fixes and not worth stressing about."]]
	bot_texts[0][9] = Reply(bot_id=0, in_group_id=9, texts=tmp_text, next_id=config.CLOSING_INDEX)
	del tmp_text


	bot_texts[0][10] = Reply(bot_id=0, in_group_id=10, texts={topics.GENERAL:[["I'm sorry I didn't quite catch that, could you rephrase that?"]]}, next_id= [(('5','6','7', 'five', 'six','seven', '8','9','10', 'eight', 'nine', 'ten', 'likely', 'certain'), 3), (('1','2','3','4','one','two','three','four', 'unlikely', 'impossible'), 4), ((config.DEFAULT_OTHERS, ), 10)])

	#---------------------------------------------------------------------------------------------------------------------------------
	# PROBLEM SOLVING BOT


	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Ok, can you give me more detail about your {problem}"]]
	# tmp_text[topics.TRAFFIC] = [["No one likes traffic.", "How bad is it out there today?"]]
	# tmp_text[topics.TIRED] = [["I see that you seem tired.", "Do you know why?"]]
	# tmp_text[topics.LATE] = [["Why are you late today?"]]
	# tmp_text[topics.DRIVER] = [["Why do these aggressive drivers have you stressed?"]]
	# tmp_text[topics.VEHICLE] = [["Can you give me more details on what you think is wrong with your vehicle?"]]
	bot_texts[1][0] = Reply(bot_id=1, in_group_id=0, texts=tmp_text, next_id=1)
	del tmp_text



	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Hmm, let's think about this together.", "Do you feel this problem is significantly affecting your life?"]]
	# tmp_text[topics.TRAFFIC] = [["Do you feel traffic is significantly affecting your life?"]]
	# tmp_text[topics.TIRED] = [["Are you frequently tired during your normal working hours?", "Is tiredness negatively affecting important aspects of your life?"]]
	# tmp_text[topics.LATE] = [["I see.", "Is lateness a problem that frequently affects your life or is this a one-time thing?"]]
	# tmp_text[topics.DRIVER] = [["Ok, is aggressive driving by others a problem that occurs often enough in your life to worry about it?"]]
	# tmp_text[topics.VEHICLE] = [["Ok, let\'s see how bad this problem is?", "Do you think it will be a quick fix?"]]
	bot_texts[1][1] = Reply(bot_id=1, in_group_id=1, texts=tmp_text, next_id=4)
	del tmp_text

	bot_texts[1][2] = Reply(bot_id=1, in_group_id=2, texts={topics.GENERAL:[["If you could solve this problem, would your life improve?"]]}, next_id=4)
	bot_texts[1][3] = Reply(bot_id=1, in_group_id=3, texts={topics.GENERAL:[["Seems this is not a problem worth worrying about.", " Do you still want to work on it?"], ["In that case, do you feel you\'d still like to spend time working on it?"]]}, next_id=[(config.DEFAULT_NO, config.CLOSING_INDEX), (config.DEFAULT_OTHERS, 4)])
	

	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Have you ever dealt with this problem or something similar before?"]]
	# tmp_text[topics.TRAFFIC] = [["Was there an effective way you coped with traffic before?"]]
	# tmp_text[topics.TIRED] = [["How have you coped with being tired in the past?"]]
	# tmp_text[topics.LATE] = [["Have you ever found a way to avoid being late in the past that worked well?"]]
	# tmp_text[topics.DRIVER] = [["Have you ever dealt with this problem or something similar before?"]]
	# tmp_text[topics.VEHICLE] = [["Have you ever experienced this problem before?"]]
	bot_texts[1][4] = Reply(bot_id=1, in_group_id=4, texts=tmp_text, next_id=[(config.DEFAULT_YES, 5), (config.DEFAULT_NO, 6), (config.DEFAULT_OTHERS, 6)])
	del tmp_text



	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Cool, tell me about a strategy you used in the past to deal with that similar problem."]]
	# tmp_text[topics.TRAFFIC] = [["Could this strategy help you deal with traffic now?"]]
	# tmp_text[topics.TIRED] = [["Could you use this method to deal with your current tiredness?"]]
	# tmp_text[topics.LATE] = [["Could a similar strategy work now?"]]
	# tmp_text[topics.DRIVER] = [["Was it effective in reducing your stress in dealing with these drivers?"]]
	# tmp_text[topics.VEHICLE] = [["Could a similar solution work here too?"]]
	bot_texts[1][5] = Reply(bot_id=1, in_group_id=5, texts=tmp_text, next_id=11)
	del tmp_text

	bot_texts[1][11] = Reply(bot_id=1, in_group_id=11, texts={topics.GENERAL:[["Could you adapt/reuse this strategy to solve the current problem"], ["Could applying this strategy to the current problem lead to a desirable outcome?"]]}, next_id=[(config.DEFAULT_NO, 6), (config.DEFAULT_OTHERS, 12)])
	bot_texts[1][12] = Reply(bot_id=1, in_group_id=12, texts={topics.GENERAL:[["Great! Is there anything holding you back from applying this?"]]}, next_id=[(config.DEFAULT_YES, 6), (config.DEFAULT_OTHERS, 13)])
	bot_texts[1][13] = Reply(bot_id=1, in_group_id=13, texts={topics.GENERAL:[["Awesome! When can you do this in the next few days? (I find it helpful to add plans to my calendar.)"]]}, next_id=config.CLOSING_INDEX)


	bot_texts[1][6] = Reply(bot_id=1, in_group_id=6, texts={topics.GENERAL:[["Perhaps breaking down the problem would be helpful", "Could you describe for me a piece of the problem and a simple solution for it?"]]}, next_id=[(config.DEFAULT_NO, 8), (config.DEFAULT_OTHERS, 9)])
	bot_texts[1][7] = Reply(bot_id=1, in_group_id=7, texts={topics.GENERAL:[["That's alright. Can you "]]}, next_id=config.CLOSING_INDEX)


	tmp_text = {}
	tmp_text[topics.GENERAL] = [["That\'s alright.", "Can you try and describe any tiny step that would lead towards solving a part of the problem?"]]
	# tmp_text[topics.TRAFFIC] = [["That\'s ok.", "Is there any small thing you could do that would reduce the amount of traffic you need to deal with?"]]
	# tmp_text[topics.TIRED] = [["That\'s ok.", "Is there any small step you could take to increase the amount of rest you get?"]]
	# tmp_text[topics.LATE] = [["That\'s alright.", "Is there a small step you could take in the future to avoid being late next time?"]]
	# tmp_text[topics.DRIVER] = [["Alright, do you feel there is anything you could do so that you could either avoid these drivers entirely or at least feel better about sharing the road with them?"]]
	# tmp_text[topics.VEHICLE] = [["Is there someone you could talk to that might help you find a fix for your vehicle?"]]
	bot_texts[1][8] = Reply(bot_id=1, in_group_id=8, texts=tmp_text, next_id=[(config.DEFAULT_NO, 10), (config.DEFAULT_OTHERS, 9)])
	del tmp_text


	bot_texts[1][9] = Reply(bot_id=1, in_group_id=9, texts={topics.GENERAL:[["Great, I\'m glad you can do something about it.", "By breaking down a problem into tiny steps, we can often string together a solution"]]}, next_id=config.CLOSING_INDEX)


	tmp_text = {}
	tmp_text[topics.GENERAL] = [["It seems like I might not be the right bot for you.", "If you'd like to talk to one of my friends type 'change bots'.", "Otherwise just type goodbye to end the conversation."]]
	# tmp_text[topics.TRAFFIC] = [["Maybe taking a different route or leaving earlier or later could solve your problem?", "Spending some time planning your travel may help you come up with a solution."]]
	# tmp_text[topics.TIRED] = [["The easiest solution would be to just go to sleep, but if this doesn\'t work for you spend some time thinking of ways to re-organize your schedule to accommodate a good night\'s rest."]]
	# tmp_text[topics.LATE] = [["Everyone\'s late once in awhile.", "However, if it is a common occurence maybe think about leaving earlier or taking a quicker route to make your scheduled events on time."]]
	# tmp_text[topics.DRIVER] = [["If aggressive driving is a frequent issue, then perhaps taking a different route could solve your problem."]]
	# tmp_text[topics.VEHICLE] = [["Taking your vehicle to the dealership or mechanic is usually a good solution", "as they can pinpoint the exact problem with your vehicle and offer you a solution."]]
	bot_texts[1][10] = Reply(bot_id=1, in_group_id=10, texts=tmp_text, next_id=config.CLOSING_INDEX)
	del tmp_text


	#---------------------------------------------------------------------------------------------------------------------------------
	## Positive thinking bot

	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Ok, what is it about the situation that is making you feel stressed?"]]
	# tmp_text[topics.TRAFFIC] = [["Could you give me more detail on the traffic is today?"]]
	# tmp_text[topics.TIRED] = [["How do you feel your tiredness is adding to your stress level?"]]
	# tmp_text[topics.LATE] = [["Can you give me more detail on the event you are late to"]]
	# tmp_text[topics.DRIVER] = [["Yeah, there are a lot of aggressive drivers on the road.", "Can you give me more detail why it\'s stressing you out?"]]
	# tmp_text[topics.VEHICLE] = [["Can you give me more details on how your vehicle isn\'t responding?"]]
	bot_texts[2][0] = Reply(bot_id=2, in_group_id=0, texts=tmp_text, next_id=1)
	del tmp_text

	bot_texts[2][1] = Reply(bot_id=2, in_group_id=1, texts={topics.GENERAL:[["I see how that can be stressful.", "I want you to take a couple minutes and write at least one positive aspect about your situation."], [":(, I\'m sorry.", "I want you to try something.", "Take a couple minutes and write at least one positive aspect about your situation."]]}, next_id=2)
	bot_texts[2][2] = Reply(bot_id=2, in_group_id=2, texts={topics.GENERAL:[["Good job finding a positive!", "Is there another positive you can find in your situation?"], ["Great!", "Do you think there is another positive you can find in your situation?"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, 3)])
	bot_texts[2][3] = Reply(bot_id=2, in_group_id=3, texts={topics.GENERAL:[["Wonderful! See, you can usually find positives even when in the most negative of situations."], ["Awesome you\'re a great positive thinker!!"]]}, next_id=5)
	bot_texts[2][4] = Reply(bot_id=2, in_group_id=4, texts={topics.GENERAL:[["That\'s ok! You found some positive to the situation"], ["That\'s alright you did find one positive which is really good."]]}, next_id=5)
	bot_texts[2][5] = Reply(bot_id=2, in_group_id=5, texts={topics.GENERAL:[["Positive thinking can be a good way to destress, making it easier to face challenges."], ["When you\'re feeling down about a situation, trying to find the positives can make it easier to handle."]]}, next_id=config.CLOSING_INDEX)


	tmp_text = {}
	tmp_text[topics.GENERAL] = [["That's ok."]]
	# tmp_text[topics.TRAFFIC] = [["That\'s ok traffic is a real nuisance.", "Maybe finding something you can do in the car while being stuck in traffic can help pass the time.", "listening to music, radio, or just thinking about life."]]
	# tmp_text[topics.TIRED] = [["That\'s ok, honestly being tired is draining.", "Maybe finding some time to sleep or at least relax a little could help you feel better."]]
	# tmp_text[topics.LATE] = [["That\'s fair, it\'s tough to find positives in being late.", "Maybe leaving a little earlier could help you avoid the situation entirely and solve your problem."]]
	# tmp_text[topics.DRIVER] = [["Yeah, honestly those drivers are real assholes sometimes.", "Maybe thinking about how much better of a driver you are can add a positive spin to the situation."]]
	# tmp_text[topics.VEHICLE] = [["Having vehicle trouble is no fun.", "Maybe you can use the time to run errands while you get it fixed"]]
	bot_texts[2][6] = Reply(bot_id=2, in_group_id=6, texts=tmp_text, next_id=5)
	del tmp_text
	
	# bot_texts[0][10] = Reply(bot_id=0, in_group_id=10, texts=[""], next_id=None)
	# bot_texts[0][11] = Reply(bot_id=0, in_group_id=11, texts=[""], next_id=None)
	#bot_texts[0][3] = Reply(bot_id=0, in_group_id=3, text=[""], next_id=4)


	#---------------------------------------------------------------------------------------------------------------------------------
	## Humor bot
	bot_texts[3][0] = Reply(bot_id=3, in_group_id=0, texts={topics.GENERAL:[["Ok, can you give me more detail about this event?"]]}, next_id=1)
	bot_texts[3][1] = Reply(bot_id=3, in_group_id=1, texts={topics.GENERAL:[["Thank you for sharing.", "That does sound stressful.", "Ok, let’s try looking at this situation in a different light.", "I want you to take a few minutes to come up with a joke about this situation", " Would you like to have an example?"]]}, next_id=[(config.DEFAULT_NO, 3), (config.DEFAULT_OTHERS, 2)])
	bot_texts[3][2] = Reply(bot_id=3, in_group_id=2, texts={topics.GENERAL:[["For example, if the situation was being stuck having to help people out constantly you might come up with the following joke:", "I\'d love to help you out. Which way did you come in again?", "Don\'t worry about it being the best joke, just find something humorous about your situation.", "Please tell me your joke!"]]}, next_id=3)
	bot_texts[3][3] = Reply(bot_id=3, in_group_id=3, texts={topics.GENERAL:[["Haha that\'s true.", "Oftentimes finding the humor in stressful situations can help diffuse some tension."], ["Good joke!", "Sometimes there are good things that happen even if the situation isn\'t the best. "], ["Heehee! You\'re funny!", "Humor can be found in many situations!"]]}, next_id=4)
	bot_texts[3][4] = Reply(bot_id=3, in_group_id=4, texts={topics.GENERAL:[["Did that help you to find something good about the situation?"]]}, next_id=config.CLOSING_INDEX)



	#---------------------------------------------------------------------------------------------------------------------------------
	## relaxation bot
	bot_texts[4][0] = Reply(bot_id=4, in_group_id=0, texts={topics.GENERAL:[["Ok, can you give me more detail about this event?"]]}, next_id=1)
	bot_texts[4][1] = Reply(bot_id=4, in_group_id=1, texts={topics.GENERAL:[["I have a couple strategies to help.", "Say yes if you rather do a visualization.", "Say no if you want to focus on your breathing.",  "If you don\'t know which activity you want to do, you can also say no preference and I can decide for you."]]}, next_id=[(('no preference', 'both'), random.randint(2,3)), (('no', ), 3), (('yes', ), 2)])

	bot_texts[4][2] = Reply(bot_id=4, in_group_id=2, texts={topics.GENERAL:[["Ok, {name}, let\'s do a visualization activity.", "I\'d like you to close your eyes and think of any place that makes you feel happy or calm.", "Think of all the details, as vivid of a picture as you can imagine.", "Think of your senses: the sights, the smells, the sounds."], ["Picture a time when you felt at peace. What was around you in this time?", "What did it feel like?", "What do you see, smell or hear?", "Let me know when you are done with your visualization."]]}, next_id=4)
	bot_texts[4][4] = Reply(bot_id=4, in_group_id=4, texts={topics.GENERAL:[["Could you walk me through your experience?", "What did you see? What did you hear?", "How did you feel?"]]}, next_id=5)
	bot_texts[4][5] = Reply(bot_id=4, in_group_id=5, texts={topics.GENERAL:[["That sounds lovely, thanks for sharing.", "You can look at what you wrote here later to remind you of this place and how good it makes you feel.", "Visualization can be a great tool to destress"]]}, next_id=11)
	bot_texts[4][11] = Reply(bot_id=4, in_group_id=11, texts={topics.GENERAL:[["Would you like to repeat the exercise?"]]}, next_id=[(config.DEFAULT_NO, 13), (config.DEFAULT_OTHERS, 2)])
	


	bot_texts[4][3] = Reply(bot_id=4, in_group_id=3, texts={topics.GENERAL:[["Okay, let me guide you through a mindfulness exercise to help you {name}. Tell me you are done after each instruction. ", "First sit up straight in your chair."]]}, next_id=7)
	bot_texts[4][7] = Reply(bot_id=4, in_group_id=7, texts={topics.GENERAL:[["Focus on the sensation of air moving through your nose."]]}, next_id=8)
	bot_texts[4][8] = Reply(bot_id=4, in_group_id=8, texts={topics.GENERAL:[["Slowly widen your focus to the room around you while still observing the sensation of air through your nose."]]}, next_id=9)
	bot_texts[4][9] = Reply(bot_id=4, in_group_id=9, texts={topics.GENERAL:[["Just think about being present in the moment, and if you feel your mind wandering, return to thinking about the original sensation of air flowing through your nose."]]}, next_id=10)
	bot_texts[4][10] = Reply(bot_id=4, in_group_id=10, texts={topics.GENERAL:[["Take 5 deep breaths while focusing on you surroundings."]]}, next_id=12)
	bot_texts[4][12] = Reply(bot_id=4, in_group_id=12, texts={topics.GENERAL:[["Would you like to repeat the exercise?"]]}, next_id=[(config.DEFAULT_NO, 13), (config.DEFAULT_OTHERS, 3)])

	bot_texts[4][13] = Reply(bot_id=4, in_group_id=13, texts={topics.GENERAL:[["That\'s okay, taking a moment to be mindful may help you in situations when you are feeling stressed."]]}, next_id=config.CLOSING_INDEX)
	#---------------------------------------------------------------------------------------------------------------------------------
	## self-love bot

	bot_texts[5][0] = Reply(bot_id=5, in_group_id=0, texts={topics.GENERAL:[["Oh, sorry to hear that. Could you give me more information about the {problem}?"]]}, next_id=2)
	bot_texts[5][2] = Reply(bot_id=5, in_group_id=2, texts={topics.GENERAL:[["Imagine a close friend came to you with a similar problem.", "How would you support them?"], ["Imagine a close friend ask you to help with a similar problem.", "What might you say to them to make them feel better?"]]}, next_id=[(config.DEFAULT_DK, 3), (config.DEFAULT_OTHERS, 5)])
	bot_texts[5][3] = Reply(bot_id=5, in_group_id=3, texts={topics.GENERAL:[["That\'s okay, sometimes it\'s hard to know how to support someone in a difficult situation.", "I send you some things I might do when I\'m stressed.", "Feel free to use this list for ideas. ", "You can also add your own if you feel like I missed something.", "Does that sound good?"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, config.CLOSING_INDEX)])
	bot_texts[5][5] = Reply(bot_id=5, in_group_id=5, texts={topics.GENERAL:[["What do you think are the benefits of offering this kind of support?"]]}, next_id=6)
	bot_texts[5][6] = Reply(bot_id=5, in_group_id=6, texts={topics.GENERAL:[["Do you have a friend you could go to for this type of support?"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, 7)])
	bot_texts[5][7] = Reply(bot_id=5, in_group_id=7, texts={topics.GENERAL:[["Could you make a plan of when to connect with this person?"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, 8)])
	bot_texts[5][8] = Reply(bot_id=5, in_group_id=8, texts={topics.GENERAL:[["Awesome, friends can often provide the best support", "It’s great that you have made time to prioritize yourself!"]]}, next_id=config.CLOSING_INDEX)

	bot_texts[5][4] = Reply(bot_id=5, in_group_id=4, texts={topics.GENERAL:[["I wish I could give you a hug right now to make you feel better.", "I care about you, and I\'m sure there are others that do to, even if they are not available right now. ", "I hope I have been able to help, and I\'m here whenever you need me. ", "Promise you would find me for help, will you?"]]}, next_id=config.CLOSING_INDEX)
	

	#---------------------------------------------------------------------------------------------------------------------------------
	## distraction bot
		#Distraction - dunno bot
	bot_texts[6][0] = Reply(bot_id=6, in_group_id=0, texts={topics.GENERAL:[["Ok, I think that can definitely be hard… Let’s try shift our attention to something else.", "Can you tell me about something you are looking forward to? "], ["Things can be stressful at times. One tool is to think about something that is coming up that is exciting.", "What is an event that you are looking forward to?"]]}, next_id=1)
	bot_texts[6][1] = Reply(bot_id=6, in_group_id=1, texts={topics.GENERAL:[["Awesome!", "What makes you excited about it?"]]}, next_id=2)
	bot_texts[6][2] = Reply(bot_id=6, in_group_id=2, texts={topics.GENERAL:[["How often do you go to it?"], ["Tell me more! I want to hear all about it!"]]}, next_id=3)
	bot_texts[6][3] = Reply(bot_id=6, in_group_id=3, texts={topics.GENERAL:[["Do you have another event that you are excited about?"], ["Would you like to do this with another event?"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, 3)])
	bot_texts[6][4] = Reply(bot_id=6, in_group_id=4, texts={topics.GENERAL:[["Cool. When you're feeling stressed, it's can be good to think about other things that you might be excited about."],["Snazzy. Next time you feel stressed, you could think about something that makes you excited."],["Dope! Sometimes if you are feeling stressed, it can be helpful to disengage from the current events and shift your attention to things that you are looking forward to."]]}, next_id=config.CLOSING_INDEX)

	#---------------------------------------------------------------------------------------------------------------------------------
	## checkin bot

	# bot_texts[7][0] = Reply(bot_id=7, in_group_id=0, texts={topics.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 1), (config.DEFAULT_OTHERS, 2)])

	# bot_texts[7][1] = Reply(bot_id=7, in_group_id=1, texts={topics.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 3), (config.DEFAULT_OTHERS, 4)])
	# bot_texts[7][2] = Reply(bot_id=7, in_group_id=2, texts={topics.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 5), (config.DEFAULT_OTHERS, 6)])



	# bot_texts[7][3] = Reply(bot_id=7, in_group_id=3, texts={topics.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 7), (config.DEFAULT_OTHERS, 2)])
	# bot_texts[7][4] = Reply(bot_id=7, in_group_id=4, texts={topics.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 1), (config.DEFAULT_OTHERS, 2)])
	# bot_texts[7][5] = Reply(bot_id=7, in_group_id=5, texts={topics.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 1), (config.DEFAULT_OTHERS, 2)])
	# bot_texts[7][6] = Reply(bot_id=7, in_group_id=6, texts={topics.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 1), (config.DEFAULT_OTHERS, 2)])



	# bot_texts[7][7] = Reply(bot_id=7, in_group_id=7, texts={topics.GENERAL:[["Wonderful, it seems as though this problem isn\'t affecting these three major aspects of your life.", "Great job staying on top of your sleeping and eating as well as reaching out to friends and family for support"]]}, next_id=config.CLOSING_INDEX)
	# bot_texts[7][8] = Reply(bot_id=7, in_group_id=8, texts={topics.GENERAL:[[""]]}, next_id=config.CLOSING_INDEX)
	# bot_texts[7][9] = Reply(bot_id=7, in_group_id=9, texts={topics.GENERAL:[[""]]}, next_id=config.CLOSING_INDEX)
	# bot_texts[7][10] = Reply(bot_id=7, in_group_id=10, texts={topics.GENERAL:[[""]]}, next_id=config.CLOSING_INDEX)

	# bot_texts[7][7] = Reply(bot_id=7, in_group_id=7, texts={topics.GENERAL:[[""]]}, next_id=)


	return bot_texts