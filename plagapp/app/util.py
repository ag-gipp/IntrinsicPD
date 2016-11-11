from app import app
import os
import glob
import sys


sys.path.append(app.config['PLAGCOMPS_LOC'])

from plagcomps.shared.util import IntrinsicUtility

#separated stylistic features into three different groups (seenu.andi-rajendran)
vocab_richness= [
        'honore_r_measure',
        'hapax_legomena',
        'hapax_dislegomena',
        'simpsons_d',
        'sichels_s',
        'brunets_w',
        'yule_k_characteristic',
        'yule_i',
        'type_token_ratio'
]

synt_feats = [
        'stopword_percentage',
        'punctuation_percentage',
        'avg_internal_word_freq_class',
        'avg_external_word_freq_class',
        'average_word_length',
        'average_sentence_length',
        'syntactic_complexity',
        'average_syllables_per_word',
        'alpha_chars_ratio',
        'digit_chars_ratio',
        'upper_chars_ratio',
        'white_chars_ratio'
]

read_feat = [
        'coleman_liau_index',
        'automated_readability_index',
        'linsear_write_formula',
        'gunning_fog_index',
        'dale_chall_readability_score',
        'polysyllablcount',
        'smog_index',
        'flesch_reading_ease',
        'flesch_kincaid_grade'
]


def get_file_options():
    #static_file_loc = os.path.join(app.config['APP_ROOT'], 'static/sample_docs')
    sample_corpus_loc = os.path.join(app.config['PLAGCOMPS_LOC'], 'plagcomps/sample_corpus')

    # Grab document options from both the plagapp static sample docs
    # and the sample corpus directory in the plagcomps repo
    #local_file_options = glob.glob(static_file_loc + '/*.txt')
    sample_corpus_options = glob.glob(sample_corpus_loc + '/*.txt')
    #file_options = [os.path.basename(f) for f in local_file_options + sample_corpus_options]
    file_options = [os.path.basename(f) for f in sample_corpus_options]
    without_extensions = [os.path.splitext(f)[0] for f in file_options]

    #full_paths = [os.path.join(static_file_loc, f) for f in local_file_options] + \
    full_paths = [os.path.join(sample_corpus_loc, f) for f in sample_corpus_options]

    # If on the comps machine, also grab the full training set of corpus
    #training_rel_paths, training_full_paths = get_training_set_files()
    #without_extensions += training_rel_paths
    #full_paths += training_full_paths

    return full_paths, without_extensions

def get_config_files():
    return [config_file[:-5] for config_file in os.listdir('./config_files') if config_file.endswith('.json')]

def get_training_set_files():
    util = IntrinsicUtility()
    full_paths = util.get_n_training_files()
    relative_paths = util.get_relative_training_set(IntrinsicUtility.TRAINING_LOC)
    # Strip leading '/' and remove '/'s to prepare for URL
    relative_paths = [r[1:].replace('/', '-') for r in relative_paths]

    return relative_paths, full_paths


def get_file_short_names():
    full_paths, file_names = get_file_options()
    return zip(file_names, file_names)

def get_folder_names():
    sample_corpus_loc = os.path.join(app.config['PLAGCOMPS_LOC'], 'plagcomps/sample_corpus')
    folders=next(os.walk(sample_corpus_loc))[1]
    return zip(folders, folders)

def get_file_to_full_paths():
    full_paths, file_names = get_file_options()

    return {name : full for name, full in zip(file_names, full_paths)}


def get_vocab_richness():
    options = vocab_richness

    return zip(options, options)

def get_word_feature_options():
    options = [
        'avg_internal_word_freq_class',
        'avg_external_word_freq_class',
    ]

    return zip(options, options)

def get_synt_feats():
    options = synt_feats
    return zip(options, options)

def get_read_feat():
    options = read_feat
    return zip(options, options)

def get_atom_options():
    options = [
        'paragraph',
        'sentence',
        'nchars'
    ]

    return zip(options, options)

#added cosine to clustering options (seenu.andi-rajendran)
def get_cluster_options():
    options = [
        'kmeans',
        'agglom',
        'density_based',
        'hmm',
        'none',
        'cos'
    ]

    return zip(options, options)


def get_similarity_options():
    options = [
        'euclidean',
        'cosine',
        'correlation',
        'cityblock',
        'chebyshev'
    ]

    return zip(options, options)
