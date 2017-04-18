from google.cloud import translate 

translate_client = translate.Client()

text = raw_input('Please enter text to be translated: ')

target = 'en'

translation = translate_client.translate(text, target_language=target)

print translation['translatedText']