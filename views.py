'''from flask import Blueprint, render_template
import importlib


views = Blueprint(__name__,"views")


@views.route("/")
def home():
    return render_template("index.html",output=importlib.import_module("main").response)

'''