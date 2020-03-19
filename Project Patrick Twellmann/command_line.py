import sys
import re
import requests
import os
import platform
import io
from bs4 import BeautifulSoup


"""All the functionality for the Command Line Feature

Requires: requests,beautifoulsoup4
The input has to follow this pattern: the first Parameter has to be the Link to the file or a directory only containing files,
additional Parameters can follow: -f: the features,separated through empty space, -s: the segmentation(default:paragraph),
-c: the clustering method [if kmeans selected the k needs to follow, seperated through an empty space] (default:kmeans,k=2),
-t: the threshold(default: 0.8), -l the location to save the .csv file to (default:the current directory)
"""

baseURL = "http://127.0.0.1:8080"
#baseURL = "https://intrinsic.test.gipp.com"

documentPath = ""
features = []
segmentation = "paragraph"
clustering = "kmeans 2"
threshold = "0.8"
destination = ""
seperator = "\\"


def parse_input(input):
    global documentPath
    global features
    global segmentation
    global clustering
    global threshold
    global destination

    parameters = str(input).split()

    documentPath = parameters[0]

    counter = 1
    while(counter<len(parameters)):     #iterating through the parameters, parsing can be done after the first iteration
        if(parameters[counter] == "-f"):
            counter+=1
            while(counter<len(parameters) and not re.match("-[fsctl]",parameters[counter])): #collecting all features and stop if a new parameter found, or if the end is reached
                features.append(parameters[counter])
                counter+=1

        if(counter<len(parameters) and parameters[counter] == "-s"):
            counter+=1
            segmentation = parameters[counter]
            counter += 1

        if(counter<len(parameters) and parameters[counter] == "-c"):
            counter+=1
            clustering = parameters[counter]
            if(clustering == "kmeans"):
                counter+=1
                clustering+=" " + parameters[counter]
            counter += 1

        if(counter<len(parameters) and parameters[counter] == "-t"):
            counter+=1
            if(parameters[counter] == "90th_percentile"):
                threshold = "pc90"
            else:
                threshold = parameters[counter]
            counter += 1

        if(counter<len(parameters) and parameters[counter] == "-l"):
            counter+=1
            destination = parameters[counter]
            counter+=1


def createCSV(csv_content,fileName):
    global destination
    global seperator

    if(destination != ""):
        destination+=seperator

    file = open(destination + fileName.split(".")[0] + ".csv","w")
    file.write(csv_content)
    file.close()

def execute():
    global documentPath
    global features
    global segmentation
    global clustering
    global threshold
    global seperator

    request = baseURL + "/view_doc?"
    request_attributes = {}

    isBatch = os.path.isdir(documentPath)
    documents = []
    if(isBatch):
        for document in os.listdir(documentPath):
            if(re.search("\\.txt",document)):
                documents.append(document)
    else:
        documents.append(documentPath)

    for fileName in documents:
        #Upload selected Document
        try:
            if(not isBatch):
                file = io.open(documentPath,encoding="utf-8")
            else:
                file = io.open(documentPath + seperator + fileName,encoding="utf-8")

        except IOError:
            sys.stdout.write("Datei konnte nicht geoeffnet werden" + "\n")
            return
        filename = os.path.basename(file.name)
        sys.stdout.write("" + str(filename) + "\n")
        upload = requests.post(url = (baseURL + "/up"),files={"file":(filename,file)})  #für Lokalen Server: up, für Live Server: upload
        if(upload.status_code != requests.codes.ok):
           sys.stdout.write("Fehler beim Upload: " + str(upload.status_code) + "\n")
           return

        fileNameSingle = filename.split(".")[0]


        #Parse Input and extract the Parameters
        request_attributes["doc"] = fileNameSingle

        feature_list = []
        for feature in features:
            feature_list.append(feature)

        request_attributes["features"] = feature_list

        request_attributes["atom"] = segmentation

        if (re.match("(kmeans)",clustering)):
            clustering_arguments = clustering.split()
            request_attributes["cluster_method"] = clustering_arguments[0]
            request_attributes["k"] = clustering_arguments[1]
        else:
            request_attributes["cluster_method"] = clustering

        request_attributes["threshold"] = threshold

        getRequest = requests.get(url=request,params=request_attributes)

        #Crawl the Site to get the csv_content
        soup = BeautifulSoup(getRequest.text,features="html.parser")
        csv_content = soup.find("input",{"name":"csv_content"}).get("value")
        if(not isBatch):
            createCSV(csv_content,fileNameSingle)
        else:
            createCSV(csv_content,fileName)


def main():
    global seperator
    if (re.match("(l|L)inux",platform.platform(terse=True))):
        seperator = "//"
    parse_input(" ".join(sys.argv[1:]))
    execute()
    sys.stdout.write("Done" + "\n")

if __name__ == '__main__':
    main()