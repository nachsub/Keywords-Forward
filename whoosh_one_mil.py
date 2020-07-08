from flask import Flask
import os.path
import json
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser

from whoosh.filedb.filestore import FileStorage
from whoosh.query import *

app = Flask(__name__)
vocab_dic = {}
querycount = 0
ix = 0
searcher = 0

def init_dictionary():
    vocab_txt = open("C:/Users/nacho/Downloads/vocab.txt", "r")
    vocab_arr = vocab_txt.readlines()
    for item in vocab_arr:
        if len(item) < 1:
            continue
        if "â€™" in item:
            item = item.replace("â€™", "'");
        if item[len(item) - 1] == '\n':
            item = item[:-1]
        vocab_dic[item] = 0

def create_whoosh():
    print('opening arxiv data corpus')
    schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))
    if not os.path.exists("one_mil_index"):
        os.mkdir("one_mil_index")
    else:
        return
    ix = create_in("one_mil_index", schema)
    f = open("C:/Users/nacho/Downloads/425370_810528_compressed_arxiv-abstracts-all/arxiv-abstracts-all.txt", "r")
    fl = f.readlines()
    print(len(fl))
    writer = ix.writer(multisegment=True)
    print('initializing writer')
    for i in range(0, len(fl)):
      writer.add_document(title= u"My document" +str(i), content = 'u'+fl[i])
      if i%1000 == 0:
          print(i/len(fl))
      if i == 1500000:
          print('750k')
          writer.commit()
          print('writer committed')
          break
    print('return')
    return

def init_globals():
    querycount = 0
    ix = 0
    searcher = 0

@app.route('/getmethod/<querystring>')
def search_index(querystring):
    global querycount
    global ix
    global searcher
    if querycount == 0:
        init_globals()
        print('creating whoosh')
        create_whoosh()
        schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))
        print('open index')
        ix = open_dir("C:/Users/nacho/Documents/whoosh_example/one_mil_index")
        print('searching index\n')
        searcher = ix.searcher()
    querycount = querycount + 1
    # phrase query
    query = Phrase("content", querystring.split(' '))
    list_of_dicts = []
    json_str = ""
    # documents = []      #array of content results
    results = []
    keywords_scores = []
    with ix.searcher() as searcher:
        print('results')
        results = searcher.search(query, limit=None)
        print(results)
        print('extract keyword')
        # Extract keywords for the top N documents in a whoosh.searching.Results object. This requires that the field is either vectored or stored.
        keywords_scores = [(keyword,score) for keyword, score in results.key_terms("content", docs=1000,numterms=1000)]
    init_dictionary()

    print('update dictionary')
    for (keyword,score) in keywords_scores:
        if keyword in vocab_dic.keys() or keyword.lower() in vocab_dic.keys():
            vocab_dic[keyword] = vocab_dic[keyword] + score

    relevant_keywords = ""
    for (key,val) in sorted(vocab_dic.items(),key=by_value, reverse=True):
        if val > 0:
            relevant_keywords = relevant_keywords + "key: "+ key + " , value:" + str(val) + "\n"
    return relevant_keywords

    
def by_value(item):
     return item[1]

if __name__ == '__main__':
    port = 8000 #the custom port you want
    app.run(host='10.0.0.38', port=port)
