# -*- coding: UTF-8 -*-

import time
import random
import string
import sys, getopt
import os, nltk


from fbchat import log, Client
from fbchat.models import *
from collections import *
from os import system
from utils import *
from get_response import get_text_from_db
from pymongo import MongoClient
from gtts import gTTS

onboarding_id = 7
relaxation_id = 4

class StressBot(Client):
	def __init__(self, email, password, reply_dict, **kwargs):
		Client.__init__(self, email, password)
		self.user_history = defaultdict(list)
		# self.user_history {thread_id: [[(bot_id, in_group_id, ab_test_id, msg, user_response_time), () ....], [], [], ...]}
		self.reply_dict = reply_dict
		self.user_name_dict = {}
		self.user_bot_dict = {}
		self.user_problem_dict = {}
		self.params = Params()
		self.config = Config()

		
		self.voice_choice = False

		additional_bot_control = kwargs.get('add_bot_ctl',{})
		if 'sleeping_time' in additional_bot_control:
			self.params.set_sleeping_time(additional_bot_control.get('sleeping_time'))

		if 'bot_choice' in additional_bot_control:
			self.params.set_bot_choice(additional_bot_control.get('bot_choice'))

		if 'mode' in additional_bot_control:
			self.params.set_mode(additional_bot_control.get('mode', 'text'))
			if self.params.MODE == Modes.VOICE:
				self.voice_choice == True

		if self.params.MODE == Modes.TEXT:
			self.db = MongoClient().textbot
		else:
			self.db = MongoClient().voicebot


	def say(self, text):
		tts = gTTS(text=text, lang='en')
		tts.save("test.mp3")
		system("mpg321 test.mp3")

	def clean_last_record(self, thread_id):
		if thread_id in self.user_history and len(self.user_history[thread_id]) > 0:
			return self.user_history[thread_id].pop()

	def delete_all_dict(self, thread_id, delete_name=False):
		if thread_id in self.user_bot_dict:
			del self.user_bot_dict[thread_id]
		if thread_id in self.user_problem_dict:
			del self.user_problem_dict[thread_id]
		if delete_name and  thread_id in self.user_name_dict:
			del self.user_name_dict[thread_id]

	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		user_response_time = time.time()
		# import datetime
		# st = datetime.datetime.fromtimestamp(user_response_time).strftime('%Y-%m-%d %H:%M:%S')
		# then you will see timestamp such as "2012-12-15 01:21:05"
		self.markAsDelivered(author_id, thread_id)
		self.markAsRead(author_id)
		log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

		if author_id != self.uid:

			try:

				msg = message_object.text.lower()
				msg = ' '.join(msg.split()) # substitute multiple spaces into one
				if msg[-1] in list(string.punctuation):
					msg = msg[:-1]
				# if not chcek_rubbish_word(msg):
				# 	reply_text = "Sorry I didn't get that. Could you repeat yourself?"
				# 	self.send(Message(text=reply_text), thread_id=thread_id, thread_type=thread_type)
				# 	if self.voice_choice:
				# 		#system('say -v Victoria ' + reply_text.replace("(", " ").replace(")", " "))#Alex
				# 		self.say(reply_text.replace("(", " ").replace(")", " "))
				# 	if not self.voice_choice:
				# 		time.sleep(self.params.SLEEPING_TIME)
				# 	return None

				if msg.strip().lower() == 'restart':
					self.clean_last_record(thread_id)
					self.delete_all_dict(thread_id)
					return None
				
				if thread_id not in self.user_history or len(self.user_history[thread_id]) == 0 \
					or len(self.user_history[thread_id][-1]) == 0 \
						or len(self.user_history[thread_id][-1][-1]) < 2 \
							or self.user_history[thread_id][-1][-1][1] == self.config.CLOSING_INDEX\
								or self.user_history[thread_id][-1][-1][1] == self.config.ABRUPT_CLOSING_INDEX:
									_bot_choice = self.user_bot_dict[thread_id] if thread_id in self.user_bot_dict else self.params.BOT_CHOICE
									# bot_id = random.randint(0, self.params.BOT_NUM-1-1) if _bot_choice == -1 else _bot_choice #onboarding should only happens at first time or when we want it
									bot_id = random.choice(range(0, relaxation_id) + range(relaxation_id+1, onboarding_id) + range(onboarding_id+1, self.params.BOT_NUM)) if _bot_choice == -1 else _bot_choice #onboarding should only happens at first time or when we want it
									
									query_name = client.fetchUserInfo(thread_id)[thread_id].name.split(" ")[0]
									if self.db.user.find({'name': query_name}).count() == 0:
										bot_id = onboarding_id
									self.user_history[thread_id].append([(bot_id, self.config.START_INDEX, 0, ["START_OF_CONVERSATION"])])
									if not self.voice_choice:
										bot_id = self.user_history[thread_id][-1][-1][0]
										self.changeThreadColor(self.params.bot_color_list[bot_id], thread_id=thread_id)
										title_to_changed = self.params.bot_name_list[bot_id][:-4]
										self.changeNickname(title_to_changed, self.uid, thread_id=thread_id, thread_type=thread_type)
				bot_id, current_id, _, _ = self.user_history[thread_id][-1][-1]  # ab_id, questions
				# self.user_history stores [(bot_id, current_id, ab_test, questions (list of texts), user_answer, timestamp)]
				next_id = self.reply_dict[bot_id][current_id].next_id


				if current_id == self.config.OPENNING_INDEX and  find_problem(msg) != None:
					self.user_problem_dict[thread_id] = find_problem(msg)
				problem = self.user_problem_dict.get(thread_id, 'that')

				#if msg.strip().lower() == 'change bot' or msg.strip().lower() in self.params.bot_tech_name_list:
				if msg.strip().lower() in self.params.bot_tech_name_list:
					whether_return = bot_id != onboarding_id
					if whether_return:
						self.clean_last_record(thread_id)
					self.delete_all_dict(thread_id, delete_name=False)
					# if msg.strip().lower() == 'change bot':
					# 	while True:
					# 		tmp = random.randint(0, self.params.BOT_NUM-1)
					# 		if tmp != bot_id:
					# 			self.user_bot_dict[thread_id] = tmp
					# 			break
					# else:
					self.user_bot_dict[thread_id] = self.params.bot_tech_name_list.index(msg.strip().lower())
					print(whether_return, bot_id)
					if whether_return:
						return None

				if current_id == 2 and bot_id == onboarding_id:
					self.user_name_dict[thread_id] = msg.lower().split()[0]

				if current_id == self.config.START_INDEX or (current_id == 2 and bot_id == onboarding_id):
					for each in ['i am', 'i\'m', 'this is', 'name is']:
						_index = msg.lower().find(each)
						if _index != -1:
							result = msg.lower()[_index + len(each)+1:]
							result = result.split()[0]
							for each_punc in list(string.punctuation):
								result = result.replace(each_punc,"")
							if len(result) > 0 and len(result) < 20:
								self.user_name_dict[thread_id] = result


				# if current_id == self.config.OPENNING_INDEX and any(map(lambda x: x != -1, [msg.lower().find(each) for each in ['nothing', 'not now', 'don\'t know']])):
				# 	next_id = self.config.DK_INDEX

				user_name = client.fetchUserInfo(thread_id)[thread_id].name.split(" ")[0]
				user_name = self.user_name_dict.get(thread_id, user_name)


				decider_dict = {
					self.config.DEFAULT_YES:find_keyword,
					self.config.DEFAULT_NO:find_keyword,
					self.config.DEFAULT_DK:find_keyword,
					self.config.DEFAULT_OTHERS:always_true,
				}


				keyword_dict = {
					self.config.DEFAULT_YES:['yes', 'ok', 'sure', 'right', 'yea', 'ye', 'yup', 'yeah'],
					self.config.DEFAULT_NO:['no', 'not',  'neither', 'neg', 'don\'t', 'doesn\'', 'donnot', 'dont', '\'t', 'nothing', 'nah'],
					self.config.DEFAULT_DK:["dk", "dunno", "dno", "don't know", "idk"]
				}

				if type(next_id) == list and len(next_id) > 0:
					if type(next_id[0][0]) == tuple:
						for (key, val) in next_id:
							if find_keyword(msg, key):
								next_id = val
								break
					elif type(next_id[0][0]) == str:
						for (key, val) in next_id:
							#print(msg, keyword_dict.get(key, [val]))
						 	if decider_dict.get(key, find_keyword)(str(msg).lower(), keyword_dict.get(key, [key])):
						 		next_id = val
						 		break
					else:
						self.clean_last_record(thread_id)
						raise ValueError

				if type(next_id) != int:
					self.clean_last_record(thread_id)
					raise ValueError

				self.user_history[thread_id][-1][-1] += (msg, user_response_time,)
				
				next_texts = self.reply_dict[bot_id][next_id].texts.get(self.params.MODE, self.reply_dict[bot_id][next_id].texts[Modes.GENERAL])
				ab_test_index = random.randint(0, len(next_texts)-1) if self.params.ABTEST_CHOICE == -1 else min(len(next_texts)-1, self.params.ABTEST_CHOICE)
				self.user_history[thread_id][-1].append((bot_id, next_id, ab_test_index))

				reply_texts = []

				if next_id == self.config.OPENNING_INDEX and (not self.voice_choice):
					self.sendLocalImage('img/{}.png'.format(bot_id), thread_id=thread_id, thread_type=thread_type)

				for each in next_texts[ab_test_index]:
					reply_text = each.format(name=user_name.capitalize(), problem=problem, bot_name=self.params.bot_name_list[bot_id])
					reply_texts.append(reply_text)
					self.send(Message(text=reply_text), thread_id=thread_id, thread_type=thread_type)
					# if self.voice_choice:
					# 	#system('say -v Victoria ' + reply_text.replace("(", " ").replace(")", " "))#Alex
					# 	self.say(reply_text.replace("(", " ").replace(")", " "))
					# else:
					time.sleep(self.params.SLEEPING_TIME)

				self.user_history[thread_id][-1][-1] += (reply_texts,)

				if next_id == self.config.CLOSING_INDEX or next_id == self.config.ABRUPT_CLOSING_INDEX:

					query_name = client.fetchUserInfo(thread_id)[thread_id].name.split(" ")[0]
					if self.db.user.find({'name': query_name}).count() == 0:
						self.db.user.insert(
								{
									'name':query_name,
									'user_id':thread_id
								}
							)


					self.user_history[thread_id][-1][-1] += ('END_OF_CONVERSATION', user_response_time,)

					self.db.user_history.insert(
							{
								'thread_id':thread_id,
								'user_history': self.user_history[thread_id][-1]
							}
						)



					#client.fetchUserInfo(thread_id)[thread_id].name.split(" ")[0]

					self.delete_all_dict(thread_id)
			except:
				pass




if __name__ == "__main__":
	usage_tips = 'python bot.py --stime SLEEPINGTIME --mode MODE'
	try:
		opts, args = getopt.getopt(sys.argv[1:],'',['stime=', 'bot=', 'mode='])
	except getopt.GetoptError:
		print usage_tips
		sys.exit()

	add_bot_ctl = {}
	for opt, arg in opts:
		if opt == '--stime':
			add_bot_ctl['sleeping_time'] = int(arg)
		elif opt == '--bot':
			add_bot_ctl['bot_choice'] = int(arg)
		elif opt == '--mode':
			add_bot_ctl['mode'] = str(arg)
		else:
			print usage_tips
			sys.exit()

	#collection = db.user_history

	reply_dict = get_text_from_db()

	if os.path.exists("/commuter/nltk_data"):
		nltk.data.path = ["/commuter/nltk_data"] + nltk.data.path

	password_file = open('password.txt','r')
	email = password_file.readline().strip()
	password = password_file.readline().strip()
	print('email: {},  password: {}'.format(email, password))

	client = StressBot(email, password, reply_dict, add_bot_ctl=add_bot_ctl)
	client.listen()