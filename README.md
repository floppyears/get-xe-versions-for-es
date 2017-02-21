# Get XE Versions for ES (Elastic Search)

This repository contains a script that uses SSH to get the names of war files on a remote server,
parses their names, versions, and instances, then finally dumps that data to a JSON file ready
to be bulk uploaded to Elastic Search.

## Instructions
1. Copy configuration_example.json as configuration.json and modify as needed. 
banner_home is where the script will be searching from.
2. Run the script passing configuration.json as an argument:
```
python ./create_es_bulk_json.py -i configuration.json
```
3. xe_apps.json will be created in the same directory as create_es_bulk_json.py
4. Post xe_apps.json to Elastic Search:
```
curl -s -XPOST localhost:9200/xe/apps/_bulk --data-binary "@xe_apps.json"
```
Note: xe_apps.json will be overwritten when running create_es_bulk_json.py