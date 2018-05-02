#Bank_Message API using Flask_RESTful and Blueprint
from flask import Flask,jsonify,request,json,Blueprint,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import abort,Api, Resource
import re,json

app = Flask(__name__)
#Initialize Blueprint
banks = Blueprint('api',__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite://///home/sumaiya/Bank_Messages/banksdata.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False


api_obj = Api(banks)

db = SQLAlchemy(app)
db.init_app(app)


#Bank Message  Model 
class banktable(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    msg = db.Column(db.String)
    
    
    def __init__(self, msg):
        self.msg = msg
        

# Extract Single bank_message info ,post,update and delete single bank_message
class Bank(Resource):   
    def get(self, id):
        one_msg = banktable.query.filter_by(id=int(id)).first()
        if one_msg:

            #Extract salary and Account no:
            salary = re.search(r'(?i)(?:(?:RS|INR|MRP)\.?\s?)(\d+(:?\,\d+)?(\,\d+)?(\.\d{1,2})?)', one_msg.msg)

            acc_no = re.search(r'(?i)(?:(?:A/c No|A/c|Account|Account Number|Ac)\.?\s?)([0-9]*[Xx\*]*[0-9]*[Xx\*]+[0-9]{3,})', one_msg.msg)
            if salary and acc_no:
                salary = salary.group()
                acc_no = acc_no.group()
                #Removing Extra characters from salary and acc_no
                for ch in ["Rs","MRP","INR"]:
                    if ch in salary:
                        salary=salary.replace(ch,"")
                for ch in ["A/c No","A/c","Account Number","Account","Ac"]:
                    if ch in acc_no:
                        acc_no=acc_no.replace(ch,"")

                return jsonify({"Account Number ":acc_no,"Salary ": salary,"Requested Bank Message" : one_msg.msg})
        return abort(404,message="Bank Msg NOT FOUND!!!")

    def post(self):
        if(request.method == 'POST'):
            bt = banktable(request.json['msg'])
            db.session.add(bt)
            db.session.commit()
            return jsonify({"Added Bank Message:" : request.json['msg'] })

            

# shows all bank_Messages item
class BankAll(Resource):  
    def get(self):
        all_msg = banktable.query.all()
        if all_msg:
            bt = []
            msgs = []
            for i in all_msg:
                all_msg_dict ={
                    'msg':i.msg
                }
                msgs.append(all_msg_dict)
            return make_response(json.dumps(msgs),201)
        return abort(404,message="NO BANK MSG AVAILABLE!!!")


## setup the Api resource routing here
api_obj.add_resource(Bank,'/banks','/banks/<int:id>') 
api_obj.add_resource(BankAll,'/banksAll') 


