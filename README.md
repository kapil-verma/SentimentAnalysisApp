# SentimentAnalysisApp

<em>Problem statement</em> - There are times when a user writes positive text in the reviews section but leaves a 1-star rating by mistake. Our goal is to identify such reviews where the semantics of review text does not match rating.
So that the app support team can point this to users.

The application takes a csv upload through user and returns a csv with the reviews where the content doesn’t match ratings. This output csv will be in the same format as the DataSet provided. <br><br>
Solution is deployed using Flask at https://kapilve.pythonanywhere.com/senti <br>
Sample data to input is given in the repo as `data/chrome_reviews.csv`
<br><br>
A similar solution to execute a Grammer Check is developed in this [notebook](https://colab.research.google.com/drive/1yrSu0F8tWMT4eUmPFLc0dM4hFiWEV9_D?usp=sharing) which is implemented on this data `data/review_data.csv`
