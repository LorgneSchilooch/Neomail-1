import os
import flask
import gevent.pywsgi

from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
import src.components.gmail_manager.tests.routes.TestGmailRoutes
import src.app.web_server.google_auth
import src.app.neomail_pipeline.transform_mail.api.BtransformApi
import src.app.neomail_pipeline.collect_mail.api.AcollectMailApi

app = flask.Flask(__name__, template_folder='./templates')
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(src.app.web_server.google_auth.app)
app.register_blueprint(src.app.web_server.test.routes.test.app)
app.register_blueprint(src.app.neomail_pipeline.collect_mail.api.AcollectMailApi.app)
app.register_blueprint(src.app.neomail_pipeline.transform_mail.api.BtransformApi.app)
app.register_blueprint(src.app.neomail_pipeline.classification_mail.api.build_label.app)
app.register_blueprint(src.app.neomail_pipeline.classification_mail.routes.delete_label.app)
app.register_blueprint(src.components.gmail_manager.tests.routes.TestGmailRoutes.app)
app_server = gevent.pywsgi

