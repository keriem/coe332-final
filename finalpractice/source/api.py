
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
    rd = redis.StrictRedis(host = redis_ip,port=6379,db=3)
    i = 0
    for animal in animal_data:
        animal_id = animal['Animal ID']
        name = animal['Name']
        date_of_entry = animal['DateTime'] 
#datetime.datetime.strptime( animal['DateTime'],'%m/%d/%Y %H:%M')
        date_of_birth = animal['Date of Birth'] 
#datetime.datetime.strptime( animal['Date of Birth'],'%m/%d/%Y')
        outcome_type = animal['Outcome Type']
        outcome_subtype = animal['Outcome Subtype']
        animal_type = animal["Animal Type"]
        sex = animal['Sex upon Outcome']
        age = animal['Age upon Outcome']
        breed = animal['Breed']
        color = animal['Color']
        
        rd.hmset(i,{'Animal_ID': animal_id,'Name':name,'Date_of_Entry':date_of_entry,'Date_of_Birth': date_of_birth, 'Outcome_Type': outcome_type,'Outcome_Subtype': outcome_subtype,'Animal_Type': animal_type, 'Sex':sex, 'Age':age, 'Breed': breed, 'Color':color})
        i = i+1
    #return str(rd.keys())

def get_data():
    animal_data = []
    rd = redis.StrictRedis(host = redis_ip,port=6379,db=3)
    for i in range(2269):
        animal = {}
        animal['Animal_ID'] = str(rd.hget(i,'Animal_ID'))[1:]
        animal['Name'] = str(rd.hget(i,'Name'))[1:]
        animal['Date_of_Entry'] = str(rd.hget(i,'Date_of_Entry'))[1:] 
#datetime.datetime.strptime( animal['DateTime'],'%m/%d/%Y %H:%M')
        animal['Date_of_Birth'] = str(rd.hget(i,'Date_of_Birth'))[1:] 
#datetime.datetime.strptime( animal['Date of Birth'],'%m/%d/%Y')
        animal['Outcome_Type'] = str(rd.hget(i,'Outcome_Type'))[1:]
        animal['Outcome_Subtype'] = str(rd.hget(i,'Outcome_Subtype'))[1:]
        animal['Animal_Type'] = str(rd.hget(i,'Animal_Type'))[1:]
        animal['Sex'] = str(rd.hget(i,'Sex'))[1:]
        animal['Age'] = str(rd.hget(i,'Age'))[1:]
        animal['Breed'] = str(rd.hget(i,'Breed'))[1:]
        animal['Color'] = str(rd.hget(i,'Color'))[1:]
        
        animal_data.append(animal) 
    
    return animal_data

@app.route('/get_animal',methods=['GET'])
def get_id_animal():
    animalid = str(request.args.get('Animal_ID'))
    test = get_data()
    return json.dumps([x for x in test if x['Animal_ID'] == "'"+animalid+"'"])
    

#@app.route('/get_results',methods=['GET'])
#def get_result():
#    jid = str(request.args.get('Job_ID'))
#    return json.dumps(jobs.get_result(jid))

@app.route('/jobs', methods=['POST'])
def jobs_api():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.add_job(job['job_type'], str(job['data'])))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
