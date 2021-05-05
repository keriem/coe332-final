import json
from flask import Flask, request
from hotqueue import HotQueue
import redis
import jobs
from jobs import rd1, q
import os
import uuid
import datetime

app = Flask(__name__)

#redis_ip = os.environ.get('REDIS_IP')
#if not redis_ip:
#   raise Exception()

#rd=redis.StrictRedis(host=redis_ip, port=6379, db=3)
#q = HotQueue('queue', host=redis_ip, port=6379, db=1)

@app.route('/helloWorld',methods=['GET'])
def hello_world():
    return "Hello World!"

@app.route('/load',methods=['GET'])
def load():
    load_data()
    return "You have loaded the data set from the json file!"
    

def load_data():
    with open("/app/animal_center_data_file.json","r") as json_file:
        animal_data = json.load(json_file)
    rd1 = redis.StrictRedis(host = redis_ip,port=6379,db=3)
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
        
        rd1.hmset(i,{'Animal_ID': animal_id,'Name':name,'Date_of_Entry':date_of_entry,'Date_of_Birth': date_of_birth, 'Outcome_Type': outcome_type,'Outcome_Subtype': outcome_subtype,'Animal_Type': animal_type, 'Sex':sex, 'Age':age, 'Breed': breed, 'Color':color})
        i = i+1
    #return str(rd1.keys())

def get_data():
    animal_data = []
    rd1 = redis.StrictRedis(host = redis_ip,port=6379,db=3)
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


# create route
@app.route('/add_animal', methods=['GET', 'POST'])
def add_animal():
    if method == 'POST'
        animal_dict = request.get_json(force=True)
        rd1.hset( rd1.dbsize(), animal_dict )
        return f'Added new animal with ID = {animal_dict['Animal_ID']}'

    else:
    return """

    Assemble and post a json structure like this:

    curl -X POST -H "Content-type: application/json" -d @file.json host-ip:5000/add_animal

    Where 'file.json' is a file containing: 

{
  "Animal_ID": "A781976",
  "Name": "*Fancy",
  "DateTime": "10/16/2018 14:25",
  "Date_of_Birth": "10/8/2017",
  "Outcome_Type": "Transfer",
  "Outcome_Subtype": "Partner",
  "Animal_Type": "Dog",
  "Sex_upon_Outcome": "Intact Female",
  "Age_upon_Outcome": "1 year",
  "Breed": "German Shepherd Mix",
  "Color": "White"
}

"""

# this is a read route
@app.route('/get_animal',methods=['GET'])
def get_id_animal():
    animalid = str(request.args.get('Animal_ID'))
    test = get_data()
    return json.dumps([x for x in test if x['Animal_ID'] == "'"+animalid+"'"])
    

# need an update route
@app.route('/update_animal', methods=['GET', 'POST'])
def update_animal():
    if method == 'POST':
        animalid = str(request.args.get('Animal_ID'))
        field_to_update = request.args.keys() # joe look this up

        for key in rd1.keys():
            if rd1.hget(key, 'Animal_ID') == animalid:
                rd1.hset(key, field_to_update, value_to_update)
    else:
    return """

    Try a curl command like:

    curl localhost:5000/update_animal?Animal_ID=A643424&Animal_Type=Dog


"""

# need a delete route
@app.route('/delete_animal', methods=['DELETE'])
def delete_animal():
    if method == 'DELETE':
        animal_to_delete = request.args.get('Animal_ID')
        for key in rd1.keys():
            if rd1.hget(key, 'Animal_ID') == animal_to_delete:
                rd1.hdel(key) # or maybe rd1.delete()












@app.route('/get_results',methods=['GET'])
def get_result():
    jid = str(request.args.get('Job_ID'))
    return json.dumps(jobs.get_result(jid))


@app.route('/jobs', methods=['POST'])
def jobs_api():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.add_job(job['start'], job['end']))

# user should do a curl request like:
# curl ip_address:5000/jobs -X POST -H "content-type: application/json" -d '{"start": "9/26/2018", "end": "9/26/2019"}'


@app.route('/download/<jobid>', methods=['GET'])
def download(jobid):
    path = f'/app/{jobid}.png'
    with open(path, 'wb') as f:
        f.write(rd.hget(jobid, 'image'))
    return send_file(path, mimetype='image/png', as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')




