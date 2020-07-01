import json
import sys
import time
import requests

def push_note(title, body):
    data_send = {"type": "note", "title": title, "body": body}

    ACCESS_TOKEN = 'YOUR_PUSHBULLET_API_TOKEN'
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})

package_number = sys.argv[1]
package_status = 'initial'

while package_status != 'ready_to_pickup':

    def get_package_info():
        api_url = 'https://api-shipx-pl.easypack24.net/v1/tracking/' + package_number
        response = requests.get(api_url)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return None

    package_info = get_package_info()
    if package_info["status"] != package_status:
        push_note("Package status changed", package_info["status"])


    package_status = package_info["status"]
    time.sleep(360)

push_note("Package is ready to pickup", "Package is ready to pickup, 48h remaining")
print("Package is ready to be picked up")
