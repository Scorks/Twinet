# Twinet

## What is Twinet?

Twinet is a Twitter-based user recommendation service based on three variables:
- **pagerank**
- **closeness centrality**
- **betweenness centrality**

Twinet includes both a "scraper.py"script that, once twurl has been verified on your local machine, extracts data based on a given user and sorts it into an edge-list file that is formatted for parsing by a second "Twinet.py" script. This second script takes the data and runs a pagerank, closeness centrality, and betweenness centrality algorithm on it. After these calculations (and a final scoring algorithm) are run, it outputs the top three users recommended for you.

## Installation

Twinet uses the curl-based API wrapper "Twurl" [https://github.com/twitter/twurl]. Installation instructions are available from the linked GitHub page. After installing and verifying your account, you can begin to run the Twinet scripts.

## Usage

To use Twinet (after Twurl has been authenticated), within the terminal, run:

`python scraper.py <screen_name> <follower_limit>`

Where **screen_name** is the name of the user you wish to receieve recommendations for, and **follower_limit** is the cutoff point (as to ensure that the scraper does not take an extremely long time due to Twitter's API-call limit). This scraper may take some time, so if you intend to acquire a large set of data, it is best to leave it running over some hours. An example file has been provided within the project.

After the scraper has finished running, you can use the **Twinet.py** script and pass in the newly created 'final.txt' file as the edge-list file. Also, select an alpha and beta value you would like to use for the pagerank algorithm:

`python Twinet.py final.txt <alpha-value> <beta-value>`

This will output the three top users recommended for you to the terminal.
