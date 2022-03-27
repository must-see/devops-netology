#!/usr/bin/env python3

import os

basedir = "C:/Users/must-/PycharmProjects/devops-netology"
bash_command = [f"cd {basedir}", "git status "]
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('modified:', basedir)
        print(prepare_result)
