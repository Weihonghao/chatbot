# -*- coding: UTF-8 -*-
import pprint
import datetime, time
import sys, getopt
from pymongo import MongoClient
from get_response import get_text_from_db
from collections import defaultdict
from utils import Params


weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def datetime2timetime(t):
	return time.mktime(t.timetuple()) + t.microsecond / 1E6

def get_weekday(t):
	return datetime.datetime.fromtimestamp(t).weekday()

def get_time_interval(start_time, end_time):
	if start_time == -1:
		start_time_formatted = datetime.datetime(1990,1,1)
	else:
		assert type(start_time)==tuple, 'start time should be a tuple'
		assert len(start_time)==6, 'start time should be in format of (year, month, day, hour, minute, second)'
		start_time_formatted = datetime.datetime(start_time[0], start_time[1],start_time[2],\
				hour=start_time[3],minute=start_time[4],second=start_time[5])
	start_time_formatted = datetime2timetime(start_time_formatted)

	if end_time == -1:
		end_time_formatted = datetime.datetime.now()
	else:
		assert type(end_time)==tuple, 'end time should be a tuple'
		assert len(end_time)==6, 'end time should be in format of (year, month, day, hour, minute, second)'
		end_time_formatted = datetime.datetime(end_time[0], end_time[1],end_time[2],\
				hour=end_time[3],minute=end_time[4],second=end_time[5])
	end_time_formatted = datetime2timetime(end_time_formatted)

	assert start_time_formatted < end_time_formatted, 'end time should be later than start time'

	return start_time_formatted, end_time_formatted



def get_all_users(db):
	collection = db.user_history
	name_set = set()
	for each in collection.find():
		name_set.add(each['thread_id'])
	return list(name_set)

def get_user_history(db, thread_id, start_time=-1, end_time=-1):
	collection = db.user_history
	out = open('output/user_history.txt','w')
	reply_dict = get_text_from_db()
	start_time_formatted, end_time_formatted = get_time_interval(start_time, end_time)
	for each in collection.find({'thread_id':thread_id}):
		if start_time_formatted > each['user_history'][0][-1] \
			or end_time_formatted < each['user_history'][-1][-1]:
				continue
		out.write('==================================\n')
		for each_round in each['user_history']:
			#print(each_round) 
			timestamp = datetime.datetime.fromtimestamp(int(each_round[5])).strftime('%c')
			print(each_round[5], timestamp)
			out.write('{}:\n'.format(timestamp))
			for each_sentence in each_round[3]:#reply_dict[each_round[0]][each_round[1]].texts[each_round[3]][each_round[2]]:
				# each_sentence = each_sentence.replace("’","'")
				out.write("BOT: {}\n".format(each_sentence))
			out.write("USER:{}\n".format(each_round[4]))
		out.write('==================================\n')

	out.close()


def get_name_userid_pairs(db):
	collection = db.user
	out = open('output/name_userid_pairs.txt','w')
	out.write('user_id name\n')
	for each in collection.find():
		out.write('{} {}\n'.format(each['user_id'], each['name']))
	out.close()


def date_report(db, start_time=-1, end_time=-1, weekday=()):
	# weekday start from Monday, Monday is 0
	collection = db.user_history
	reply_dict = get_text_from_db()
	start_time_formatted, end_time_formatted = get_time_interval(start_time, end_time)
	user_set = set()
	bot_choice = defaultdict(list)
	weekday_choice = defaultdict(int)
	out = open('output/time_report.txt','w')
	params = Params()
	for each in collection.find({}):
		if start_time_formatted > each['user_history'][0][-1] \
			or end_time_formatted < each['user_history'][-1][-1]:
				continue 
		each_weekday = get_weekday(each['user_history'][0][-1])
		if len(weekday) != 0 and each_weekday not in weekday:
			continue
		user_id = each['thread_id']
		user_set.add(user_id)
		bot_choice[each['user_history'][0][0]].append(user_id)
		weekday_choice[each_weekday] += 1
			
	out.write('total number of user: {}\n'.format(len(user_set)))
	out.write('==================================\n')
	out.write('user list\n')
	for each in user_set:
		out.write("{}\n".format(each))
	out.write('==================================\n')

	if len(weekday) != 0:
		for key, val in weekday_choice.items():
			#print(key, val)
			out.write("There are {} users on {}\n".format(val, weekdays[key]))
		out.write('==================================\n')
	for key, val in bot_choice.items():
		out.write("{} is used {} time(s)\n".format(params.bot_name_list[key], len(val)))
		out.write("{}\n".format(val))
	if len(user_set) > 0:
		out.write('==================================\n')
	out.close()

if __name__ == "__main__":

	usage_tips = 'python db_check.py --mode MODE'
	try:
		opts, args = getopt.getopt(sys.argv[1:],'',['mode='])
	except getopt.GetoptError:
		print usage_tips
		sys.exit()

	pymongo_client = MongoClient()
	db = pymongo_client.textbot

	for opt, arg in opts:
		if opt == '--mode':
			if str(arg) == 'voice':
				db = pymongo_client.voicebot
		else:
			print usage_tips
			sys.exit()

	
	pprint.pprint(get_all_users(db))
	#get_user_history(db, '100000019168085')
	get_name_userid_pairs(db)
	get_user_history(db, '100000019168085', start_time=(2018, 1, 19, 0, 10, 0), end_time=(2018, 5, 1, 0, 10, 0))
	date_report(db, start_time=(2018, 1, 19, 0, 10, 0), end_time=(2018, 5, 1, 11, 40, 0), weekday=[0])