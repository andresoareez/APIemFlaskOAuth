import os
from flask import Flask, request
from flask_restful import Resource, Api
from models import User
import google_auth
import json


app = Flask(__name__)
app.register_blueprint(google_auth.app)
app.secret_key = "123456"
api = Api(app)

@app.route('/')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info, indent=4) + "</pre>"

    return 'You are not currently logged in.'


class ListaContatos(Resource):
    def get(self):
        contato = User.query.all()
        response = [{'dominio':i.dominio, 'email': i.email} for i in contato]
        return response

class FilterByDominio(Resource):
    def get(self, dominio):
        contatos = User.query.filter_by(dominio=dominio).all()
        try:
            response = {
                'dominio':contatos.dominio,
                'email':contatos.email,
            }
        except AttributeError:
            response = {
                'status':'error',
                'mensagem':'Dominio nao encontrado'
            }
        return response

api.add_resource(ListaContatos, '/contatos/')
api.add_resource(FilterByDominio, '/contatos/<string:dominio>/')

if __name__ == '__main__':
    app.run(debug=True)