# flaskr/__init__.py
from flask import Flask, render_template, render_template_string, jsonify, send_from_directory, redirect, url_for, session
from flask_bootstrap import Bootstrap
import os
import json
import matplotlib.pyplot as plt
import io
import base64
# from matplotlib_chart import MatplotlibChart
from flaskr.MatplotlibChart import MatplotlibChart
# from MatplotlibChart import MatplotlibChart

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
    
    @app.route('/')
    def index():
        return render_template('index.html')

    
    # fonctionnel avant
    # @app.route('/accueil')
    # def accueil():
    #     print("page accueil")
    #     return render_template('accueil.html')

    @app.route('/accueil')
    def accueil():
        print("page accueil")
        usb_data = [
            {
                "usb_id": 0,
                "usb_name": "Usb noire 32Go Jean Vier",
                "details": {
                    "capacity": "32Go",
                    "brand": "Jean Vier"
                }
            },
            {
                "usb_id": 1,
                "usb_name": "Usb bleu 64Go Jean Vier",
                "details": {
                    "capacity": "64Go",
                    "brand": "Jean Vier"
                }
            },
            {
                "usb_id": 2,
                "usb_name": "Usb verte 16Go Jean Vier",
                "details": {
                    "capacity": "16Go",
                    "brand": "Jean Vier"
                }
            }
        ]

        # session['usb_data'] = usb_data
        print("Rendering accueil.html")
        print("usb_data:", usb_data)
        # print("session['usb_data']:", session['usb_data'])
        # return redirect(url_for('statistiques'))
    
        # Pass the entire list of values to the template
        return render_template('accueil.html', usb_data=usb_data)
        # return jsonify([datas.to_json() for datas in usb_data])

    @app.route('/statistiques')
    def statistiques():
        usb_datas_list_content = []
        with open('./json_files/MalwaresJsonExample_01.json', 'r') as f:
            usb_datas_list_content = json.load(f)
            f.close()
        session['usb_datas_list_content']=usb_datas_list_content
        return render_template('statistiques_resultats.html', usb_datas_list_content=session['usb_datas_list_content'])
        # return render_template('statistiques_resultats.html')
    
    @app.route('/home')
    def home():
        return render_template('home.html')
    
    @app.route('/statistiques2')
    def statistiques2():
        # Vérifiez si le fichier existe
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

    # @app.route('/statistiques_resultats')
    # def statistiques_resultats():
    #     # Charger les données JSON 
        
    #     with open('./json_files/json_file_example.json') as f:
    #         data = json.load(f)
    #     # Créer un graphique avec Matplotlib
    #     fig, ax = plt.subplots()
    #     ax.pie([data['value1'], data['value2'], data['value3']], labels=['Label1', 'Label2', 'Label3'], autopct='%1.1f%%')
    #     # Extract categories and values
    #     categories = data['categories']
    #     values = data['values']

    #     # Create a pie chart
    #     fig, ax = plt.subplots()
    #     ax.pie(values, labels=categories, autopct='%1.1f%%')

    #     # Display the chart
    #     plt.show()

    #     # Sauvegarder le graphique dans un buffer
    #     buf = io.BytesIO()
    #     plt.savefig(buf, format='png')
    #     buf.seek(0)
    #     img = base64.b64encode(buf.getvalue()).decode('ascii')

        
            
    #     try:
    #         # Exemple de génération de graphique
    #         plt.plot([1, 2, 3], [4, 5, 6])
    #         plt.savefig('static/total_malwares.png')
    #         with open('./json_files/MalwaresJsonExample_01.json') as f:
    #             data = json.load(f)

    #         usb_analysis = data
    #         print("usb_analysis :\n")
    #         print(usb_analysis)
            
    #         usb_ids = [usb_analysis['usb_id'] for usb in data['usb_analysis']]
    #         total_malwares = [usb['total_malwares'] for usb in data['usb_analysis']]

    #         # Créer un graphique avec Matplotlib
    #         # fig, ax = plt.subplots()
    #         ax.pie([data[usb_analysis['value1']], data['value2'], data['value1'], total_malwares['value2']], labels=['Label1', 'Label2', 'Label3'], autopct='%1.1f%%')
    #         # Extract categories and values
    #         categories = data['categories']
    #         values = data['values']
    #         plt.show()
            

    #         plt.bar(usb_ids, total_malwares)
    #         plt.xlabel('USB ID')
    #         plt.ylabel('Total Malwares')
    #         plt.title('Total Malwares per USB')

    #         current_dir = os.path.dirname(os.path.abspath(__file__))
    #         save_path = os.path.join(current_dir, 'static', 'total_malwares.png')
    #         plt.savefig(save_path)
    #         plt.close()
    #         print(f"Chart saved at {save_path}")
    #     except Exception as e:
    #         print(f"Error generating chart: {e}")
    #     MatplotlibChart.generate_chart(data)

    #     # return render_template('statistiques_resultats.html', img_data=img)
    #     # return render_template('statistiques_resultats.html', data=data)
    #     # message_console =  render_template_string('''
    #     #     <script>
    #     #         console.log("Ceci est un message de debug depuis Python Flask, pour la redirection /statistiques_resultats");
    #     #     </script>
    #     # ''')
    
    #     statistiques_resultats_page = render_template('statistiques_resultats.html')
    #     # return message_console + statistiques_resultats_page
    #     return statistiques_resultats_page

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('page_not_found.html'), 404

    return app


