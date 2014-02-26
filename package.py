#!/usr/bin/env python2.7

import os, shutil, subprocess, sys, tempfile, zipfile

try:
    import _config
except ImportError:
    _config = type('_config', (object, ), {})


def config_attr(attr_name):
    return getattr(_config, attr_name, None)

VERBOSE = config_attr('VERBOSE') or False


def clone_repo(git_cmd, repo_url):
    tmp_dir = tempfile.mkdtemp()

    actual_url = repo_url
    if repo_url.startswith('https'):  # need username and password, unlike for git+ssh
        host_name = repo_url.split('/')[2]
        print "Username for {}:".format(host_name),
        username = raw_input()
        print "Password for {}@{}:".format(username, host_name),
        passwd = raw_input()

        split_link = repo_url.split('://')
        actual_url = "{}://{}:{}@{}".format(split_link[0], username, passwd, split_link[1])

    subprocess.call([git_cmd, 'clone', actual_url, tmp_dir])
    print "Done!"

    return tmp_dir


def zip_file(src, dst):
    zf = zipfile.ZipFile("{}.zip".format(dst), "w")
    print "Zipping {} to {}.zip".format(src, dst)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            if VERBOSE:
                print '\tzipping {} as {}'.format(os.path.join(dirname, filename), arcname)
            zf.write(absname, arcname)
    zf.close()

if __name__ == '__main__':
    repo_url = sys.argv[1] if len(sys.argv) > 1 else config_attr('REPOSITORY_URL')
    if not repo_url:
        raise RuntimeError("Must provide a repository URL")

    repo_name = repo_url.split('/')[-1].split('.')[0]
    repo_dir = clone_repo(config_attr('GIT_CMD') or "/usr/bin/git", repo_url)

    subdir_name = ''
    if not os.path.isfile(os.path.join(repo_dir, 'manifest.json')):
        subdir_name = raw_input("Enter directory name to package: ")
    flag_file = os.path.join(repo_dir, subdir_name, 'manifest.json')
    if not os.path.isfile(flag_file):
        raise RuntimeError("Could not find {}; aborting".format(flag_file))

    output_dir = config_attr('OUTPUT_DIR') or os.getcwd()
    zip_file(os.path.join(repo_dir, subdir_name), os.path.join(output_dir, repo_name))

    try:
        shutil.rmtree(repo_dir)
    except WindowsError:
        print "Unable to remove temp directory {}".format(repo_dir)