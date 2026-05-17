import requests
from flask import Flask, jsonify, request, send_from_directory
from lib import get_fass_url_from_faas_name, get_lista_faas

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return send_from_directory(".", "demo-faas-call.html")


@app.route("/faas", methods=["GET"])
def lista_faas():
    return jsonify(get_lista_faas())


@app.route("/trigger", methods=["POST"])
def trigger(): 
    data = {}
    faas_url = ""
    try:
        data = request.get_json(force=True)
    except Exception as e1:
        return jsonify({
            "status": "API-GW error in data",
            "message": str(e1)
        }), 400
    try:
        faas_url = get_fass_url_from_faas_name(data.get("nome-faas"))
    except Exception as e1:
        return jsonify({
            "status": "API-GW error in faas-url",
            "message": "faas non indicata o non presente"
        }), 400
    try:
        response = requests.post(faas_url, json=data, timeout=60)
        return jsonify({
            "status_code": response.status_code,
            "response": response.json()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "API-GW error in response",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)