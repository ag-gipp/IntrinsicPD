''' This module acquires evaluation measures such as F1s, P,R and prints them as csv and creates visualization of the same. Corpus location has to be pasted under/plagapp folder. for example:plagapp/vroniplag/
author:seenu.andi-rajendran

'''

from __future__ import division #to automatically create float values
import os# library for folder reading operations
import csv# library for csv operations

#to create images
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np # numpy to create arrays from lists

import json #to read models

#to import plagcomps functions
import imp
pd = imp.load_source('PlagDetector', './app/plag_detector.py')
ut = imp.load_source('', './app/util.py')

#importing functions for performing cross validation
from sklearn import cross_validation
from sklearn import linear_model
lr = linear_model.LinearRegression()



features=[
        'honore_r_measure',
        'hapax_legomena',
        'hapax_dislegomena',
        'simpsons_d',
        'sichels_s',
        'brunets_w',
        'yule_k_characteristic',
        'yule_i',
        'type_token_ratio',
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
        'white_chars_ratio',
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
clusterops = [
    'kmeans',
    'agglom',
    'density_based'
]

atom_types=['paragraph','sentence']


vrfiles=[f for f in os.listdir('vroniplag') if f.endswith('.txt')] #list of all vroniplag files
configs=[f for f in os.listdir('configs') if f.endswith('.json')] #list of all models


#getting confidences and ground truths
def getconf(file,features,clustering,atom_type):
    print file

    confs = []
    try:
        all_passages = pd.PlagDetector().get_passages(atom_type, features, clustering, 2, 'vroniplag/' + file)
        for passage in all_passages:  # for each row or atom as each atom is represented as such
            confs.append([passage.plag_confidence, 'True' if len(passage.plag_spans) > 0 else 'False'])
    except IndexError:
        confs=[]
    return confs

#creating image with one bar for each entry (for f1 and cross validation)
def getimg1bar(f1s,sets,imgnm):
    print len(f1s)
    print len(sets)
    plt.figure(figsize=(20, 10))
    y_pos = np.arange(len(sets))
    plt.barh(y_pos, f1s, align='center', alpha=0.5)
    plt.yticks(y_pos, sets)
    plt.savefig(imgnm)

#creating image with two bars for each entry (for precision and recall)
def getimg2bars(precs,recs,sets,imgnm):
    y_pos = np.arange(len(sets))
    fig, ax = plt.subplots(figsize=(20,10))
    ax.barh(y_pos,precs,0.4,color='red',label='Precision')
    ax.barh(y_pos+0.4, recs, 0.4, color='green', label='Recall')
    ax.set(yticks=y_pos+0.4,yticklabels=sets)
    ax.legend()
    plt.savefig(imgnm)

#retrieving settings from the models
def getsettings(file):
    with open('configs/' + file, 'r') as inj:
        sett = json.loads(inj.read())
    return (file,sett)

#calculating precision and recall and f1 takes threshold and confidences(with ground truths) as input
def getrates(confs,lim):
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for conf in confs:
        if conf[0] >= lim and conf[1]=='True':  # true positive condition when conf is above threshold
            tp += 1  # increment count of true positive when threshold is 0.85

        if conf[0] >= lim and conf[1]=='False':  # false positive condition when conf is above threshold
            fp += 1

        if conf[0] < lim and conf[1]=='True':  # false negative condition when conf is below threshold
            fn += 1
        if conf[0] < lim and conf[1]=='False':  # true negative condition when conf is above threshold
            tn += 1

    # calculate all precision and recall values
    try:
        precision = (tp / (tp + fp))
    except ZeroDivisionError:
        precision = 0

    try:
        recall = (tp / (tp + fn))
    except ZeroDivisionError:
        recall = 0

    try:
        f1 = 2 * ((precision * recall) / (precision + recall))
    except ZeroDivisionError:
        f1 = 0
    #print (precision,recall,f1)
    return (precision,recall,f1)

#perform cross validation
def testxval():
    scsavgs=[]
    for cf in configs:
        scs=[]
        for file in vrfiles:
            sett = getsettings(cf)
            k = sett['k']
            cluster_method = sett['cluster_method']
            atom_type = sett['atom_type']
            features = sett['features']
            all_passages = pd.PlagDetector().get_passages(atom_type, features, cluster_method, 2, 'vroniplag/' + file)
            cfs = []
            for passage in all_passages:  # for each row or atom as each atom is represented as such
                cfs.append([passage.plag_confidence, 'True' if passage.plag_spans else 'False'])
                fs=[passage.features[f] for f in features]
            Y = cfs
            X = fs

            try:
                scores = cross_validation.cross_val_score(lr, np.array(X), np.array(Y), cv=5)  # retrieves cross validation scores after performing it for five times
                scs.append(scores.mean())
            except ValueError:
                continue
        try:
            scsavg = (sum(scs) / len(scs))
        except ZeroDivisionError:
            scsavg = 0
        scsavgs.append(scsavg)
    getimg1bar(scsavgs, configs, 'configs_xval.png')

#get list of precision, recall and f1 values for each file
def getavgs(sett,thres):
    precs = []
    recs = []
    f1s = []
    for file in vrfiles[:5]:
        k = sett['k']
        cluster_method = sett['cluster_method']
        atom_type = sett['atom_type']
        features = sett['features']
        confs = getconf(file, features, cluster_method, atom_type)
        cfs = [cf[0] for cf in confs]
        if 'pc' in str(thres):
            lim = np.percentile(cfs, int(thres[:2]))
        else:
            lim = thres
        rates = getrates(confs, lim)
        precs.append(rates[0])
        recs.append(rates[1])
        f1s.append(rates[2])
    #print (precs,recs,f1s)
    return precs,recs,f1s

#getting average precision, recall and f1 values and creating their images
def testconfigs(thres):
    avgprecs = []
    avgrecs = []
    avgf1s = []

    csvfile = open('configs_'+str(thres) + '.csv', 'wb')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['config', 'avgf1', 'avgprec', 'avgrec'])

    for cf in configs:
        sett = getsettings(cf)
        precs,recs,f1s=getavgs(sett[1],thres)
        try:
            avgprec=sum(precs) / len(precs)
            avgprecs.append(avgprec)
        except ZeroDivisionError:
            avgprecs.append(0)
        try:
            avgrec=sum(recs) / len(recs)
            avgrecs.append(avgrec)
        except ZeroDivisionError:
            avgrecs.append(0)
        try:
            avgf1=sum(f1s) / len(f1s)
            avgf1s.append(avgf1)
        except ZeroDivisionError:
            avgf1s.append(0)
        csvwriter.writerow([cf, avgf1, avgprec, avgrec])
    getimg1bar(avgf1s, configs, 'configs_f1s_'+str(thres)+'.png')
    getimg2bars(avgprecs, avgrecs, configs, 'configs_prec_rec_'+str(thres)+'.png')

