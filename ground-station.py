from flask import Flask, request, render_template, jsonify
from commands import Command
import json
# import transmission
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/")
def hello():
    return "HelloWorld"

@app.route('/index', methods=['GET', 'POST'])
def index():   
    return render_template("index.html")



@cross_origin(supports_credentials=True)
@app.route('/commands', methods=['GET'])
def get_commands():
    print("Getting Commands...")
    cmd = [name for name, member in Command.__members__.items()]
    print("Got the commands")
    return jsonify({"commands":cmd})

# @app.route('/transmit', methods=['POST'])
# def transmit():
    
#     if request.method == 'POST':
#         result = request.form
#         print(result)

#     print("Transmitting...")
#     request_json = request.form
#     print(request_json)
#     for k, v in request_json.items():

#     	if k not in Command.__members__:
#     		print("ERROR: {} is not a valid command.".format(k))
#     		continue

#     	if v is None or len(v) < 1:
#     		print("ERROR: Command {} has no value.".format(k))
#     		continue

#     	command_line = str(Command.ENDSTOP.value + Command[k].value 
#     	+ str(v))

#     	print(command_line)

#     	transmission.write_packets(command_line)

#     return "Done"



if __name__ == '__main__':
    app.run(port=5000,debug=True, threaded=True) 