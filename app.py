import convergence_resources as cr
from flask import Flask, request, render_template, jsonify

@app.route('/') 
def index():
    """Return the main page."""
    return render_template('convergence.html')


@app.route('/play', methods=['GET', 'POST'])
def play_online():
    """Start a game of Covnergence."""
    return cr.play_convergence ()

