from flask import render_template, redirect, url_for, request, session, flash
from flask_login import login_user, logout_user, current_user, login_required

from . import app, db, login_manager
from flask import render_template
from .models import Question, User, Disease, Farmer
from .forms import SignupForm, LoginForm, AddDiseaseForm

from textblob import TextBlob

import twilio.twiml

from .naiveBayesClassifier.tokenizer import Tokenizer
from .naiveBayesClassifier.trainer import Trainer
from .naiveBayesClassifier.classifier import Classifier

token = Tokenizer()

newsTrainer = Trainer()

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
    { "name":"Diahorea", "symptoms":"Running stomach"},
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


@login_manager.user_loader
def load_user(userid):
	return User.query.get(int(userid))

@app.route('/message', methods=['GET','POST'])
def sms_survey():
    response = twilio.twiml.Response()
    body = request.values.get('Body', None)
    phone = request.values.get('From', None)

    if body is not None:
        blob = TextBlob(body)

        if 'register' in blob.lower():
            new = blob.split(' ')
            farmer = Farmer(number=phone, name=new[1], surname=new[2], location=" ".join(new[3:]))
            db.session.add(farmer)
            db.session.commit()
            response.message('{} you have been added successfully!'.format(farmer.name))
        else:
            classification = newsClassifier.classify(body)
            for cl in classification:
                if cl[1] > 0.1:
                    response.message(cl[0])
                else:
                    response.message('Your query has been forwarded to experts you will be texted the results')
                    ques = Question(content=body)
                    db.session.add(ques)
                    db.session.commit()

    response.message('Please specify the symptoms that you are seeing')

    return str(response)


@app.route('/')
@app.route('/index')
@login_required
def index():
    requests = Question.query.all()
    return render_template('index.html', requests=requests)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None:
            login_user(user, form.remember_me.data)
            flash("logged in successfully as {}".format(user.username))
            return redirect(request.args.get('next') or url_for('index'))
        flash("Incorrect username or password")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('.login'))
    return render_template("signup.html", form=form)

@app.route('/add', methods=["GET","POST"])
@login_required
def add():
    form = AddDiseaseForm()
    if form.validate_on_submit():
        new = Disease(name=form.name.data, symptoms=form.symptoms.data,remedy=form.remedy.data)
        db.session.add(new)
        db.session.commit()
        flash('Diesease added to database!')
        return redirect(url_for('index'))
    return render_template('addDiesease.html', form=form)