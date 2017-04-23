from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import desc

import twilio.twiml
from google.cloud import translate
from textblob import TextBlob

from . import app, basic_auth, db, login_manager
from .forms import AddDiseaseForm, LoginForm, SignupForm, EditForm
from .models import Disease, Farmer, Question, User
from .naiveBayesClassifier.classifier import Classifier
from .naiveBayesClassifier.tokenizer import Tokenizer
from .naiveBayesClassifier.trainer import Trainer

token = Tokenizer()

symptomTrainer = Trainer()

symptomSet =[
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
    { "name":"Tuberculosis", "symptoms":"Lungs are affected.  However, other organs may be affected.  Some animals show no symptoms; others appear unthrifty & have a cough"},
    { "name":"Calf", "symptoms":"calf having difficulties in breathing, sore throat ,nasal mucus discharge, dead tissues on gums" },
    { "name":"Calf", "symptoms":"Calf has difficulties in breathing, eating, and drinking.  Patches of yellowish, dead tissue appear on the edges of the tongue, gums, & throat." },
    { "name":"Calf", "symptoms":"Small yellowish dead tissue on the tongue ,gums and throat ,and difficulties in breathing on my calf" },
    { "name":"Calf", "symptoms":"My calf ,has Dead tissues on the gums ,throats,tongue,which are yellow in colour and problems in breathing, eating and drinking" },
    { "name":"Calf", "symptoms":"Calf ,Problems in feeding and has yellow patches of dead tissues on the throat ,gums and tongue " },
    { "name":"Calf", "symptoms":"Patches of yellowish, dead tissue appear on the edges of the tongue, gums, & throat and not breathing properly." },
    { "name":"Calf", "symptoms":"Calves not eating and drinking and have problems in breathing" },
    { "name":"Calf", "symptoms":"calf is breathing problem" },
    { "name":"Calf", "symptoms":"calf does not drink well sikudya" },
    { "name":"Calf", "symptoms":"calf will not drink sikudya and difficulty breathing" },
    { "name":"Calf", "symptoms":"Patches of dead tissues on the calves tongue ,gums and throats" },
    { "name":"Calf", "symptoms":"Gums cracking ,showing dead tissues and having difficulties in feeding and breathing" },
    { "name":"Grain overload", "symptoms":"Indigestion,collapse,frequently death, temperature too high 41 degrees" },
    { "name":"Grain overload", "symptoms":"Cows eating too much maize " },
    { "name":"Grain overload", "symptoms":"Cows failing to digest properly and die quickly" },
    { "name":"Grain overload", "symptoms":"Cows temperature is too high up to 41 degrees  and  sudden death" },
    { "name":"Grain overload", "symptoms":"Cows usually collapse and failing to digest in a normal way " },
    { "name":"Grain overload", "symptoms":"Temperature of cows to high and collapse followed by sudden death " },
    { "name":"Grain overload", "symptoms":"Frequent death of cows and failing to digest properly " },
    { "name":"Grain overload", "symptoms":"Failing to digest food and sudden death " },
    { "name":"Grain overload", "symptoms":"41 degress temperature,failing to digest ,collapsing and  sudden death" },
    { "name":"ketosis", "symptoms":"Occurs a week after calving ,mucus covered feces,loss of weight,constipation,hump back posture, odour breath, drop in milk production" },
    { "name":"ketosis", "symptoms":"Cow milk production decreasing ,bad has a bad odour faeces covered with mucus after a week of calving" },
    { "name":"ketosis", "symptoms":"Cows losing weight, failing to pass dirty ,drop in milk production" },
    { "name":"ketosis", "symptoms":"Cows having constipation, losing weight,feaces covered with mucus" },
    { "name":"ketosis", "symptoms":"Changes in milk production after calving and losing weight ,and bad odour" },
    { "name":"ketosis", "symptoms":"Cows having  a hump back posture ,drop in milk production and constipation" },
    { "name":"ketosis", "symptoms":"Murky feaces,loss of weight ,constipation, bad odour in cows" },
    { "name":"ketosis", "symptoms":"My cow has a bad odour and its losing weight." },
    { "name":"Pregnancy toxemia", "symptoms":"Decrease in appetite ,faecal production, nose licking ,weakness, depressed" },
    { "name":"Pregnancy toxemia", "symptoms":"My cow does not have appetite ,and its always weak" },
    { "name":"Pregnancy toxemia", "symptoms":"Cow is losing appetite ,looking depressed, always licking its nose" },
    { "name":"Pregnancy toxemia", "symptoms":"Faecal production increasing in my cow and its always weak ,and has no appetite" },
    { "name":"Pregnancy toxemia", "symptoms":"Loss of appetite, nose licking,weakness,and looking depressed in cows" },
    { "name":"Pregnancy toxemia", "symptoms":"Eating too little ,increase in faecal production and feeling weak all the time in female cows " },
    { "name":"Pregnancy toxemia", "symptoms":"Nose licking and losing weight and depression in cows" },
    { "name":"Simple indigestion", "symptoms":"Anorexia, rumen becomes full, doughy, excessive fluid,feces usually soft and foul smelling." },
    { "name":"Simple indigestion", "symptoms":"Cows getting supper thin and watery faeces " },
    { "name":"Simple indigestion", "symptoms":"Feaces to smelly and to watery.Cows to thin" },
    { "name":"Simple indigestion", "symptoms":"Too soft faeces and have a foul smell ,and too thin" },
    { "name":"Simple indigestion", "symptoms":"Anorexia ,and a foul smell coming from faeces" },
    { "name":"Simple indigestion", "symptoms":"Excessive fluids ,and watery feaces with a foul smell" },
    { "name":"Simple indigestion", "symptoms":"feces usually soft and foul smelling" },
    { "name":"Simple indigestion", "symptoms":"My cows rumen becomes full, doughy, excessive fluid, and faeces too watery" },
    { "name":"Simple indigestion", "symptoms":"My cow is getting to thin and passes out smelly faeces which are too watery" },
    { "name":"Colic", "symptoms":"Improper feeding. Pain, sweating, & constipation, kicking, & groaning. " },
    { "name":"Colic", "symptoms":"Cows not eating properly ,sweats a lot and groans" },
    { "name":"Colic", "symptoms":"Cows shows sign of pain and always sweating and suffers from constipation" },
    { "name":"Colic", "symptoms":"Kicking,groaning,sweating in cows " },
    { "name":"Colic", "symptoms":"Cows not able to pass out dirty and does not rat properly." },
    { "name":"Colic", "symptoms":"Cows not feeding well and suffers from groaning pains at the same time suffers from constipation" },
    { "name":"Colic", "symptoms":"Cows sweats, groans ,and does not pass out dirty" },
    { "name":"Foot rot.", "symptoms":"Animals are most apt to contact foot rot when forced to live in wet, muddy, unsanitary lots for long periods of time." },
    { "name":"Foot rot.", "symptoms":"Cracks between cows hooves" },
    { "name":"Foot rot.", "symptoms":"Sores on animals feet" },
    { "name":"Foot rot.", "symptoms":"Unpleasant sores on cows feet" },
    { "name":"Foot rot.", "symptoms":"Cows not walking properly due to sores between the hooves" },
    { "name":"Foot rot.", "symptoms":"Cracks and sores on cows" },
    { "name":"Foot rot.", "symptoms":"Worms coming out of foot " },
    { "name":"Tuberculosis", "symptoms":"Lungs are affected.  However, other organs may be affected.  Some animals show no symptoms; others appear unthrifty & have a cough. " },
    { "name":"Tuberculosis", "symptoms":"Cow has a running nose and always coughing" },
    { "name":"Tuberculosis", "symptoms":"Red  teary eyes and a cough" },
    { "name":"Parturient Paresis(Milk fever)", "symptoms":"Inappetence,dullness,cold ears, tremors of muscle (limbs and head) grinding of teeth,incordination may occur, not passing urine and feces,unable to stand .temperature decrease" },
    { "name":"Parturient Paresis(Milk fever)", "symptoms":"Cows trembling ,grinding of teeth, not able to pass urine" },
    { "name":"Parturient Paresis(Milk fever)", "symptoms":"Incoordination in the body parts of the cows and temperature decreases" },
    { "name":"Parturient Paresis(Milk fever)", "symptoms":"Unable to pass urine and feaces,cold ears in cows .grinding of teeth" },
    { "name":"Parturient Paresis(Milk fever)", "symptoms":"Tremors of muscle in cows and incoordination ,inability to pass urine" },
    { "name":"Parturient Paresis(Milk fever)", "symptoms":"My cow is not passing out urine and faeces, unable to stand on its own and its temperature is too low " },
    { "name":"Parturient Paresis(Milk fever)", "symptoms":"Inappetence,dullness, ears are cold, tremors of muscle (appendages and head) crushing of teeth,incordination may happen, not passing pee and feces,unable to stand .temperature diminish" },
    { "name":"Parturient Paresis(Milk fever)", "symptoms":"Grinding off teeth and trembling ,and have constipation ,also looking dull in cows" },
    { "name":"Anthrax", "symptoms":"Fever, stomach pain,trembling,hematuria,blood-shivered diarrehea,low drain creation with blood" },
    { "name":"Anthrax", "symptoms":"Fever, abdominal pain,trembling,hematuria,blood-tingled diarrehea,low milk production with blood," },
    { "name":"Anthrax", "symptoms":"Faeces with blood, and low milk coming out with blood stains" },
    { "name":"Anthrax", "symptoms":"Milk production with blood and fever .running stomach" },
    { "name":"Anthrax", "symptoms":"Shivering ,blood in feaces,and milk with blood stains" },
    { "name":"Anthrax", "symptoms":"Stomach Ache, milk with blood ,fever" },
    { "name":"Warts", "symptoms":"A virus causes warts. Protruding growths on the skin" },
    { "name":"Warts", "symptoms":"Cows having lumps on the skin" },
    { "name":"Warts", "symptoms":"cows developing pimples on the skin" },
    { "name":"Warts", "symptoms":"Pimples all over the skin  on a cow" },
    { "name":"Warts", "symptoms":"Growth on the skin of cattle" },
    { "name":"Hemorrhagic Septicemia.","symptoms":"Facing difficulty in breathing ,a discharge from the nose" },
    { "name":"Hemorrhagic Septicemia.","symptoms":"Watery Discharge from the nose and the eyes ,and having problems in breathing" },
    { "name":"Hemorrhagic Septicemia.","symptoms":"eyes & nose bringing out discharge and coughing"  },
    { "name":"Abomasal displacement." , "symptoms":"Decrease in milk production and loss weight " },
    { "name":"Abomasal displacement." , "symptoms":"Aneroxia,decrease milk production" },
    { "name":"Abomasal displacement." , "symptoms":"Serious  loss of weight and no milk coming out" },
    { "name":"Abomasal displacement." , "symptoms":"Milk not coming out and losing weight" },
    { "name":"Abomasal displacement." , "symptoms":"Too little milk coming out and weight loss" },
    { "name":"Pullorum." , "symptoms":"Infected chicks huddle together with their eyes closed, wings drooped, and feathers ruffled, & have foamy droppings." },
    { "name":"Pullorum." , "symptoms":"Foamy dropping and huddling together of chicks" },
    { "name":"Pullorum." , "symptoms":"Eyes are always closed and chicks have foamy droppings " },
    { "name":"Pullorum." , "symptoms":"Chicks have ruffled feathers and the wings are drooped" },
    { "name":"Pullorum." , "symptoms":"Drooped wings and chicks are always huddled together" },
    { "name":"Pullorum." , "symptoms":"Chicks eyes are always closed ,and feathers are ruffled with foamy droppings" },
    { "name":"Coccidiosis.", "symptoms":"high mortality rate, bloody droppings, & sudden death loss of appetite, weakness, pale comb, & low production." },
    { "name":"Coccidiosis.", "symptoms":"Chicks die at a fast rate ,loss of appetite ,and always weak" },
    { "name":"Coccidiosis.", "symptoms":"Chicks has no appetite and they are losing weight and feeling weak" },
    { "name":"Coccidiosis.", "symptoms":"Loss of appetite and weakness in chicks ,affected chicks huddling together" },
    { "name":"Coccidiosis.", "symptoms":"Low production of chicks ,weakness and sudden death" },
    { "name":"Coccidiosis.", "symptoms":"high mortality rate, bloody droppings, & sudden death Loss of appetite." },
    { "name":"Coccidiosis.", "symptoms":"sudden death loss of appetite, weakness, pale comb, & low production in chicken" },
    { "name":"Pneumonia." , "symptoms":"dullness, failing appetite, fever & difficulty breathing" },
    { "name":"Pneumonia." , "symptoms":"Chicks are always coughing and have no appetite" },
    { "name":"Pneumonia." , "symptoms":"Chicks facing difficulties in breathing and fever" },
    { "name":"Pneumonia." , "symptoms":"failing appetite, fever & difficulty breathing in poultry" },
    { "name":"Pneumonia." , "symptoms":"Chicks are dull and have no appetite" },
    { "name":"Pneumonia." , "symptoms":"Fever  and not eating well accompanied by not eating" },
    { "name":"Newcastle." , "symptoms":"Chicks make circular movements, walk backwards, fall, twist their necks so that their heads are lying on their backs, cough, sneeze, and develop high fever & diarrhoea" },
    { "name":"Newcastle." , "symptoms":"Chicks walk backwards, fall and twist their heads." },
    { "name":"Newcastle." , "symptoms":"Chicks turn their heads and lying on their backs, cough, sneeze, have high fever & diarrhoea." },
    { "name":"Newcastle." , "symptoms":"Chicks coughing, twist their necks ,have a diarrhoea" },
    { "name":"Newcastle." , "symptoms":"Chicks walk in circular movements, and have diarrhoea, and have a high fever" },
    { "name":"Newcastle." , "symptoms":"Chicken has a high fever, coughing and sneezing also walking backwards" },
    { "name":"Newcastle." , "symptoms":"Twisted necks and walking backwards  of chicken" },
    { "name":"Newcastle." , "symptoms":"Chicks lie on their heads ,coughing and sneezing" },
    { "name":"Newcastle." , "symptoms":"Diarrhoea in chicks and walk backwards  in a circular movements" },
    { "name":"Newcastle." , "symptoms":"Chicken developing higher fever, sneezing and walk backwards " },
    { "name":"Enterotoxemia" , "symptoms":"Constipation is early symptom & sometimes followed by diarrhoea.in chicks" },
    { "name":"Enterotoxemia" , "symptoms":"Chicks unable to pass out dirty and  having diarrhoea" },
    { "name":"Enterotoxemia" , "symptoms":"Constipation and diarrhoea in chicken " },
    { "name":"Enterotoxemia" , "symptoms":"Chicks have a running stomach ,not passing faeces" },
    { "name":"Cannibalism" , "symptoms":"Chicken and turkey picking at unfeather skin on head,comb,wattles,and toes" },
    { "name":"Cannibalism" , "symptoms":"Chicken eating each on the head. " },
    { "name":"Cannibalism" , "symptoms":"Chicken eating each on the head. " },
    { "name":"Cannibalism" , "symptoms":"Chicken eating each on the head. " },
    { "name":"Cannibalism" , "symptoms":"Chicken eating each on the head. " },
    { "name":"Cannibalism" , "symptoms":"Chicken eating each on the head. " },
    { "name":"Cannibalism" , "symptoms":"Chicken eating each on the head. " },
    { "name":"Cannibalism" , "symptoms":"Chicken eating each on the head. " },
    { "name":"Cannibalism" , "symptoms":"Chicken eating each on the head. " },
    { "name":"Cannibalism" , "symptoms":"Chicken biting each other on the head, comb and toes" },
    { "name":"Cannibalism" , "symptoms":"Turkeys picking at unfeather skin" },
    { "name":"Cannibalism" , "symptoms":"Birds biting each other on unfeather skin" },
    { "name":"Cannibalism" , "symptoms":"Chicks have sores on toes, wattles due to biting each other" },
    { "name":"Fowl cholera" , "symptoms":"Sudden death,fever,depression,mucus discharge from the mouth,diarrhea" },
    { "name":"Fowl cholera" , "symptoms":"Birds having diarrhoea ,with mucus  discharge from the mouth" },
    { "name":"Fowl cholera" , "symptoms":"Diarrhoea and fever in birds followed by death" },
    { "name":"Fowl cholera" , "symptoms":"Sudden death of chicks after suffering from high fever and diarrhoea " },
    { "name":"Fowl cholera" , "symptoms":"Looking sad and suffering from running stomach  in turkey" },
    { "name":"Fowl cholera" , "symptoms":"Running stomach ,fever and mucus discharge in birds" },
    { "name":"Fowl cholera" , "symptoms":"Mucus discharge from the chicken and diarrhoea" },
    { "name":"Fowl cholera" , "symptoms":"Turkeys and chicks having stomach ache, diarrhoea" },
    { "name":"Vitamin D deficiency", "symptoms":"Frequently rest in a squatting positions,stiff gait,retarded growth" },
    { "name":"Vitamin D deficiency", "symptoms":"Chicken not showing any signs of growth" },
    { "name":"Vitamin D deficiency", "symptoms":"Chicken growing to slow" },
    { "name":"Vitamin D deficiency", "symptoms":"Chicken always resting in a squat position" },
    { "name":"Vitamin D deficiency", "symptoms":"Squatting positions when chicken is resting " },
    { "name":"Vitamin D deficiency", "symptoms":"Retarded growth of chicken and stiff gait" },
    { "name":"Vitamin D deficiency", "symptoms":"Chicken is very stiff in body muscles" },
    { "name":"Riboflavin deficiency", "symptoms":"Curling toes, inability to walk in 1 week old chicks, diarrhoea" },
    { "name":"Riboflavin deficiency", "symptoms":"Chicks cannot walk at 1 week old" },
    { "name":"Riboflavin deficiency", "symptoms":"Chicks having diarrhoea and  have curly toes" },
    { "name":"Riboflavin deficiency", "symptoms":"Diarrhoea an inability to walk in small chicks" },
    { "name":"Riboflavin deficiency", "symptoms":"Bending toes and running stomach" },
    { "name":"Riboflavin deficiency", "symptoms":"Not straight toes and inability to walk" },
    { "name":"Manganese  deficiency", "symptoms":"Joints are swollen, and flattened, the tibia bone is usually bent" },
    { "name":"Manganese  deficiency", "symptoms":"Chicken have flattened joints which are flattened" },
    { "name":"Manganese  deficiency", "symptoms":"Tibia bone of the chicks is bent" },
    { "name":"Manganese  deficiency", "symptoms":"Joints of the chicken is swollen " },
    { "name":"Manganese  deficiency", "symptoms":"Joints of the chicken is swollen and the bones are flattened" },
    { "name":"Manganese  deficiency", "symptoms":"Chicken having difficulties in walking and the joints are swollen" },
    { "name":"Manganese  deficiency", "symptoms":"Swollen joints in chicken " },
    { "name":"African  swine  fever", "symptoms":"Huddling together,incordination of hind quarter,anorexia,naso-occular discharge, cough" },
    { "name":"African  swine  fever", "symptoms":"Pigs having incoordination of the hind quater" },
    { "name":"African  swine  fever", "symptoms":"Pigs huddling together and have cough" },
    { "name":"African  swine  fever", "symptoms":"Discharge from the nose and always coughing ,also losing weight in pigs" },
    { "name":"African  swine  fever", "symptoms":"The lower part of the pigs is not coordinating properly and have a discharge in the nose" },
    { "name":"African  swine  fever", "symptoms":"Losing weight ,coughing and huddling together in pigs" },
    { "name":"Blackleg", "symptoms":"Lameness, followed by depression & fever.. The muscles in the hip, shoulder, chest, back, & neck swell." },
    { "name":"Blackleg", "symptoms":"Pigs has a high fever and showing signs of sadness" },
    { "name":"Blackleg", "symptoms":"The  muscles in the hips are stiff and the pig cannot turn well" },
    { "name":"Blackleg", "symptoms":"Pig is lame and has high fever " },
    { "name":"Blackleg", "symptoms":"Pigs not feeding well and have chest ,back neck pain" },
    { "name":"Blackleg", "symptoms":"The pigs is infected with the bacteria ,and have fever" },
    { "name":"Cocccidiosis", "symptoms":"Piglets appear weak,dehydrated,weight gains are depressed, watery or greasy diarrhoea yellowish in colour ,white foul smelling" },
    { "name":"Cocccidiosis", "symptoms":"Piglets are looking pale and passing out watery greasy diarrhoea" },
    { "name":"Cocccidiosis", "symptoms":"Foul smell coming out of the pigs mouth and yellowish in colour" },
    { "name":"Cocccidiosis", "symptoms":"Pigs losing weight and having a running stomach" },
    { "name":"Cocccidiosis", "symptoms":"watery or greasy diarrhoea yellowish in colour ,white foul smelling in pigs" },
    { "name":"Cocccidiosis", "symptoms":"Pigs are always dehydrated and have a foul smell " },
    { "name":"Salmonellosis", "symptoms":"anorexia,depression,fever,severe watery diarrhea,dysentery,tetanus,death within 24-48hrs" },
    { "name":"Salmonellosis", "symptoms":"Diarrhoea ,and depression,sudden death of pigs" },
    { "name":"Salmonellosis", "symptoms":"Loss of weight in pigs and also serious running stomach and looking sad" },
    { "name":"Salmonellosis", "symptoms":"High temperature and loss of weight and death of pigs" },
    { "name":"Salmonellosis", "symptoms":"Dysentery ,tetanus, and death of pigs" },
    { "name":"Salmonellosis", "symptoms":"Anorexia, fever and loss of weight" },
    { "name":"Salmonellosis", "symptoms":"Pigs showing signs of dysentery and severe running stomach" },
    { "name":"Brucellosis", "symptoms":"Pigs not able to produce babies " },
    { "name":"Ascaciasis", "symptoms":"Abdominal breathing ,weight loss,unthriftiness" },
    { "name":"Ascaciasis", "symptoms":"Pigs breathing heavily and losing weight" },
    { "name":"Ascaciasis", "symptoms":"Loss of weight in pigs and not breathing well" },
    { "name":"Ascaciasis", "symptoms":"Weight loss and abdominal breathing in pigs" },
    { "name":"Ascaciasis", "symptoms":"Pigs not unhealthy and losing weight" },
    { "name":"Ascaciasis", "symptoms":"Pigs not growing " },
    { "name":"Ascaciasis", "symptoms":"Loss of weight in pigs and not growing well" },
    { "name":"Erysipelas", "symptoms":"Constipation, diarrhoea, & reddish patches on the skin." },
    { "name":"Erysipelas", "symptoms":"Pigs having difficulties in passing out dirty and have red patches on the skin" },
    { "name":"Erysipelas", "symptoms":"Reddish patches on the skin of the pigs" },
    { "name":"Erysipelas", "symptoms":"Running stomach and red patches on the skin of the pigs" },
    { "name":"Erysipelas", "symptoms":"Unable to pass out dirty and a running stomach" },
    { "name":"Erysipelas", "symptoms":"Skin becoming red" },
    { "name":"Erysipelas", "symptoms":"Small reddish patches on the skin and difficulties in passing out dirty" },
    { "name":"Streptococcosis", "symptoms":"Tremors ,convulsions,blindness,deafness" },
    { "name":"Streptococcosis", "symptoms":"Pigs becoming blind and deaf" },
    { "name":"Streptococcosis", "symptoms":"Pigs showing signs irregular movement of a limb or of the body" },
    { "name":"Streptococcosis", "symptoms":"Pigs being violent towards others and blind" },
    { "name":"Streptococcosis", "symptoms":"Deafness and muscle stuffiness" },
    { "name":"Streptococcosis", "symptoms":"Muscles becoming stiff,violent,blindness and unable to hear" },
    { "name":"Foot Scald / Footrot", "symptoms":"Sore  infects only the area between the toes" },
    { "name":"Foot Scald / Footrot", "symptoms":"Sheeps and goats have sores between toes" },
    { "name":"Foot Scald / Footrot", "symptoms":"Sheeps having difficulties in walking because of the pain between toes" },
    { "name":"Foot Scald / Footrot", "symptoms":"Toes of goats are in pain" },
    { "name":"Foot Scald / Footrot", "symptoms":"Infected area between toes in sheep" },
    { "name":"Foot Scald / Footrot", "symptoms":"Sheeps have serious wounds between toes" },
    { "name":"Polioencephalomacia", "symptoms":"incoordination, weakness, tremors, blindness, and depression." },
    { "name":"Polioencephalomacia", "symptoms":"Sheeps looking sad and have muscles stiffness" },
    { "name":"Polioencephalomacia", "symptoms":"Blindness and muscle are stiff, and there is incoordination" },
    { "name":"White muscle disease", "symptoms":"affect skeletal muscles, heart muscle, breathing; fever; and frothy, blood-stained nasal discharge" },
    { "name":"White muscle disease", "symptoms":"Sheeps muscles are affected and breath heavily and a nasal blood discharge" },
    { "name":"White muscle disease", "symptoms":"Sheeps has high temperature and the heart muscle is affected too" },
    { "name":"White muscle disease", "symptoms":"breathing; fever; and frothy, blood-stained nasal discharge in sheeps and goats" },
    { "name":"White muscle disease", "symptoms":"Skin muscles becomes too thin and discharge a stain from the  nose with blood" },
    { "name":"White muscle disease", "symptoms":"High temperature and muscles breathing heavily " },
    { "name":"White muscle disease", "symptoms":"White foamy discharge stained with blood from the nose" },
    { "name":"Ruminal lactic acidosis", "symptoms":"discomfort, anorexia, teeth grinding, muscle twitching, ruminal stasis, and diarrhea" },
    { "name":"Ruminal lactic acidosis", "symptoms":"Losing weight and grinding of teeth in sheeps" },
    { "name":"Ruminal lactic acidosis", "symptoms":"Muscle too tough and  losing too much and teeth grinding " },
    { "name":"Ruminal lactic acidosis", "symptoms":"Aneroxia and teeth grinding in sheeps" },
    { "name":"Soremouth", "symptoms":"scabs or blisters on the lips, nose, udder and teats, or sometimes at the junction of the hoof and skin of the lower leg. " },
    { "name":"Soremouth", "symptoms":"Sheep have blisters on the lips and on the  teats" },
    { "name":"Soremouth", "symptoms":"Blisters developing at the junction of the hoof and skin of the lower leg" },
    { "name":"Soremouth", "symptoms":"Blood clots on the lips, nose and teats of the teats of the sheeps" },
    { "name":"Soremouth", "symptoms":"At the joint of the ships legs there are blisters " },
    { "name":"Respiratory infections, or pneumonia", "symptoms":"fever with a temperature over 104F, along with a moist, painful cough and dyspnea (difficulty breathing). Anorexia and depression" },
    { "name":"Respiratory infections, or pneumonia", "symptoms":"High fever in sheeps and signs of painful cough" },
    { "name":"Respiratory infections, or pneumonia", "symptoms":"difficulty breathing and loosing too much weight" },
    { "name":"Respiratory infections, or pneumonia", "symptoms":"Moist cough associated with high fever and shows signs of depression" },
    { "name":"Respiratory infections, or pneumonia", "symptoms":"Signs of sadness and breathing difficulties and losing weight" },
    { "name":"Caseous lymphadenitis", "symptoms":"anemia, anorexia, weight loss, and fever." },
    { "name":"Caseous lymphadenitis", "symptoms":"sheep having low blood count and severe weight loss" },
    { "name":"Caseous lymphadenitis", "symptoms":"Fever is too high in sheeps" },
    { "name":"Caseous lymphadenitis", "symptoms":"Losing weight and low blood count in sheep" },
    { "name":"Caseous lymphadenitis", "symptoms":"Sheep losing a lot of blood and has high temperature" }
]
for symptom in symptomSet:
    symptomTrainer.train(symptom['symptoms'], symptom['name'])

