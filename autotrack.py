#! /usr/bin/python
import subprocess
import datetime
import os

quiet_mins = 5

now = datetime.datetime.today()
quiet_period = datetime.timedelta(minutes=quiet_mins)



def _run(*args):
    output = subprocess.Popen(args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,).communicate()[0]
    return output

def _check_time(filename):
    if not os.path.exists(filename):
        return True #removed files are READY!
    last_mod = os.path.getmtime(filename)
    pending_mod = datetime.datetime.fromtimestamp(last_mod)
    pending_mod += quiet_period
    return pending_mod < now

status = _run("git", "status", "-uall", "--porcelain")
add_list = []
commit_list = []
for each in status.splitlines():
    x, y , filename = each[0], each[1], each[3:]
    
    ready = _check_time(filename)
    if ready:
        if x+y == "??":
            add_list.append(filename)
        elif x+y == " M" or x+y == "A " or x+y == " D":
            commit_list.append(filename)
        else:
            print "Unknown status "+x+y + "  for file "+filename

if(add_list):
    _run("git", "add", *add_list)
commit_list.extend(add_list)
if(commit_list):
    _run("git", "commit", "-m", "autocommited", *commit_list)

