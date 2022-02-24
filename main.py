import os
import ast
import gazu
import json
import datetime
import messages

# variables
kitsuHost = os.environ['KITSU_URL']
kitsuLogin = os.environ['KITSU_LOGIN']
kitsuPassword = os.environ['KITSU_PASSWORD']

# parse stringified array
excludeList = ast.literal_eval(os.environ['EXCLUDE_EVENTS'])
excludeList = [n.strip() for n in excludeList]

lang = os.environ['LANG']

# init gazu
gazu.client.set_host(kitsuHost + "/api")
gazu.log_in(kitsuLogin, kitsuPassword)
gazu.set_event_host(kitsuHost + "/socket.io")


def rtw(data):
    print("rtw (ready for work) started..")

    # debug
    print(json.dumps(data))

    # verify task is set to 'Done'
    done = gazu.task.get_task_status_by_short_name("done")
    if (data["new_task_status_id"] != done["id"]):
        return

    # get task info
    task = gazu.client.get("data/tasks/" + data["task_id"])
    
    # get entity task belongs to (to determine if it's shot or asset)
    entity = gazu.client.get("data/entities/" + task["entity_id"])

    # get all tasks associated with this entity
    tasksList = gazu.client.get("data/tasks?entity_id=" + entity["id"])
    #tasksList = gazu.task.get_task_by_entity(entity, task["task_type_id"])
    
    # red or blue pill
    forShots = "false"
    if (entity["type"] != "Asset"):
        forShots = "true"

    # get all task types for assets only
    taskTypesList = gazu.client.get("data/task-types?for_shots="+forShots)
    
    # sort the list of task types by 'priority' field
    sortedTaskTypesList = sorted(taskTypesList, key=lambda d: d['priority']) 

    # get id's of all task types
    IDs = []
    for elem in sortedTaskTypesList:
        IDs.append(elem["id"])
    
    # make array of excluded id's of task types
    toExcludeIDs = []
    for id in IDs:
        toExcludeIDs.append(id)
        if (id == task["task_type_id"]):
            break

    # exclude using list of id's to exclude
    for i in toExcludeIDs:
        if i in IDs:
            IDs.remove(i)

    # change status for 'next' task type
    rtw = gazu.task.get_task_status_by_short_name("rtw") # be sure to have a status in Kitsu with 'rtw' short name wich is: Ready to Work
    if (len(IDs) > 0):
        id = IDs[0]
        for task in tasksList:
            if (task["task_type_id"] == id):
                # Get fresh data for particular task
                if (task["task_status_id"] != done["id"]):
                    gazu.task.add_comment(task["id"], rtw, messages.say(lang, "rtw_changed"))
                else:
                    return

def delta(data):
    print("delta (delta between plan / actual) started..")

    # verify task is set to 'Done'
    done = gazu.task.get_task_status_by_short_name("done")
    if (data["new_task_status_id"] != done["id"]):
        return
    
    # get task info
    task = gazu.client.get("data/tasks/" + data["task_id"])
    start_date = task["start_date"]
    due_date = task["due_date"]
    end_date = task["end_date"]

    if (start_date is None or due_date is None or end_date is None):
        return

    # datetime(year, month, day, hour, minute, second)
    start = datetime.datetime.strptime(task["start_date"], '%Y-%m-%dT%H:%M:%S')
    due = datetime.datetime.strptime(task["due_date"], '%Y-%m-%dT%H:%M:%S')
    end = datetime.datetime.strptime(task["end_date"], '%Y-%m-%dT%H:%M:%S')

    # returns a timedelta object
    plan_delta = due-start
    print('Difference: ', plan_delta)
    
    '''
    plan_minutes = plan_delta.total_seconds() / 60
    print('Total difference in minutes: ', plan_minutes)
    
    # returns the difference of the time of the day
    plan_hours = plan_delta.total_seconds() / 60 / 60
    print('Total difference in hours: ', plan_hours)

    # returns the difference of the time of the day
    plan_days = plan_delta.total_seconds() / 60 / 60 / 24
    print('Total difference in days: ', plan_days)
    '''

    fact_delta = end-start    

    if (fact_delta.total_seconds() > plan_delta.total_seconds()):
        done = gazu.task.get_task_status_by_short_name("done")
        late_diff = fact_delta - plan_delta
        late_diff_days = late_diff.total_seconds() / 60 / 60 / 24
        gazu.task.add_comment(task["id"], done, messages.say(lang, "plan_short") + str(round(late_diff_days, 1)))
    else:
        done = gazu.task.get_task_status_by_short_name("done")
        late_diff =  plan_delta - fact_delta
        late_diff_days = late_diff.total_seconds() / 60 / 60 / 24
        gazu.task.add_comment(task["id"], done, messages.say(lang, "plan_long") + str(round(late_diff_days, 1)))

def lock(data):
    print("lock (new new task if old unfinished) started..")

    # debug
    print(json.dumps(data))

    # skip if todo was reassigned (we ignore todo all the time)
    todo = gazu.task.get_task_status_by_short_name("todo")
    if (data["new_task_status_id"] == todo["id"]):
        return

    # get task info
    task = gazu.client.get("data/tasks/" + data["task_id"])
    
    # get entity task belongs to (to determine if it's shot or asset)
    entity = gazu.client.get("data/entities/" + task["entity_id"])

    # get all tasks associated with this entity
    tasksList = gazu.client.get("data/tasks?entity_id=" + entity["id"])

    # red or blue pill
    forShots = "false"
    if (entity["type"] != "Asset"):
        forShots = "true"

    # get all task types for assets only
    taskTypesList = gazu.client.get("data/task-types?for_shots="+forShots)
    
    # sort the list of task types by 'priority' field
    sortedTaskTypesList = sorted(taskTypesList, key=lambda d: d['priority']) 

    # get id's of all task types
    IDs = []
    for elem in sortedTaskTypesList:
        IDs.append(elem["id"])
    
    # exclude current task type form id's list
    toExcludeIDs = []
    for id in IDs:
        if (id == task["task_type_id"]):
            break
        toExcludeIDs.append(id)

    # parse past tasks to check if they are done
    done = gazu.task.get_task_status_by_short_name("done")    
    if (len(toExcludeIDs) > 0):
        for id in toExcludeIDs:
            for tsk in tasksList:
                if id == tsk["task_type_id"]:
                    if tsk["task_status_id"] != done["id"]:
                        gazu.task.add_comment(task["id"], todo, messages.say(lang, "cant_skip"))

    

# main callback - collection of callbacks
def callbacks(data):
    if "rtw" not in excludeList:
        rtw(data)

    if "delta" not in excludeList:
        delta(data)

    if "lock" not in excludeList:
        lock(data)

# main
if __name__ == "__main__":
    event_client = gazu.events.init(logger=True)
    gazu.events.add_listener(event_client, "task:status-changed", callbacks)
    gazu.events.run_client(event_client)