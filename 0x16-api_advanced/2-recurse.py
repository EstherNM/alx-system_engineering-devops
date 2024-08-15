#!/usr/bin/python3
"""
This module contains a recursive function to query the Reddit API
and return a list of titles for all hot articles in a given subreddit.
If no results are found, the function returns None.
"""

import requests


def recurse(subreddit, hot_list=[], after=""):
    """
    Recursively queries the Reddit API to get the titles of hot articles
    from a specified subreddit.

    Args:
        subreddit (str): The subreddit to query.
        hot_list (list): The list to store titles of hot articles.
        after (str): The parameter for pagination.

    Returns:
        list: A list of titles of hot articles, or None if the subreddit is invalid.
    """
    req = requests.get(
        "https://www.reddit.com/r/{}/hot.json".format(subreddit),
        headers={"User-Agent": "Custom"},
        params={"after": after},
    )

    if req.status_code == 200:
        for get_data in req.json().get("data").get("children"):
            dat = get_data.get("data")
            title = dat.get("title")
            hot_list.append(title)
        after = req.json().get("data").get("after")

        if after is None:
            return hot_list
        else:
            return recurse(subreddit, hot_list, after)
    else:
        return None
