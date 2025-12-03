#!/usr/bin/env python3

from flask import Blueprint, render_template, request, redirect, url_for
from musical import db
from musical.models import Production, Student, Role, Song, Thanks, Crew, Team
from musical.logic import import_students_from_csv

edit_bp = Blueprint("edit", __name__, template_folder="templates")

@edit_bp.route("/")
def dashboard():
    """Director dashboard: overview of productions and quick links."""
    productions = Production.query.all()
    return render_template("edit/dashboard.jinja", productions=productions)


@edit_bp.route("/productions", methods=["GET", "POST"])
def productions():
    """List all productions and allow adding new ones inline."""
    if request.method == "POST":
        prod = Production(
            title=request.form["title"],
            subtitle=request.form.get("subtitle"),
            cover_image=request.form.get("cover_image"),
            location=request.form.get("location"),
            price=request.form.get("price"),
            copyright_info=request.form.get("copyright"),
            notes=request.form.get("notes"),
        )
        db.session.add(prod)
        db.session.commit()
        return redirect(url_for("edit.productions"))

    productions = Production.query.all()
    return render_template("edit/productions.jinja", productions=productions)


@edit_bp.route("/productions/new", methods=["GET", "POST"])
def new_production():
    """Add a new production via form."""
    if request.method == "POST":
        prod = Production(
            title=request.form["title"],
            subtitle=request.form.get("subtitle"),
            cover_image=request.form.get("cover_image"),
            location=request.form.get("location"),
            price=request.form.get("price"),
            copyright_info=request.form.get("copyright"),
            notes=request.form.get("notes"),
        )
        db.session.add(prod)
        db.session.commit()
        return redirect(url_for("edit.productions"))
    return render_template("edit/new_productions.jinja")


@edit_bp.route("/students/import", methods=["POST"])
def import_students():
    """Import students from CSV into the database."""
    import_students_from_csv("cast.csv")
    return redirect(url_for("edit.dashboard"))


@edit_bp.route("/production/<int:production_id>/roles", methods=["GET", "POST"])
def roles(production_id):
    production = Production.query.get_or_404(production_id)
    students = Student.query.order_by(Student.name).all()  # get all students

    if request.method == "POST":
        if "delete_role_id" in request.form:
            role = Role.query.get_or_404(int(request.form["delete_role_id"]))
            db.session.delete(role)
            db.session.commit()
        else:
            role = Role(
                name=request.form["name"],
                actor=request.form["actor"],
                is_group="is_group" in request.form,
                display_order=int(request.form["display_order"]),
                production_id=production.id,
            )
            db.session.add(role)
            db.session.commit()
        return redirect(url_for("edit.roles", production_id=production.id))

    return render_template("edit/roles.jinja", production=production, roles=production.roles, students=students)


@edit_bp.route("/production/<int:production_id>/songs", methods=["GET", "POST"])
def songs(production_id):
    production = Production.query.get_or_404(production_id)
    

    if request.method == "POST":
        if "delete_song_id" in request.form:
            song = Song.query.get_or_404(int(request.form["delete_song_id"]))
            db.session.delete(song)
            db.session.commit()
        else:
            song = Song(
                title=request.form["title"],
                act_number=int(request.form.get("act_number", 1)),
                who_sings=request.form["who_sings"],
                is_reprise=("is_reprise" in request.form),
                production_id=production.id,
            )
            db.session.add(song)
            db.session.commit()
        return redirect(url_for("edit.songs", production_id=production.id))

    return render_template("edit/songs.jinja", production=production, songs=production.songs)


@edit_bp.route("/production/<int:production_id>/thanks", methods=["GET", "POST"])
def thanks(production_id):
    production = Production.query.get_or_404(production_id)

    if request.method == "POST":
        if "delete_thanks_id" in request.form:
            t = Thanks.query.get_or_404(int(request.form["delete_thanks_id"]))
            db.session.delete(t)
            db.session.commit()
        else:
            new_thanks = Thanks(
                production_id=production.id,
                thanks_text=request.form["thanks_text"],
            )
            db.session.add(new_thanks)
            db.session.commit()
        return redirect(url_for("edit.thanks", production_id=production.id))

    return render_template("edit/thanks.jinja", production=production, thanks=production.thanks)


