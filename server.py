
import http.server
import socketserver
import json

import requests

import bs4

import MeCab

import json

import math

from collections import Counter

import os
term_index = json.loads( open('../model/term_index_ascii.json').read() )

class Handler(http.server.SimpleHTTPRequestHandler):
  def _set_response(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
 
  def do_GET(self):
    print("Client requested:", self.command, self.path )
    http.server.SimpleHTTPRequestHandler.do_GET(self)
    self.wfile.write(bytes("Hello World !",'utf8'))
  
  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    data = self.rfile.read(content_length) 
    data = json.loads( data.decode() )

    self._set_response()
    try:
      print( data )
      target = data['data'] 
      user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
      res = requests.get(target, headers=user_agent)
      print('code', res.status_code )
      if res.status_code != 200:
        raise Exception("Cannot Access")

      soup = bs4.BeautifulSoup(res.text)
      [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
      text = soup.getText()
      urltext = target.replace('/', ' ').replace('.', ' ')
      m = MeCab.Tagger('-Owakati')
      wakati = m.parse(text).strip()
      term_freq = Counter( (urltext + ' ' + wakati).split() )

      index_score = {}
      for term, freq in term_freq.items():
        try:
          index = term_index[term]
          score = math.log(freq+1)
          index_score[index] = score        
        except Exception:
          ...

      x = '1 ' + ' '.join( [ '{}:{}'.format(index, score) for index,score in index_score.items() ] )
      open('dataset_{pid}.txt'.format(pid=os.getpid()), 'w').write( x + '\n' )

      conf = \
'''task = predict
data = ./dataset_{pid}.txt
input_model= ../LightGBM_model.txt
output_result = LightGBM_predict_result_{pid}.txt
'''.format(pid=os.getpid()) 
      open('predict_{pid}.conf'.format(pid=os.getpid()), 'w').write( conf )
      os.system('lightgbm config=predict_{pid}.conf'.format(pid=os.getpid())) 
      score = float( open('LightGBM_predict_result_{pid}.txt'.format(pid=os.getpid()) ).read().strip() ) 
      self.wfile.write(bytes( json.dumps( {'status':'normal', 'score':score} ),'utf8'))
    except Exception as ex:
      ex = str(ex)
      self.wfile.write( bytes( json.dumps({'status':'error', 'code':0, 'detail':ex}, ensure_ascii=False), 'utf8') )


httpd = socketserver.TCPServer(('0.0.0.0', 11000), Handler)
httpd.serve_forever()
