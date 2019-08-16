from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
from src.app.neomail_pipeline.transform_mail.manager.TransformMailManager import TransformMmailManager
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import os

env_path = Path('src/app/neomail_pipeline/transform_mail/.env')
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

    # read path from .env
    load_dotenv(dotenv_path=env_path)
    schema = os.getenv("SCHEMA")
    path_collect_mail = os.getenv("PATH_COLLECT")
    path_transform_mail = os.getenv("PATH_SAVE")

    # collect mail from csv
    df_mail_collected = pd.read_csv(path_collect_mail + name_file, encoding='utf-8')

    # Transform part of mail
    df_mail = TransformMmailManager(df_mail_collected, schema).transform_mail()

    # Store mail in csv
    df_mail.to_csv(path_or_buf=path_transform_mail + name_file)


if __name__ == '__main__':
    name = "manitra.harison@gmail.com1565679252.csv"
    main(name)
