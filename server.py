from flask import Flask, request, jsonify
from flask.views import MethodView
from schema import validate_create_user, validate_create_bulletin
from errors import HttpError
from db import Session, User, Bulletin
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

app = Flask('server')
bcrypt = Bcrypt(app)


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error', 'description': error.message})
    http_response.status_code = error.status_code
    return http_response


def get_user(user_id: int, session: Session):
    user = session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, 'user not found')
    return user



class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            return jsonify({
                'id': user.id,
                'username': user.username,
                'creation_time': user.creation_time.isoformat()

            })

    def post(self):
        json_data = validate_create_user(request.json)
        json_data['password'] = bcrypt.generate_password_hash(json_data['password'].encode()).decode()
        with Session() as session:
            new_user = User(**json_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'user already exists')
            return jsonify(
                {
                    'id': new_user.id,
                    'creation_time': int(new_user.creation_time.timestamp()),
                    'password': new_user.password
                }
            )

    def patch(self, user_id: int):
        json_data = request.json
        with Session() as session:
            user = get_user(user_id, session)
            for field, value in json_data.items():
                setattr(user, field, value)
            session.add(user)
            session.commit()
        return jsonify({'status': 'succes'})

    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()
        return jsonify({'status': 'succes'})


def get_bulletin(bulletin_id: int, session: Session):
    bulletin = session.query(Bulletin).get(bulletin_id)
    if bulletin is None:
        raise HttpError(404, 'bulletin not found')
    return bulletin



class BulletinView(MethodView):

    def get(self, bulletin_id: int):
        with Session() as session:
            bulletin = get_bulletin(bulletin_id, session)
            return jsonify({
                'id': bulletin.id,
                'header': bulletin.header,
                'description': bulletin.decription,
                'creation_bulletin': bulletin.creation_time.isoformat(),
                'owner': bulletin.user.username
            })

    def post(self):
        json_data = validate_create_bulletin(request.json)
        json_data['password'] = bcrypt.generate_password_hash(json_data['password'].encode()).decode()

        with Session() as session:
            user = get_user(json_data['username'], session)
            password = get_user(json_data['password'], session)
            if password == json_data['password']:
                new_bulletin = Bulletin(**json_data)
                session.add(new_bulletin)
                try:
                    session.commit()
                except IntegrityError:
                    raise HttpError(409, 'bulletin already exists')
                return jsonify(
                    {
                        'id': new_bulletin.id,
                        'header': new_bulletin.header,
                        'description': new_bulletin.description,
                        'creation_time': int(new_bulletin.creation_time.timestamp()),
                        'owner': new_bulletin.user.username
                    }
                )
            else:
                HttpError(401, 'authorisation Error')



    def delete(self, bulletin_id: int):
        with Session() as session:
            bulletin = get_user(bulletin_id, session)
            session.delete(bulletin)
            session.commit()
        return jsonify({'status': 'succes'})


app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('users_witg_id'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users', view_func=UserView.as_view('users'), methods=['POST'])

app.add_url_rule('/bulletin/<int:bulletin_id>', view_func=BulletinView.as_view('buletins_witg_id'), methods=['GET', 'DELETE'])
app.add_url_rule('/bulletin', view_func=BulletinView.as_view('bulletins'), methods=['POST'])

app.run(port=5000)