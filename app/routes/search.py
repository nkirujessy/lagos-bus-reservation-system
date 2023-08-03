from flask import Blueprint, render_template, request
from app import app
search_route = Blueprint('search_route', __name__,template_folder='templates')


@app.route("/search")
def buses_search():
    path = 'Search Result'
    if request.method == 'GET':

        result = request.args.get('result', None)
        ticket = request.args.get('ticket', None)

    return render_template('web/search.html', path=path, value=result, ticket=ticket)
