from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.contact import Contact
from utils.db import db

contacts = Blueprint("contacts", __name__)


@contacts.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

#Realiza una inserción en la base de datos
@contacts.route('/new', methods=['POST'])
def add_contact():
    if request.method == 'POST':

        # Recibe la información del formulario
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']

        # Crea un nuevo objeto de tipo Contacto
        new_contact = Contact(fullname, email, phone)

        # Guarda la información en la base de datos
        db.session.add(new_contact)
        db.session.commit()

        flash('Contact added successfully!')

        return redirect(url_for('contacts.index'))

#Acualiza la información de un contacto registrado en la base de datos
@contacts.route("/update/<string:id>", methods=["GET", "POST"])
def update(id):
    # Obtiene un contacto mediante un id
    print(id)
    contact = Contact.query.get(id)

    #Realiza la actualización de los datos con los datos del formulario
    if request.method == "POST":
        contact.fullname = request.form['fullname']
        contact.email = request.form['email']
        contact.phone = request.form['phone']

        db.session.commit()

        flash('Contact updated successfully!')

        return redirect(url_for('contacts.index'))

    return render_template("update.html", contact=contact)

#Elimina la información de un contacto registrado en la base de datos
@contacts.route("/delete/<id>", methods=["GET"])
def delete(id):
    #Elimina el registro de un contacto mediante su id
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()

    flash('Contact deleted successfully!')

    return redirect(url_for('contacts.index'))


@contacts.route("/about")
def about():
    return render_template("about.html")
