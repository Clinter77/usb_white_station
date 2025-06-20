"""Module providing a init function as entry point of project."""
import os
import json
import io
import base64
from flask import Flask, render_template, render_template_string
from flask import jsonify, send_from_directory, redirect, url_for, session
from flask_bootstrap import Bootstrap
import matplotlib.pyplot as plt
# from flaskr.MatplotlibChart import MatplotlibChart
from flask import abort

def create_app(test_config=None):
    """
    Crée et configure l'application Flask.
    Args:
        test_config (dict, optionnel): Dictionnaire de configuration pour les tests.
        Par défaut à None
    Returns:
        app (Flask): Instance de l'application Flask configurée.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # charger la configuration de l'instance, si elle existe, lorsqu'on ne teste pas
        app.config.from_pyfile('config.py', silent=True)
    else:
        # charger la configuration de test si elle est passée
        app.config.from_mapping(test_config)

    # s'assurer que le dossier de l'instance existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    Bootstrap(app)  # Initialisation de Bootstrap

    # ci-dessous les routes de l'application

    @app.route('/favicon.ico')
    def favicon():
        """
        Servir le fichier favicon.ico.
        Returns:
            Response: Réponse du fichier favicon.
        """
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/hello')
    def hello():
        """
        Afficher une page simple qui dit bonjour.
        Returns:
            str: Contenu HTML pour la page hello.
        """
        return render_template_string('''
            <script>
                console.log("Ceci est un message de debug depuis Python");
            </script>
            <h1>Hello, World!</h1>
        ''')

    @app.route('/index')
    def index_page():
        """
        Afficher la page index.
        Returns:
            Response: Template rendu de index.html.
        """
        return render_template('index.html')

    @app.route('/')
    def index():
        """
        Afficher la page accueil.html.
        Returns:
            Response: Template rendu de accueil.html.
        """
        return render_template('accueil.html')

    @app.route('/accueil')
    def accueil():
        """
        Afficher la page accueil.html.
        Returns:
            Response: Template rendu de accueil.html.
        """
        return render_template('accueil.html')

    @app.route('/statistiques')
    def statistiques():
        """
        Afficher la page statistiques_resultats.html avec les données issues des analyses.
        Returns:
            Response: Template rendu de statistiques_resultats.html
            avec les données issues des analyses.
        """
        usb_datas_list_content: list = []
        # file_path_json_file_analysis = '/flaskr/json_files/analysis.json'
        file_path_json_file_analysis:str = '/flaskr/json_files/logs.json'
        with open(file_path_json_file_analysis, mode='r', encoding='utf-8') as f:
            usb_datas_list_content = json.load(f)
        return render_template(
            'statistiques_resultats.html', usb_datas_list_content=usb_datas_list_content)

    @app.route('/statistiques2')
    def statistiques2():
        """
        Afficher la page statistiques2.html avec un graphique en camembert.
        Returns:
            Response: Template rendu de statistiques2.html avec l'image du graphique en camembert.
        """
        file_path = './json_files/json_file_example.json'
        if not os.path.exists(file_path):
            return "Le fichier JSON n'existe pas.", 404

        # Lire les données JSON à partir du fichier
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
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
        """
        Afficher la page home.html.
        Returns:
            Response: Template rendu de home.html.
        """
        return render_template('home.html')

    @app.errorhandler(404)
    def page_not_found(error=None):
        """
        Afficher la page page_not_found.html pour les erreurs 404.
        Returns:
            Response: Template rendu de page_not_found.html avec le code de statut 404.
        """
        return render_template('page_not_found.html'), 404
    

    @app.route('/trigger-teapot')
    def trigger_teapot():
        abort(418)

    @app.errorhandler(418)
    def page_teapot(error=None):
        """
        Afficher la page teapot.html pour l'erreur 418.
        """
        return render_template('teapot.html'), 418
    
    def test_page_teapot(client):
        response = client.get('/trigger-teapot')
        assert response.status_code == 418
        assert b"Page Teapot" in response.data
    
    


    return app
