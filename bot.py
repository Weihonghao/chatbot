# -*- coding: UTF-8 -*-

import time
import random
import string
import sys, getopt

from fbchat import log, Client
from fbchat.models import *
from collections import *
from os import system
from utils import *
from get_response import get_text_from_db
from pymongo import MongoClient
from gtts import gTTS



class StressBot(Client):
	def __init__(self, email, password, reply_dict, mongo_db, voice_choice=False, **kwargs):
		Client.__init__(self, email, password)
		self.user_history = defaultdict(list)
		# self.user_history {thread_id: [[(bot_id, in_group_id, ab_test_id, msg, user_response_time), () ....], [], [], ...]}
		self.reply_dict = reply_dict
		self.user_name_dict = {}
		self.user_bot_dict = {}
		self.user_topic_dict = {}
		self.user_problem_dict = {}
		self.params = Params()
		self.config = Config()
		self.topics = Topics()

		self.db = mongo_db
		self.voice_choice = voice_choice

		additional_bot_control = kwargs.get('add_bot_ctl',{})
		if 'sleeping_time' in additional_bot_control:
			self.params.set_sleeping_time(additional_bot_control.get('sleeping_time'))

		if 'bot_choice' in additional_bot_control:
			self.params.set_bot_choice(additional_bot_control.get('bot_choice'))


	def say(self, text):
		tts = gTTS(text=text, lang='en')
		tts.save("test.mp3")
		system("mpg321 test.mp3")

	def clean_last_record(self, thread_id):
		if thread_id in self.user_history and len(self.user_history[thread_id]) > 0:
			return self.user_history[thread_id].pop()

	def delete_all_dict(self, thread_id, delete_name=True):
		if thread_id in self.user_bot_dict:
			del self.user_bot_dict[thread_id]
		if thread_id in self.user_topic_dict:
			del self.user_topic_dict[thread_id]
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

			msg = message_object.text.lower()
			msg = ' '.join(msg.split()) # substitute multiple spaces into one
			if msg[-1] in list(string.punctuation):
				msg = msg[:-1]
			if not chcek_rubbish_word(msg):
				reply_text = "Sorry I cannot understand your word. Could you repeat it again?"
				self.send(Message(text=reply_text), thread_id=thread_id, thread_type=thread_type)
				if self.voice_choice:
					#system('say -v Victoria ' + reply_text.replace("(", " ").replace(")", " "))#Alex
					self.say(reply_text.replace("(", " ").replace(")", " "))
				if not self.voice_choice:
					time.sleep(self.params.SLEEPING_TIME)
				return None

			if msg.strip().lower() == 'restart':
				self.clean_last_record(thread_id)
				self.delete_all_dict(thread_id)
				return None
			
			if thread_id not in self.user_history or len(self.user_history[thread_id]) == 0 \
				or len(self.user_history[thread_id][-1]) == 0 \
					or len(self.user_history[thread_id][-1][-1]) < 2 \
						or self.user_history[thread_id][-1][-1][1] == self.config.CLOSING_INDEX:
							_bot_choice = self.user_bot_dict[thread_id] if thread_id in self.user_bot_dict else self.params.BOT_CHOICE
							bot_id = random.randint(0, self.params.BOT_NUM-1) if _bot_choice == -1 else _bot_choice
							self.user_history[thread_id].append([(bot_id, self.config.START_INDEX, 0)])
			bot_id, current_id, _ = self.user_history[thread_id][-1][-1]
			next_id = self.reply_dict[bot_id][current_id].next_id


			if current_id == self.config.OPENNING_INDEX and  find_problem(msg)[0] != None:
				self.user_problem_dict[thread_id], self.user_topic_dict[thread_id] = find_problem(msg)
			problem = self.user_problem_dict.get(thread_id, 'problem')
			topic = self.user_topic_dict.get(thread_id, self.topics.GENERAL)

			if msg.strip().lower() == 'change bot':
				self.clean_last_record(thread_id)
				self.delete_all_dict(thread_id, delete_name=False)
				while True:
					tmp = random.randint(0, self.params.BOT_NUM-1)
					if tmp != bot_id:
						self.user_bot_dict[thread_id] = tmp
						break
				return None

			if current_id == self.config.START_INDEX:
				for each in ['i am', 'i\'m', 'this is', 'name is']:
					_index = msg.lower().find(each)
					if _index != -1:
						result = msg.lower()[_index + len(each)+1:]
						result = result.split()[0]
						for each_punc in list(string.punctuation):
							result = result.replace(each_punc,"")
						if len(result) > 0 and len(result) < 20:
							self.user_name_dict[thread_id] = result

			if current_id == self.config.OPENNING_INDEX and any(map(lambda x: x != -1, [msg.lower().find(each) for each in ['nothing', 'not now', 'don\'t know']])):
				next_id = self.config.DK_INDEX

			user_name = client.fetchUserInfo(thread_id)[thread_id].name.split(" ")[0]
			user_name = self.user_name_dict.get(thread_id, user_name)


			decider_dict = {
				self.config.DEFAULT_YES:find_keyword,
				self.config.DEFAULT_NO:find_keyword,
				self.config.DEFAULT_DK:find_keyword,
				self.config.DEFAULT_OTHERS:always_true,
			}


			keyword_dict = {
				self.config.DEFAULT_YES:['yes', 'ok', 'sure', 'right'],
				self.config.DEFAULT_NO:['no', 'not',  'neither', 'neg', 'don\'t', 'doesn\'', 'donnot', 'dont', '\'t', 'nothing'],
				self.config.DEFAULT_DK:["dk", "dunno", "dno", "don't know"]
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

			self.user_history[thread_id][-1][-1] += (topic, msg, user_response_time,)
			
			next_texts = self.reply_dict[bot_id][next_id].texts.get(topic, self.reply_dict[bot_id][next_id].texts[self.topics.GENERAL])
			ab_test_index = random.randint(0, len(next_texts)-1) if self.params.ABTEST_CHOICE == -1 else min(len(next_texts)-1, self.params.ABTEST_CHOICE)
			self.user_history[thread_id][-1].append((bot_id, next_id, ab_test_index))
			# if not self.voice_choice:
			# 	time.sleep(self.params.SLEEPING_TIME)
			for each in next_texts[ab_test_index]:
				reply_text = each.format(name=user_name, problem=problem, bot_name=self.params.bot_name_list[bot_id])
				self.send(Message(text=reply_text), thread_id=thread_id, thread_type=thread_type)
				if self.voice_choice:
					#system('say -v Victoria ' + reply_text.replace("(", " ").replace(")", " "))#Alex
					self.say(reply_text.replace("(", " ").replace(")", " "))
				else:
					time.sleep(self.params.SLEEPING_TIME)

			if next_id == self.config.CLOSING_INDEX:

				query_name = client.fetchUserInfo(thread_id)[thread_id].name.split(" ")[0]
				if self.db.user.find({'name': query_name}).count() == 0:
					self.db.user.insert(
							{
								'name':query_name,
								'user_id':thread_id
							}
						)


				self.user_history[thread_id][-1][-1] += (topic, 'END_OF_CONVERSATION', user_response_time,)

				self.db.user_history.insert(
						{
							'thread_id':thread_id,
							'user_history': self.user_history[thread_id][-1]
						}
					)



				#client.fetchUserInfo(thread_id)[thread_id].name.split(" ")[0]

				self.delete_all_dict(thread_id)




if __name__ == "__main__":
	usage_tips = 'python bot.py --voice'
	try:
		opts, args = getopt.getopt(sys.argv[1:],'',["voice", 'stime=', 'bot='])
	except getopt.GetoptError:
		print usage_tips
		sys.exit()

	voice_choice = False
	add_bot_ctl = {}
	for opt, arg in opts:
		if opt == '--voice':
			voice_choice = True
		elif opt == '--stime':
			add_bot_ctl['sleeping_time'] = int(arg)
		elif opt == '--bot':
			add_bot_ctl['bot_choice'] = int(arg)
		else:
			print usage_tips
			sys.exit()

	pymongo_client = MongoClient()
	db = pymongo_client.chatbot
	#collection = db.user_history

	reply_dict = get_text_from_db()
	email = "stressbotcommuter@gmail.com"
	password = "stressbot@commuter"
	client = StressBot(email, password, reply_dict, db, voice_choice, add_bot_ctl=add_bot_ctl)
	client.listen()