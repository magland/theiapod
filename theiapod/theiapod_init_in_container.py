#!/usr/bin/env python3

import yaml
import subprocess

def main():
  gitpod=_parse_gitpod_yaml()
  print('gitpod',gitpod)
  if 'tasks' in gitpod:
    for task in gitpod['tasks']:
      if 'command' in task:
        _run_command_and_print_output(task['command'])

def _parse_gitpod_yaml():
  try:
    fname='.gitpod.yml'
    with open(fname) as f:
      obj=yaml.load(f)
    return obj
  except:
    return {}

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        #yield stdout_line
        print(stdout_line,end='\r')
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def _run_command_and_print_output(cmd):
    print('RUNNING: '+cmd);
    execute(cmd.split())

if __name__== "__main__":
  main()