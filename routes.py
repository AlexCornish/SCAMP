from app import tempMatch
from app import app
from flask import render_template, request


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/exactword')
def exact():    
    return render_template('exactword.html')       

@app.route('/exactwordresult', methods = ["POST","GET"])
def exactResult():
    if request.method == 'POST':
        result = request.form
        return render_template('exactWordResult.html',result=tempMatch.exactSearch(result)) 

@app.route('/stringparser')
def parser():    
    return render_template('stringparser.html')   

@app.route('/stringparserresult', methods = ["POST","GET"])
def parserResult():
    if request.method == 'POST':
        result = request.form
        return render_template('stringparserresult.html',result=tempMatch.parseResult(result)) 

@app.route('/blsrequest')
def blsrequest():
    return render_template('blsrequest.html')   

@app.route('/blsrequestresult', methods = ["POST","GET"])
def blsrequestResult():
    if request.method == 'POST':
        result = request.form
        return render_template('blsrequestresult.html',result=result) 

@app.route('/codesearch')
def codesearch():
    return render_template('codesearch.html')   
    
@app.route('/codesearchresult', methods = ["POST","GET"])
def codesearchResult():
    if request.method == 'POST':
        result = request.form
        return render_template('codesearchresult.html',result=tempMatch.main(result)) 