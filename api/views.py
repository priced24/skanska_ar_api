from flask import Blueprint, render_template
from flask.views import View

bp = Blueprint('views', __name__, url_prefix='/')


class UserViews(View):
    """ UserViews

    View class for rendering HTML templates
    """

    def __init__(self, template):
        self.template = template

    def dispatch_request(self, id=None):
        # Data will be called from routes using post requests.
        # If the id is present provide it to the template
        if id is None:
            return render_template(self.template)
        else:
            return render_template(self.template, sid=id)


bp.add_url_rule(
    "/",
    view_func=UserViews.as_view("mainpage", "index.html"),
)

bp.add_url_rule(
    "/configure/",
    view_func=UserViews.as_view("configure", "configure.html"),
)

bp.add_url_rule(
    "/ar/<int:id>/",
    view_func=UserViews.as_view("ar", "ar.html"),
)
