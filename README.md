# theiapod

Self-host gitpod-style workspaces for github repositories using theia.

## Belief and objectives

1. Every repository should have a single-click method for trying it out within a browser using a cloud-backed container with customizable environment.
2. That container/environment should also serve as a fully-functional development environment with a rich browser-based IDE (e.g., Theia) and the ability to push changes back to the original repository or to a forked version.
3. This environment should also be launchable from the command line in order to use local resources for the environment.
4. Offline mode should be supported, and the workspace should persist on the local disk.
5. It should be possible to expose network ports so that web services may be tested in a separate browser tab.
6. When working locally, it should be possible to mount data volumes on the local disk. This enables operating on local data and including configuration files (e.g., git credentials).

The [gitpod](https://gitpod.io/) project solves the first two requirements. The goal of theiapod is to provide a command-line utility that accomplishes the remaining objectives. Thus theiapod is meant to be used in conjunction with gitpod.

## Prerequisites

* Install git, docker and python 3 (>=3.6).
* Install theiapod as follows

```
pip install git+https://github.com/magland/theiapod
```

For updates:

```
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

A shortcut (that automatically clones the repository into a temporary directory):

```
theiapod https://github.com/magland/theiapod --port 3000
```
