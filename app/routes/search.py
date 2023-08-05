from flask import Blueprint, render_template, request
from app import app
search_route = Blueprint('search_route', __name__,template_folder='templates')


@app.route("/search")
def buses_search():
    path = 'Search Result'
    status='false'
    response=''
    if request.method == 'GET':

        status = request.args.get('status', None)
        response = request.args.get('response', None)


    return render_template('web/search.html', path=path, status=status, response=response)
