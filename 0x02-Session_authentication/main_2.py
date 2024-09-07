#!/usr/bin/python3
""" Check response
"""
import requests
import json

if __name__ == "__main__":
    user_id = None
    session_id = None
    
    """ Read user_id and session_id from file """
    with open("session_id_hbtn.json", "r") as file:
        dJson = json.load(file)
        if dJson is None:
            dJson = {}
        user_id = dJson.get('user_id')
        session_id = dJson.get('session_id')

    r = requests.get('http://0.0.0.0:3456/', cookies={ '_my_session_id': session_id })
    if r.status_code != 200:
        print("Wrong status code: {}".format(r.status_code))
        exit(1)
    if r.headers.get('content-type') != "application/json":
        print("Wrong content type: {}".format(r.headers.get('content-type')))
        exit(1)
    
    try:
        r_json = r.json()
        
        user_id_r = r_json.get('user_id')
        if user_id_r is None:
            print("User ID not found")
            exit(1)
        
        if user_id_r != user_id:
            print("Wrong User ID not found")
            exit(1)
            
        print("OK", end="")
    except:
        print("Error, not a JSON")
