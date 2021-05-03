
import json
from flask import Flask, request
from hotqueue import HotQueue
import redis
import jobs
import os
import uuid
import datetime

app = Flask(__name__)

redis_ip = "10.111.115.155"#os.environ.get('REDIS_IP')
#if not redis_ip:
#   raise Exception()
rd=redis.StrictRedis(host=redis_ip, port=6379, db=3)
q = HotQueue('queue', host=redis_ip, port=6379, db=1)

@app.route('/helloWorld',methods=['GET'])
def hello_world():
    return "Hello World!"

@app.route('/load',methods=['GET'])
def load():
    load_data()
    return json.dumps(get_data())
    

def load_data():
    with open("/app/animal_center_data_file.json","r") as json_file:
        animal_data = json.load(json_file)
    return animal_data
    rd = redis.StrictRedis(host = redis_ip,port=6379,db=3)
    i = 0
    for animal in animal_data:
        animal_id = animal["Animal ID"]
        name = animal["Name"]
        date_of_entry = animal["DateTime"] #datetime.datetime.strptime( animal['DateTime'],'%m/%d/%Y %H:%M')
        date_of_birth = animal["Date of Birth"] #datetime.datetime.strptime( animal['Date of Birth'],'%m/%d/%Y')
        outcome_type = animal["Outcome Type"]
        outcome_subtype = animal["Outcome Subtype"]
        animal_type = animal["Animal Type"]
        sex = animal["Sex upon Outcome"]
        age = animal["Age upon Outcome"]
        breed = animal["Breed"]
        color = anmal["Color"]
        
        rd.hmset[i,{'Animal_ID': animal_id,'Name':name,'Date_of_Entry':date_on_entry,'Date_of_Birth': date_of_birth, 'Outcome_Type': outcome_type,'Outcome_Subtype': outcome_subtype,'Animal_Type': anial_type, 'Sex':sex, 'Age':age, 'Breed': breed, 'Color':color}]

        i = i+1

def get_data():
    animal_data = []
    rd = redis.StrictRedis(host = redis_ip,port=6379,db=3)
    for i in range(0,2269):
        animal = {}
        animal['Animal_ID'] = rd.hget(i,'Animal ID')
        animal['Name'] = rd.hget(i,'Name')
        animal['Date_of_Entry'] = rd.get(i,'Date_of_Entry') #datetime.datetime.strptime( animal['DateTime'],'%m/%d/%Y %H:%M')
        animal['Date_of_Birth'] = rd.get(i,'Date_of_Birth') #datetime.datetime.strptime( animal['Date of Birth'],'%m/%d/%Y')
        animal['Outcome_Type'] = rd.get(i,'Outcome_Type')
        animal['Outcome_Subtype'] = rd.get(i,'Outcome_Subtype')
        animal['Animal_Type'] = rd.get(i,'Animal_Type')
        animal['Sex'] = rd.get(i,'Sex')
        animal['Age'] = rd.get(i,'Age')
        animal['Breed'] = rd.get(i,'Breed')
        animal['color'] = rd.get(i,'Color')
        
        animal_data.append(animal) 
    
        return animal_data

@app.route('/jobs', methods=['POST'])
def jobs_api():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
#    return json.dumps(jobs.add_job(job['start'], job['end']))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
