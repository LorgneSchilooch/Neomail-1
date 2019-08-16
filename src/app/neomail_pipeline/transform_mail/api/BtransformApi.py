from src.app.neomail_pipeline.transform_mail.manager.TransformMailManager import TransformMmailManager
from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
from src.components.cloud_storage_manager.client.CloudStorageClient import CloudStorageClient
from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
import flask
import re

SERVICE_ACCOUNT = os.environ.get("SERVICE_ACCOUNT_GCP", default=False)
env_path = Path('src/apps/utils/data_pipeline/transform_mail/.env')

"""
Usage: transform data mails
GET host:port/transform/{name_file}
"""
app = flask.Blueprint('b_transform_gmail', __name__)


@app.route('/transform/<name_file>', methods=['GET', 'POST'])
def transform_mail(name_file):
    """
    Args:
        name_file:

    Returns:

    """

    name_user_dict = GmailDataFactory('prod').get_user().execute()
    name_user = re.search(r'(.*[^@]?)@', name_user_dict['emailAddress'])
    name_user = str(name_user.group(0).replace('@', '')).replace('.', '_')

    # read path from .env
    load_dotenv(dotenv_path=env_path)
    schema = os.getenv("SCHEMA")
    path_collect_mail = os.getenv("PATH_COLLECT")
    path_transform_mail = os.getenv("PATH_SAVE")
    bucket_id = os.getenv("BUCKET_ID")

    # collect mail from csv
    df_mail_collected = pd.read_csv(path_collect_mail + name_file, encoding='utf-8')

    # Transform part of mail
    df_mail = TransformMmailManager(df_mail_collected, schema).transform_mail()

    # Store mail in csv
    df_mail.to_csv(path_or_buf=path_transform_mail + name_file)

    # Insert data into GS
    # Send Csv into cloud storage
    object_path = path_transform_mail + name_file
    CloudStorageClient(SERVICE_ACCOUNT, bucket_id).buckets().insert(object_path)

