import sys;
#uncomment bottom line if import praw doesnt work and you installed praw, change the path to the path you get from pip show praw
#sys.path.append("path to where praw installed")
import time
import praw
import csv

f = open("results.txt", "w")
reddit = praw.Reddit(client_id='your_id', client_secret='your_secret', user_agent='your_bot_name')
all_stocks = []

#open list of all stocks and read it
with open('symbols.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        row = ', '.join(row)
        if row.split(",")[0] != "Symbol":
            all_stocks.append(row.split(",")[0])

#get stocks from nyse too
with open('symbols2.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        row = ', '.join(row)
        if row.split(",")[0] != "Symbol" and row.split(",")[0] not in all_stocks:
            all_stocks.append(row.split(",")[0])      
#create the subreddit object
wsb = reddit.subreddit("wallstreetbets")

results = list(wsb.top(limit=None))

d = {}

#cycle through all post titles and check if the mentioned stock exists
for post in results:
    words = post.title.split(" ");
    for word in words:
        if word.isupper():
            if word[0] == "$":
                word = word[1:]
            if (word in all_stocks):
                if word in d:
                    d[word] += 1
                else:
                    d[word] = 1


sorted_arr = []
for key in d:
    sorted_arr.append([d[key], key])

sorted_arr.sort(reverse = True) 

for item in sorted_arr:
    for item in ["Stock ticker:",item[1],"Mentioned:",str(item[0])]:
        print(item.ljust(10), end = '')
        f.write(item.ljust(10))
    print()
    f.write("\n")
f.close()
