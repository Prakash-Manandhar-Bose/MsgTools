#!/usr/bin/env python3
import os
import sys
import argparse
import json
import shutil
import jinja2

apppath = os.path.split(os.path.realpath(__file__))[0]

description = '''Build a base MsgTools web app.  This utility will inspect a given generated code
    directory and generate a boilerplate web app that initializes msgtools, and loads all the
    messages defined in the given message directory.  The utility also copies over the bundled
    version of msgtools.js, plotting, and ui components into your new app directory.  This
    keeps the parser Javascript templates in sync with MsgTools libraries so changes to templates
    or the libraries don't break across versions.

    Jinja2 is used to generate the final web app.  Command line arguments are provided that allow
    you to replace the default template provided by MsgTools withyour own and provide template
    arguments in the form of key/value pairs.  Required command line arguments cover template
    arguments we deem essential.  For your own templates we require:
        {{webdir}}   - a web friendly base path to generated message code
        {{messages}} - an array of messages files to load.  Autogenerated from the generated
                       code directory.
        {{appname}} - The name of the app'''


def discoverMessages(msgdir):
    '''Iterate the message directory and subdirectory to identify all .js
    files and build a list of all message "modules" within the directory

    return that list'''

    # Make sure msgdir ends with a slash to simplify things later
    if msgdir[len(msgdir) - 1] != os.sep:
        msgdir += os.sep

    messages = []
    dirs = [msgdir]
    while len(dirs) is not 0:
        currentDir = dirs.pop()
        for entry in os.listdir(currentDir):
            currentPath = os.path.join(currentDir, entry)
            if os.path.isdir(currentPath):
                dirs.append(currentPath)
            elif entry.endswith('.js'):
                # Drop the base msgdir and extension
                message = currentPath[
                    0:currentPath.rfind('.')][len(msgdir):]
                message = message.replace(os.sep, '.')
                messages.append(message)
            else:
                print('Skipping {0}; not a Javascript file'.format(
                    currentPath))

    return messages


def generateAppFile(templatepath, jinjaArgs, outputfile):
    '''Apply the template args to the template and dump the result into
    the outputfile
    templatepath should be a filepath
    jinjaArsgs should be a string to value dictionary
    outputfile should be an output filepath
    '''
    with open(templatepath, 'r') as fp:
        content = fp.read()

    template = jinja2.Template(content)
    rendering = template.render(**jinjaArgs)

    with open(outputfile, 'w') as fp:
        fp.write(rendering)


def copyFiles(srcFiles, destdir):
    for file in srcFiles:
        srcpath = os.path.join(apppath, file)
        destpath = os.path.join(destdir, file)
        shutil.copy2(srcpath, destpath)


def buildApp(htmlTemplate, jsTemplate, jinjaArgs, msgdir, outputdir):
    '''We're  just going to iterate each file in the directlry and build a message entry for it.
    Then we'll run Jinja to build a custom web app based on the messages we've processed'''

    print('Analyzing message directory...')
    jinjaArgs['messages'] = discoverMessages(msgdir)
    jinjaArgs['appjs'] = jinjaArgs['appname'].replace(' ', '_').lower() + '.js'

    print('Generating {0}...'.format(os.path.join(outputdir, 'index.html')))
    generateAppFile(htmlTemplate, jinjaArgs,
                    os.path.join(outputdir, 'index.html'))

    # Generate the app js file
    jsOutputname = os.path.join(outputdir, jinjaArgs['appjs'])
    print('Generating {0}...'.format(jsOutputname))
    generateAppFile(jsTemplate, jinjaArgs, jsOutputname)

    # Copy msgtools libraries to the output directory
    # Note that you should also add these files to setup.py: package data
    # so they are included with the pip install package.  Otherwise this 
    # call will fail...
    print('Copying library files...')
    files = ['msgtools.js']
    copyFiles(files, outputdir)

def getTemplate(templatePath, defaultTemplate):
    retVal = None
    if templatePath is None:
        retVal = os.path.join(apppath, defaultTemplate)
    elif os.path.exists(templatePath) and os.path.isfile(templatePath):
        retVal = templatePath
    else:
        print('{0} does not exist, or is a directory'.format(templatePath))
        sys.exit(1)

    return retVal

def main():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-w', '--web', dest='webdir', required=False, 
        help='The web friendly msg path inserted into the app template.  Defaults to msgdir if not specified.')
    parser.add_argument('-m', '--html', dest='htmlTemplate',
        help='Use the specified HTML template instead of the default for building the web app')
    parser.add_argument('-j', '--javascript', dest='jsTemplate',
        help='Use the specified Javascript template instead of the default')
    parser.add_argument('-t', '--templateargs', dest='templateArgs', type=str,
        help='''Arguments to pass to the template engine as a set of key/value pairs. This argument is first interpreted
                as a path to a JSON formatted file.  If it is not a valid file, then the argument is treated as a
                JSON string.  Literal JSON example: \'{"key":"value"}\' ''')
    parser.add_argument('appname', help='The name of the app.')
    parser.add_argument(
        'msgdir', help='The basepath for where generated message code is placed.  For example, obj/CodeGenerator/Javascript')
    parser.add_argument(
        'outputdir', help='The destination directory for the resulting HTML app.  Defaults to the current directory.')

    args = parser.parse_args()

    print('Preparing environment...')
    
    # Setup our templates
    htmlTemplate = getTemplate(args.htmlTemplate, 'template.html')
    jsTemplate = getTemplate(args.jsTemplate, 'template.js')

    # Setup our template arguments
    jinjaArgs = {}
    if args.templateArgs is not None:
        if os.path.exists(args.templateArgs) is True:
            if os.path.isdir(args.templateArgs):
                print('{0} is a directory.'.format(args.templateArgs))
                sys.exit(1)
            elif os.path.exists(args.templateArgs) is True:
                with open(args.templateArgs) as fp:
                    try:
                        jinjaArgs = json.load(fp)
                    except Exception as e:
                        print('{0} not valid json'.format(args.templateArgs))
                        print(e)
                        sys.exit(1)
        else:
            try:
                jinjaArgs = json.loads(args.templateArgs)
            except Exception as e:
                print('{0} not valid json'.format(args.templateArgs))
                print(e)
                sys.exit(1)

    jinjaArgs['appname'] = args.appname
    jinjaArgs['webdir'] = args.msgdir if args.webdir is None else args.webdir
    
    # Verify the message basepath exists
    if os.path.exists(args.msgdir) is False or os.path.isdir(args.msgdir) is False:
        print('{0} does not exist, or is not a directory'.format(args.msgdir))
        sys.exit(1)

    # Setup our destination dir
    if os.path.exists(args.outputdir) is False or os.path.isdir(args.outputdir) is False:
        os.mkdir(args.outputdir)
        
    buildApp(htmlTemplate, jsTemplate, jinjaArgs, args.msgdir, args.outputdir)

    print('DONE')

if __name__ == '__main__':
    main()