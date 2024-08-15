#!/usr/bin/python3
"""
This module contains a function to count words in all hot posts of a given Reddit subreddit.
"""

import requests


def count_words(subreddit, word_list, after=None, counts={}):
    """
    Recursively queries the Reddit API, parses the titles of all hot articles,
    and prints a sorted count of specified keywords.

    Args:
        subreddit (str): The subreddit to query.
        word_list (list): List of words to count in the titles.
        after (str): The parameter for pagination.
        counts (dict): A dictionary to store the counts of words.

    Returns:
        None
    """
    if not word_list or not subreddit:
        return

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"limit": 100}
    
    if after:
        params["after"] = after

    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        return

    data = response.json()
    children = data["data"]["children"]

    for post in children:
        title = post["data"]["title"].lower()
        for word in word_list:
            word_lower = word.lower()
            if word_lower in title:
                counts[word_lower] = counts.get(word_lower, 0) + title.count(word_lower)

    after = data["data"]["after"]
    if after:
        count_words(subreddit, word_list, after, counts)
    else:
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(f"{word}: {count}")
