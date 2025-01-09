# flaskr/__init__.py
from flask import Flask, render_template, jsonify
import os
import json
import matplotlib.pyplot as plt
import io
import base64

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    
    @app.route('/accueil')
    def accueil():
        return render_template('accueil.html')
    
    @app.route('/statistiques_resultats')
    def statistiques_resultats_load():
        # Charger les données JSON
        with open('./json_files/json_file_example.json') as f:
            data = json.load(f)

        # Créer un graphique avec Matplotlib
        # fig, ax = plt.subplots()
        # ax.pie([data['value1'], data['value2'], data['value3']], labels=['Label1', 'Label2', 'Label3'], autopct='%1.1f%%')
        # Extract categories and values
        categories = data['categories']
        values = data['values']

        # Create a pie chart
        fig, ax = plt.subplots()
        ax.pie(values, labels=categories, autopct='%1.1f%%')

        # Display the chart
        plt.show()

        # Sauvegarder le graphique dans un buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img = base64.b64encode(buf.getvalue()).decode('ascii')

        return render_template('statistiques_resultats.html', img_data=img)

    return app
