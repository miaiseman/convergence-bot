def converge(user_input=str, bot_input=str, exclude=None):
    """Return the "average word" of the input words."""
    if exclude is None:
        exclude = set()
    exclude.add(user_input)
    exclude.add(bot_input)  
    mean_vector = ((model[user_input] + model[bot_input])/2)
    cos_sim_dict = {}
    response_options_dict = {key: common_word_vectors[key] for key in common_word_vectors 
                             if key not in exclude}
    for word, vector in response_options_dict.items():
        cos_sim_dict[float(cosine_similarity(mean_vector, vector))] = word
    max_cos_sim = max(cos_sim_dict.keys())
    bot_response = cos_sim_dict[max_cos_sim]
    return bot_response

def play_round(user_input, user_history=None, bot_history=None):
    if bot_history is None:
        user_history = []
        bot_history = []
        bot_response = random.choice(cwordlist)
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