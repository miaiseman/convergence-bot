import pandas as pd
import numpy as np
import random
from sklearn.metrics.pairwise import cosine_similarity
import pickle


def load_model(filename):
    """Load any pickled model."""
    unpickled_model = pickle.load(open(filename, "rb"))
    return unpickled_model


def converge(model, common_word_vectors, user_input, bot_input, exclude=None):
    """Return the "average word" of the input words."""

    if exclude is None:
        exclude = set()
    exclude.add(user_input)
    exclude.add(bot_input)

    mean_vector = (model[user_input]) + model[bot_input] / 2
    cos_sim_dict = {}
    response_options_dict = {
        key: common_word_vectors[key]
        for key in common_word_vectors
        if key not in exclude
    }
    for word, vector in response_options_dict.items():
        cos_sim_dict[float(cosine_similarity(mean_vector, vector))] = word
    max_cos_sim = max(cos_sim_dict.keys())
    bot_response = cos_sim_dict[max_cos_sim]
    return bot_response


def play_round(
    model, common_word_vectors, user_input, user_history=None, bot_history=None
):
    """Play a round of Convergence."""
    user_input = user_input.lower().strip().replace(" ", "")
    if user_input not in model:
        return {
            "error": f"""Is {user_input} an English word? 
        I don't know it. 
        Choose a different word."""
        }
    if bot_history is None:
        user_history = []
        bot_history = []
        bot_response = random.choice(list(common_word_vectors.keys()))
    else:
        if user_input in bot_history or user_input in user_history:
            return {
                "error": f"""No repeats! 
            One of us already said {user_input}. 
            Choose a different word."""
            }
        else:
            bot_response = converge(
                model,
                common_word_vectors,
                user_history[-1],
                bot_history[-1],
                exclude=set(user_history + bot_history),
            )
    user_history.append(user_input)
    bot_history.append(bot_response)
    return {
        "user_history": user_history,
        "bot_history": bot_history,
        "bot_response": bot_response,
    }
