from app import app
import sys
import os
import cPickle

sys.path.append(app.config['PLAGCOMPS_LOC'])

from plagcomps.intrinsic import get_plagiarism_passages
from plagcomps.shared import util 

class PlagDetector:
    '''
    Class used (for the moment) to interact with the detection
    module. Should be removed later once the detection module
    has been nicely packaged.
    '''

    def get_passages(self, atom_type, features, cluster_method, k, filename=None):
        if filename == 'pickle':
            pickle_file = os.path.join(app.config['APP_ROOT'], 'static/sample_docs/passages.dat')
            f = file(pickle_file, 'rb')
            passages = cPickle.load(f)
            f.close()

            return passages
        elif filename is None:
            filename = os.path.join(app.config['APP_ROOT'], 'static/sample_docs/head_training_sample.txt')        

        
        u = util.IntrinsicUtility()
        f = file(filename, 'rb')
        content = unicode(f.read(), errors='ignore')
        #print content
        f.close()
        
        passages = get_plagiarism_passages(content, atom_type, features, cluster_method, k)

        # Look for a corresponding XML file and add ground truth if one exists
        xml_path = filename.replace('.txt', '.xml')
        if os.path.exists(xml_path):
            u.add_ground_truth_to_passages(passages, xml_path)
    

        return passages

    def get_ground_truth_passages(self, atom_type, file_path, xml_path):
        passages = util.BaseUtility().get_bare_passages_and_plagiarized_spans(file_path, xml_path, atom_type)

        return passages



