#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers
"""
from fabric.api import *
from os import path

env.hosts = ['3.85.84.57', '54.196.167.246']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Get the base name of the archive without extension
        archive_filename = path.basename(archive_path).split('.')[0]

        # Create directory to uncompress the archive
        run('mkdir -p /data/web_static/releases/{}'.format(archive_filename))

        # Uncompress the archive
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
            .format(archive_filename, archive_filename))

        # Remove the archive
        run('rm /tmp/{}.tgz'.format(archive_filename))

        # Move contents of the uncompressed archive to the releases directory
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'
            .format(archive_filename, archive_filename))

        # Remove the web_static directory
        run('rm -rf /data/web_static/releases/{}/web_static'.format(archive_filename))

        # Remove the existing symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_filename))

        print("New version deployed!")
        return True
    except:
        return False

