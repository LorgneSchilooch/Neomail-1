from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import base64
import bleach
import re
import unicodedata
import json

class TransformMmailManager(object):

    def __init__(self, mail, schema):
        """

        Args:
            mail:
        """
        """Get a Data from table in BigQuery
        Args:
            self : Authorized BigQuery API service instance.
            mail:
        Returns:
        """
        self.__mail = mail
        self.__schema = schema
        self.__mails_collected = []

    def __get_fieldnames(self):
        """
        Returns:

        """
        schema = {}
        fieldnames = []
        with open(self.__schema) as json_file:
            schema['fields'] = json.load(json_file)
        for field in schema['fields']:
            fieldnames.append(field['name'])
        return fieldnames

    def transform_mail(self):
        """
        Returns:

        """
        df_mail_len = self.__mail['idMail'].size
        df_mail_clean = pd.DataFrame(columns=self.__get_fieldnames())

        for i in range(0, df_mail_len):
            df_mail_clean = df_mail_clean.append({'idMail': self.__mail['idMail'][i],
                                                  'threadId': self.__mail['threadId'][i],
                                                  'historyId': self.__mail['historyId'][i],
                                                  'from': self.__mail['from'][i],
                                                  'to': self.__mail['to'][i],
                                                  'date': self.__mail['date'][i],
                                                  'labelIds': str((self.__mail['labelIds'][i])).replace('[',
                                                                                                        '').replace(']',
                                                                                                                    '').replace(
                                                      '\'', ''),
                                                  'spam': 1 if 'SPAM' in self.__mail['labelIds'][i] else 0,
                                                  'mimeType': self.__mail['mimeType'][i],
                                                  'body': self.__html_to_text(str(self.__mail['body'][i]))
                                                  },
                                                 ignore_index=True)

        return df_mail_clean
        # elif self.__mail['snippet'] is not None:
        #     mail['idMail'] = self.__mail['idMail']
        #     mail['threadId'] = self.__mail['threadId']
        #     mail['historyId'] = self.__mail['historyId']
        #     mail['from'] = self.__mail['from']
        #     mail['to'] = self.__mail['to']
        #     mail['date'] = self.__mail['date']
        #     mail['labelIds'] = str((self.__mail['labelIds'])).replace('[', '').replace(']', '').replace('\'', '')
        #     mail['spam'] = 1 if 'SPAM' in self.__mail['labelIds'] else 0
        #     mail['body'] = self.__html_to_text(self.__mail['snippet'])
        #     return mail

    def __split_sender_mail(self):
        pass

    @staticmethod
    def __split_sender(mail):
        """
        Args:
            mail:

        Returns:

        """
        part_sender = mail['sender']
        try:
            name_sender, mail_sender = part_sender.split('<')
            mail_sender = mail_sender.replace('>', '')
            yield name_sender, mail_sender

        except Exception as exception:
            print(exception)

    def __html_to_text(self, body_dirty):
        """
        Args:
            body:

        Returns:

        """
        df_body_clean = {}

        if body_dirty is not None:
            soup = BeautifulSoup(body_dirty, 'html.parser')
            text = soup.getText()  # getting text from html

            lines = [line.strip() for line in text.splitlines()]  # removing leading/trailing spaces
            chunks = [phrase.strip() for line in lines for phrase in
                      line.split(' ')]  # breaking multi-headlines into
            # line each
            text = ' '.join([chunk for chunk in chunks])  # removing newlines
            # Using bleach
            clean_text = bleach.clean(text, strip=True)
            df_body_clean = self.remove_urls(clean_text)
        else:
            df_body_clean = ''

        return df_body_clean

    def remove_urls(self, v_text):
        """
        Args:
            v_text:

        Returns:

        """
        v_text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', v_text, flags=re.MULTILINE)
        new_string = self.strip_accents(v_text.lower())
        new_string = new_string.replace('&gt', '')
        text = re.sub('<[^<]+?>', '', new_string)
        text_clean = ' '.join([w for w in text.split() if ((len(w) > 3) and (len(w) < 23))])
        return text_clean

    @staticmethod
    def strip_accents(text):
        """
        Strip accents from input String.
        Args:
            text:

        Returns:

        """
        try:
            text = str(text, 'utf-8')
        except (TypeError, NameError):  # unicode is a src on python 3
            pass
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ASCII', 'ignore')
        text = text.decode("utf-8")
        return str(text)
