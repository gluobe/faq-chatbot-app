# Faqchatbot

Slack chatbotapp dat gebuik maakt van de slack event API en de confluence rest API. Het dient om te zoeken in een database of en api call bij confluence naar de juidte url. 

## Benodigdheid

Best te gebruiken met docker of door de infrastruktuur op te zeten op aws. De code van de infrastructuur stat op [github](https://github.com/gluobe/faq-chatbot-infra.git). 
Deploy de infrastructuur en run vervolgens de applicatie.

Mysql database opzeten

Volg de instructie op [slack](https://api.slack.com/bot-users) om en slack chatbot app te maken
Men heeft van slack:
*  De slack-secret
* slack access-tokken nodig
* veranderd de **Event Subscriptions url** met de output van de terraform url
* voeg de gemaakte chatbot app in de channels die men wil gebruiken

## Gebruik
 start vanaf chat.py
 
 chat.py maakt gebruik van volgende script:
 * databank.py
 * help.py
 * slack.py
 
 In help.py zitten de functies die de crud functie in de database gebruikt worden en de gegevens worden in chat.py gestuurd naar de bijhorende channel.
 Men moet in help.py, in de functie get_space_id(channelid): de juiste channelid en de juiste space tezeten.
  
De chatbot reageerd zondet '@' teken te gebruiken. De bot reageerd op volgende sleutelwoorden:
* aan
* confugureer
* documentatie
* hallo
* help
* lijst
* status
* uit

Bij het gebruik van de sleutel woord documentatie moet men een **TITEL** mee geven indien dat de titel in de database bestaat geef het een url terug.
Indien de titel niet in de database zit maar wel in confluence wordt die ingevoegd in de database en krijg men een url terug.

Push deze code op een repo die je ga gebruiken in de pipeline in jou repo. De code word gedeployd op een aws pipeline. 
De berichten gepost op de channel waar de bot in zit worden gestuurd naar de applicatie. De applicatie onderzoek in de fuctie
check_for_word(sentence, channelid) of een van de sleutel woorden gebruikt werd, als het zo is woord een gepaste antwoord 
gepost op de channel door de slackeventapi opteroepen.

## License
[GLUO](http://www.gluo.be/)