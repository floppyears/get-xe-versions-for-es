# coding=utf-8
import sys, json, subprocess

# SSH into a remote server and find war files under certain directories
def get_file_names(instance):
    path = "*/%s/*/current/dist/*[[:digit:]].war" % instance
    ssh = subprocess.Popen(['ssh', '-l', xe_user, xe_host, 'find', banner_home, '-type f -wholename', path, '-printf "%f\n"'],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    # If we didn't get any files, something's wrong
    if result == []:
        error = ssh.stderr.readlines()
        print >> sys.stderr, "ERROR: %s" % error
        sys.exit(1)

    return result    

# Parse the whole filename into the application name and version.
def parse_file_names(instance, xe_apps):
    file_names = get_file_names(instance)

    for file in file_names:
        app = file.split('-', 1)[0]
        version = file.split('-', 1)[-1]
        version = version.split('.war', 1)[0]

        version_dict = {"instance": instance, "version": version}

        if app in xe_apps:
            xe_apps[app]['versions'].append(version_dict)
        else:
            xe_apps[app] = {"applicationName": app, "versions": [version_dict]}

# Call above methods to get a dict containing all the apps, then write to a json file
def write_apps_to_file():
    xe_apps = {}

    # For each deployed environment, do a search for war files in the respective directories
    for instance in environments:
        parse_file_names(instance, xe_apps)

    # Create json file, overwrite if it exists.
    with open('xe_apps.json', 'w') as xe_app_file:
        # Create two lines in the json file for each app, one for id, and one for data
        for app in xe_apps:
            xe_app_file.write(json.dumps({"index":{"_id":xe_apps[app]['applicationName']}}))
            xe_app_file.write('\n')
            xe_app_file.write(json.dumps(xe_apps[app]))
            xe_app_file.write('\n')

if __name__ == '__main__':
    options_tpl = ('-i', 'config_path')
    del_list = []
    
    for i,config_path in enumerate(sys.argv):
        if config_path in options_tpl:
            del_list.append(i)
            del_list.append(i+1)

    del_list.reverse()

    for i in del_list:
        del sys.argv[i]

    config_data_file = open(config_path)
    config_json = json.load(config_data_file)

    xe_user = config_json["xe_user"]
    xe_host = config_json["xe_host"]
    banner_home = config_json["banner_home"]
    environments = config_json["environments"]

    xe_apps = {}

    write_apps_to_file()
