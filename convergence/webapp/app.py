from ..convergence import play_round
from ..convergence import load_model
from flask import Flask, request, render_template, jsonify

model = load_model('./convergence/pre_trained_model.pkl')
common_word_vectors = load_model('./convergence/common_word_vectors.pkl')

app = Flask(__name__, static_url_path="")

@app.route('/') 
def index():
    """Return the main page."""
    return render_template('./convergence/templates/convergence.html')


@app.route('/play_round', methods=['GET', 'POST'])
def play_a_single_round():
    """Play a round of Convergence."""
    params = request.json  # web browser will send these back as a dictionary when you click the button
    response = play_round(model=model, common_word_vectors=common_word_vectors, **params)  # what we send back (dict)
    return jsonify(response)  # flask version of json.dumps

