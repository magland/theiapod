import subprocess
import os
import shutil
import tempfile
import random
import string
import yaml

src_dir=os.path.dirname(os.path.realpath(__file__))

def theiapod(*,repository='',port=3000,image=None,expose_ports=[],volumes=[],mount_tmp=True,host_working_directory=None):
    if host_working_directory is None:
        if not repository:
            raise Exception('You must either specify a repository or a host working directory.')
        host_working_directory=_get_random_directory()
    host_working_directory=os.path.abspath(host_working_directory)
    if repository:
        if os.path.exists(host_working_directory):
            raise Exception('Host working directory already exists: '+host_working_directory)
        _git_clone_into_directory(repository,host_working_directory)

    if os.path.exists(host_working_directory+'/.theiapod.yml'):
        config=_parse_yaml(host_working_directory+'/.theiapod.yml')
    else:
        config=_parse_yaml(host_working_directory+'/.gitpod.yml')
        if config:
            if 'image' in config:
                config['image']=None # don't use the gitpod image
    if not config:
        config={}

    print(':::::::::::::::::::::::config:',config)
    if image is None:
        if 'image' in config:
            image=config['image']
        
    if image is None:
        image='magland/theiapod:latest'

    print('Using image: '+image)

    opts=[
        '-p {port}:{port}',
        '-it',
        '-v {src_dir}/theiapod_init_in_container.py:/theiapod_init',
        '-v {host_working_directory}:/home/project',
        '--network host'
    ]
    if mount_tmp:
        opts.append('-v /tmp:/tmp')
    for pp in expose_ports:
        if not (type(pp)==tuple):
            pp=(pp,pp)
        pp0_list=str(pp[0]).split('-')
        pp1_list=str(pp[1]).split('-')
        if len(pp0_list)!=len(pp1_list):
            raise Exception('Invalid -p option')
        if len(pp0_list)==1:
            opts.append('-p {}:{}'.format(pp[0],pp[1]))
        elif len(pp0_list)==2:
            p0min=int(pp0_list[0])
            p0max=int(pp0_list[1])
            p1min=int(pp1_list[0])
            p1max=int(pp1_list[1])
            p0s=list(range(p0min,p0max+1))
            p1s=list(range(p1min,p1max+1))
            if len(p0s)!=len(p1s):
                raise Exception('Invalid -p option')
            for i in range(len(p0s)):
                opts.append('-p {}:{}'.format(p0s[i],p1s[i]))
        else:
            raise Exception('Invalid -p option')

    for vv in volumes:
        if type(vv)==tuple:
            opts.append('-v {}:{}'.format(os.path.abspath(vv[0]),os.path.abspath(vv[1])))
        else:
            raise Exception('volumes must be tuples.')

    cmd='docker run {opts} {image} /home/project {port} {user} {uid}'
    #cmd='docker run {opts} {image}'
    cmd=cmd.replace('{opts}',' '.join(opts))
    cmd=cmd.replace('{src_dir}',src_dir)
    cmd=cmd.replace('{image}',image)
    # cmd=cmd.replace('{repository}',repository)
    cmd=cmd.replace('{host_working_directory}',host_working_directory)
    cmd=cmd.replace('{port}',str(port))
    cmd=cmd.replace('{user}',os.environ['USER'])
    cmd=cmd.replace('{uid}',str(os.getuid()))

    _run_command_and_print_output(cmd)

#def _write_text_file(fname,txt):
#    with open(fname,'w') as f:
#        f.write(txt)

def _parse_yaml(fname):
  try:
    with open(fname) as f:
      obj=yaml.load(f)
    return obj
  except:
    return None

def _get_random_directory():
    return tempfile.gettempdir()+'/theiapod_workspace_'+_get_random_string(10)

def _get_random_string(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def _git_clone_into_directory(repo,path):
    cmd='git clone {} {}'.format(repo,path)
    _run_command_and_print_output(cmd)

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
