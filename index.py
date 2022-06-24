import re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import ToktokTokenizer
import string as st
import unicodedata
from bs4 import BeautifulSoup
from spellchecker import SpellChecker
from textblob import TextBlob

lemma=WordNetLemmatizer()
token=ToktokTokenizer()
spell = SpellChecker()

stopWordList=stopwords.words('english')
stopWordList.remove('no')
stopWordList.remove('not')
stopWordList.remove('very')


def removeSpecialChars(string):
    clean_string = re.sub(r"[^a-zA-Z0-9]+", ' ', string).lower().strip()
    return clean_string

def remove_punc(text):
    text = [w for w in text if w not in st.punctuation]
    return ''.join(text)

def removeAscendingChar(string):
    #converts Accented characters into english characters
    string=unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return string

def correctLemitizeWords(text,is_misspelled='no',correct='no'):
    
    words=token.tokenize(text)
    listLemma=[]
    misspelled = list(spell.unknown(words))
    if misspelled:
        is_misspelled='yes'
    #treating misspelled words
    if correct!='no':    
        for word in misspelled:
            words = [spell.correction(word) if x==word else x for x in words]

    for w in words:
        x=lemma.lemmatize(w,'v')
        listLemma.append(x)
    text=' '.join(listLemma)
    return text, is_misspelled

def removeStopWords(text):
    wordList=[x.lower().strip() for x in token.tokenize(text)]
    removedList=[x for x in wordList if not x in stopWordList]
    text=' '.join(removedList)
    return text

def PreProcessing(text,is_misspelled ='no'):
    text=removeStopWords(text)
    text=remove_punc(text)
    text=removeSpecialChars(text)
    text=removeAscendingChar(text)
    text, is_misspelled =correctLemitizeWords(text)
    return text, is_misspelled
    
#preprocessing whole dataframe
def main_fun(path):
    df = pd.read_csv(path)
    pos_list = df['Text'].tolist()
    misspell_list,processed_txt = [],[]
    for text in pos_list:
        text,is_misspelled = PreProcessing(text)
        misspell_list.append(is_misspelled)
        processed_txt.append(text)
    df['processed_txt'] = processed_txt
    df["polarity"] = df['processed_txt'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['misspelled'] = misspell_list
    df_out = df[(df.Star<3) & (df.polarity>0.5)]
    return df_out

import os
from flask import Flask,request,render_template, make_response
#from flask_ngrok import run_with_ngrok

app = Flask(__name__)
#run_with_ngrok(app)

@app.route('/')
def home():
    """
    Renders a HTML page which allows us to input an image.
    
    """
    return render_template('index.html' ,title='Home')

@app.route('/predict' ,methods=['POST'])
def predict():
    """
    Main API function which takes path of csv from local storage as params with request 
    and uses function main_fun for estimation 
    and covert the result to CSV format
    """
        
    if request.method == 'POST':
        if 'file' not in request.files:
            print(request.files)
            return 'No file found'
    user_file = request.files['file']
    if user_file.filename == '':
        return 'file name not found …'
    else:
        path=os.path.join(os.getcwd(),user_file.filename)
        print(path)
        result_df = main_fun(path)
        result_csv = result_df.to_csv()
        output = make_response(result_csv)
        output.headers["Content-Disposition"] = "attachment; filename=output.csv"
        output.headers["Content-type"] = "text/csv"
    return output


# if __name__ == '__main__':
#     #ssl_context='adhoc'
#     # Open a HTTP tunnel on the default port 80
#     # public_url = ngrok.connect(port = '5000')
#     # print(public_url)
#     app.run(host='0.0.0.0')
    
#     # If address is in use, may need to terminate other sessions:
#     # Runtime > Manage Sessions > Terminate Other Sessions
            
