# Import the actual Flask app
from app import app
#from plagcomps.dbconstants import *
from flask import render_template, redirect, jsonify, request, url_for
import sys, json
import os, csv, time, datetime
import numpy as np

#from forms import PlagSelection, PlagSelection4folder
from plag_detector import PlagDetector
from util import *
#import psycopg2 as dbops
THRES = 0.85


sample_corpus_loc = os.path.join(app.config['PLAGCOMPS_LOC'], 'plagcomps/sample_corpus')

@app.route('/index/')
@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/select_doc/') #seperated features into three different varieties and arranged them accordingly in the web page (seenu.andi-rajendran)
def select_doc():
    return render_template('select_doc.html',
                    docs = get_file_short_names(), synt_feats=get_synt_feats(),vocab_richness=get_vocab_richness(),config_fold=get_config_files(),
                           read_feat=get_read_feat(), word_features = get_word_feature_options(),cluster_methods = get_cluster_options(), atom_options = get_atom_options())#, similarity_measures = get_similarity_options())

@app.route('/view_doc')
def view_doc():
    modelyn = ''
    doc_name = request.args.get('doc')
    file_to_full_path = get_file_to_full_paths()
    if doc_name in file_to_full_path:
        full_path = file_to_full_path[doc_name]
    else:
        # TODO Make a nice error msg
        return 'some error'

    atom_type = request.args.get('atom')
    features = request.args.getlist('features')
    cluster_method = request.args.get('cluster_method')
    save_config = request.args.get('save_config')
    over_config = request.args.get('over_config')
    qload = request.args.get('qload')
    k = int(request.args.get('k'))
    # saving/modifying style models (seenu.andi-rajendran)
    if save_config=='yes':
        options = {'k': k, 'features': features, 'atom_type': atom_type, 'cluster_method': cluster_method}
        with open('config_files/'+request.args.get('fname')+'.json', "wb") as outconf: outconf.write(json.dumps(options))
    elif save_config=='no':
        if over_config=='no' and qload=='yes':
            with open('config_files/'+request.args.get('lname')+'.json', "rb") as inconf: options=json.loads(inconf.read())
            k=options['k']
            atom_type = options['atom_type']
            features = options['features']
            cluster_method = options['cluster_method']
            modelyn=request.args.get('lname')
        elif over_config=='yes' and qload=='yes':
            options = {'k': k, 'features': features, 'atom_type': atom_type, 'cluster_method': cluster_method}
            with open('config_files/' + request.args.get('lname') + '.json', "wb") as outconf:
                outconf.write(json.dumps(options))
    all_passages = PlagDetector().get_passages(atom_type, features, cluster_method, k, full_path)
    feature_names = all_passages[0].features.keys()

    chart = {"renderTo": 'chart', "type": 'heatmap', "height": 350, 'zoomType': 'x', 'panning': 'true', 'panKey': 'shift'}
    title = {"text": str(doc_name)}
    categories= [str(passage.char_index_start) for passage in all_passages]

    j=0
    i=0
    data=[]
    '''
    for feature in features:
        i=0
        for passage in all_passages:
            data.append([i, j, passage.features[feature]])
            i+=1
        j+=1
    '''
    #getting percentiles (seenu.andi-rajendran)
    cfs=[passage.plag_confidence for passage in all_passages]
    confs = np.array(cfs)
    lq_conf = np.percentile(confs,25)
    avg_conf = np.percentile(confs,50)
    uq_conf = np.percentile(confs,90)
    pc90 = np.percentile(confs,90)

    uq_cnt, thres_cnt, lq_cnt = 0,0,0
    for passage in all_passages:
        data.append([i, j, passage.plag_confidence])
        if passage.plag_confidence > THRES:
            thres_cnt += 1
        if passage.plag_confidence > uq_conf and passage.plag_confidence < THRES:
            uq_cnt+=1
        if passage.plag_confidence < uq_conf:
            lq_cnt+=1
        i+=1


    #getting values to build heatmap (seenu.andi-rajendran)
    series=[{'name':str(doc_name),'borderWidth': 1,
            'data':data, 'dataLabels': {
                'color': '#000000'
            }}]
    yAxis = {'categories': ['Plag. Conf.']}

    chart2 = {"type": 'heatmap'}
    title2 = {'text':str(doc_name)}
    categories2 = [str(doc_name)]#,'title':{'text':'null'}}

    '''
    if uq_conf<0.85:
        if avg_conf<uq_conf:
            dat=[0.0,avg_conf,uq_conf,0.85,1.0]
        elif avg_conf > uq_conf:
            dat = [0.0, uq_conf, avg_conf, 0.85, 1.0]
    elif uq_conf>0.85:
    '''
    dat = [0.0,lq_conf, avg_conf, uq_conf, 1.0]
    
    ser_dat=[]
    cp=0
    for passage in all_passages:
        ser_dat.append([0,passage.plag_confidence,passage.char_index_start,cp])
        cp+=1

    plag_cats =[str(passage.plag_spans[0][0]) for passage in all_passages if passage.plag_spans]

    if plag_cats:

        zone=[{
                 'value': THRES,
                 'color': 'black'
             }, {'value': 1.0,
                 'color': 'red'
                 }]

    else:
        zone=[{
                 'value': THRES,
                 'color': 'black'
             }, {'value': 1.0,
                 'color': 'orange'
                 }]

    #values to build boxplot (seenu.andi-rajendran)
    series_box = [{
        'name': 'Percentile Values',
        'data': [dat]
    },{
        'name': 'Atoms',
        'type':'scatter',
        'keys': ['x', 'y', 'z','c'],
        'data': ser_dat,
        'tooltip': {
            'pointFormat': 'Index: {point.z}, Suspicion Score: {point.y}'
        },
        'zones':zone
    }]

    #getting values to build the column chart (seenu.andi-rajendran)
    series_col = [{
        'name': 'Greater than 90pc of the highest value',
        'data': [lq_cnt],
        'color':'#FFA500'
    }, {
        'name': 'Greater than THRES',
        'data': [thres_cnt],
        'color': 'rgb(255,0,0)'
    }, {
        'name': 'Rest',
        'data': [uq_cnt],
        'color': '#F0E7E7'
    }]

    column=[]
    for e in categories:
        column.append({'id':e})
    dataset=[]
    z=0
    for cf in cfs:
        if uq_conf > THRES:
            if cf < THRES:
                colran = 'Cold'
            elif cf < uq_conf and cf >= THRES:
                colran = 'Warm'
            elif cf >= uq_conf and cf > THRES:
                colran = 'Hot'
        elif uq_conf < THRES:
            if cf < uq_conf:
                colran = 'Cold'
            elif cf >= uq_conf and cf < THRES:
                colran = 'Warm'
            elif cf >= THRES and cf > uq_conf:
                colran = 'Hot'
        dataset.append({"rowid": "pc","columnid": categories[z],'value':str(cf),'colorRangeLabel':colran})
        z+=1

    if uq_conf>THRES:
        color=[
                {
                    "code": "#F0E7E7",
                    "minValue": "0.00",
                    "maxValue": THRES,
                    "label": "Cold"
                },
                {
                    "code": "#f6bc33",
                    "minValue": THRES,
                    "maxValue": uq_conf,
                    "label": "Warm"
                },
                {
                    "code": "#FF0000",
                    "minValue": uq_conf,
                    "maxValue": 1.0,
                    "label": "Hot"
                }
            ]
    else:
        color=[
                {
                    "code": "#F0E7E7",
                    "minValue": "0.00",
                    "maxValue": uq_conf,
                    "label": "Cold"
                },
                {
                    "code": "#f6bc33",
                    "minValue": uq_conf,
                    "maxValue": THRES,
                    "label": "Warm"
                },
                {
                    "code": "#FF0000",
                    "minValue": THRES,
                    "maxValue": 1.0,
                    "label": "Hot"
                }
            ]

    dataSource = {
        'chart':{
            'theme':'fint',
            'caption': doc_name,
            'xAxisName': 'indexes',
            'yAxisName': 'Plag. Conf.',
        },
        'rows':{'row':[{'id':'pc'}]},
        'columns': {'column': column},
        "dataset":[{'data':dataset}],
        "colorRange": {
            "gradient": "0",
            "color": color
        }
    }


    return render_template('view_doc.html',
        atom_type = atom_type,
        cluster_method = cluster_method,
        k = k,
        passages = all_passages,
        features = feature_names,
        doc_name = doc_name,
        chartID='chart', chart=chart, prop=float(100)/float(len(all_passages)),series=series, title=title, categories=categories, yAxis=yAxis, plag_cats=plag_cats, categories2=categories2, series_box=series_box,series_col=series_col,dataSource=json.dumps(dataSource), title2=title2, chart2=chart2,uq_conf=uq_conf,lq_conf=lq_conf, pc90=pc90, modelyn=modelyn)


#@app.route('/view_source_doc/<doc_name>', methods=['GET'])
#def view_source_doc(doc_name):
@app.route('/test_source_doc')
def view_source_doc():
    full_path = os.path.join(app.config['APP_ROOT'], 'static/sample_docs/test2.txt')
    xml_path = os.path.join(app.config['APP_ROOT'], 'static/sample_docs/test2.xml')

    atom_type = 'paragraph'

    passages = PlagDetector().get_ground_truth_passages(atom_type, full_path, xml_path)

    return render_template('view_source_doc.html',
        passages = passages,
        atom_type = atom_type)


@app.route('/sample/')
def show_sample():
    '''
    Use a pickled file of passage objects parsed from static/training_sample.txt
    to sample the front-end
    '''
    #all_passages = PlagDetector().get_passages('pickle')
    all_passages = PlagDetector().get_passages()
    features = all_passages[0].features.keys()

    return render_template('view_doc.html',
        doc_name = 'Sample',
        passages = all_passages,
        features = features)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug = True, port=port)
