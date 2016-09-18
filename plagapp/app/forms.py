from app import app
import os
from util import get_file_short_names, get_folder_names, get_sent_feature_options, get_word_feature_options, get_para_feature_options, get_cluster_options, get_similarity_options, get_atom_options

from flask_wtf import Form
from wtforms import SelectField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired

class PlagSelection(Form):
    file_options = get_file_short_names()
    doc_name = SelectField('Doc Name', choices=file_options)

    sent_feature_options = get_sent_feature_options()
    sent_features = SelectMultipleField('Features (Select Multiple)', choices=sent_feature_options)

    para_feature_options = get_para_feature_options()
    para_features = SelectMultipleField('Features (Select Multiple)', choices=para_feature_options)

    word_feature_options = get_word_feature_options()
    word_features = SelectMultipleField('Features (Select Multiple)', choices=word_feature_options)

    atom_options = RadioField()

    cluster_options = get_cluster_options()
    cluster_method = SelectField('Cluster Method', choices=cluster_options)

    similarity_options = get_similarity_options()
    similarity_measure = SelectField('Similarity Measure', choices=similarity_options)

    k_options = [2, 3, 4, 5]
    k = SelectField('k', choices=zip(k_options, k_options), coerce=int)

class PlagSelection4folder(Form):
    folder_options = get_folder_names()
    folder_name = SelectField('Folder Name', choices=folder_options)