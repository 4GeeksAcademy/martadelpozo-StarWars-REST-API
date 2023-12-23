from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorite', back_populates='user')


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "favorites": [favorite.serialize() for favorite in self.favorites],
        }
  

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.String(50))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.Integer)
    favorites = db.relationship('Favorite', back_populates='planet')

    def __repr__(self):
        return '{}'.format(self.name)


    def serialize(self):
        return {
            "id"                :self.id,
            "name"              :self.name,
            "diameter"          :self.diameter,
            "rotation_period"   :self.rotation_period,
            "orbital_period"    :self.orbital_period,
            "gravity"           :self.gravity,
            "population"        :self.population,
            "climate"           :self.climate,
            "terrain"           :self.terrain,
            "surface_water"     :self.surface_water ,
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.String(10))
    mass = db.Column(db.String(10))
    hair_color = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))
    birth_year = db.Column(db.String(10))
    gender = db.Column(db.String(20))
    favorites = db.relationship('Favorite', back_populates='people')

    def __repr__(self):
        return '{}'.format(self.name)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    user = db.relationship('User', back_populates='favorites')
    planet = db.relationship('Planet', back_populates='favorites')
    people = db.relationship('People', back_populates='favorites')

    def __repr__(self):
        return 'Planet: {}, People: {}'.format(self.planet_id, self.people_id)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id,
        }
    
    

