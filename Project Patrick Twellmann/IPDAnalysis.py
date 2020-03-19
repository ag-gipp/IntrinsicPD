import sys
import re
import platform
import os
import csv
import shutil
import numpy

runBaseAnalysis = True

path = ""
basePath = ""
seperator = "\\"

lexicalFeatures = ['punctuation_percentage', 'average_word_length','average_sentence_length','average_syllables_per_word','alpha_chars_ratio','digit_chars_ratio','upper_chars_ratio','white_chars_ratio','polysyllablcount']
syntacticFeatures = ['stopword_percentage','avg_internal_word_freq_class','avg_external_word_freq_class','syntactic_complexity']
vocabularyRichness = ['honore_r_measure','hapax_legomena','hapax_dislegomena','simpsons_d','sichels_s','brunets_w','yule_k_characteristic','yule_i','type_token_ratio']
readabilityFeatures = ['coleman_liau_index','automated_readability_index','linsear_write_formula','gunning_fog_index','dale_chall_readability_score','smog_index','flesch_reading_ease','flesch_kincaid_grade']

allFeatures = {"LexicalFeatures":lexicalFeatures,"SyntacticFeatures":syntacticFeatures,"VocabularyRichness":vocabularyRichness,"ReadabilityFeatures":readabilityFeatures}

segmentation = "paragraph"   #später Dateien aufräumen (ersetzen: linebreak -> linebreak * 2), dann paragraph

originalDocuments = {}
spunDocuments = {}

def loadDocuments():
    global originalDocuments
    global spunDocuments
    global path

    for document in os.listdir(path):
        if(re.search("ORIG",document)):
            originalDocuments[document] = path + seperator + document
        else:
            spunDocuments[document] = path + seperator + document

def createFileStructure():
    global allFeatures
    global seperator
    global basePath
    global originalDocuments
    global spunDocuments
    global runBaseAnalysis

    basePath += seperator + "Analysis"
    if runBaseAnalysis:
        if(os.path.exists(basePath)):
            shutil.rmtree(basePath,True)
        os.makedirs(basePath,True)

    for category,features in allFeatures.items():
        categoryPath = basePath + seperator + category
        if runBaseAnalysis:
            os.makedirs(categoryPath, True)
        categoryAverageFileName = category + "Averages" + ".csv"
        featureAverages = []
        with open(categoryPath + seperator + categoryAverageFileName, 'w') as categoryAverageCSV:

            for feature in features:
                featureAverageFileName = feature + "Averages" + ".csv"

                featureSum = 0
                featureAtomCount = 0
                averages = []
                featurePath = categoryPath + seperator + feature
                if runBaseAnalysis:
                    os.makedirs(featurePath,True)
                with open(featurePath + seperator + featureAverageFileName,'w') as featureAverageCSV:
                    if runBaseAnalysis:
                        originalDirectoryPath = featurePath + seperator + "Original"
                        os.makedirs(originalDirectoryPath, True)   #hier die Analysen durchführen?
                        for documents,documentPath in originalDocuments.items():
                            analysis(documentPath,originalDirectoryPath,feature)

                        spunDirectoryPath = featurePath + seperator + "Spun"
                        os.makedirs(spunDirectoryPath, True)
                        for documents,documentPath in spunDocuments.items():
                            analysis(documentPath,spunDirectoryPath,feature)

                    featureAnalysisPath = featurePath + seperator + "Deviation"
                    os.makedirs(featureAnalysisPath,True)
                    #os.chdir(featureAnalysisPath)
                    documentIDs = []
                    for document in os.listdir(originalDirectoryPath):
                        documentID = document.split("-")[0]
                        documentIDs.append(documentID)
                        #spunDocument = findFile(documentID,spunDirectoryPath)
                        averages.append(analyseDifferences(originalDirectoryPath + seperator + document,spunDirectoryPath + seperator + documentID + "-SPUN.csv",featureAnalysisPath + seperator +str(documentID) + "Deviation"))

                    csvwriter = csv.writer(featureAverageCSV)
                    csvwriter.writerow(["Document","Average"])
                    for element in averages:
                        csvwriter.writerow([str(documentIDs[featureAtomCount]),str(element)])  # Format: Document,Atom Score Average
                        featureAtomCount += 1
                        featureSum += element
                    sys.stdout.write("Feature " + feature + " complete" + "\n")

                featureAverages.append(numpy.mean(averages))
                #featureAverages.append(featureSum/featureAtomCount) #ist hier das Problem? vielleicht keine float Division?

            csvwriter = csv.writer(categoryAverageCSV)
            csvwriter.writerow(["Feature","Average"])
            counter = 0
            for element in featureAverages:
                csvwriter.writerow([str(features[counter]),str(element)])  # Format: Feature,Atom Score Average
                counter += 1
            sys.stdout.write("Category" + category + " complete" + "\n")

def findFile(documentId,directory):
    for document in os.listdir(directory):
        currentID = document.split("-")[0]
        if(currentID == documentId):
            return document

def analysis(documentPath,savePath,feature):
    global path
    global segmentation
    os.system("python command_line.py " + documentPath + " -f " + feature + " -s " + segmentation +  " -l " + savePath) #funktioniert das so?
    #muss hier noch was hin?

def analyseDifferences(csvOriginal,csvSpun,name):
    differences = []
    with open(csvOriginal, 'r', newline='') as f:
        readerOriginal = csv.reader(f, delimiter=',')
        with open(csvSpun, 'r', newline='') as f:
            readerSpun = csv.reader(f, delimiter=',')
            firstRow = True
            for (row,spunRow) in zip(readerOriginal,readerSpun):
                #zum besseren Analysieren in Listen/Arrays zwischenspeichern?
                #spunRow = readerSpun.__next__()
                if(firstRow):   #header nicht auslesen
                    firstRow = False
                    continue

                #beide Reader sollten die gleiche Anzahl an Zeilen haben
                #rowElements = row.split(",")
                #spunRowElements = spunRow.split(",")
                #differences.append(rowElements[2] - spunRowElements[2]) #erste Spalte: atom no, zweite Spalte: start index, dritte Spalte: Feature score
                differences.append(float(row[2]) - float(spunRow[2]))  # erste Spalte: atom no, zweite Spalte: start index, dritte Spalte: Feature score

    sum = 0
    atomNumbers = [i+1 for i in range(differences.__len__())]
    with open(name+".csv","w") as analysisCSV:
        csvwriter = csv.writer(analysisCSV)
        counter = 0
        csvwriter.writerow(["Atom No","Atom Score Difference"])
        for element in differences:
            csvwriter.writerow([str(atomNumbers[counter]),str(element)])    #Format: Atom No,Atom Score Difference
            counter+=1
            sum += element

    return numpy.mean(differences)  #float(sum) / float(differences.__len__())


def main():
    global seperator
    global path
    global basePath
    global runBaseAnalysis
    if (re.match("(l|L)inux", platform.platform(terse=True))):
        seperator = "//"
    path = sys.argv[1]  #Speicherort der zu analysierenden Dateien
    basePath = sys.argv[2] #Speicherort der Analyse
    if runBaseAnalysis:
        loadDocuments()
    createFileStructure()

if __name__ == '__main__':
    main()

