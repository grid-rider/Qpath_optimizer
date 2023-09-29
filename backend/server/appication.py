from flask import Flask, request
import json

application = Flask(__name__)

@application.route("/path/generate", methods=["POST"])
def index():
    
    content_type = request.headers.get('Content-Type')
    try:
        if (content_type == 'application/json'):
            parsed_reqest = request.json
            start_point = parsed_reqest.get("start_point")
            end_point = parsed_reqest.get("end_point")
            
            path = [start_point, { "lat": 40.7431, "lng": -73.971321 }, { "lat": 40.7531, "lng": -73.961321 }, end_point] #ToDo Generate ideal path
            return json.dumps({"path" : path}), 200 #OK 
        else:
            return 'Content-Type not supported!', 400 #Bad-request
    except Exception as e:
        print("Error occured ", e)
        return ("Server side error: " + str(e)), 500  #Server-side error 

if __name__ == "__main__":
	application.run(host='0.0.0.0', port=80, debug=False) ## Using webcommon port 80    