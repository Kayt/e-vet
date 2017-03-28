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
    { "name":"Calf",  "symptoms":"Diphtheria Lives in soil, litter, & unclean stables& enters the body through small scratches or wounds. Difficulty breathing, eating, and drinking.Patches of yellowish, dead tissue appear on the edges of the tongue, gums, & throat.  Often, a nasal discharge occurs"},
    { "name":"bloat", "symptoms":"Gases of fermentation"},
    { "name":"Grain overload", "symptoms":"Indigestion,collapse,frequently death, temperature too high 41 degrees"},
    { "name":"ketosis", "symptoms":"Occurs a week after calving ,mucus covered feces,loss of weight,constipation,hump back posture, odour breath, drop in milk production"},
    { "name":"Pregnancy toxemia", "symptoms":"Decrease in appetite ,faecal production, nose licking ,weakness, depressed"},
    { "name":"Simple indigestion", "symptoms":"Anorexia, rumen becomes full, doughy,excessive fluid,feces usually soft and foul smelling."},
    { "name":"Bacillary Hemoglobinuria", "symptoms":"Temperature too high, red dark urine, jaundice,anemic,dyspnoea,oedema of the brisket."},
    { "name":"Bovine farcy", "symptoms":"Chronic painless,cellulitis in lymph nodes, yellow pus ,ulcers"},
    { "name":"Body ticks", "symptoms":"Ticks all over the body"},
    { "name":"Diahorea","symptoms":"Running stomach"},
    { "name":"Colic", "symptoms":"Improper feeding. Pain, sweating, & constipation, kicking, & groaning."},
    { "name":"Foot rot", "symptoms":"Animals are most apt to contact foot rot when forced to live in wet, muddy, unsanitary lots for long periods of time"},
    { "name":"Founder", "symptoms":"Overeating of grain, or lush, highly improved pasture grasses, Affected animals experience pain and may have fever as high as 106 degrees F" },
    { "name":"Tuberculosis", "symptoms":"Lungs are affected.  However, other organs may be affected.  Some animals show no symptoms; others appear unthrifty & have a cough"}
]
for news in newsSet:
    newsTrainer.train(news['symptoms'], news['name'])

# When you have sufficient trained data, you are almost done and can start to use
# a classifier.
newsClassifier = Classifier(newsTrainer.data, token)

# Now you have a classifier which can give a try to classifiy text of news whose
# category is unknown, yet.
classification = newsClassifier.classify("Overeating of grain, or lush, highly improved pasture grasses, Affected animals experience pain and may have fever as high as 106 degrees F")



# the classification variable holds the detected categories sorted
for cl in classification:
    print cl