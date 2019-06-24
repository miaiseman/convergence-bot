# Convergence Bot 
Play the game Convergence with a robot - try to say the 
same word at the same time!  
 
People need to play more, especially adults. Convergence is sometimes called Same Page or Mindmeld, and it’s a popular game among improvisers though it is not well known to the general public. The bot allows people to play the game when no one else is around, creating joy and popularizing a game whose main goal is to get people to be on the same page.

#Data Understanding
The model will train on a corpora of text that is representative of how people speak and think in terms of word associations. There are many options, and I will test with various ones. If I find the scope is too large, I could limit the game to certain filtered words or themed inputs. (“Hey, Alexa, let’s play Disney Convergence!”) 

#Data Preparation
I will need to convert the data to usable a corpus, apply tokenization, lemmitization, and more...

#Modeling
I will try different models such as GLoVE, Word2Vec, and perhaps BERT as well. Elmo takes more context into account, especially for words with more than one meaning, which seems like it will be better than other options. An important note for modeling will be to include the previous inputs as immediately influential on the output, but not too influential. There are also no repeats allowed per game, so this will be important to track as well. 

It would be great to incorporate the input “answers” from the other player immediately into the corpus of text. That way, if after many rounds, a person has answered “dog” several more times than “puppy,” the computer will give a preference to dog instead of puppy in the future, where it makes sense. 

#Evaluation
I could have the computer play against a differently trained bot and log the results of playing against humans. I will look at the average number of rounds before a convergence as well as other evaluation methods TBD. 

#Deployment
I will deploy on a website similar to the 20 Questions Game. In terms of UI, it might be nice to have the user set a limit on the number of rounds, or to have that be automatically built in. 
Stretch goal: Alexa skill or siri app that utilizes voice to text. 
