## Twitter Data Scraper that goes 3 layers of data deep
## Please ensure that you have Twurl installed and verified before running

import sys
import os
import io
import time

layer_1 = []
layer_2 = []
following_dict = {} # dictionary to hold all follower data

USER_ID = sys.argv[1]
CUTOFF = sys.argv[2]

init_cmd = 'twurl "/1.1/friends/ids.json?cursor=-1&screen_name=' + USER_ID + '&count=' + CUTOFF + '"'

os.system(init_cmd + ' %s > out.txt') # outputs all initial followers

# split into a list of followers of initial user--------------------------------------------------------

initial_file = open('out.txt', 'r').read()
initial_file = initial_file.split('[', 1)[-1]
initial_file = initial_file.split(']', 1)[0]
initial_file = initial_file.split(',')

for item in iter(initial_file):
	if item:
		layer_1.append(item)

for user in layer_1:
	sys.stdout.write("\r Working...")
	sys.stdout.flush()
	cmd = 'twurl "/1.1/followers/ids.json?cursor=-1&id=' + user + '&count=' + CUTOFF + '"'
	os.system(cmd + ' %s > data1.txt')
	if '"code":88' in open('data1.txt').read():
		for i in range(900):
			time.sleep(1)
			i = float(i/9)
			sys.stdout.write("\r%d%%   Progress" % i)
			sys.stdout.flush()
		os.system(cmd + ' %s > data1.txt')

	following_file = open('data1.txt', 'r').read()
	following_file = following_file.split('[', 1)[-1]
	following_file = following_file.split(']', 1)[0]
	following_file = following_file.split(',')

	for item in iter(following_file):
		if item:
			if (item.isdigit() and user.isdigit()):
				layer_2.append(item)
				addition = item + "    " + user
				final_file = open('final.txt', 'a') # where a = append
				final_file.write("%r\n" %addition)
				final_file.close()
			else:
				continue

for user in layer_2:
	sys.stdout.write("\r Working...")
	sys.stdout.flush()
	cmd = 'twurl "/1.1/followers/ids.json?cursor=-1&id=' + user + '&count=' + CUTOFF + '"'
	os.system(cmd + ' %s > data1.txt')
	if '"code":88' in open('data1.txt').read():
		for i in range(900):
			time.sleep(1)
			i = float(i/9)
			sys.stdout.write("\r%d%%    Progress" % i)
			sys.stdout.flush()
		os.system(cmd + ' %s > data1.txt')

	following_file = open('data1.txt', 'r').read()
	following_file = following_file.split('[', 1)[-1]
	following_file = following_file.split(']', 1)[0]
	following_file = following_file.split(',')

	for item in iter(following_file):
		if item:
			if (item.isdigit() and user.isdigit()):
				addition = item + "    " + user # append to final file, 'user' [tab] 'user2'
				final_file = open('final.txt', 'a') # where a = append
				final_file.write("%r\n" %addition)
				final_file.close()
			else:
				continue

# When all importing is completed:

final_file = open('final.txt', 'w')
for item in iter(final_file):
	item.replace("'", "")

os.remove("data1.txt")