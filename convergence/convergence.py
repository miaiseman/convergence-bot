import pandas as pd 
import numpy as np  
import random 
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import requests


def load_model(filename):
    """Load any pickled model."""
    unpickled_model = pickle.load(open(filename, 'rb'))
    return unpickled_model


def converge(model, common_word_vectors, user_input, bot_input, exclude=None):
    """Return the "average word" of the input words."""
    
    if exclude is None:
        exclude = set()
    exclude.add(user_input)
    exclude.add(bot_input)  

    mean_vector = (model[user_input]) + model[bot_input]/2
    cos_sim_dict = {}
    response_options_dict = {key: common_word_vectors[key] for key in common_word_vectors 
                             if key not in exclude}
    for word, vector in response_options_dict.items():
        cos_sim_dict[float(cosine_similarity(mean_vector, vector))] = word
    max_cos_sim = max(cos_sim_dict.keys())
    bot_response = cos_sim_dict[max_cos_sim]
    return bot_response

def play_round(model, common_word_vectors, user_input, user_history=None, bot_history=None):
    """Play a round of Convergence."""
    user_input = user_input.lower().strip().replace(' ', '')
    if user_input not in model: 
        return {'error': f"Is {user_input} an English word? I don't know it. Choose a different word."}
    if bot_history is None:
        user_history = []
        bot_history = []
        bot_response = random.choice(list(common_word_vectors.keys()))
    else:
        if user_input in bot_history or user_input in user_history:
            return {'error': f"No repeats! One of us already said {user_input}. Choose a different word."}
        else: 
            bot_response = converge(model, common_word_vectors, 
                                    user_history[-1], bot_history[-1],
                                    exclude=set(user_history + bot_history))
    user_history.append(user_input)
    bot_history.append(bot_response)
    return {
        'user_history': user_history,
        'bot_history': bot_history,
        'bot_response': bot_response,}


#can look at this later to make sure it runs in terminal
def play_convergence(round_results=None):
    """Play a game of Convergence."""
    print("Let's play Convergence! \nThe game starts with two random words - "
          "one from you and one from the computer. The goal is to converge upon the same word" 
          " without repeating any words from a previous round. \nLet's begin. Type any word!") 
    
    model = make_model() #define models
    common_word_vectors = make_cwv()
    
    while True: 
        user_response = input().lower()
        
        if user_response not in model.keys(): #invalid word  
           print (f"Is {user_response} an English word? I don't know it. Choose a different word.") 
        else: #word is valid
            if round_results is None: #check for first round 
                bot_history = None 
                user_history = None
                round_results = play_round(model, user_response, user_history, bot_history)    
                
                #first round convergence will basically never happen, but just in case: 
                if user_response != round_results['bot_response']:
                    print(f"You said {user_response}, but I said {round_results['bot_response']}.")
                    print(f"What's the convergence of {user_response} and {round_results['bot_response']}?")   
                else:
                    print(f"CONVERGENCE!!!! WE BOTH said {user_response}!!! WE GOT CONVERGENCE!!!!")
                    break              
        
            else: #not first round
                bot_history = round_results['bot_history']
                user_history = round_results['user_history']

                if user_response in bot_history or user_response in user_history: #repeated word
                    print(f"Looks like one of us has already said {user_response}. Choose a different word.")
                else: #valid new word 
                    round_results = play_round(model, user_response, user_history, bot_history)    
                    if user_response != round_results['bot_response']:
                        print(f"You said {user_response}, but I said {round_results['bot_response']}.")
                        print(f"What's the convergence of {user_response} and {round_results['bot_response']}?")   
                        if len(round_results['bot_history'])>1:
                              print(f"Remember, don't repeat what you said: {user_history} or what I said: {bot_history}")
                    else:
                        print(f"CONVERGENCE!!!! WE BOTH said {user_response}!!! WE GOT CONVERGENCE!!!!")
                        break  
         
                              
if __name__ == '__main__':  #if someone runs directly (in any way that it's called with python)                            
    play_convergence()