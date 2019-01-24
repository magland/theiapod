from subprocess import Popen, PIPE
import shlex

def theiapod(*,repository):
    script_path='/tmp/test.sh'
    script="""
cd /home/theia
yarn theia start /home/project --hostname=0.0.0.0
    """
    _write_text_file(script_path,script)
    opts=[
        '-p 3000:3000'
    ]
    cmd='docker run -v {script_path}:/code/script.sh {opts} -it magland/theiapod:latest bash /code/script.sh'
    cmd=cmd.replace('{script_path}',script_path)
    cmd=cmd.replace('{opts}',' '.join(opts))
    _run_command_and_print_output(cmd)

def _write_text_file(fname,txt):
    with open(fname,'w') as f:
        f.write(txt)

def _run_command_and_print_output(command):
    print('RUNNING: '+command)
    with Popen(shlex.split(command), stdout=PIPE, stderr=PIPE) as process:
        while True:
            output_stdout = process.stdout.readline()
            output_stderr = process.stderr.readline()
            if (not output_stdout) and (not output_stderr) and (process.poll() is not None):
                break
            if output_stdout:
                print(output_stdout.decode())
            if output_stderr:
                print(output_stderr.decode())
        rc = process.poll()
        return rc