@edit_bp.route("/production/<int:production_id>/crew", methods=["GET", "POST"])
def crew(production_id):
    production = Production.query.get_or_404(production_id)

    if request.method == "POST":
        if "delete_crew_id" in request.form:
            crew_member = Crew.query.get_or_404(int(request.form["delete_crew_id"]))
            db.session.delete(crew_member)
            db.session.commit()
        else:
            crew_member = Crew(
                name=request.form["name"],
                responsibility=request.form.get("responsibility"),
                production_id=production.id,
            )
            db.session.add(crew_member)
            db.session.commit()
        return redirect(url_for("edit.crew", production_id=production.id))

    return render_template("edit/crew.jinja", production=production, crew=production.crew)


@edit_bp.route("/production/<int:production_id>/team", methods=["GET", "POST"])
def team(production_id):
    production = Production.query.get_or_404(production_id)

    if request.method == "POST":
        if "delete_team_id" in request.form:
            team_member = Team.query.get_or_404(int(request.form["delete_team_id"]))
            db.session.delete(team_member)
            db.session.commit()
        else:
            team_member = Team(
                name=request.form["name"],
                role=request.form.get("role"),
                production_id=production.id,
            )
            db.session.add(team_member)
            db.session.commit()
        return redirect(url_for("edit.team", production_id=production.id))

    return render_template("edit/team.jinja", production=production, team=production.team)

@edit_bp.route("/productions/<int:production_id>/edit", methods=["GET", "POST"])
def edit_production(production_id):
    production = Production.query.get_or_404(production_id)

    if request.method == "POST":
        production.title = request.form["title"]
        production.subtitle = request.form.get("subtitle")
        production.cover_image = request.form.get("cover_image")
        production.location = request.form.get("location")
        production.price = request.form.get("price")
        production.copyright_info = request.form.get("copyright")
        production.notes = request.form.get("notes")

        db.session.commit()
        return redirect(url_for("edit.productions"))

    return render_template("edit/edit_production.jinja", production=production)


view_bp = Blueprint("view", __name__, template_folder="templates")

@view_bp.route("/")
def index():
    productions = Production.query.all()
    return render_template("view/index.jinja", productions=productions)


@view_bp.route("/production/<int:production_id>")
def production(production_id):
    production = Production.query.get_or_404(production_id)
    return render_template("view/program.jinja", production=production)


@view_bp.route("/cast/<int:production_id>")
def cast(production_id):
    production = Production.query.get_or_404(production_id)
    individual_roles = (
        Role.query.filter_by(production_id=production.id, is_group=False)
        .order_by(Role.display_order)
        .all()
    )
    group_roles = (
        Role.query.filter_by(production_id=production.id, is_group=True)
        .order_by(Role.display_order)
        .all()
    )
    return render_template(
        "view/cast.jinja",
        production=production,
        individual_roles=individual_roles,
        group_roles=group_roles,
    )


@view_bp.route("/crew/<int:production_id>")
def crew(production_id):
    production = Production.query.get_or_404(production_id)
    return render_template("view/crew.jinja", production=production)


@view_bp.route("/team/<int:production_id>")
def team(production_id):
    production = Production.query.get_or_404(production_id)
    return render_template("view/team.jinja", production=production)


@view_bp.route("/songs/<int:production_id>")
def songs(production_id):
    production = Production.query.get_or_404(production_id)
    songs_by_act = {}
    for song in production.songs:
        songs_by_act.setdefault(song.act_number, []).append(song)

    intermission = None
    if production.dates:
        intermission = production.dates[0].intermission_length

    return render_template(
        "view/songs.jinja",
        production=production,
        songs_by_act=songs_by_act,
        intermission=intermission,
    )


@view_bp.route("/thanks/<int:production_id>")
def thanks(production_id):
    production = Production.query.get_or_404(production_id)
    return render_template("view/thanks.jinja", production=production, thanks=production.thanks)
