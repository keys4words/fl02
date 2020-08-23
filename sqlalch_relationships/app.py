from flask import Flask, render_template, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os, json


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'rel-db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

actors = db.Table(
    "actors",
    db.Column("actor_id", db.Integer, db.ForeignKey("actor.id")),
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id")),
)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    release_date = db.Column(db.DateTime)
    actors = db.relationship("Actor", secondary=actors, backref="movies", lazy="select")

    def release_year(self):
        return self.release_date.strftime("%Y")

    # def actor_list(self):
    #     return self.actors.split(',')


class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    movies = db.relationship('Movie', backref='director', lazy="select")
    guild = db.relationship(
        "GuildMembership", backref="director", lazy="select", uselist=False
    )


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))


class GuildMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guild = db.Column(db.String(255))
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))



@app.route('/')
def index():
    movie = db.session.query(Movie).first()
    return render_template('movie.html', movie=movie)


@app.cli.command("initdb")
def reset_db():
    """Drops and Creates fresh database"""
    db.drop_all()
    db.create_all()

    print("Initialized default DB")


@app.cli.command("bootstrap")
def bootstrap_data():
    """Populates database with data"""
    db.drop_all()
    db.create_all()

    m = Movie(
        title="Evil Dead",
        release_date=datetime.strptime("Oct 15 1981", "%b %d %Y"),
        # actors="Bruce Campbell,Ellen Sandweiss,Hal Delrich, Betsy Baker,Sarah York",
    )

    # m2 = Movie(
    #     title="Darkman", release_date=datetime.strptime("Aug 24 1990", "%b %d %Y")
    # )

    # m3 = Movie(
    #     title="The Quick and the Dead",
    #     release_date=datetime.strptime("Feb 10 1995", "%b %d %Y"),
    # )

    # m4 = Movie(
    #     title="The Gift", release_date=datetime.strptime("Jan 19 2001", "%b %d %Y")
    # )

    # m5 = Movie(
    #     title="Army of Darkness",
    #     release_date=datetime.strptime("Feb 19 1993", "%b %d %Y"),
    # )

    db.session.add(m)
    # db.session.add(m2)
    # db.session.add(m3)
    # db.session.add(m4)
    # db.session.add(m5)

    d = Director(
        # first_name="Sam", last_name="Raimi", guild=GuildMembership(guild="Raimi DGA")
        first_name="Sam", last_name="Raimi"
    )
    guild = GuildMembership(guild="Raimi DGA")

    # d.movies.append(m)
    # m.director = d
    # m2.director = d
    # m3.director = d
    # m4.director = d
    # m5.director = d
    db.session.add(d)
    db.session.add(guild)
    d.movies.append(m)
    d.guild = guild

    bruce = Actor(
        first_name="Bruce",
        last_name="Campbell",
        # guild=GuildMembership(guild="Campbell SAG"),
    )
    ellen = Actor(
        first_name="Ellen",
        last_name="Sandweiss",
        # guild=GuildMembership(guild="Sandweiss SAG"),
    )
    hal = Actor(
        first_name="Hal",
        last_name="Delrich",
        # guild=GuildMembership(guild="Delrich SAG"),
    )
    betsy = Actor(
        first_name="Betsy", last_name="Baker",
        # guild=GuildMembership(guild="Baker SAG")
    )
    sarah = Actor(
        first_name="Sarah", last_name="York", 
        # guild=GuildMembership(guild="York SAG")
    )

    # darkman actors
    # liam = Actor(
    #     first_name="Liam", last_name="Neeson", guild=GuildMembership(guild="Neeson SAG")
    # )
    # frances = Actor(
    #     first_name="Frances",
    #     last_name="McDormand",
    #     guild=GuildMembership(guild="McDormand SAG"),
    # )

    # # Quick and the Dead Actors
    # sharon = Actor(
    #     first_name="Sharon", last_name="Stone", guild=GuildMembership(guild="Stone Sag")
    # )
    # gene = Actor(
    #     first_name="Gene",
    #     last_name="Hackman",
    #     guild=GuildMembership(guild="Hackman Sag"),
    # )

    # # The Gift Actors
    # cate = Actor(
    #     first_name="Cate",
    #     last_name="Blanchett",
    #     guild=GuildMembership(guild="Blanchett Sag"),
    # )
    # keanu = Actor(
    #     first_name="Keanu",
    #     last_name="Reeves",
    #     guild=GuildMembership(guild="Reeves Sag"),
    # )

    db.session.add(bruce)
    db.session.add(ellen)
    db.session.add(hal)
    db.session.add(betsy)
    db.session.add(sarah)
    # db.session.add(liam)
    # db.session.add(frances)
    # db.session.add(sharon)
    # db.session.add(gene)
    # db.session.add(cate)
    # db.session.add(keanu)

    m.actors.extend((bruce, ellen, hal, betsy, sarah))
    # m2.actors.extend((bruce, liam, frances))
    # m3.actors.extend((bruce, sharon, gene))
    # m4.actors.extend((bruce, cate, keanu))
    # m5.actors.append(bruce)

    db.session.commit()

    print("Added development dataset")


if __name__ == "__main__":
    app.run()