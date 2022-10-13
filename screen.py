import subprocess
import shlex
from subprocess import Popen
import os
import glob

NODE_SCRIPT = "run_node.sh"
FARMER_SCRIPT = "run_farmer.sh"
import time
import sys


def start_nodes_farmers(script_file, from_path, from_subfolder_from_to=None):
    if from_subfolder_from_to:
        subfolder_path = []
        for i in range(from_subfolder_from_to[0], from_subfolder_from_to[-1] + 1):
            subfolder_path.append("/sub" + str(i) + "/")
        print(subfolder_path)
    fname = []
    for root, d_names, f_names in os.walk(from_path):
        for f in f_names:
            if f.find(script_file) > -1:
                if from_subfolder_from_to and len(subfolder_path) > 0:
                    for folder in subfolder_path:
                        if root.find(folder) > -1:
                            fname.append(os.path.join(root, f))

                else:
                    fname.append(os.path.join(root, f))
    for script in fname:
        script_arr = script.split("/")
        screen_name = script_arr[2] + "_" + script_arr[-3] + "_" + script_arr[-2]
        exec_path = os.path.dirname(script)
        script_name = script.split("/")[-1]
        print("screen_name " + screen_name + ", exec_path " + exec_path + ", script_name " + script_name)
        start_script(exec_path=exec_path, script_name=script_name, screen_name=screen_name)


def start_script(exec_path, script_name, screen_name):
    cmd = "screen -dmS " + screen_name + " bash -c \"./" + script_name + "\""

    try:
        cmd_spl = shlex.split(cmd)
        print(cmd_spl)
        out, err = Popen(cmd_spl, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, cwd=exec_path).communicate()
        if out and err:
            print(out)
            print(err)

    except:
        pass


def main():
    SLEEP_TIME=10
    n = len(sys.argv)
    if n == 1:
        start_nodes_farmers(script_file=NODE_SCRIPT, from_path="/mnt/nvme1/subspace", from_subfolder_from_to=[1, 6])
        time.sleep(10)
        start_nodes_farmers(script_file=FARMER_SCRIPT, from_path="/mnt/nvme1/subspace", from_subfolder_from_to=[1, 6])
    elif n == 2:
        location = sys.argv[1]
        if str(location) == "home":
            start_nodes_farmers(script_file=NODE_SCRIPT, from_path="/home/tung/subspace", from_subfolder_from_to=[1, 5])
            time.sleep(10)
            start_nodes_farmers(script_file=FARMER_SCRIPT, from_path="/home/tung/subspace",
                                from_subfolder_from_to=[1, 5])
        else:
            path = "/mnt/" + location + "/subspace"
            start_nodes_farmers(script_file=NODE_SCRIPT, from_path=path,
                                from_subfolder_from_to=[1, 6])
            time.sleep(10)
            start_nodes_farmers(script_file=FARMER_SCRIPT, from_path=path,
                                from_subfolder_from_to=[1, 6])
    elif n == 3:
        location = sys.argv[1]
        number = (int)(sys.argv[2])
        if str(location) == "home":
            start_nodes_farmers(script_file=NODE_SCRIPT, from_path="/home/tung/subspace",
                                from_subfolder_from_to=[1, number])
            time.sleep(SLEEP_TIME)
            start_nodes_farmers(script_file=FARMER_SCRIPT, from_path="/home/tung/subspace",
                                from_subfolder_from_to=[1, number])
        else:
            path = "/mnt/" + location + "/subspace"
            start_nodes_farmers(script_file=NODE_SCRIPT, from_path=path,
                                from_subfolder_from_to=[1, number])
            time.sleep(SLEEP_TIME)
            start_nodes_farmers(script_file=FARMER_SCRIPT, from_path=path,
                                from_subfolder_from_to=[1, number])
    elif n == 4:
        location = sys.argv[1]
        number1 = (int)(sys.argv[2])
        number2 = (int)(sys.argv[3])
        if str(location) == "home":
            start_nodes_farmers(script_file=NODE_SCRIPT, from_path="/home/tung/subspace",
                                from_subfolder_from_to=[number1, number2])
            time.sleep(SLEEP_TIME)
            start_nodes_farmers(script_file=FARMER_SCRIPT, from_path="/home/tung/subspace",
                                from_subfolder_from_to=[number1, number2])
        else:
            path = "/mnt/" + location + "/subspace"
            start_nodes_farmers(script_file=NODE_SCRIPT, from_path=path,
                                from_subfolder_from_to=[number1, number2])
            time.sleep(SLEEP_TIME)
            start_nodes_farmers(script_file=FARMER_SCRIPT, from_path=path,
                                from_subfolder_from_to=[number1, number2])
    elif n == 5:
        location = sys.argv[1]
        number1 = (int)(sys.argv[2])
        number2 = (int)(sys.argv[3])
        farmer_or_node = str(sys.argv[4]).strip().lower()
        if str(location) == "home":
            if farmer_or_node == "node":
                start_nodes_farmers(script_file=NODE_SCRIPT, from_path="/home/tung/subspace",
                                from_subfolder_from_to=[number1, number2])
            else:
                start_nodes_farmers(script_file=FARMER_SCRIPT, from_path="/home/tung/subspace",
                                from_subfolder_from_to=[number1, number2])
        else:
            path = "/mnt/" + location + "/subspace"
            if farmer_or_node == "node":
                start_nodes_farmers(script_file=NODE_SCRIPT, from_path=path,
                                from_subfolder_from_to=[number1, number2])
            else:
                start_nodes_farmers(script_file=FARMER_SCRIPT, from_path=path,
                                from_subfolder_from_to=[number1, number2])



# start_nodes(from_path="/home/tung/subspace")


if __name__ == '__main__':
    main()
