import convergence as cr
from flask import Flask, request, render_template, jsonify

model = cr.load_model('https://convergencerobot.s3-us-west-2.amazonaws.com/pre_trained_model.pkl')
common_word_vectors = cr.load_model('https://convergencerobot.s3-us-west-2.amazonaws.com/common_word_vectors.pkl')

app = Flask(__name__, static_url_path="")

@app.route('/') 
def index():
    """Return the main page."""
    return render_template('convergence.html')


@app.route('/play_round', methods=['GET', 'POST'])
def play_round():
    """Play a round of Convergence."""
    params = request.json  # web browser will send these back as a dictionary when you click the button
    response = cr.play_round(model=model, common_word_vectors=common_word_vectors, **params)  # what we send back (dict)
    return jsonify(response)  # flask version of json.dumps

#need to reproduce logic from play_conergence

