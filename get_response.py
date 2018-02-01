# -*- coding: UTF-8 -*-

from collections import *
from utils import Params, Config, Topics, Reply



def get_text_from_db():
	params = Params()
	config = Config()
	topics = Topics()

	openning = [["Hi {name}, I’m {bot_name}.", "I’m here to help you deal with your stress.", "Can you tell me a little bit about a recent event that makes you stressed?"],
				["Hi {name}, I’m {bot_name}.", "I’m here to help you deal with your stress.", "What’s stressing you out right now?"],
				["Hi {name}, I’m {bot_name}.", "I’m here to help you deal with your stress.", "What’s on your mind?"],
				["Hi {name}, I’m {bot_name}.", "I’m here to help you deal with your stress.", "Could you share something that’s on your mind?"]]
	closing = [["Thank you for sharing with me. I hope I’ve been able to help.", "Have a nice day!"]]

	dk_check_at_begining = [["Do you want me to come back later?"]]

	bot_texts = defaultdict(dict)
	for i in range(params.BOT_NUM):
		bot_texts[i][config.START_INDEX] = Reply(bot_id=i, in_group_id=config.START_INDEX, texts={topics.GENERAL:[["START_OF_CONVERSATION"]]}, next_id=-1)
		bot_texts[i][config.OPENNING_INDEX] = Reply(bot_id=i, in_group_id=config.OPENNING_INDEX, texts={topics.GENERAL:openning}, next_id=0)
		bot_texts[i][config.CLOSING_INDEX] = Reply(bot_id=i, in_group_id=config.CLOSING_INDEX, texts={topics.GENERAL:closing}, next_id=None)
		bot_texts[i][config.DK_INDEX] = Reply(bot_id=i, in_group_id=config.DK_INDEX, texts={topics.GENERAL:dk_check_at_begining}, next_id=[(config.DEFAULT_DK, config.DK_INDEX), (config.DEFAULT_NO, config.CLOSING_INDEX), (config.DEFAULT_OTHERS, config.CLOSING_INDEX)])


	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Can you give me more details on why that is stressful?"], ["Why is that stressing you out?"]]
	tmp_text[topics.TRAFFIC] = [["Traffic can really suck.", "How bad is it out there today?"]]
	tmp_text[topics.TIRED] = [["I see that you seem tired.", "Do you feel you got enough sleep last night?"]]
	tmp_text[topics.LATE] = [["Sorry to hear that you are late.", "How bad is it?"]]
	tmp_text[topics.DRIVER] = [["Yeah, there are a lot of aggressive drivers on the road.", "Can you give me more detail why it’s stressing you out?"]]
	tmp_text[topics.VEHICLE] = [["Can you give me more details on how your vehicle isn’t responding?"]]
	bot_texts[0][0] = Reply(bot_id=0, in_group_id=0, texts=tmp_text, next_id=1)
	del tmp_text


	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Hmm I see…", "Let me ask you something, what is the worst possible outcome of {problem}?"], ["Sorry to hear that.", "What are you most afraid might happen as a result?"]]
	tmp_text[topics.TRAFFIC] = [["That’s unfortunate.", "What do you think the worst possible outcome of this traffic is for you?"]]
	tmp_text[topics.TIRED] = [["That could be a possible fix.", "What’s the worst possible outcome of you being tired?"]]
	tmp_text[topics.LATE] = [["Sorry to hear that.", "Let me ask you something, what is the worst possible outcome of your lateness?"]]
	tmp_text[topics.DRIVER] = [["Hmm I see…", "What are most afraid might happen as a result of these other drivers?"]]
	tmp_text[topics.VEHICLE] = [["That’s unfortunate.", "What’s the worst possible outcome of this malfunction?"]]
	bot_texts[0][1] = Reply(bot_id=0, in_group_id=1, texts=tmp_text, next_id=2)
	del tmp_text

	bot_texts[0][2] = Reply(bot_id=0, in_group_id=2, texts={topics.GENERAL:[["Ok, on a scale of 1 to 10, with 1 being almost impossible, how likely is this scenario?"], ["Alright, on a scale of 1 to 10 (1 impossible, 10 certain), how likely is this scenario?"]]}, next_id= [(('8','9','10', 'eight', 'nine', 'ten', 'likely', 'certain'), 3), (('5','6','7', 'five', 'six','seven'), 4), (('1','2','3','4','one','two','three','four', 'unlikely', 'impossible'), 5), ((config.DEFAULT_OTHERS, ), 10)])


	bot_texts[0][3] = Reply(bot_id=0, in_group_id=3, texts={topics.GENERAL:[["Damn, sorry to hear that. If it happens, what could you do to get back on track?"]]}, next_id=[(config.DEFAULT_DK, 6), (config.DEFAULT_NO, 7), (config.DEFAULT_OTHERS, 8)])
	bot_texts[0][4] = Reply(bot_id=0, in_group_id=4, texts={topics.GENERAL:[["In that case, what could you do to get back on track if it does happen?"]]}, next_id=[(config.DEFAULT_DK, 6), (config.DEFAULT_NO, 7), (config.DEFAULT_OTHERS, 8)])
	bot_texts[0][5] = Reply(bot_id=0, in_group_id=5, texts={topics.GENERAL:[["So would you agree that the worst case situation is unlikely?"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, 9)])

	bot_texts[0][6] = Reply(bot_id=0, in_group_id=6, texts={topics.GENERAL:[["That’s ok. Could you try and think of a solution?"], ["Is there anything you could do to improve the situation?"]]}, next_id= [(config.DEFAULT_NO, 7), (config.DEFAULT_OTHERS, 8)])
	

	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Maybe spend some time thinking about you problem and possible ways to approach it."]]
	tmp_text[topics.TRAFFIC] = [["Maybe taking a different route or leaving earlier or later could solve your problem?", "Spending some time planning your travel may help you come up with a solution."]]
	tmp_text[topics.TIRED] = [["The easiest solution would be to just go to sleep.", "But if this doesn’t work for you,", "spend some time thinking of ways to re-organize your schedule to accommodate a good night’s rest."]]
	tmp_text[topics.LATE] = [["Everyone’s late once in awhile.", "However, if it is a common occurence maybe think about leaving earlier or taking a quicker route to make your scheduled events on time."]]
	tmp_text[topics.DRIVER] = [["If aggressive driving is a frequent issue, then perhaps taking a different route could solve your problem."]]
	tmp_text[topics.VEHICLE] = [["Taking your vehicle to the dealership or mechanic is usually a good solution", "as they can pinpoint the exact problem with your vehicle and offer you a solution."]]
	bot_texts[0][7] = Reply(bot_id=0, in_group_id=7, texts=tmp_text, next_id=config.CLOSING_INDEX)
	del tmp_text



	bot_texts[0][8] = Reply(bot_id=0, in_group_id=8, texts={topics.GENERAL:[["See you have a plan B.", "Just remember if you’re stressing that there is always a way to get back on your feet."]]}, next_id=config.CLOSING_INDEX)


	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Glad to hear that.", "Seems like you have things in perspective."],["Glad to hear that.", "Sounds like you have things in perspective."]]
	tmp_text[topics.TRAFFIC] = [["Glad to hear that.", "Traffic is a nuisance but getting too stressed out by it is often more trouble than it’s worth."]]
	tmp_text[topics.TIRED] = [["Seems like you have things in perspective.", "Often, we just need a good night’s rest or even  a short nap to feel refreshed."]]
	tmp_text[topics.LATE] = [["Even the best prepared are sometimes late.", "It’s usually more trouble than it’s worth to get too worked up about it."]]
	tmp_text[topics.DRIVER] = [["Sounds like you have things in perspective.", "Aggressive drivers can often be scary to share the road with, but as long as you are driving safely it will usually work out."]]
	tmp_text[topics.VEHICLE] = [["Glad to hear that.", "Oftentimes, vehicle malfunctions are quick fixes and not worth stressing about."]]
	bot_texts[0][9] = Reply(bot_id=0, in_group_id=9, texts=tmp_text, next_id=config.CLOSING_INDEX)
	del tmp_text


	bot_texts[0][10] = Reply(bot_id=0, in_group_id=10, texts={topics.GENERAL:[["Could you say it again?"]]}, next_id= [(('8','9','10', 'eight', 'nine', 'ten', 'likely', 'certain'), 3), (('5','6','7', 'five', 'six','seven'), 4), (('1','2','3','4','one','two','three','four', 'impossible'), 5), ((config.DEFAULT_OTHERS, ), 10)])

	#---------------------------------------------------------------------------------------------------------------------------------


	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Can you give me more details on why {problem} is stressing?"], ["Why is {problem} stressing you out?"]]
	tmp_text[topics.TRAFFIC] = [["No one likes traffic.", "How bad is it out there today?"]]
	tmp_text[topics.TIRED] = [["I see that you seem tired.", "Do you know why?"]]
	tmp_text[topics.LATE] = [["Why are you late today?"]]
	tmp_text[topics.DRIVER] = [["Why do these aggressive drivers have you stressed?"]]
	tmp_text[topics.VEHICLE] = [["Can you give me more details on what you think is wrong with your vehicle?"]]
	bot_texts[1][0] = Reply(bot_id=1, in_group_id=0, texts=tmp_text, next_id=1)
	del tmp_text



	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Ok, let’s see how bad this problem is.", " Is it really that big?"," Would others think so?"], ["Do you feel this problem is significantly affecting your life?"]]
	tmp_text[topics.TRAFFIC] = [["Do you feel traffic is significantly affecting your life?"]]
	tmp_text[topics.TIRED] = [["Are you frequently tired during your normal working hours?", "Is tiredness negatively affecting important aspects of your life?"]]
	tmp_text[topics.LATE] = [["I see.", "Is lateness a problem that frequently affects your life or is this a one-time thing?"]]
	tmp_text[topics.DRIVER] = [["Ok, is aggressive driving by others a problem that occurs often enough in your life to worry about it?"]]
	tmp_text[topics.VEHICLE] = [["Ok, let’s see how bad this problem is?", "Do you think it will be a quick fix?"]]
	bot_texts[1][1] = Reply(bot_id=1, in_group_id=1, texts=tmp_text, next_id=[(config.DEFAULT_NO, 3), (config.DEFAULT_OTHERS, 2)])
	del tmp_text

	bot_texts[1][2] = Reply(bot_id=1, in_group_id=2, texts={topics.GENERAL:[["If you could solve this problem, would your life improve?"]]}, next_id=4)
	bot_texts[1][3] = Reply(bot_id=1, in_group_id=3, texts={topics.GENERAL:[["Seems this is not a problem worth worrying about.", " Do you still want to work on it?"], ["In that case, do you feel you’d still like to spend time working on it?"]]}, next_id=[(config.DEFAULT_NO, config.CLOSING_INDEX), (config.DEFAULT_OTHERS, 4)])
	

	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Have you ever dealt with this problem or something similar before?"]]
	tmp_text[topics.TRAFFIC] = [["Was there an effective way you coped with traffic before?"]]
	tmp_text[topics.TIRED] = [["How have you coped with being tired in the past?"]]
	tmp_text[topics.LATE] = [["Have you ever found a way to avoid being late in the past that worked well?"]]
	tmp_text[topics.DRIVER] = [["Have you ever dealt with this problem or something similar before?"]]
	tmp_text[topics.VEHICLE] = [["Have you ever experienced this problem before?"]]
	bot_texts[1][4] = Reply(bot_id=1, in_group_id=4, texts=tmp_text, next_id=[(config.DEFAULT_NO, 6), (config.DEFAULT_OTHERS, 5)])
	del tmp_text



	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Could you use a similar strategy to solve it this time?"]]
	tmp_text[topics.TRAFFIC] = [["Could this strategy help you deal with traffic now?"]]
	tmp_text[topics.TIRED] = [["Could you use this method to deal with your current tiredness?"]]
	tmp_text[topics.LATE] = [["Could a similar strategy work now?"]]
	tmp_text[topics.DRIVER] = [["Was it effective in reducing your stress in dealing with these drivers?"]]
	tmp_text[topics.VEHICLE] = [["Could a similar solution work here too?"]]
	bot_texts[1][5] = Reply(bot_id=1, in_group_id=5, texts=tmp_text, next_id=[(config.DEFAULT_NO, 8), (config.DEFAULT_OTHERS, 7)])
	del tmp_text



	bot_texts[1][6] = Reply(bot_id=1, in_group_id=6, texts={topics.GENERAL:[["Perhaps you should break down the problem.", "Could you identify a piece of your problem and a simple solution for it?"]]}, next_id=[(config.DEFAULT_NO, 8), (config.DEFAULT_OTHERS, 7)])
	bot_texts[1][7] = Reply(bot_id=1, in_group_id=7, texts={topics.GENERAL:[["Good, you have a plan now!","Go ahead and implement it."]]}, next_id=config.CLOSING_INDEX)


	tmp_text = {}
	tmp_text[topics.GENERAL] = [["That’s alright.", "Is there a small step you could take to improve the situation?"]]
	tmp_text[topics.TRAFFIC] = [["That’s ok.", "Is there any small thing you could do that would reduce the amount of traffic you need to deal with?"]]
	tmp_text[topics.TIRED] = [["That’s ok.", "Is there any small step you could take to increase the amount of rest you get?"]]
	tmp_text[topics.LATE] = [["That’s alright.", "Is there a small step you could take in the future to avoid being late next time?"]]
	tmp_text[topics.DRIVER] = [["Alright, do you feel there is anything you could do so that you could either avoid these drivers entirely or at least feel better about sharing the road with them?"]]
	tmp_text[topics.VEHICLE] = [["Is there someone you could talk to that might help you find a fix for your vehicle?"]]
	bot_texts[1][8] = Reply(bot_id=1, in_group_id=8, texts=tmp_text, next_id=[(config.DEFAULT_NO, 10), (config.DEFAULT_OTHERS, 9)])
	del tmp_text


	bot_texts[1][9] = Reply(bot_id=1, in_group_id=9, texts={topics.GENERAL:[["Great, I’m glad you can do something about it."]]}, next_id=config.CLOSING_INDEX)


	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Maybe spend some time thinking about you problem and possible ways to approach it."]]
	tmp_text[topics.TRAFFIC] = [["Maybe taking a different route or leaving earlier or later could solve your problem?", "Spending some time planning your travel may help you come up with a solution."]]
	tmp_text[topics.TIRED] = [["The easiest solution would be to just go to sleep, but if this doesn’t work for you spend some time thinking of ways to re-organize your schedule to accommodate a good night’s rest."]]
	tmp_text[topics.LATE] = [["Everyone’s late once in awhile.", "However, if it is a common occurence maybe think about leaving earlier or taking a quicker route to make your scheduled events on time."]]
	tmp_text[topics.DRIVER] = [["If aggressive driving is a frequent issue, then perhaps taking a different route could solve your problem."]]
	tmp_text[topics.VEHICLE] = [["Taking your vehicle to the dealership or mechanic is usually a good solution", "as they can pinpoint the exact problem with your vehicle and offer you a solution."]]
	bot_texts[1][10] = Reply(bot_id=1, in_group_id=10, texts=tmp_text, next_id=config.CLOSING_INDEX)
	del tmp_text


	#---------------------------------------------------------------------------------------------------------------------------------

	tmp_text = {}
	tmp_text[topics.GENERAL] = [["Can you give me more details on why {problem} is stressing?"], ["Why is {problem} stressing you out?"]]
	tmp_text[topics.TRAFFIC] = [["Could you give me more detail on the traffic is today?"]]
	tmp_text[topics.TIRED] = [["How do you feel your tiredness is adding to your stress level?"]]
	tmp_text[topics.LATE] = [["Can you give me more detail on the event you are late to"]]
	tmp_text[topics.DRIVER] = [["Yeah, there are a lot of aggressive drivers on the road.", "Can you give me more detail why it’s stressing you out?"]]
	tmp_text[topics.VEHICLE] = [["Can you give me more details on how your vehicle isn’t responding?"]]
	bot_texts[2][0] = Reply(bot_id=2, in_group_id=0, texts=tmp_text, next_id=1)
	del tmp_text

	bot_texts[2][1] = Reply(bot_id=2, in_group_id=1, texts={topics.GENERAL:[["I see how that can be stressful.", "I want you to take a couple minutes and think about least one positive aspect about your situation.", "Let me know when you are done."], ["Wow that really sucks, I’m sorry.", "Try this: Take a couple minutes to find at least one positive aspect in your situation.", "Let me know when you are done."]]}, next_id=[(config.DEFAULT_NO, 6), (config.DEFAULT_OTHERS, 2)])
	bot_texts[2][2] = Reply(bot_id=2, in_group_id=2, texts={topics.GENERAL:[["Is there another positive you can find in your situation?"], ["Great!", "Do you think there is another positive you can find in your situation?"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, 3)])
	bot_texts[2][3] = Reply(bot_id=2, in_group_id=3, texts={topics.GENERAL:[["See, you can usually find positives even when in the most negative of situations."], ["Awesome you’re a great positive thinker!!"]]}, next_id=5)
	bot_texts[2][4] = Reply(bot_id=2, in_group_id=4, texts={topics.GENERAL:[["That’s ok at least you found one positive."], ["That’s alright you did find one positive."]]}, next_id=5)
	bot_texts[2][5] = Reply(bot_id=2, in_group_id=5, texts={topics.GENERAL:[["Positive thinking can be a good way to destress, making it easier to face challenges."], ["When you’re feeling down about a situation, trying to find the positives can make it easier to handle."]]}, next_id=config.CLOSING_INDEX)


	tmp_text = {}
	tmp_text[topics.GENERAL] = [["That's ok."]]
	tmp_text[topics.TRAFFIC] = [["That’s ok traffic is a real nuisance.", "Maybe finding something you can do in the car while being stuck in traffic can help pass the time.", "listening to music, radio, or just thinking about life."]]
	tmp_text[topics.TIRED] = [["That’s ok, honestly being tired is draining.", "Maybe finding some time to sleep or at least relax a little could help you feel better."]]
	tmp_text[topics.LATE] = [["That’s fair, it’s tough to find positives in being late.", "Maybe leaving a little earlier could help you avoid the situation entirely and solve your problem."]]
	tmp_text[topics.DRIVER] = [["Yeah, honestly those drivers are real assholes sometimes.", "Maybe thinking about how much better of a driver you are can add a positive spin to the situation."]]
	tmp_text[topics.VEHICLE] = [["Having vehicle trouble is no fun.", "Maybe you can use the time to run errands while you get it fixed"]]
	bot_texts[2][6] = Reply(bot_id=2, in_group_id=6, texts=tmp_text, next_id=5)
	del tmp_text
	
	# bot_texts[0][10] = Reply(bot_id=0, in_group_id=10, texts=[""], next_id=None)
	# bot_texts[0][11] = Reply(bot_id=0, in_group_id=11, texts=[""], next_id=None)
	#bot_texts[0][3] = Reply(bot_id=0, in_group_id=3, text=[""], next_id=4)
	return bot_texts