# When you have sufficient trained data, you are almost done and can start to use
# a classifier.
symptomClassifier = Classifier(symptomTrainer.data, token)

translate_client = translate.Client()

# Now you have a classifier which can give a try to classifiy text of news whose
# category is unknown, yet.pyt


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
        text = body
        target = 'en'
        translation = translate_client.translate(text, target_language=target)
        result = translation['translatedText']

        if 'register' in result.lower():
            new = result.split(' ')
            farmer = Farmer(number=phone, name=new[1], surname=new[2], location=" ".join(new[3:]))
            db.session.add(farmer)
            db.session.commit()
            response.message('{} you have been added successfully!'.format(farmer.name))
            return str(response)
        else:
            classification = symptomClassifier.classify(result)
            for cl in classification[:1]:
                sol = Disease.query.filter_by(name=cl[0]).first()
                if sol is not None:
                    if sol.category == 'Primary':
                        ques = Critical(content=body, number=phone)
                        db.session.add(ques)
                        db.session.commit()
                        response.message("Mubvunzo venyu vatumirwa vana mazvikokota Primary")
                    text = sol.remedy
                    target = 'sn'
                    translation = translate_client.translate(text, target_language=target)
                    result = translation['translatedText']
                    response.message(result)
                    ques = Question(content=body, number=phone)
                    db.session.add(ques)
                    db.session.commit()
                    return str(response)
                response.message('Mubvunzo venyu vatumirwa vana mazvikokota')
                ques = Question(content=body, number=phone)
                db.session.add(ques)
                db.session.commit()
                return str(response)

    response.message('Please specify the symptoms that you are seeing')

    return str(response)


