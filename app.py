
from flask import Flask, jsonify, Response
from flask_cors import CORS
from flask_restful import Api, request
from dicttoxml import dicttoxml
import json

import src.geocode as gloc


# from src.employee_signup import employee_signup,employee_signup_password

UPLOAD_FOLDER = 'static/media/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3'}
app = Flask(__name__)
CORS(app)

api = Api(app, prefix="/api", catch_all_404s=True)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = 'application/json'
app.config["DEBUG"] = True

app.config["APPLICATION_ROOT"] = "/verloop/api/v1"

root_url = app.config['APPLICATION_ROOT']


# app.register_blueprint(employee_signup)

'''
r = Response(response="TEST OK", status=200, mimetype="application/xml")
r.headers["Content-Type"] = "text/xml; charset=utf-8"
return r
'''


@app.route(root_url+'/getAddressDetails', methods=['POST'])
def getAddressDetails():
    try:
        # get the data from request
        req_data = request.get_json()
        # check token valid for get the api data
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            if token != app.config['SECRET_KEY']:
                return jsonify({"msg": "Record not found"}), 401
        else:
            return "Record not found", 401
        # check wheather address string empty 
        address_got = req_data.get("address", "NA")
        if address_got == "" or address_got == "NA":
            return jsonify({"msg": "empty address not acceptable"}), 406
        # check output_format
        output_format = req_data.get('output_format', "NA")
        # get the data from google geocode api
        rgeoloc = gloc.geocode(req_data)
        # check response from api
        if rgeoloc['status'] == 1:
            data = {"coordinates": {
                            "lat": rgeoloc["location"]["lat"],
                            "lng": rgeoloc["location"]["lng"]
                            },
                    "address": req_data["address"]
                    }
            if output_format == 'json' or output_format == 'NA':
                # response in json
                r = Response(response=json.dumps(data), status=200,
                             mimetype="application/json")
                r.headers["Content-Type"] = "text/json; charset=utf-8"
                return r
            if output_format == 'xml':
                # response in xml
                r = Response(response=dicttoxml(data),
                             status=200,
                             mimetype="application/xml")
                r.headers["Content-Type"] = "text/xml; charset=utf-8"
                return r
        else:
            # throw message from geocde error 
            return jsonify({"msg": "geocode error->"+rgeoloc["msg"]}), 500

    except Exception as e:

        return jsonify({"msg": "Internal server error->"+str(e)}), 500


if __name__ == '__main__':
    app.run(port='8123', host='0.0.0.0', debug=True)
