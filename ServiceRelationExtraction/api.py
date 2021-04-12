import tools
import time
# seq = "《岁月如歌》是TVB台庆剧《冲上云霄》的主题曲，是香港歌手陈奕迅演唱的歌曲，由徐伟贤作曲，刘卓辉作词，刘志远编曲"
# triples = tools.extract_items(seq)

# print(triples)

from flask import Flask,request,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False
class Resp():
    code = 0
    data = ""
    message = ""
    def __init__(self,code,data,message):
        self.code = code
        self.data = data
        self.message = message
    def toDict(self):
        return dict(code=self.code,data=self.data,message=self.message)

@app.route('/')
def hello_world():
    r = Resp(200,"欢迎访问本接口","")
    return r.__dict__

@app.route("/api/extractTriples",methods=["GET","POST"])
def e():
    if request.method=="GET":
        sent = request.args.get("sentence")
    else:
        sent = request.form.get("sentence")
    t = tools.extract_items(sent)
    
    triples = []
    for i in t:
        _ =  dict(obj1=i[0],relation=i[1],obj2=i[2])
        triples.append(_)
    r = Resp(200,triples,"ok")
    #return jsonify(r.toDict())
    time.sleep(0.3)
    return r.__dict__

app.run(port=4236)