# Package Chrome Extension

Python script to download (from git repository) and package a Chrome extension for upload on the developer dashboard.

## Usage

> $ python package.py [extension repository URL]

## Configuration

Create a file named `_config.py` in the same directory as `package.py`.  This may contain any of the following parameters:

* VERBOSE (default `False`): if `True`, will print each file added to ZIP archive.
* GIT_CMD (default `'/usr/bin/git'`): the full path to the `git` executable on your system.
* OUTPUT_DIR (defaults to current directory): where you want the archive to be created.
* REPOSITORY_URL (no default): URL of a repository to pull.  If not provided in config file, must be provided on command line.  Command line argument overrides config argument.

## Notes

* If your repository URL's protocol is HTTPS, you will be asked for a username and password for the repository.
* If your `manifest.json` file is not in the root directory of the repository, the script will prompt you for the subdirectory name you wish to package.  If this does not contain `manifest.json` the script will exit with a `RuntimeError`.