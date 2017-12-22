# -*- coding: UTF-8 -*-
import pprint
from pymongo import MongoClient



def get_all_users():
	pymongo_client = MongoClient()
	db = pymongo_client.chatbot
	collection = db.user_history
	name_set = set()
	for each in collection.find():
		name_set.add(each['thread_id'])
	return list(name_set)

def get_user_history(thread_id):
	pymongo_client = MongoClient()
	db = pymongo_client.chatbot
	collection = db.user_history

	for each in collection.find({'thread_id':thread_id}):
		pprint.pprint(each)

if __name__ == "__main__":
	#pprint.pprint(get_all_users())
	get_user_history('100000019168085')

