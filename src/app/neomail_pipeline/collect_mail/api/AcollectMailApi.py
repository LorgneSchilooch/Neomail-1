# Importing required libraries
from src.components.cloud_storage_manager.client.CloudStorageClient import CloudStorageClient
from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
from src.components.big_query_manager.client.BigQueryClient import BigQueryClient
from src.app.neomail_pipeline.collect_mail.manager.CollectManager import CollectManager
from dotenv import load_dotenv
import flask
from pathlib import Path
import json
import csv
import os
import re
import time

SERVICE_ACCOUNT = os.environ.get("SERVICE_ACCOUNT_GCP", default=False)
SCHEMA = "src/apps/utils/data_pipeline/collect_mail/resources/schema/gmail_fields.json"
PATH_SAVE = "a_collect_gmail/"

"""
Usage: collect data from Gmail
GET host:port/collect/gmail/{name_file}

example : 
"""

app = flask.Blueprint('a_collect_gmail', __name__)


@app.route('/collect', methods=['GET'])
def collect_mail():
    """
    Returns:

    """
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')
    begin_time = time.time()

    name_file_dict = GmailDataFactory('prod').get_user().execute()
    name_file = name_file_dict['emailAddress'] + str(int(begin_time))

    # transform_uri = os.environ.get("FN_BASE_URI", src=False) + '/transform/' + name_file + '.csv'
    name_file_csv = name_file + '.csv'

    schema = {}
    with open(SCHEMA) as json_file:
        schema['fields'] = json.load(json_file)

    fieldnames = []
    for field in schema['fields']:
        fieldnames.append(field['name'])

    # Collect mail
    message_id = GmailDataFactory('prod').get_message_id('me',
                                                         include_spam_trash=False,
                                                         max_results=10000,
                                                         batch_using=True)

    reader = csv.mails = CollectManager('prod').collect_mail('me', message_id)
    # Save mail in Csv
    with open(PATH_SAVE + name_file + '.csv', 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=fieldnames)
        fc.writeheader()
        fc.writerows(reader)

    return flask.redirect(flask.url_for('b_transform_gmail.transform_mail', name_file=name_file_csv, code=302))