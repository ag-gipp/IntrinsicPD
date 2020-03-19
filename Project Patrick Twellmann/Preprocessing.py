import sys
import re
import platform
import os
import csv
import shutil
from collections import OrderedDict
from operator import itemgetter

seperator = "\\"

def processDocuments():
    global seperator
    documentPath = "D:\Patrick\Desktop\IPDAnalysis\documents"   #wird nicht auf Linux funzen
    proccessedDocumentsPath = "D:\Patrick\Desktop\IPDAnalysis" + seperator + "proccessedDocuments"

    if (os.path.exists(proccessedDocumentsPath)):
        shutil.rmtree(proccessedDocumentsPath, True)
    os.makedirs(proccessedDocumentsPath, True)

    for document in os.listdir(documentPath):
        text = ""
        with open(documentPath + seperator +document,"r",encoding="utf-8") as unprocessedDocument:
            sys.stdout.write(document + "\n")
            text = unprocessedDocument.read()
        text.replace("\n","\n\n")
        with open(proccessedDocumentsPath + seperator + document,"w",encoding="utf-8") as processedDocument:
            processedDocument.write(text)

def countWords():
    global seperator
    documentPath = "D:\Patrick\Desktop\IPDAnalysis\documents"  # wird nicht auf Linux funzen
    proccessedDocumentsPath = "D:\Patrick\Desktop\IPDAnalysis" + seperator + "wordCounts"

    if (os.path.exists(proccessedDocumentsPath)):
        shutil.rmtree(proccessedDocumentsPath, True)
    os.makedirs(proccessedDocumentsPath, True)

    wordCount = {}
    for document in os.listdir(documentPath):
        with open(documentPath + seperator + document,'r',encoding="utf-8") as text:
            textString = text.read()
            tokens = re.split("(\s|\.|,|!|\?|:|;|\(|\)|-|–|\"|\[|\[)",textString,0)
            for token in tokens:
                if token in wordCount:
                    currentCount = wordCount[token]
                    wordCount[token] = currentCount + 1
                else:
                    wordCount[token] = 1

        wordCount = OrderedDict(sorted(wordCount.items(), key=itemgetter(1)))

        with open(proccessedDocumentsPath + seperator + document + ".csv","w",encoding="utf-8") as wordCountCSV:
            csvwriter = csv.writer(wordCountCSV)
            csvwriter.writerow(["Word", "Count"])
            for key,value in wordCount.items():
                csvwriter.writerow([key, value])


def analysis(documentPath,savePath):
    features = "coleman_liau_index automated_readability_index linsear_write_formula gunning_fog_index dale_chall_readability_score smog_index flesch_reading_ease flesch_kincaid_grade"
    allFeatures = features + " punctuation_percentage average_word_length average_sentence_length average_syllables_per_word alpha_chars_ratio digit_chars_ratio upper_chars_ratio white_chars_ratio polysyllablcount stopword_percentage avg_internal_word_freq_class avg_external_word_freq_class syntactic_complexity honore_r_measure hapax_legomena hapax_dislegomena simpsons_d sichels_s brunets_w yule_k_characteristic yule_i type_token_ratio"
    segmentation = "sentence"
    os.system("python command_line.py " + documentPath + " -f " + allFeatures + " -s " + segmentation +  " -l " + savePath) #funktioniert das so?
    #muss hier noch was hin?

def evaluationPreperation():
    global seperator
    documentPath = "D:\Patrick\Desktop\IPDAnalysis\documents"  # wird nicht auf Linux funzen
    proccessedDocumentsPath = "D:\Patrick\Desktop\IPDAnalysis" + seperator + "evaluationDocuments"

    if (os.path.exists(proccessedDocumentsPath)):
        shutil.rmtree(proccessedDocumentsPath, True)
    os.makedirs(proccessedDocumentsPath, True)

    originalPath = proccessedDocumentsPath + seperator + "original"
    spunPath = proccessedDocumentsPath + seperator + "spun"

    os.makedirs(originalPath, True)
    os.makedirs(spunPath, True)

    for document in os.listdir(documentPath):
        fullDocumentPath = documentPath + seperator + document
        if(re.search("ORIG",document)):
            analysis(fullDocumentPath,originalPath)
        else:
            analysis(fullDocumentPath,spunPath)

def main():
    global seperator
    if (re.match("(l|L)inux", platform.platform(terse=True))):
        seperator = "//"

    #processDocuments()
    #countWords()
    #evaluationPreperation()
    analysis("D:\Patrick\Desktop\IPDAnalysis\documents","D:\Patrick\Desktop\IPDAnalysis" + seperator + "evaluationDocuments" + seperator + "baseLine")

if __name__ == '__main__':
    main()