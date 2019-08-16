from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
from src.app.neomail_pipeline.transform_mail.manager.TransformMailManager import TransformMmailManager
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import json
import os
import csv
import time
import sys

SERVICE_ACCOUNT = Path('resources/gcp_credential/service_account.json')
SCHEMA = Path('src/app/neomail_pipeline/transform_mail/resources/schema/gmail_fields.json')
PATH_COLLECT = 'a_collect_gmail/'
PATH_SAVE = './b_transform_gmail/'

"""
Usage:
python -m src.app.neomail_pipeline.transform_mail.tests.BtransformMail
"""


def main(name_file):
    """
    Args:
        name_file:

    Returns:

    """
    df_mail_collected = pd.read_csv(PATH_COLLECT + name_file, encoding='utf-8')

    df_mail = TransformMmailManager(df_mail_collected).transform_mail()

    df_mail.to_csv(path_or_buf=PATH_SAVE + name_file)


if __name__ == '__main__':
    name = "manitra.harison@gmail.com1565679252.csv"
    main(name)
