#!/usr/bin/env python3

import os
import sys

basedir = ""
try:
    basedir = sys.argv[1]
except:
    print("Incorrect repository path")

if basedir != "":
        bash_command = [f"cd {basedir}",  "git status "]
        result_os1 = os.listdir(basedir);

        if result_os1.__contains__(".git"):
                result_os = os.popen(' && '.join(bash_command)).read()
                for result in result_os.split('\n'):
                    if result.find('modified') != -1:
                        prepare_result = result.replace('modified:', basedir)
                        print(prepare_result)
        else:
                print("There is no git repository on the entered path")