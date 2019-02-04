#!/bin/bash

set -ex

PROJECT_DIRECTORY=$1
PORT=$2
USER=$3
UID_=$4

useradd -l -u $UID_ -G sudo -md /home/$USER -s /bin/bash -p $USER $USER
sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers
chown -R $USER:$USER /venv

#chown -R $USER:$USER $PROJECT_DIRECTORY
#if [ -f "/theiapod_init" ]; then
#	chmod a+x /theiapod_init
#	chown $USER:$USER /theiapod_init
#fi

## IMPORTANT to put single quotes around EOL here so that the stuff does not get interpretted
cat >/the_script.sh <<'EOL' 
#!/bin/bash
set -ex

# symbolic links to files in /home/theiapod to the home directory
if [ -d /home/theiapod ]; then
    echo "test"
    ls /home
    ls /home/theiapod/.*
    for filename in $(ls -A /home/theiapod/); do
        ln -s /home/theiapod/$filename ~/$filename
    done
fi

cd $PROJECT_DIRECTORY
source /venv/bin/activate
if [ -f "/theiapod_init" ]; then
	echo "RUNNING python /theiapod_init"
	python /theiapod_init
fi
cd /home/theia
yarn theia start $PROJECT_DIRECTORY --hostname=0.0.0.0 --port=$PORT
EOL
chmod a+x /the_script.sh

sudo -u $USER bash -c "PROJECT_DIRECTORY=$PROJECT_DIRECTORY PORT=$PORT /the_script.sh"
