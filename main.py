from flask import Flask, request
import json
import hashlib

app = Flask(__name__)

key_value = {
    "hospital_name": "test",
    "patient_name": "testname",
    "doctor_name": "doc_name"
}


json_string = json.dumps(key_value, sort_keys=True)


secret_key = hashlib.sha256(json_string.encode()).hexdigest()

print(secret_key)
@app.route("/")
def hello_world():
    return f"Secret Key: {secret_key}"


@app.route("/verify/<key>/", methods=['GET'])
def verify(key):    
    if request.method == 'GET':
        if secret_key == key:
            return 'secret key verification passed.'
        else:
            return 'Secret key do not match.'
    else:
        return 'failed'

if __name__ == '__main__':
    app.run(debug=True)
