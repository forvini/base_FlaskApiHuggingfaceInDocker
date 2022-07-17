#Importing
from flask import Flask
import os
import requests
import json
import base64


# Setting Auth token, API URL and header
API_TOKEN = ""
API_URL = "https://api-inference.huggingface.co/models/mpariente/ConvTasNet_WHAM_sepclean"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


# Function definition of Huggingface query
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


app = Flask(__name__)

@app.route("/")
def main():

    print()

    # Making Query to Huggingface API
    output = query("./data/input/input.flac") 


    # Save base64 blob as Flac 
    for i in range(len(output)):

        blob = output[i]
        content = blob.get("blob")
        content_name = 'label_' + str(i)

        # Saving returning Base64 strings to WAV files
        wav_file = open(f"./data/output/{content_name}.wav", "wb")
        decode_string = base64.b64decode(content)
        wav_file.write(decode_string)



    return str(output)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True,host='0.0.0.0',port=port)