import urllib.request
import urllib.parse
import json
# import pprint
# import os

key = "AIzaSyCOD3KvY2DDzEfel-NZ_LKIWXr86EF_EUw"
# At the time of deployment we should use environment variable
# key = os.environ.get("GEOCODE_API")


def geocode(rec_data):
    try:

        url_str = "https://maps.googleapis.com/maps/api/geocode/json?address="

        address = rec_data["address"]
        key_data = "&key="+key
        string_data_url = urllib.parse.quote(address)
        print(url_str+string_data_url)
        response_data = urllib.request.urlopen(url_str+string_data_url+key_data)
        response_code = response_data.getcode()
        if response_code != 200:
            return {"status": 0, "msg": response_code}
        response_data_text = response_data.read().decode("utf-8")
        print(response_data_text)

        if "geometry" in response_data_text:
            dictdata = json.loads(response_data_text)
            print(dictdata["results"][0]["geometry"]["location"])
            return {"status": 1, "location": dictdata["results"][0]["geometry"]["location"]}
        else:
            return {"status": 0, "msg": "no location data found"}

    except Exception as e:

        return {"status": 0, "msg": " msg->"+str(e)}
