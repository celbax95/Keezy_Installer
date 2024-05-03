import os, sys, subprocess, re

fileVersion = None

with open(os.path.join(os.path.dirname(__file__), r"..\Exe\file_version_info.txt"), "r") as stream:
    for line in stream.readlines():
        fileVersionFull = re.search("filevers=\((.*)\),", line, re.IGNORECASE)
        if (fileVersionFull):
            fileVersion = fileVersionFull.group(1).split(", ")[:2]
        

if (fileVersion == None):
    print("Cannot find file version")
    sys.exit(1)

print(("Version: {}.{}".format(fileVersion[0], fileVersion[1])))
nextVersion = ""
while (not re.match("[0-9]+\.[0-9]+", nextVersion)):
    if (nextVersion != ""):
        print("Version doesnt match [1-9]+.[1-9]+\n")
    nextVersion = input("Next version : ")

nextVersion = nextVersion.split(".")

# Replace lines with version for Exe
with open(os.path.join(os.path.dirname(__file__), r"..\Exe\file_version_info.txt"), "r+") as stream:
    lines = stream.readlines()
    stream.seek(0)
    for line in lines:
        if (re.match("filevers=\((.*)\),", line, re.IGNORECASE)):
            stream.write("filevers=({}, {}, 0, 0),\n".format(nextVersion[0],nextVersion[1]))
        elif (re.match("prodvers=\((.*)\),", line, re.IGNORECASE)):
            stream.write("prodvers=({}, {}, 0, 0),\n".format(nextVersion[0], nextVersion[1]))
        elif (re.match(" *StringStruct\(u'FileVersion',(.*)'\),", line, re.IGNORECASE)):
            stream.write("    StringStruct(u'FileVersion', u'{}.{}'),\n".format(nextVersion[0],nextVersion[1]))
        elif (re.match(" *StringStruct\(u'ProductVersion',(.*)'\)", line, re.IGNORECASE)):
            stream.write("    StringStruct(u'ProductVersion', u'{}.{}')\n".format(nextVersion[0],nextVersion[1]))
        else:
            stream.write(line)

# Generate exe
if (0 != subprocess.call(['cd', os.path.join(os.path.dirname(__file__), "../Exe"), '&&', '.\createExe.cmd'], shell=True)):
    print("Error during createExe.cmd")
    sys.exit(2)

# Replace lines with version for Install
with open(os.path.join(os.path.dirname(__file__), r"..\Install\installer.iss"), "r+") as stream:
    lines = stream.readlines()
    stream.seek(0)
    for line in lines:
        if (re.match("AppVersion=.*", line, re.IGNORECASE)):
            stream.write("AppVersion={}.{}.0.0\n".format(nextVersion[0],nextVersion[1]))
        elif (re.match("VersionInfoProductName=.*", line, re.IGNORECASE)):
            stream.write("VersionInfoProductName=\"{}.{}\"\n".format(nextVersion[0],nextVersion[1]))
        elif (re.match(";AppVerName=Keezy .*", line, re.IGNORECASE)):
            stream.write(";AppVerName=Keezy {}.{}\n".format(nextVersion[0],nextVersion[1]))
        else:
            stream.write(line)

if (0 != subprocess.call(['cd', os.path.join(os.path.dirname(__file__), "../Install"), '&&', '.\createInstaller.cmd'], shell=True)):
    print("Error during createInstaller.cmd")
    sys.exit(3)

# Copy setup.exe
if (os.system("copy /Y "
          + os.path.join(os.path.dirname(__file__), r"..\Install\Keezy_setup.exe")
          + " " + os.path.dirname(__file__))):
    print("Error during copy Keezy_setup.exe")
    sys.exit(1)

# Git

print()

publish = ""
while (not re.match("y|n", publish)):
    publish = input("Publish ? [y/n] : ")

if (publish == "y"):
    os.system("cd " + os.path.dirname(__file__) + " && git add Keezy_setup.exe && git commit -m \"Maj {}.{}\"".format(nextVersion[0],nextVersion[1]))
    os.system("cd " + os.path.dirname(__file__) + " && git push origin main")
    os.system("cd " + os.path.join(os.path.dirname(__file__), "..")
              + " && git add *Keezy_setup.exe *installer.iss *Keezy.exe *file_version_info.txt && git commit -m \"Maj {}.{}\"".format(
              nextVersion[0],nextVersion[1]))
    os.system("cd " + os.path.join(os.path.dirname(__file__), "..") + " && git push origin main")
