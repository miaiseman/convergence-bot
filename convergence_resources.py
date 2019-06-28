def converge(user_input=str, bot_input=str, exclude=None):
    """Return the "average word" of the input words."""
    if exclude is None:
        exclude = set()
    exclude.add(user_input)
    exclude.add(bot_input)  

    mean_vector = ((6*model[user_input] + 2*model[bot_input])/2)
    cos_sim_dict = {}
    response_options_dict = {key: common_word_vectors[key] for key in common_word_vectors 
                             if key not in exclude}
    for word, vector in response_options_dict.items():
        cos_sim_dict[float(cosine_similarity(mean_vector, vector))] = word
    max_cos_sim = max(cos_sim_dict.keys())
    bot_response = cos_sim_dict[max_cos_sim]
    return bot_response


def play_round(user_input, user_history=None, bot_history=None):
    """Play a round of Convergence."""
    if bot_history is None:
        user_history = []
        bot_history = []
        bot_response = random.choice(lemmas[:])
    else:
        bot_response = converge(user_history[-1], bot_history[-1], 
                                exclude=set(user_history + bot_history))
    user_history.append(user_input)
    bot_history.append(bot_response)
    return {
        'user_history': user_history,
        'bot_history': bot_history,
        'bot_response': bot_response,
    }


play_convergence(round_results=None):
    """Play a game of Convergence."""
    print("Let's play Convergence. Type any word!") 
    while True: 
        user_response = input()
        if round_results is None:
            bot_history = None 
            user_history = None
            round_results = play_round(user_response, user_history, bot_history)    
            #this will practically never happen, but just in case: 
            if user_response != round_results['bot_response']:
                print(f"You said {user_response}, but I said {round_results['bot_response']}.")
                print(f"What's the convergence of {user_response} and {round_results['bot_response']}?")   

            else:
                print(f"CONVERGENCE!!!! WE BOTH said {user_response}!!! WE GOT CONVERGENCE!!!!")
                break              
        else: 
            bot_history = round_results['bot_history']
            user_history = round_results['user_history']
            
            #ensure user_response is a real word: 
            if user_response in bot_history or user_response in user_history: 
                print(f"Looks like one of us has already said {user_response}. Choose a different word.")
            elif user_response in model.keys():  
#             #first round:
#             if round_results is None:
#                 bot_history = None 
#                 user_history = None
#             #rounds with history
#             else: 
#                 bot_history = round_results['bot_history']
#                 user_history = round_results['user_history']
                #make sure the word hasn't been said already 
                #call the function that plays a round
                round_results = play_round(user_response, user_history, bot_history)    
                if user_response != round_results['bot_response']:
                    print(f"You said {user_response}, but I said {round_results['bot_response']}.")
                    print(f"What's the convergence of {user_response} and {round_results['bot_response']}?")   
                    if len(round_results['bot_history'])>1:
                          print(f"Remember, don't repeat what you said: {user_history} or what I said: {bot_history}")
                else:
                    print(f"CONVERGENCE!!!! WE BOTH said {user_response}!!! WE GOT CONVERGENCE!!!!")
                    break              
            else: 
                print (f"Hmm...Is {user_response} an English word? I don't know it. Choose a different one!")
                          
                          
                          