@app.route('/')
@app.route('/index')
@login_required
def index():
    requests = Question.query.order_by(desc(Question.id)).limit(20)
    reginal = Farmer.query.filter_by(location=current_user.region)
    return render_template('index.html', requests=requests, reginal=reginal)

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
def addDiesease():
    form = AddDiseaseForm()
    if form.validate_on_submit():
        new = Disease(name=form.name.data, symptoms=form.symptoms.data,remedy=form.remedy.data)
        db.session.add(new)
        db.session.commit()
        flash('Diesease added to database!')
        return redirect(url_for('index'))
    return render_template('addDiesease.html', form=form)

@app.route('/farmers')
@login_required
def viewFarmers():
    farmers = Farmer.query.all()
    return render_template('farmers.html', farmers=farmers)

@app.route('/profile/<id>', methods=["GET","POST"])
@login_required
def profile(id):
    form = EditForm()
    user = User.query.get(id)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.region = form.region.data
        db.session.add(user)
        db.session.commit()
        flash('Changes were made successfully!!')
        return redirect(url_for('index'))
    form.username.data = user.username
    form.email.data = user.email
    form.region.data = user.region
    return render_template('profile.html', form=form)

@app.route('/diseases')
@login_required
def diseases():
    diseases = Disease.query.all()
    return render_template('diseases.html', diseases=diseases)
    

@app.route('/admin')
@basic_auth.required
def dashboard():
    users = User.query.all()
    return render_template('dashboard.html', users=users)
