from flask import Flask, request, jsonify
from pony import orm
from pony.orm import *
from datetime import datetime
from pony.converting import str2datetime
DB = orm.Database()

app = Flask(__name__)


class Room(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    room_name = orm.Required(str)
    temperature = orm.Required(float)
    date = orm.Required(datetime)


DB.bind(provider="sqlite",
    filename="database.sqlite", create_db=True)

DB.generate_mapping(create_tables=True)


@app.route('/room', methods=['POST'])
@db_session
def add_room():
    room = Room(
        room_name=request.json['room_name'],
        temperature=float(request.json['temperature']),
        date=datetime.strptime(request.json['date'], '%Y-%m-%d')
    )
    return {"room name": room.room_name}, 201


@app.route('/room/<name>/<date>', methods=['GET'])
@db_session
def get_temperature(name, date):
    room = Room.get(room_name=name, date=datetime.strptime(date, '%Y-%m-%d'))
    if room is None:
        return {'error': 'Room not found'}, 404
    return {'temperature': room.temperature}


@app.route('/room/<name>/average', methods=['GET'])
@db_session
def get_average_temperature(name):
    avg_temperature = avg(room.temperature for room in select(
        room for room in Room if room.room_name == name))
    if avg_temperature is None:
        return {'error': 'Room not found'}, 404
    return {'average_temperature': avg_temperature}



@app.route('/room/<name>/<date>', methods=['DELETE'])
@db_session
def delete_temperature(name, date):
    room = Room.get(room_name=name, date=datetime.strptime(date, '%Y-%m-%d'))
    if room is None:
        return {'error': 'Room not found'}, 404
    room.delete()
    return {"room deleted"}, 204


if __name__ == '__main__':
    app.run(port='8080', host='0.0.0.0', debug=True)
