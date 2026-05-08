from flask import render_template

def register_error_handlers(app):
    @app.errorhandler(401)
    def unauthorized(e):
        return render_template('errors/error.html', code=401, title="Who are you?", message="You need to be logged in."), 401

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/error.html', code=403, title="Access Denied", message="Staff eyes only!"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/error.html', code=404, title="Page Vanished", message="This page isn't in the basket."), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/error.html', code=500, title="System Jam", message="Something went wrong."), 500
