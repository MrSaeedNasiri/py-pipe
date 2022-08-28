from time import sleep
import subprocess
import shlex

project_repo = "CHANGE_ME"
project_dir = "/CHANGE/ME"


# def clone():
#     subprocess.run(["git","clone",project_repo], cwd="/home/ubuntu/")


def pull():
    subprocess.run(shlex.split("git pull"), cwd=project_dir)


def local_commit():
    return (
        subprocess.run(
            shlex.split("git rev-parse main"), cwd=project_dir, capture_output=True
        )
        .stdout.decode("utf-8")
        .rstrip()
    )


def remote_commit():
    ps = subprocess.Popen(
        ["git", "ls-remote", project_repo, "refs/heads/main"],
        cwd=project_dir,
        stdout=subprocess.PIPE,
    )
    output = (
        subprocess.check_output(["cut", "-f", "1"], stdin=ps.stdout)
        .decode("utf-8")
        .rstrip()
    )
    ps.wait()
    return output


while True:
    print("job is runing")
    if local_commit() != remote_commit():
        try:
            # TODO: kill started Popen processes
            subprocess.run(
                shlex.split("killall node"), cwd=project_dir, capture_output=True
            )
            print("current app killed")
        except:
            print("nothing for kill")
        pull()
        subprocess.run(shlex.split("yarn"), cwd=project_dir, capture_output=True)
        print("installed")
        subprocess.run(
            shlex.split("yarn build:prod"), cwd=project_dir, capture_output=True
        )
        print("builded")
        subprocess.Popen(shlex.split("yarn start:prod"), cwd=project_dir)
        print("started")
    print("nothing to do")
    sleep(60)
