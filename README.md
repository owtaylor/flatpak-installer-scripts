About
=====
Some test scripts for embedding Flatpaks into a Fedora Silverblue installer

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
