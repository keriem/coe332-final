
import jobs
from jobs import q
import time
import redis





rd2=redis.StrictRedis(host=redis_ip, port=6379, db=2)
@q.worker
def execute_job(jid):
    
    jobs.update_job_status(jid, 'in progress')
    
    job_type = jobs.get_job_type(jid)
    
    if(job_type=='create'):
        data = jobs.get_job_data(jid)
        result = jobs.add_animal(jid,data)   
        rd2.hmset(jid,result)

    jobs.update_job_status(jid, 'complete')

execute_job()
