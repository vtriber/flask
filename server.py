from flask import Flask, request, jsonify
from flask.views import MethodView
from schema import  validate_create_user
from errors import HttpError
from db import Session, User
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
        pass

    def delete(self, user_id: int):
        pass

app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('users_witg_id'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users', view_func=UserView.as_view('users'), methods=['POST'])

app.run(port=5000)