from textblob.classifiers import NaiveBayesClassifier


train = [
    ( "Diphtheria Lives in soil, litter, & unclean stables& enters the body through small scratches or wounds. Difficulty breathing, eating, and drinking.Patches of yellowish, dead tissue appear on the edges of the tongue, gums, & throat.  Often, a nasal discharge occurs", "Calf"),
    ( "Gases of fermentation", "bloat"),
    ( "Indigestion,collapse,frequently death, temperature too high 41 degrees", "Grain overload"),
    ( "Occurs a week after calving ,mucus covered feces,loss of weight,constipation,hump back posture, odour breath, drop in milk production", "ketosis"),
    ( "Decrease in appetite ,faecal production, nose licking ,weakness, depressed", "Pregnancy toxemia"),
    ( "Anorexia, rumen becomes full, doughy,excessive fluid,feces usually soft and foul smelling.", "Simple indigestion"),
    ( "Temperature too high, red dark urine, jaundice,anemic,dyspnoea,oedema of the brisket.", "Bacillary Hemoglobinuria"),
    ( "Chronic painless,cellulitis in lymph nodes, yellow pus ,ulcers", "Bovine farcy"),
    ( "Ticks all over the body", "Body ticks"),
    ( "Running stomach", "Diahorea"),
    ( "Improper feeding. Pain, sweating, & constipation, kicking, & groaning.", "Colic" ),
    ( "Animals are most apt to contact foot rot when forced to live in wet, muddy, unsanitary lots for long periods of time", "Foot rot"),
    ( "Overeating of grain, or lush, highly improved pasture grasses, Affected animals experience pain and may have fever as high as 106 degrees F",  "Founder" ),
    ("Lungs are affected.  However, other organs may be affected.  Some animals show no symptoms; others appear unthrifty & have a cough", "Tuberculosis"),
    ( "calf having difficulties in breathing, sore throat ,nasal mucus discharge, dead tissues on gums", "Calf" )
]

test = [
    ( "Diphtheria Lives in soil, litter, & unclean stables& enters the body through small scratches or wounds. Difficulty breathing, eating, and drinking.Patches of yellowish, dead tissue appear on the edges of the tongue, gums, & throat.  Often, a nasal discharge occurs", "Calf"),
    ( "Gases of fermentation", "bloat"),
    ( "temperature too high 41 degrees", "Grain overload"),
    ( "loss of weight,", "ketosis"),
    ( "Decrease in appetite", "Pregnancy toxemia"),
    ( "excessive fluid,feces usually soft and foul smelling.", "Simple indigestion"),
    ( "red dark urine,", "Bacillary Hemoglobinuria"),
    ( "ulcers", "Bovine farcy"),
    ( "Ticks all over the body", "Body ticks"),
    ( "Running stomach", "Diahorea")
]

cl = NaiveBayesClassifier(train)
print 'The determined accuracy is: {}'.format(cl.accuracy(test))