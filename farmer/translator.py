from google.cloud import translate 

translate_client = translate.Client()

text = raw_input('Please enter text to be translated: ')

target = 'en'

translation = translate_client.translate(text, target_language=target)

result = translation['translatedText']

if text == result:
    print 'English text was provided'
else:
    print 'Shona or some other language was provided'

