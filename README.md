# SentimentAnalysisApp

Problem statement - There are times when a user writes positive text in the reviews section but gives a 1-star rating. Our goal is to identify such reviews where the semantics of review text does not match rating.
So that the support team can point this to users.

The application takes a csv upload through user and you returns a csv with the reviews where the content doesn’t match ratings. This csv will be in the same format as the DataSet provided. <br><br>
Solution is deployed using Flask at https://kapilve.pythonanywhere.com/senti <br>
Sample data to input is given in the repo as chrome_reviews.csv
