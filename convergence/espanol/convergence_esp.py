import pandas as pd 
import numpy as np  
import random 
from sklearn.metrics.pairwise import cosine_similarity
import pickle

def load_model(filename):
    """Load any pickled model."""
    any_model = pickle.load(open(filename, 'rb'))
    return any_model
  
def converge(sbw_model, pcv_model, user_input, bot_input, exclude=None):
    """Return the "average word" of the input words."""
    
    if exclude is None:
        exclude = set()
    exclude.add(user_input)
    exclude.add(bot_input)  

    mean_vector = (sbw_model[user_input]) + sbw_model[bot_input]/2
    cos_sim_dict = {}
    response_options_dict = {key: pcv_model[key] for key in pcv_model 
                             if key not in exclude}
    for word, vector in response_options_dict.items():
        cos_sim_dict[float(cosine_similarity(mean_vector, vector))] = word
    max_cos_sim = max(cos_sim_dict.keys())
    bot_response = cos_sim_dict[max_cos_sim]
    return bot_response

def play_round(sbw_model, pcv_model, user_input, user_history=None, bot_history=None):
    """Play a round of Convergence."""
    user_input = user_input.lower()
    if user_input not in sbw_model: # check for invalid word  
        return {'error': f"¿{user_input.upper()} es una palabra española? No la sé. Escoja otra."}
    if bot_history is None:
        user_history = []
        bot_history = []
        bot_response = random.choice(list(pcv_model.keys()))
    else:
        if user_input in bot_history or user_input in user_history:
            return {'error': f"No repitir! Alguién ya dijo {user_input}. Escoja otra palabra."}
        else: 
            bot_response = converge(sbw_model, pcv_model, 
                                    user_history[-1], bot_history[-1],
                                    exclude=set(user_history + bot_history))
    user_history.append(user_input)
    bot_history.append(bot_response)
    return {
        'user_history': user_history,
        'bot_history': bot_history,
        'bot_response': bot_response,}

#to run locally:
def juega(round_results=None):
    """Play a game of Convergence."""
    print("!Vamos a jugar Convergencia! Escoja quisiera palabra española para empezar.") 
    
    sbw_model = load_model('sbw_model.pkl')
    pcv_model = load_model('pal_com_vectores.pkl')
    
    while True: 
        user_response = input().lower()
        
        if user_response not in sbw_model: 
           print (f"¿{user_response.capitalize()} es una palabra española? No la sé. Escoja otra.") 
        else: #word is valid
            if round_results is None: #check for first round 
                bot_history = None 
                user_history = None
                round_results = play_round(sbw_model, pcv_model, user_response, user_history, bot_history)    
                
                #first round convergence will basically never happen, but just in case: 
                if user_response != round_results['bot_response']:
                    print(f"Dijiste {user_response}, pero dijo {round_results['bot_response']}.")
                    print(f"Qué es la convergencia de {user_response} y {round_results['bot_response']}?")   
                else:
                    print(f"CONVERGENCIA!!!! NOSOTR@S DOS DIJIMOS {user_response}!!! CONVERGENCIA!!!!")
                    break              
        
            else: 
                bot_history = round_results['bot_history']
                user_history = round_results['user_history']

                if user_response in bot_history or user_response in user_history: 
                    print(f"No repitir! Alguién ya dijo {user_response}. Escoja otra palabra.")
                else: #valid new word 
                    round_results = play_round(sbw_model, pcv_model, user_response, user_history, bot_history)    
                    if user_response != round_results['bot_response']:
                        print(f"Dijiste {user_response}, pero dijo {round_results['bot_response']}.")
                        print(f"Qué es la convergencia de {user_response} y {round_results['bot_response']}?")   
                        if len(round_results['bot_history'])>1:
                              print(f"Recuerda, no repita lo que has dicho: {user_history} ni lo que he dicho: {bot_history}")
                    else:
                        print(f"CONVERGENCIA!!!! NOSOTR@S DOS DIJIMOS {user_response}!!! CONVERGENCIA!!!!")
                        break  
                              
if __name__ == '__main__':  #if someone runs directly (in any way that it's called with python)                            
    juega()