#getting average precision, recall and f1 values and creating their images
def testfeats(thres):
    for atom_type in atom_types:
        for cluster_method in clusterops:
            csvfile = open(cluster_method+'_'+atom_type + '_' + str(thres) + '.csv', 'wb')
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['feature','avgf1','avgprec','avgrec'])
            avgprecs = []
            avgrecs = []
            avgf1s = []
            sett = {}
            for feature in features:
                sett['features']=[feature]
                sett['atom_type']=atom_type
                sett['k']=2
                sett['cluster_method'] = cluster_method
                precs,recs,f1s=getavgs(sett,thres)
                try:
                    avgprec=sum(precs) / len(precs)
                    avgprecs.append(avgprec)
                except ZeroDivisionError:
                    avgprecs.append(0)
                try:
                    avgrec = sum(recs) / len(recs)
                    avgrecs.append(avgrec)
                except ZeroDivisionError:
                    avgrecs.append(0)
                try:
                    avgf1=sum(f1s) / len(f1s)
                    avgf1s.append(avgf1)
                except ZeroDivisionError:
                    avgf1s.append(0)
                csvwriter.writerow([feature,avgf1,avgprec,avgrec])
            getimg1bar(avgf1s,features,cluster_method + '_' + atom_type + '_' + str(thres)+'_f1.png')
            getimg2bars(avgprecs,avgrecs,features,cluster_method + '_' + atom_type + '_' + str(thres)+'_prec_rec.png')
            csvfile.close()

#testing
if __name__ == '__main__':
    #testfeats(0.85) #tests for confidence 0.85
    #testfeats('90pc') #tests for upper quartile '90pc'
    testconfigs(0.85)
