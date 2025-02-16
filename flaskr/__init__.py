# flaskr/__init__.py
from flask import Flask, render_template, render_template_string, jsonify, send_from_directory, redirect, url_for, session
from flask_bootstrap import Bootstrap
import os
import json
import matplotlib.pyplot as plt
import io
import base64
from flaskr.MatplotlibChart import MatplotlibChart

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

    Bootstrap(app)  # Initialiser Bootstrap

    # ci-dessous les routes de l'application

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        # print("redirection /hello")
        # return 'Hello, World!'
        return render_template_string('''
            <script>
                console.log("Ceci est un message de debug depuis Python");
            </script>
            <h1>Hello, World!</h1>
        ''')
    
    @app.route('/index')
    def index_page():
        return render_template('index.html')
    
    # fonctionnel avant
    # @app.route('/accueil')
    # def accueil():
    #     print("page accueil")
    #     return render_template('accueil.html')

    @app.route('/')
    def index():
        print("Rendering accueil.html")
        return render_template('accueil.html')

    @app.route('/accueil')
    def accueil():
        print("Rendering accueil.html")
        return render_template('accueil.html')

    @app.route('/statistiques')
    def statistiques():
        usb_datas_list_content = []
        with open('./json_files/MalwaresJsonExample_01.json', 'r') as f:
            usb_datas_list_content = json.load(f)
            f.close()
        session['usb_datas_list_content']=usb_datas_list_content
        return render_template('statistiques_resultats.html', usb_datas_list_content=session['usb_datas_list_content'])
    
    @app.route('/statistiques2')
    def statistiques2():
        file_path = './json_files/json_file_example.json'
        if not os.path.exists(file_path):
            return "Le fichier JSON n'existe pas.", 404

        # Lire les données JSON à partir du fichier
        try:
            with open(file_path) as f:
                data = json.load(f)
        except Exception as e:
            return f"Erreur lors de la lecture du fichier JSON : {e}", 500

        # Extraire les catégories et les valeurs
        categories = data["categories"]
        values = data["values"]

        # Créer un graphique de type camembert
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
        ax.set_title('Pie Chart of Categories')

        # Enregistrer dans un buffer temporaire
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
        buf.close()

        return render_template('statistiques2.html', image_base64=image_base64)
    
    @app.route('/home')
    def home():
        return render_template('home.html')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('page_not_found.html'), 404

    return app
