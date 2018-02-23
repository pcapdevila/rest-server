from marathon_client import *
from flask import Flask


app = Flask(__name__)


@app.route('/instance/start')
def starti():
    out = start_service_instance(c)
    return out+'\n'


@app.route('/instance/stop')
def stopi():
    out = stop_service_instance(c)
    return out+'\n'


@app.route('/instance/list')
def listi():
    out = list_service_instances(c)
    return out+'\n'


@app.route('/instance/get/<task_id>')
def geti(task_id):
    out = get_service_instance(c, task_id)
    return out+'\n'


if __name__ == "__main__":
    c = MarathonClient('http://172.16.121.5:8080')
    app.run(host="0.0.0.0", debug=True)

