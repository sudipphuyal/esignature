# from flask import Flask, request
# import json
# import hashlib

# app = Flask(__name__)

# key_value = {
#     "hospital_name": "test",
#     "patient_name": "testname",
#     "doctor_name": "doc_name"
#     "Secret":""
# }


# json_string = json.dumps(key_value, sort_keys=True)


# secret_key = hashlib.sha256(json_string.encode()).hexdigest()

# print(secret_key)
# @app.route("/")
# def hello_world():
#     return f"Secret Key: {secret_key}"


# @app.route("/verify/<key>/", methods=['GET'])
# def verify(key):    
#     if request.method == 'GET':
#         if secret_key == key:
#             return 'secret key verification passed.'
#         else:
#             return 'Secret key do not match.'
#     else:
#         return 'failed'

# if __name__ == '__main__':
#     app.run(debug=True)


## 20 Oct
from datetime import datetime

class QESValidator:
    def __init__(self, sigCert, trustedList, signingTime=None):
        self.sigCert = sigCert
        self.trustedList = trustedList
        self.signingTime = signingTime or datetime.now()
    
    def is_qualified_certificate(self):
        for entry in self.trustedList:
            if self.cert_matches_trusted_list_entry(entry):
                if self.entry_is_qualified(entry):
                    return True
        return False

    def cert_matches_trusted_list_entry(self, entry):
        """Checks if the certificate matches a CA/QC entry in the trusted list"""
        return entry['cert_id'] == self.sigCert['cert_id']  # Simplified check

    def entry_is_qualified(self, entry):
        """Determines if the entry in the trusted list is a qualified certificate"""
        return entry['status'] == 'granted'

    def check_qscd(self):
        """Determines if the signature creation device is qualified"""
        if 'QSCD' in self.sigCert and self.sigCert['QSCD']:
            return True
        return False

    def validate_qes(self):
        """Main function to validate the QES based on Articles 32 and 40"""
        if not self.is_qualified_certificate():
            return "The certificate is not qualified."
        
        if not self.check_qscd():
            return "The QSCD is not valid."
        
        return "The signature is a valid QES."

# Example data (replace with actual sigCert and trustedList structures)
sigCert = {
    'cert_id': '12345',
    'QSCD': True
}

trustedList = [
    {'cert_id': '12345', 'status': 'granted'},
    {'cert_id': '67890', 'status': 'revoked'}
]

validator = QESValidator(sigCert, trustedList)
result = validator.validate_qes()
print(result)