# NewsQRanking
Created for HackGT 7 2020. Sentiment Analysis model using supervised machine learning for bias in the media to determine a news ranking algorithm.
link to website "got bias?": https://github.gatech.edu/pages/pshah365/gotbias/

## Inspiration
To create a platform that could filter out biased and unreliable news sources that can influence constituents political views.

## What it does
"got bias?" filters news articles and ranks them according to a base algorithm that favors unbiased writers and reliable sources. On the "got bias?" website, a list of the top-ranked news sources is displayed. The algorithm also takes news date into account, so the most recent news is always near the top of the rankings.

## How we built it
The sentiment analysis model was trained with data that was web-scraped using pythons scripts from news articles. The sentiment analysis model used Naive Bayes Classifier to analyze for bias. The ranked articles were then input into an Excel spreadsheet. The "got bias?" website was made with HTML/CSS and hosted using GitHub.

## What's next for got bias?
We hope to deploy the bias checker remotely across all platforms so that anyone can use it.
