import jobs
from jobs import q, rd1, rd
import datetime
import redis
import matplotlib.pyplot as plt

@q.worker
def execute_job(jid):
    
    data = jobs.get_job_data(jid)

    job_type = jobs.get_job_type(jid)

    #jobs.update_job_status(jid, job_type)#'in progress')
   
 
    #analysis: plot total number of outcomes for each day in date range

    #first job type: dates
    if (job_type == 'dates'):
        #jobs.update_job_status(jid, str(data))
        #jobs.update_job_status(jid, 'You have entered the if statement')
        #format of how dates come in??????????? should be a string
        start = jobs.get_job_start(jid)
        end = jobs.get_job_end(jid)
        #jobs.update_job_status(jid, str(start))
        #set inital outcomes count
        animal_outcomes_of_day = 0

        #x values: list of dates
        x_values_to_plot = []

        #y values: list of integer numbers of outcomes per date
        y_values_to_plot = []

        
        start_date = datetime.datetime.strptime( start, "%m-%d-%Y")
        end_date = datetime.datetime.strptime( end, '%m-%d-%Y')

        #format to check for full day, rather than specific time??????????
        for key in rd1.keys():
            #jobs.update_job_status(jid, 'you have entered the for loop')
            key_time_temp = str(rd1.hget(key,'Date_of_Entry'))[1:]
            #jobs.update_job_status(jid, str(key_time_temp))
            #key_time_temp = key_time_temp.replace("/","-")
            
            #jobs.update_job_status(jid, str(key_time_temp))
            key_time = datetime.datetime.strptime(key_time_temp, "'%m-%d-%Y'")
            
            #jobs.update_job_status(jid, str(key_time_temp)) # -------------------
            #check for keys in date range
            if (start_date <= key_time and end_date >= key_time):
                #jobs.update_job_status(jid, 'this is entering 2nd if statement')
                #set specific date
                x = str(key_time)
                jobs.update_job_status(jid, str(x))                     #  -----------
                #check if date is alread in x_values_to_plot
                if x not in x_values_to_plot:
                    jobs.update_job_status(jid, 'this is entering 3rd if statement')
                    #if new date: add to list of x_values_to_plot
                    x_values_to_plot.append(x)

                    #check through db for each animal with matching Date_of_Entry
                    for i in range( rd1.dbsize() ):
                        
                        #will there be an issue with b formatting? should we use [1:]?
                        if (x == rd1.hget(i, 'Date_of_Entry')):

                            #increment animal_outcomes_of_day count
                            animal_outcomes_of_day = animal_outcomes_of_day + 1

                    #finalize count for the day
                    y = animal_outcomes_of_day

                    #add total count to list of y_values_to_plot
                    y_values_to_plot.append(y)

                #reset animal_outcomes_of_day count before moving to next day
                animal_outcomes_of_day = 0

        #plot line graph
        plt.scatter(x_values_to_plot, y_values_to_plot)
        #plt.show()
        plt.savefig('/outcomes_by_date.png')

        with open('/outcomes_by_date.png', 'rb') as f:
            img = f.read()

        rd.hset(f'job.{jid}', 'result', img)
        #rd.hset(jobid, 'image', img)        

        #jobs.update_job_status(jid, 'complete')

    #analysis: plot total # of outcomes by type of animal in date range
    if (job_type == 'animal_type'):
        #jobs.update_job_status(jid, 'it has entered the for loop')
        animal_types = ['Bird', 'Cat', 'Dog', 'Livestock', 'Other']
        animal_counts = [0, 0, 0, 0, 0]

        for key in rd1.keys():
            #jobs.update_job_status(jid, str(key))#'it has entered the for loop')
            this_animal_type = str(rd1.hget(key, 'Animal_Type'))[1:]
            #jobs.update_job_status(jid, str(this_animal_type))
            if this_animal_type == "'Bird'":
                animal_counts[0] += 1
            elif this_animal_type == "'Cat'":
                animal_counts[1] += 1
            elif this_animal_type == "'Dog'":
                animal_counts[2] += 1
            elif this_animal_type == "'Livestock'":
                animal_counts[3] += 1
            elif this_animal_type == "'Other'":
                animal_counts[4] += 1
        #jobs.update_job_status(jid, str(animal_counts))
        plt.clf()
        plt.bar(animal_types, animal_counts, color='green')
        plt.xlabel('Animal Type')
        plt.ylabel('Frequency')
        plt.title('Outcomes by Animal Type')
        #plt.show()
        plt.savefig('/outcomes_by_animal_type.png')
        with open('/outcomes_by_animal_type.png', 'rb') as f:
            img = f.read()

        #rd.hset("job.{}".format(jid), 'image' img)
        rd.hset(f'job.{jid}', 'result', img)

             
        jobs.update_job_status(jid, 'complete')

execute_job()
