from flask import Flask, jsonify
import os 
from scrapy_function import scrape_and_upload

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def execute_scheduled_job():
    """
    Déclenche l'exécution du scraping en réponse à l'appel HTTP de Cloud Scheduler.
    """
    try:
        # L'exécution du script principal
        scrape_and_upload()
        
        # Réponse HTTP 200 (OK) pour confirmer l'exécution
        return jsonify({"status": "Success", "message": "Scraping completed and data written to BigQuery."}), 200
    
    except ValueError as ve:
        # Erreur liée aux variables d'environnement manquantes
        print(f"Configuration Error: {ve}")
        return jsonify({"status": "Configuration Error", "message": str(ve)}), 500
        
    except Exception as e:
        # Toute autre erreur (API, BigQuery, etc.)
        print(f"Execution Error: {e}")
        return jsonify({"status": "Execution Error", "message": str(e)}), 500

if __name__ == '__main__':
    # Cloud Run fournit la variable d'environnement PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)