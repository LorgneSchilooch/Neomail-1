import os
import flask
import gevent.pywsgi

from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
import src.components.gmail_manager.tests.routes.TestGmailRoutes
import src.components.o_auth2_web_server.test.routes.test
import src.components.o_auth2_web_server.google_auth
import src.apps.classification_mail.api.build_label
import src.apps.classification_mail.routes.delete_label
import src.apps.collect_mail.api.AcollectMailApi
import src.apps.transform_mail.api.BtransformApi

app = flask.Flask(__name__, template_folder='./templates')
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(src.components.o_auth2_web_server.google_auth.app)
app.register_blueprint(src.components.gmail_manager.tests.routes.TestGmailRoutes.app)
app.register_blueprint(src.apps.collect_mail.api.AcollectMailApi.app)
app.register_blueprint(src.apps.transform_mail.api.BtransformApi.app)
app.register_blueprint(src.apps.classification_mail.api.build_label.app)
app.register_blueprint(src.apps.classification_mail.routes.delete_label.app)
app.register_blueprint(src.components.o_auth2_web_server.test.routes.test.app)
app_server = gevent.pywsgi

