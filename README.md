About
=====
Some test scripts for embedding Flatpaks into a Fedora Silverblue installer

Setup
=====
fedora-lorax-templates (for Silverblue specified templates) and lorax (for generic templates)
are submodules of this project. Lorax and flatpak also needs to be installed on your system.
Hopefully the lorax submodule and the lorax code from the system install are sufficiently
in-sync. (This is true at time of writing for F29 and F30, building an image for F31 rawhide.)

``` sh
sudo dnf install flatpak lorax
git submodule init
git submodule update
```

run-lorax.sh:
=============
Run lorax to create a Silverblue repository with embedded Flatpaks

Usage:
``` sh
sudo run-lorax.sh
```

Creates the following directories:

* `cache/`: DNF cache directory, speeds up multiple runs
* `logs/`: Logs go here
* `out/`: Directory with output boot.iso
* `work/`: Temporary working directory

install-flatpak-content.py
==========================
Installs Flatpak content from a local repository into a specified destination, rewriting refs to point to the upstream Fedora repository

Usage:

``` sh
install-flatpak-content.py [local_repo] [dest_flatpak_installation]

```

for example, after running run-lorax.sh, you can install from the install tree it leaves in its workdir:

``` sh
rm -rf dest-flatpak && install-flatpak-content.py work/installtree/flatpak/repo dest-flatpak

```
