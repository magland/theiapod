import subprocess
import os

src_dir=os.path.dirname(os.path.realpath(__file__))

def theiapod(*,repository,port=3000,image=None,expose_ports=[],mount_tmp=True):
    if image is None:
        image='magland/theiapod:latest'
    opts=[
        '-p {port}:{port}',
        '-it',
        '-v {src_dir}/theiapod_init_in_container.py:/theiapod_init'
    ]
    if mount_tmp:
        opts.append('-v /tmp:/tmp')
    for pp in expose_ports:
        if type(pp)==tuple:
            opts.append('-p {}:{}'.format(pp[0],pp[1]))
        else:
            opts.append('-p {}:{}'.format(pp,pp))

    cmd='docker run {opts} {image} {repository} {port}'
    cmd=cmd.replace('{opts}',' '.join(opts))
    cmd=cmd.replace('{src_dir}',src_dir)
    cmd=cmd.replace('{image}',image)
    cmd=cmd.replace('{repository}',repository)
    cmd=cmd.replace('{port}',str(port))
    _run_command_and_print_output(cmd)

#def _write_text_file(fname,txt):
#    with open(fname,'w') as f:
#        f.write(txt)

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
    for aa in execute(cmd.split()):
        print(aa, end="")
