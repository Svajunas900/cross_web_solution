from flask import Flask, render_template, jsonify, request, redirect
import pandas as pd
from flask_oauthlib.provider import OAuth2Provider
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime
import uuid


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oauth.db'
db = SQLAlchemy(app)

oauth = OAuth2Provider(app)
oauth.init_app(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/current_compet_info")
def current_competitors_info():
    df = pd.read_csv('competitors.csv')
    return render_template("current_info.html", data=df.to_dict())


@app.route("/letter_compet/<letter>")
def letter_competitor(letter: str):
    df = pd.read_csv('competitors.csv')
    df = df.where(df['name'].str.startswith(letter)).dropna()
    df = pd.DataFrame(df)
    return render_template("letter_compet.html", data=df.to_dict())


@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if request.method == 'POST':
        client_id = request.form["client_id"]
        redirect_uri = request.form["redirect_uri"]
        grant = Grant(client_id=client_id, code="authorization_code", redirect_uri=redirect_uri, scope="read,write")
        save_grant(grant)

        return redirect("/")
    return render_template("authorize.html")


@app.route('/token', methods=['GET','POST'])
def issue_token():
    if request.method == 'POST':
        grant_type = request.form.get('grant_type')
        if grant_type == 'authorization_code':
            code = request.form.get('code')
            client_id = request.form.get('client_id')
            client = get_client(client_id)
            print(code, client, client_id)
            grant = get_grant(client_id=client_id, code=code)
            print(grant)
            if grant:
                token = {
                    'access_token': 'generated_access_token', 
                    'refresh_token': 'generated_refresh_token',  
                    'expires_in': 3600,
                    'scope': grant.scope,
                }
                save_token(token, client_id)
                return jsonify(token)  
            return 'Invalid grant code', 400

        else:
            return 'Unsupported grant type', 400
    return render_template("token.html")




@app.route('/profile')
@oauth.require_oauth()
def profile():
    return jsonify(username='example_user', email='example@example.com')


@oauth.invalid_response
def invalid_require_oauth(req):
    for x in Token.query.all():
        print(x.access_token, x.refresh_token, x.client_id)
    return jsonify(message=req.error_message), 401


@app.route('/register-client', methods=['POST'])
def register_client():
    data = request.get_json()

    # if 'default_scopes' not in data:
    #     return jsonify({'error': 'Missing required fields'}), 400

    redirect_uris = "http://127.0.0.1:5000"
    default_scopes = "read,write"


    client_id = str(uuid.uuid4())  
    client_secret = str(uuid.uuid4())  

    new_client = Client(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uris=redirect_uris,
        default_scopes=default_scopes
    )

    db.session.add(new_client)
    db.session.commit()

    return jsonify({
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uris': redirect_uris,
        'default_scopes': default_scopes
    }), 201 


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(55)) 
    email = db.Column(db.String(100), unique=True)  
    password_hash = db.Column(db.Text)  


class Client(db.Model):
  __tablename__ = 'clients'
  client_id = db.Column(db.String(40), primary_key=True)
  client_secret = db.Column(db.String(55), unique=True, index=True,
                            nullable=False)
  user_id = db.Column(db.ForeignKey('users.id'))
  user = db.relationship('User')
  redirect_uris = db.Column(db.Text)
  default_scopes = db.Column(db.Text)


class Grant(db.Model):
  __tablename__ = 'grants'
  id = db.Column(db.Integer, primary_key=True)
  client_id = db.Column(db.String(40))
  user_id = db.Column(db.ForeignKey('users.id'))
  user = db.relationship('User')
  code = db.Column(db.String(120))
  redirect_uri = db.Column(db.String(120))
  scope = db.Column(db.Text)


class Token(db.Model):
  __tablename__ = 'tokens'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.ForeignKey('users.id'))
  user = db.relationship('User')
  access_token = db.Column(db.String(120), unique=True)
  refresh_token = db.Column(db.String(120), unique=True)
  expires = db.Column(db.DateTime)
  client_id = db.Column(db.String(40))
  scope = db.Column(db.Text)


@oauth.clientgetter
def get_client(client_id):
    for x in Client.query.all():
        print(x.client_id, x.client_secret)
    return Client.query.filter_by(client_id=client_id).first()

@oauth.grantgetter
def get_grant(client_id, code):
    for x in Grant.query.all():
        print(x.client_id, x.code, x.scope, x.redirect_uri)
    print(client_id, code)
    return Grant.query.filter_by(client_id=client_id, code=code).first()

@oauth.grantsetter
def save_grant(grant):
    db.session.add(grant)
    db.session.commit()

@oauth.tokengetter
def get_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    if refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()

@oauth.tokensetter
def save_token(token, client_id, *args, **kwargs):
    toks = Token.query.filter_by(client_id=client_id)
   
    for t in toks:
        db.session.delete(t)

    expires_in = token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        scope=token['scope'],
        expires=expires,
        client_id=client_id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok



if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)