#!/bin/sh

set -ex

die() {
    echo $1 2>&1
    exit 1
}

[ -d fedora-lorax-templates ] || die "Please run: git submodule init; git submodule update"

templatedir=$(cd fedora-lorax-templates/ostree-based-installer && pwd)

rm -rf work
mkdir work

rm -rf logs
mkdir logs

rm -rf out

cat > work/Everything.repo <<EOF
[everything]
name=Fedora $releasever - $basearch
baseurl=https://kojipkgs.fedoraproject.org/compose/rawhide/latest-Fedora-Rawhide/compose/Everything/x86_64/os/
enabled=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-31-$basearch
skip_if_unavailable=False
EOF

cd logs
exec lorax \
    --sharedir=../lorax/share \
    --workdir=../work \
    --cachedir=../cache \
    --repo=../work/Everything.repo \
    --product="Fedora Silverblue" \
    --version=31  \
    --release=None \
    --rootfs-size=8 \
    --add-template=$templatedir/lorax-embed-flatpaks.tmpl \
    --add-template=$templatedir/lorax-configure-repo.tmpl \
    --add-template=$templatedir/lorax-embed-repo.tmpl \
    --add-template-var=ostree_install_repo=https://kojipkgs.fedoraproject.org/compose/ostree/repo/ \
    --add-template-var=ostree_update_repo=https://ostree.fedoraproject.org \
    --add-template-var=ostree_osname=fedora \
    --add-template-var=ostree_oskey=fedora-31-primary \
    --add-template-var=ostree_contenturl=mirrorlist=https://ostree.fedoraproject.org/mirrorlist \
    --add-template-var=ostree_install_ref=fedora/rawhide/x86_64/silverblue \
    --add-template-var=ostree_update_ref=fedora/rawhide/x86_64/silverblue \
    --add-template-var=flatpak_remote_name=fedora \
    --add-template-var=flatpak_remote_url=oci+https://registry.fedoraproject.org \
    --add-template-var=flatpak_remote_refs="runtime/org.fedoraproject.Platform/x86_64/f30 app/org.gnome.gedit/x86_64/stable" \
    ../out
