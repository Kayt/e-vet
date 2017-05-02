"""
Suppose you have some texts of news and know their categories.
You want to train a system with this pre-categorized/pre-classified 
texts. So, you have better call this data your training set.
"""
from naiveBayesClassifier.tokenizer import Tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier

token = Tokenizer()

newsTrainer = Trainer()

# You need to train the system passing each text one by one to the trainer module.
newsSet =[
    { "name":"Zimbabwe",  "symptoms":"The capital city is Harare"}
]
for news in newsSet:
    newsTrainer.train(news['symptoms'], news['name'])

# When you have sufficient trained data, you are almost done and can start to use
# a classifier.
newsClassifier = Classifier(newsTrainer.data, token)

# Now you have a classifier which can give a try to classifiy text of news whose
# category is unknown, yet.
classification = newsClassifier.classify("harare is the capital, however it used to be called salisbury")



# the classification variable holds the detected categories sorted
for cl in classification:
    print cl