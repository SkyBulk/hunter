import os
import json
from flask import request, render_template
from app import app



@app.route("/")
def index():
    
    return render_template("public/index.html")

 
@app.route('/index_get_data')
def stuff():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'static', 'data.json')
    data = json.load(open(json_url))
    return data