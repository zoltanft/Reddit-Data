# Reddit Data Analysis, by Zoltan Talaber


import praw
# Obtains Reddit instance to see data from the site
r = praw.Reddit(user_agent='Zoltans Data Analysis v0.1',
                client_id='IWSZeiGXbcntlg',
                client_secret='9rGKr9FdRqdPfwtg2KCjvQn39Kg')


# SubReddit class stores all gathered data on a unique subreddit
class SubReddit:
    name = ""
    num_top_posts = 0
    score_total = 0
    highest_score = 0
    common_words = {}


# Word class stores all gathered data on a unique word appearing in the data
class Word:
    name = ""
    count = 0


# Catalogs the data from the top posts from the Reddit instance for later use
def create_top_post_dictionary():
    # keys = subreddit name, values = SubReddit object storing the data
    sub_dict = {}
    word_dict = {}

    # Finds the top x number of submissions from the past year
    top_posts = r.subreddit('all').top('year', limit=1000)

    # Create or add to data on a subreddit by checking which sub each submission is from
    for x in top_posts:
        sub = x.subreddit.display_name
        title = x.title.lower()

        if sub not in sub_dict.keys():
            subreddit = SubReddit()
            subreddit.name = sub
            sub_dict[sub] = subreddit

        sub_dict[sub].num_top_posts += 1
        sub_dict[sub].score_total += x.score

        if x.score > sub_dict[sub].highest_score:
            sub_dict[sub].highest_score = x.score

        formatted_title = ""

        # Rewrites the title, omitting punctuation
        for c in title:
            if c.isalpha() or c == " ":
                formatted_title = formatted_title + c

        # Adds each word from title into word dictionary
        for word in formatted_title.split():
            if word not in word_dict.keys():
                word_dict[word] = Word()
                word_dict[word].name = word
                word_dict[word].count = 0
            word_dict[word].count += 1

    return [sub_dict, word_dict]


# Creates a sorted list of SubReddit objects to display
def sub_list_by_num_top_posts(sub_dict):
    print("Subreddits Listed by Number of Posts in the Top 1000")
    print("Format: # of Top Posts, Total Score across Posts, Single Highest Post Score")
    sub_list = list(sub_dict.values())
    sub_list.sort(key=lambda y: y.num_top_posts, reverse=True)
    for sr in sub_list:
        print(sr.name + ": " + str(sr.num_top_posts) + " | " + str(sr.score_total) +
              " | " + str(sr.highest_score))


# Displays the most commonly ocurring words from the posts processed in create_top_post_dictionary
def common_words(word_dict):
    limit = 50

    print("Top " + str(limit) + " Most Common Words")
    print("Format: word --> number of occurences")
    word_list = list(word_dict.values())
    word_list.sort(key=lambda y: y.count, reverse=True)

    word_limiter = 0
    for w in word_list:
        word_limiter += 1
        print(str(word_limiter) + ") " + w.name + ": " + str(w.count))
        if word_limiter >= limit:
            return


data = create_top_post_dictionary()
# sub_list_by_num_top_posts(data[0])
common_words(data[1])
