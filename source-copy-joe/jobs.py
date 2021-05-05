import uuid
from hotqueue import HotQueue
import redis
import os 
from random import randint 
import datetime
import json
import ast

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

q   = HotQueue("queue", host=redis_ip, port=6379, db=1)
rd  = redis.StrictRedis(host=redis_ip, port=6379, db=0) # jobs
#rd2 = redis.StrictRedis(host=redis_ip, port=6379, db=2)
rd1 = redis.StrictRedis(host = redis_ip,port=6379,db=3) # raw data


def _get_data():
    animal_data = []
    for i in range(2269):
        animal = {}
        animal['Animal_ID'] = str(rd1.hget(i,'Animal_ID'))[1:]
        animal['Name'] = str(rd1.hget(i,'Name'))[1:]
        animal['Date_of_Entry'] = str(rd1.hget(i,'Date_of_Entry'))[1:]
#datetime.datetime.strptime( animal['DateTime'],'%m/%d/%Y %H:%M')
        animal['Date_of_Birth'] = str(rd1.hget(i,'Date_of_Birth'))[1:]
#datetime.datetime.strptime( animal['Date of Birth'],'%m/%d/%Y')
        animal['Outcome_Type'] = str(rd1.hget(i,'Outcome_Type'))[1:]
        animal['Outcome_Subtype'] = str(rd1.hget(i,'Outcome_Subtype'))[1:]
        animal['Animal_Type'] = str(rd1.hget(i,'Animal_Type'))[1:]
        animal['Sex'] = str(rd1.hget(i,'Sex'))[1:]
        animal['Age'] = str(rd1.hget(i,'Age'))[1:]
        animal['Breed'] = str(rd1.hget(i,'Breed'))[1:]
        animal['Color'] = str(rd1.hget(i,'Color'))[1:]

        animal_data.append(animal)

    return animal_data


def _generate_jid():
    return str(uuid.uuid4())

def _generate_job_key(jid):
    return 'job.{}'.format(jid)

def _instantiate_job(jid, status, job_type, data):
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'job_type': job_type,
                'data': data
        }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'job_type': job_type.decode('utf-8'),
            'data': data.decode('utf-8')
    }

def _save_job(job_key, job_dict):
    
    rd.hmset(job_key, job_dict)

def _queue_job(jid):
    
    q.put(jid)
    

def add_job(job_type,data, status="submitted"):
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, job_type, data)
    _save_job(_generate_job_key(jid), job_dict)
    _queue_job(jid)
    #index = index +1
    return job_dict

def get_job_type(jid):
    jid, status, job_type, data = rd.hmget(_generate_job_key(jid), 'id', 'status', 'job_type', 'data')
    return (str(job_type)[1:]).replace("'","")

def get_job_data(jid):
    jid, status, job_type, data = rd.hmget(_generate_job_key(jid), 'id', 'status', 'job_type', 'data')
    #data = data.strip('\"')
    return data

def add_animal(jid, data):
    rd1=redis.StrictRedis(host = redis_ip,port=6379,db=3)
    test = _get_data()
    
    #data = ast.literal_eval(data)    
    #data = str(rd.hmget(_generate_job_key(jid),'data'))[1:]
    #data = data.replace('"','')
    #data = ast.letral_eval(data)
#    return data



    animal_id = 'A123456'
    name = data['Name']
    date_of_entry = str(datetime.datetime.now())
    #d = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
    #date_entry  = d.strftime("%m/%d/%Y %H:%M")
    date_of_birth = data['Date_of_Birth']
    outcome_type = data['Outcome_Type']
    outcome_subtype = data['Outcome_Subtype']
    animal_type = data['Animal_Type']
    sex = data['Sex']
    age = data['Age']
    breed = data['Breed']
    color = data['Color']

    #jid, status, job_type, data = rd.hmget(_generate_job_key(jid), 'id', 'status', 'job_type', 'data')
    #job = _instantiate_job(jid, status, job_type, data)

    rd1.hmset(rd1.dbsize(),{'Animal_ID':animal_id,'Name':name,'Date_of_Entry':date_entry,'Date_of_Birth':date_of_birth,'Outcome_Type':outcome_type,'Outcome_Subtype':outcome_subtype,'Animal_Type':animal_type,'Sex':sex,'Age':age,'Breed':breed,'Color':color})
    #jid, status, job_type, data = rd.hmget(_generate_job_key(job['id']), 'id', 'status', 'job_type', 'data')
    rd2.hmset(_generate_job_key(jid),{'id': jid, 'status':status, 'job_type':job_type, 'result':rd1.hget(rd1.dbsize())})

def get_result(jid):
    return rd2.hgetall(_generate_job_key(jid))

def update_job_status(jid, new_status):
    jid, status, job_type, data = rd.hmget(_generate_job_key(jid), 'id', 'status', 'job_type', 'data') 
    job = _instantiate_job(jid, status, job_type, data)
    IP = os.environ.get('WORKER_IP')

    if job:                                                                 
        job['status'] = new_status     
        if new_status == 'in progress':
            job['IP'] = IP             
        _save_job(_generate_job_key(job['id']), job)
    else:
        raise Exception()
