import subprocess

def theiapod(*,repository,port=3000,image='magland/theiapod:latest'):
    print('test 1')
    opts=[
        '-p {port}:{port}',
        '-it'
    ]
    cmd='docker run {opts} {image} {repository}'
    cmd=cmd.replace('{opts}',' '.join(opts))
    cmd=cmd.replace('{image}',image)
    cmd=cmd.replace('{repository}',repository)
    cmd=cmd.replace('{port}',str(port))
    print('test 2')
    _run_command_and_print_output(cmd)
    print('test 3')

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
    for aa in execute(cmd.split()):
        print(aa, end="")
