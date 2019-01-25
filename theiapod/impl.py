import subprocess
import os
import shutil
import tempfile
import random
import string

src_dir=os.path.dirname(os.path.realpath(__file__))

def theiapod(*,repository='',port=3000,image=None,expose_ports=[],mount_tmp=True,host_working_directory=None):
    if host_working_directory is None:
        if not repository:
            raise Exception('You must either specify a repository or a host working directory.')
        host_working_directory=_get_random_directory()
    if repository:
        if os.path.exists(host_working_directory):
            raise Exception('Host working directory already exists: '+host_working_directory)
        _git_clone_into_directory(repository,host_working_directory)

    if image is None:
        image='magland/theiapod:latest'
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
        if type(pp)==tuple:
            opts.append('-p {}:{}'.format(pp[0],pp[1]))
        else:
            opts.append('-p {}:{}'.format(pp,pp))

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
