from default.apps.classification_mail.model.KMeansModel import *
from default.apps.classification_mail.model.Metrics import *
from default.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
import pandas as pd
import requests
import flask
import nltk
import os

PATH = 'b_transform_gmail/'
nltk.download('punkt')
nltk.download("stopwords")
ENV = os.environ.get("FLASK_ENV", default=False)
GOOGLE_GMAIL_URI = 'https://mail.google.com/mail/u/0/#inbox'
"""
Usage: build labels in mails from clustering Model
GET host:port/labelling/gmail/{name_file}

example : 
"""

app = flask.Blueprint('labelling', __name__)


@app.route('/labelling/<name_file>', methods=['GET', 'POST'])
def build_label_mail(name_file):
    """method to build label from clustering Model
    this function take word, convert its to vector, calculate distance between vector from elbow method and using Kmeans.
    Args:
        name_file:

    Returns:

    """
    train = pd.read_csv(PATH + name_file, encoding='utf-8')

    clean_train_reviews = pre_processing_dataset(train)

    vocab_frame = build_vocab_frame(clean_train_reviews)

    tfidf_matrix, tfidf_vectorizer = build_tfidf_matrix_vector(clean_train_reviews)

    # calculating the within clusters sum-of-squares for 19 cluster amounts
    # calculating the optimal number of clusters
    n_clusters = optimal_number_of_clusters(calculate_wcss(tfidf_matrix))

    clusters, k_means_model = build_cluster_from_model(n_clusters, tfidf_matrix)

    labels = build_label_mails(vocab_frame,
                               k_means_model,
                               tfidf_vectorizer,
                               clusters,
                               clean_train_reviews, n_clusters)

    if ENV == 'production':
        len_labels = len(labels[0])
        return flask.redirect(flask.url_for('google_auth.home_page',
                                            code=302,
                                            len_labels=len_labels,
                                            mails=clean_train_reviews))
    else:
        for mail in clean_train_reviews:
            # print(mail)
            # print(mail['idMail'])
            for lbl in mail['label'][:1]:
                GmailDataFactory('prod').create_label('me',
                                                      name_label=lbl,
                                                      label_list_visibility="labelShow",
                                                      message_list_visibility="show")
            labels_ids = GmailDataFactory('prod').get_label_ids('me', mail['label'])

            GmailDataFactory('prod').modify_message(user_id='me',
                                                    mail_id=mail['idMail'],
                                                    mail_labels=create_msg_labels(labels_ids[:1]))

        return flask.redirect(flask.url_for('google_auth.home_page', code=302))


@app.route('/labelling/create/', methods=['POST'])
def create_label_mails(requests):
    clean_train_reviews = requests.form['mails']
    len_labels = requests.form['len_labels']

    for mail in clean_train_reviews:
        for lbl in mail['label'][:len_labels]:
            GmailDataFactory('prod').create_label('me',
                                                  name_label=lbl,
                                                  label_list_visibility="labelShow",
                                                  message_list_visibility="show")
        labels_ids = GmailDataFactory('prod').get_label_ids('me', mail['label'])

        GmailDataFactory('prod').modify_message(user_id='me',
                                                mail_id=mail['idMail'],
                                                mail_labels=create_msg_labels(labels_ids[:1]))

    return flask.redirect(GOOGLE_GMAIL_URI, code=302)


def create_msg_labels(labels_id):
    """Create object to update labels.
    Args:
        labels_id:
    Returns:
      A label update object.
    """
    return {'removeLabelIds': [], 'addLabelIds': labels_id}
