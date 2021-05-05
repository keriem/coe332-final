
import jobs
from jobs import q, rd1, rd
import time
import redis
import ast
import matplotlib.pyplot as plt


#redis_ip= "10.111.115.155"#
#rd2=redis.StrictRedis(host=redis_ip, port=6379, db=2)
#rd1=redis.StrictRedis(host=redis_ip, port=6379, db=3)

@q.worker
def execute_job(jid):
     
    data = jobs.get_job_data(jid)

    # call matplotlib to make a plot of something 
    # plot stuff here...
    start = data['start']
    end = data['end']

    # pplot the counts of each type of animal adopted in between a date range
    animal_types = ['Bird', 'Cat', 'Dog', 'Livestock', 'Other']
    animal_counts = [0, 0, 0, 0, 0]

    for key in rd1.keys():
        if (start <= key[DateTime].decode('utf-8') <= end):
             this_animal_type = key['Animal_Type']
             if this_animal_type == 'Bird':
                 animal_counts[0] += 1
             else if this_animal_type == 'Cat':
                 animal_counts[1] += 1
             else if this_animal_type == 'Dog':
                 animal_counts[2] += 1
             else if this_animal_type == 'Livestock':
                 animal_counts[3] += 1
             else if this_animal_type == 'Other':
                 animal_counts[4] += 1


    plt.clf()
    plt.bar(animal_types, animal_counts, color='green')
    plt.xlabel('Animal Type')
    plt.ylabel('Frequency')
    #plt.title('Amino Acid Frequency')
    #plt.xticks(aas_pos, aas)

    plt.savefig('/output_image.png')
    with open('/output_image.png', 'rb') as f:
        img = f.read()
    
    rd.hset(f'job.{jid}', 'result', img)
    jobs.update_job_status(jid, "completed")



execute_job()
