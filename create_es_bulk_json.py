# coding=utf-8
import sys, json, subprocess

def get_file_names(instance):
    path = "*/%s/*/current/dist/*[[:digit:]].war" % instance
    ssh = subprocess.Popen(['ssh', '-l', xe_user, xe_host, 'find', banner_home, '-type f -wholename', path, '-printf "%f\n"'],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        print >> sys.stderr, "ERROR: %s" % error
        sys.exit(1)

    return result    

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

def write_apps_to_file():
    xe_apps = {}

    for instance in environments:
        parse_file_names(instance, xe_apps)

    with open('xe_apps.json', 'w') as xe_app_file:
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
