
import jobs
from jobs import q, rd1, rd
import time
import redis
#import matplotlib.pyplot as plt


#redis_ip= "10.111.115.155"#
#rd2=redis.StrictRedis(host=redis_ip, port=6379, db=2)
#rd1=redis.StrictRedis(host=redis_ip, port=6379, db=3)
@q.worker
def execute_job(jid):
     
        
    jobs.update_job_status(jid, "in progress")
       
            
    jobs.update_job_status(jid, "completed")

execute_job()
