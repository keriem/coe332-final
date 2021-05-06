
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

q = HotQueue("queue", host=redis_ip, port=6379, db=1)#queue
rd = redis.StrictRedis(host=redis_ip, port=6379, db=0)#jobs
rd1=redis.StrictRedis(host=redis_ip, port=6379, db=3)# raw data


def _get_data():
    animal_data = []
    rd1 = redis.StrictRedis(host = redis_ip,port=6379,db=3)
    for i in range(2269):
        animal = {}
        animal['Animal_ID'] = str(rd1.hget(i,'Animal_ID'))[1:]
        animal['Name'] = str(rd1.hget(i,'Name'))[1:]
        animal['Date_of_Entry'] = str(rd1.hget(i,'Date_of_Entry'))[1:]

        animal['Date_of_Birth'] = str(rd1.hget(i,'Date_of_Birth'))[1:]

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

def _instantiate_job(jid, status, job_type, start, end):
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'job_type': job_type,
                'start': start,
                'end': end 
        }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'job_type': job_type.decode('utf-8'),
            'start': start.decode('utf-8'),
            'end': end.decode('utf-8')
    }

def _save_job(job_key, job_dict):
    
    rd.hmset(job_key, job_dict)

def _queue_job(jid):
    
    q.put(jid)
    

def add_job(job_type,start,end, status="submitted"):
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, job_type, start, end)
    _save_job(_generate_job_key(jid), job_dict)
    _queue_job(jid)
    #index = index +1
    return job_dict

def get_job_type(jid):
    jid, status, job_type, start, end = rd.hmget(_generate_job_key(jid), 'id', 'status', 'job_type', 'start', 'end')
    return (str(job_type)[1:]).replace("'","")

def get_job_data(jid):
    jid, status, job_type, start, end = rd.hmget(_generate_job_key(jid), 'id', 'status', 'job_type', 'start', 'end')
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, job_type, start, end)
    return job_dict

def get_job_start(jid):
    jid, status, job_type, start, end = rd.hmget(_generate_job_key(jid), 'id', 'status', 'job_type', 'start', 'end')
    return (str(start)[1:]).replace("'","")

def get_job_end(jid):
    jid, status, job_type, start, end = rd.hmget(_generate_job_key(jid), 'id', 'status', 'job_type', 'start', 'end')
    return (str(end)[1:]).replace("'","")

def update_job_status(jid, new_status):
    jid, status, job_type, start, end = rd.hmget(_generate_job_key(jid), 'id', 'status', 'job_type', 'start', 'end') 
    job = _instantiate_job(jid, status, job_type, start, end)
    IP = os.environ.get('WORKER_IP')

    if job:                                                                 
        job['status'] = new_status     
        if new_status == 'in progress':
            job['IP'] = IP             
        _save_job(_generate_job_key(job['id']), job)
    else:
        raise Exception()
