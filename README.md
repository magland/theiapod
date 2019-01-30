# Theiapod

Self-hosted [gitpod](https://gitpod.io/)-style workspaces for github repositories using [theia](https://www.theia-ide.org/).

## Objectives

Philosophy and beliefs:

1. Every repository should have a single-click method for trying it out within a browser using a cloud-backed container with customizable environment.
2. That container/environment should also serve as a fully-functional development environment with a rich browser-based IDE (e.g., Theia) and the ability to push changes back to the original repository or to a forked version.
3. This environment should also be launchable from the command line in order to use local resources for the environment.
4. Offline mode should be supported, and the workspace should persist on the local disk.
5. It should be possible to expose network ports so that web services may be tested in a separate browser tab.
6. When working locally, it should be possible to mount data volumes on the local disk. This enables operating on local data and including configuration files (e.g., git credentials).

The [gitpod](https://gitpod.io/) project solves the first two requirements. It uses the [Theia browser-based IDE](https://www.theia-ide.org/). The goal of theiapod is to provide a command-line utility that accomplishes the remaining objectives (i.e., operating on a local machine). Thus theiapod is meant to be used in conjunction with gitpod.

## Prerequisites

* Install git, docker and python 3 (>=3.6).
* Install theiapod as follows

```
pip install git+https://github.com/magland/theiapod
# for subsequent updates:
pip install --upgrade git+https://github.com/magland/theiapod
```

## Basic usage

```
theiapod [repository_name] <options>
<or>
theiapod -w [workspace directory] <options>
```

For example, to open the theiapod project itself:
```
git clone https://github.com/magland/theiapod
theiapod -w $PWD/theiapod --port 3000
```

Then point your browser to:

```
http://localhost:3000
```

This will open the Theia IDE in a browser with the workspace mounted at `/home/project` within the container. The source files may be edited either inside the container (via browser) or outside the container on the local (host) machine. Programs in the project should be executed inside the container, because that's where the development environment is set up.

A shortcut command (that automatically clones the repository into a temporary directory):

```
theiapod https://github.com/magland/theiapod --port 3000
```

To run the environment in the cloud, directly from github, use [gitpod](https://gitpod.io/workspaces/), which has a really nice [chrome or firefox extension](https://docs.gitpod.io/20_Browser_Extension.html). Then you can just click the "gitpod" button directly from the github page for the project.

## Configuring the theiapod environment for your project

Gitpod uses the .gitpod.yml configuration file at the root of the project repository. Similarly, theiapod uses the .theiapod.yml. If no .theiapod.yml file exists, the .gitpod.yml configuration file will instead be used (although the custom docker image option is not respected in this case). If neither configuration file is present, the default configuration will be used.

**Why two different config files?** It is because theiapod uses a different base docker image than gitpod. Any custom docker image (optional) should be built off of the corresponding gitpod/theiapod image. Therefore two files are needed in order to specify the two custom images.

An example .theiapod.yml file:

```
image: "docker_user/theiapod_custom"
tasks:
- command: ./init.sh
```

If a custom image is used (optional), it should be based on one of the default theiapod docker images. Right now, there is only one -- it is `magland/theiapod` on dockerhub.

Upon startup of the theiapod container, the task commands are run sequentially. Note that this is a bit different from the gitpod behavior where the task commands seem to run simultaneously. Another difference is that the theiapod commands run prior to launching the IDE, whereas gitpod runs the commands within the IDE environment.

## Exposing ports

Use the `-p` option. For example, to expose ports 3005-3007:

```
theiapod -w [workspace] --port 4001 -p 3005,3006,3007
```

Or to map ports (docker style):

```
theiapod -w [workspace] --port 4001 -p 3005:6005,3006,6006,3007:6007
```

## Mounting volumes

Mounting volumes is docker style using the `-v` option. For example:

```
theiapod -w [workspace] --port 4001 -v /disk1/data:/data
```

## Using a custom docker image for the environment

TODO: write this section

## Mounting git credentials in the theiapod container

TODO: write this section


## Some Theia IDE hints

* Press F1 within the IDE to search for commands and shortcuts.
* Click "Files" in the upper-left corner to open the file browser (if it isn't already open).
* Click "Git" in the upper-left corner for the graphical git integration.
* Open a new terminal via **Ctrl+Shift+`**
* Preview for markdown files is supported.

## Authors

Jeremy Magland