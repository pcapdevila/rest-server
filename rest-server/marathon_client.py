import json
from marathon import MarathonClient
from marathon.models import MarathonApp
from marathon.models import MarathonTask
from marathon.models.container import MarathonContainer
from marathon.models.container import MarathonDockerContainer


def start_service_instance(client):

    """ Starts an app if no one exists, otherwise scales app by 1

        Arguments: MarathonClient object

        Returns: app or deployment JSON data
    """

    # Get the number of apps named 'sleepy' running

    app_list = client.list_apps(app_id='sleepy')
    
    if len(app_list) == 0:
        # If app does not exist, create app
        app = create_app(client)
        return app.to_json()
    else:
        # If app exist scale up app
        deployment = client.scale_app('sleepy', delta=1)  
        return json.dumps(deployment)
    

def stop_service_instance(client):

    """ Stops one instance by scaling down app by 1

        Arguments: MarathonClient object

        Returns: deployment JSON output
    """

    deployment = client.scale_app('sleepy', delta=-1)  # Scale down app
    return json.dumps(deployment)


def create_app(client):
    """ Spins up a service based on predefined parameters

        Arguments: MarathonClient object

        Returns: app creation JSON output
    """

    # Creates app running a command within a docker container

    app = client.create_app(
        'sleepy', 
        MarathonApp(
            cmd='while true; do sleep 33 ; done', 
            mem=32, 
            cpus=0.1, 
            container=MarathonContainer(
                docker=MarathonDockerContainer(image='python:3'), 
                type='DOCKER'
            )
        )
    )
    return app


def list_service_instances(client):
    """ Lists existing instances for app 'sleepy'

        Arguments: MarathonClient object

        Returns: JSON array of existing instances
    """

    # Returns a list of MarathonTask objects

    task_list = client.list_tasks('sleepy') 

    # Builds list convertng MarathonTask objects into JSON

    instances = [MarathonTask.to_json(x) for x in task_list]
    return '['+','.join(instances)+']'  # Builds valid JSON output


def get_service_instance(client, instance_id='null'):
    """ Gets instance by matching id'

        Arguments: MarathonClient object

        Returns: JSON applicatoin task
    """

    task_list = client.list_tasks('sleepy')
    for task in task_list:  # iterate over list
        if task.id == instance_id:  # match by MarathonTask.id parameter
            return task.to_json()

