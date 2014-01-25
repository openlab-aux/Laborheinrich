"""
labissues.py - Lists the lab's issues by priority
Author: Profpatsch
"""

from __future__ import unicode_literals
from willie import module
import requests
import functools

USER = "openlab-aux"
REPO = "orgafoo"

def get_issues(user, repo):
    res = requests.get('https://api.github.com/repos/{}/{}/issues'
                         .format(user, repo))
    issues = res.json()
    return [
        {
            "title": i["title"],
            "id": i["id"],
            "created_at": i["created_at"],
            "updated_at": i["updated_at"],
            "url": i["html_url"],
            "labels": [l["name"] for l in i["labels"]],
        }
        for i in issues
    ]

def map_to_priority(issues, coefficients):
    """Assignes a priority to each issue.

    Args:
        issues: List of issues
        coefficients: Map of keyword to coefficient

    Returns: Tuples of (issue, priority)
    """
    return sorted([
        # Haha, sorry.
        (i, functools.reduce(lambda x,coeff: x*coeff,
                             [coefficients.get(label.encode('utf-8'), 1)
                              for label in i['labels']],
                             1))
        for i in issues
    ], key=lambda i: i[1], reverse=True)

def check_config(bot):
    if bot.config.has_option('labissues', 'coefficients'):
        return True


@module.commands('issues', 'whatdo')
def list_issues(bot, trigger):
    """Lists the first first three issues with the highest priority."""

    if check_config(bot):
        coeffs = bot.config.labissues.get_list('coefficients')
        coeffs = {
            entry.split(":")[0]: float(entry.split(":")[1])
            for entry in coeffs
        }
    else:
        coeffs = []
    issues = get_issues(USER, REPO)
    prio_issues = map_to_priority(issues, coeffs)
    [bot.say("{} (pri: {}): {}".format(i[0]['title'], i[1], i[0]['url']))
     for i in prio_issues[:3]]
