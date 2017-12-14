# Twinet

## What is Twinet?

Twinet is a Twitter-based user recommendation service based on three variables:
- pagerank
- closeness centrality
- betweenness centrality

Twinet includes both a "scraper.py" script that, once twurl has been verified on your local machine, extracts data based on a given user and sorts it into an edge-list file that is formatted for parsing by a second "twinet.py" script. This second script takes the data and runs a pagerank, closeness centrality, and betweenness centrality algorithm on it. After these calculations (and a final scoring algorithm) are run, it outputs the top three users recommended for you.

## Installation

Twinet uses Twurl [https://github.com/twitter/twurl].
