from init_reddit_db import initialize_db, upsert_user_data_if_changed

# initialize database
initialize_db()

# example data
user_data_1 = {
    "userID": "u_shraeya",
    "subreddits": ["r/Philosophy", "r/MachineLearning"],
    "posts": ["The Good Place Trolley Problem", "Thoughts on AGI?"],
    "comments": ["Nice post!", "Aw, thank you!"],
    "interest_score": 88.5,
    "sorted_interests": {"AI": 50, "Education": 25, "Philosophy": 13}
}

# insert initial data
upsert_user_data_if_changed(user_data_1)

# simulate a re-scrape with only one change (new comments)
user_data_2 = {
    "userID": "u_shraeya",
    "subreddits": ["r/Philosophy", "r/MachineLearning"], # same
    "posts": ["The Good Place Trolley Problem", "Thoughts on AGI?"],  # same
    "comments": ["Nice post!", "Check this link.", "Interesting take!"],  # changed
    "interest_score": 88.5,  # same
    "sorted_interests": {"AI": 50, "Education": 25, "Philosophy": 13}  # same
}

# run update to data
upsert_user_data_if_changed(user_data_2)
