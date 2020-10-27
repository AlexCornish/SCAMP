import pandas as pd
import os
import math
import requests
from zipfile import ZipFile
path = str(os.path.dirname(os.path.realpath(__file__)))      

def loadCSV(filename):
    newPath = os.path.join(path, filename)
    return pd.read_csv(newPath)

def correlation(mergedDF):
    if len(mergedDF["RMPI_NAPCS"].unique()) > len(mergedDF["IPP_NAPCS"].unique()):
        correlation = []
        for i in mergedDF["RMPI_NAPCS"].unique():
            tempMerged = mergedDF[mergedDF["RMPI_NAPCS"]==i]
            n = len(tempMerged)
            sumX = tempMerged["RMPI_VALUE"].sum()
            tempMerged["xSqr"] = tempMerged["RMPI_VALUE"]**2
            sumXSqr = tempMerged["xSqr"].sum()
            sumY = tempMerged["IPP_VALUE"].sum()
            tempMerged["ySqr"] = tempMerged["IPP_VALUE"]**2
            sumYSqr = tempMerged["ySqr"].sum()
            tempMerged["xySqr"] = tempMerged["IPP_VALUE"]*tempMerged["RMPI_VALUE"]
            sumXY = tempMerged["xySqr"].sum()
            Sxy = sumXY - ((sumX * sumY)/n) 
            Sxx = sumXSqr - ((sumX**2)/n)
            Syy = sumYSqr - ((sumY**2)/n)
            try:
                r = Sxy / math.sqrt((Sxx * Syy))
                if math.isnan(r) == False and math.isinf(r) == False:
                    correlation.append([i,r])
            except ValueError:
                continue;
    elif len(mergedDF["RMPI_NAPCS"].unique()) < len(mergedDF["IPP_NAPCS"].unique()):
        correlation = []
        for i in mergedDF["IPP_NAPCS"].unique():
            tempMerged = mergedDF[mergedDF["IPP_NAPCS"]==i]
            n = len(tempMerged)
            sumX = tempMerged["IPP_VALUE"].sum()
            tempMerged["xSqr"] = tempMerged["IPP_VALUE"]**2
            sumXSqr = tempMerged["xSqr"].sum()
            sumY = tempMerged["RMPI_VALUE"].sum()
            tempMerged["ySqr"] = tempMerged["RMPI_VALUE"]**2
            sumYSqr = tempMerged["ySqr"].sum()
            tempMerged["xySqr"] = tempMerged["RMPI_VALUE"]*tempMerged["IPP_VALUE"]
            sumXY = tempMerged["xySqr"].sum()
            Sxy = sumXY - ((sumX * sumY)/n) 
            Sxx = sumXSqr - ((sumX**2)/n)
            Syy = sumYSqr - ((sumY**2)/n)
            try:
                r = Sxy / math.sqrt((Sxx * Syy))
                if math.isnan(r) == False and math.isinf(r) == False:
                    correlation.append([i,r])
            except ValueError:
                continue;
    correlationDF = pd.DataFrame(correlation, columns=["series_id","correlation"])
    correlationDF = correlationDF.sort_values(by=["correlation"], ascending=False)
    correlationDF = correlationDF.head(20)
    correlationDF = correlationDF.reset_index(drop=True)
    return correlationDF.head(20)

def getLatestVersion():
    r = requests.get("https://www150.statcan.gc.ca/n1/tbl/csv/18100034-eng.zip",allow_redirects=True)
    storagePath = os.path.join(path,'RMPI.zip')
    open(storagePath,'wb').write(r.content)
    with ZipFile(storagePath,'r') as zipObject:
        listOfFileNames = zipObject.namelist()
        for fileName in listOfFileNames:
            if "MetaData" not in fileName:
                zipObject.extract(fileName, path)
                if os.path.exists(os.path.join(path,"RMPI.csv")):
                    os.remove(os.path.join(path,"RMPI.csv"))
                os.rename(os.path.join(path,fileName),os.path.join(path,"RMPI.csv"))

    if os.path.exists(os.path.join(path,"18100034.csv")):
        os.remove(os.path.join(path,"18100034.csv"))
    if os.path.exists(os.path.join(path,"RMPI.zip")):
        os.remove(os.path.join(path,"RMPI.zip"))

    r = requests.get("https://www150.statcan.gc.ca/n1/tbl/csv/18100030-eng.zip",allow_redirects=True)
    storagePath = os.path.join(path,'IPP.zip')
    open(storagePath,'wb').write(r.content)
    with ZipFile(storagePath,'r') as zipObject:
        listOfFileNames = zipObject.namelist()
        for fileName in listOfFileNames:
            if "MetaData" not in fileName:
                zipObject.extract(fileName, path)
                if os.path.exists(os.path.join(path,"IPP.csv")):
                    os.remove(os.path.join(path,"IPP.csv"))
                os.rename(os.path.join(path,fileName),os.path.join(path,"IPP.csv"))

    if os.path.exists(os.path.join(path,"18100030.csv")):
        os.remove(os.path.join(path,"18100030.csv"))
    if os.path.exists(os.path.join(path,"IPP.zip")):
        os.remove(os.path.join(path,"IPP.zip"))

def prepareBeforeCorrelation():
    RMPI_DF = loadCSV("RMPI.csv")
    
    IPP_DF = loadCSV("IPP.csv")
    RMPI_DF = RMPI_DF[RMPI_DF["REF_DATE"]>"2009-13"]
    RMPI_DF = RMPI_DF.rename(columns={"North American Product Classification System (NAPCS)":"RMPI_NAPCS","VALUE":"RMPI_VALUE"})
    RMPI_DF = RMPI_DF.drop(columns=["GEO","DGUID","UOM","UOM_ID","SCALAR_FACTOR","VECTOR","COORDINATE","STATUS","SYMBOL","TERMINATED","DECIMALS","SCALAR_ID"])

    IPP_DF = IPP_DF[IPP_DF["REF_DATE"]>"2009-13"]
    IPP_DF = IPP_DF.rename(columns={"North American Product Classification System (NAPCS)":"IPP_NAPCS","VALUE":"IPP_VALUE"})
    IPP_DF = IPP_DF.drop(columns=["GEO","DGUID","UOM","UOM_ID","SCALAR_FACTOR","VECTOR","COORDINATE","STATUS","SYMBOL","TERMINATED","DECIMALS","SCALAR_ID"])
    return RMPI_DF, IPP_DF

def performCorrelation(codeToFind):    
    codeToFind = codeToFind.get("toCorrelate")
    getLatestVersion()
    RMPI_DF, IPP_DF = prepareBeforeCorrelation()
    RMPI_DF_Unique = RMPI_DF["RMPI_NAPCS"].unique()
    IPP_DF_Unique = IPP_DF["IPP_NAPCS"].unique()
    codeFullDF = ""
    for i in RMPI_DF_Unique:
        if codeToFind in i:
            codeFullDF = RMPI_DF[RMPI_DF["RMPI_NAPCS"]==i]
            tempDf = pd.merge(IPP_DF,codeFullDF,on="REF_DATE",how="left")
            return correlation(tempDf).to_html()
    if codeFullDF == "":
        for i in IPP_DF_Unique:
            if codeToFind in i:
                codeFullDF = IPP_DF[IPP_DF["IPP_NAPCS"]==i]
                tempDf = pd.merge(RMPI_DF,codeFullDF,on="REF_DATE",how="left")
                return correlation(tempDf).to_html()
