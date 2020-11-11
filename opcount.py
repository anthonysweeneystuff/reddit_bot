import praw
import time

f = open("settings.conf", "r")
lines_unformatted = f.readlines()
f.close()
lines = []

for line in lines_unformatted:
    lines.append(line.split('=')[1].rstrip())


reddit = praw.Reddit(client_id=lines[0],
                    client_secret=lines[1],
                    username=lines[2],
                    password=lines[3],
                    user_agent=lines[4])

while True:

    home_sub = lines[5]
    sub_to_count = lines[6]
 
    subreddit = reddit.subreddit(home_sub).new(limit=25)

    for submission in subreddit:

        for comment in submission.comments:
            if comment.body == 'do it working?':
                comment_i_want_to_reply_to = comment
                authors = []
                for response in comment.replies:
                    authors.append(response.author)
                if lines[2] not in authors:
                    sub_post_count = 0
                    total_post_count = 0
                    for comment in reddit.redditor(str(submission.author)).comments.new(limit=None):
                        total_post_count += 1
                        if comment.subreddit == sub_to_count:
                            sub_post_count += 1
                            print('found')

                    message = "The user " + str(submission.author) + \
                    " has " + str(sub_post_count) + " posts in " + "/r/" + \
                    sub_to_count + " out of " + str(total_post_count) + \
                    " total posts. This accounts for approximately " + \
                    str(round(sub_post_count/total_post_count * 100, 2)) + "%" + " of the user's posts."

                    comment_i_want_to_reply_to.reply(message)
                    print('Message posted. Timing out for 5 seconds...')
                    time.sleep(5)


