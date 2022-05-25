from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#pipenv run migrate
#pipenv run upgrade

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=True)
    hair_color = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,

            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=True)
    gravity = db.Column(db.Integer, unique=False, nullable=True)
    population = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,

            # do not serialize the password, its a security breach
        }

class Fav_people(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #quien le dio a favoritos
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #cual es el favorito
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    #defino las relaciones
    rel_user = db.relationship(User)
    rel_people = db.relationship(People)
    
    def __repr__(self):
        return '<FavPeople %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
         
            # do not serialize the password, its a security breach
        }

class Fav_planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #quien le dio a favoritos
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #cual es el favorito
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    #defino las relaciones
    rel_user = db.relationship(User)
    rel_planets = db.relationship(Planets)
    
    def __repr__(self):
        return '<FavPlanets %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planets_id": self.planets_id,
         
            # do not serialize the password, its a security breach
        }


