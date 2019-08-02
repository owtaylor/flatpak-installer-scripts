#!/usr/bin/python3

import os
import subprocess
import sys

import gi
from gi.repository import GLib


# See FLATPAK_DEPLOY_DATA_GVARIANT_STRING in flatpak/common/flatpak-dir-private.h
# First element is the remote name
FLATPAK_DEPLOY_DATA_GVARIANT_STRING='(ssasta{sv})'
FLATPAK_DEPLOY_DATA_GVARIANT_TYPE=GLib.VariantType(FLATPAK_DEPLOY_DATA_GVARIANT_STRING)

def change_ref_origin(flatpak_installation, ref, new_origin):
    deploy_file = os.path.join(flatpak_installation, ref, 'active/deploy')
    with open(deploy_file, "rb") as f:
        content = f.read()

    variant = GLib.Variant.new_from_bytes(FLATPAK_DEPLOY_DATA_GVARIANT_TYPE, GLib.Bytes(content), False)
    children = [variant.get_child_value(i) for i in range(variant.n_children())]
    # Replace the origin
    children[0] = GLib.Variant('s', new_origin)
    new_variant = GLib.Variant.new_tuple(*children)
    serialized = new_variant.get_data_as_bytes().get_data()
    with open(deploy_file, "wb") as f:
        f.write(serialized)

if len(sys.argv) != 3:
    print("Usage: install-flatpak-content.py [local_repo] [dest_flatpak_installation]", file=sys.stderr)
    sys.exit(1)

local_repo = sys.argv[1]
dest_flatpak_dir = sys.argv[2]

os.environ['FLATPAK_USER_DIR'] = dest_flatpak_dir

if os.path.exists(dest_flatpak_dir):
    print("'{}' should not already exist".format(dest_flatpak_dir))
    sys.exit(1)

subprocess.check_call(['flatpak', '--user', 'remote-add', '--no-gpg-verify', 'anaconda', local_repo])

output = subprocess.check_output(['flatpak', '--user', 'remote-ls', '--columns=ref', 'anaconda'], encoding="UTF-8")
refs = output.strip().split('\n')

subprocess.check_call(['flatpak', '-y', '--user', 'install', 'anaconda'] + refs)
subprocess.check_call(['flatpak', '--user', 'remote-add', 'fedora', 'oci+https://registry.fedoraproject.org'])

for ref in refs:
    change_ref_origin(dest_flatpak_dir, ref, 'fedora')
