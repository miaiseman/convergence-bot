import convergence_esp as ce
from flask import Flask, request, render_template, jsonify

sbw_model = ce.load_model('sbw_model.pkl')
pcv_model = ce.load_model('pal_com_vectores.pkl')

esp_app = Flask(__name__, static_url_path="")

@esp_app.route('/') 
def index():
    """Return the main page."""
    return render_template('convergence_espanol.html')


@esp_app.route('/play_round', methods=['GET', 'POST'])
def play_round():
    """Play a round of Convergence."""
    params = request.json  # web browser will send these back as a dictionary when you click the button
    response = ce.play_round(model=sbw_model, common_word_vectors=pcv_model, **params)  # what we send back (dict)
    return jsonify(response)  # flask version of json.dumps

