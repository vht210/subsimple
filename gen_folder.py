import os
from subprocess import Popen
import subprocess
import socket
import shutil
import traceback
from urllib.request import urlopen

HOST_PREFIX = "tb210"
TMP_NODE_CMD0 = "./subspace-node  --chain  gemini-2a --base-path ../chain --execution wasm  --state-pruning archive --validator --name  <NAME_ID>"
TMP_FARMER_CMD0 = "./subspace-farmer --farm hdd=../data,ssd=../meta,size=100G farm  --reward-address  <REWARD_ADDR>"
TMP_NODE_CMD1 = "./subspace-node  --chain  gemini-2a --base-path ../chain --execution wasm  --state-pruning archive --validator --name  <NAME_ID>  --reserved-nodes /ip4/127.0.0.1/tcp/30333/p2p/<NODE_ID>  --ws-port <WS_PORT> --rpc-port <RPC_PORT> --port <PORT>"
TMP_NODE_CMD1_NO_RESERVE = "./subspace-node  --chain  gemini-2a --base-path ../chain --execution wasm  --state-pruning archive --validator --name  <NAME_ID>  --ws-port <WS_PORT> --rpc-port <RPC_PORT> --port <PORT>"
TMP_FARMER_CMD1 = "./subspace-farmer  --farm hdd=../data,ssd=../meta,size=100G farm  --reward-address  <REWARD_ADDR> --node-rpc-url ws://127.0.0.1:<RPC_PORT> --ws-server-listen-addr 0.0.0.0:<WS_PORT>"

WS_PORT_START = 11000
RPC_PORT_START = 15000
PORT_START = 30334
FIRST_NODE = True

GITHUB_LOC = "https://github.com/subspace/subspace/releases"
NODE_FILE = "https://github.com/subspace/subspace/releases/download/gemini-2a-2022-sep-10/subspace-node-ubuntu-x86_64-gemini-2a-2022-sep-10"
FARMER_FILE = "https://github.com/subspace/subspace/releases/download/gemini-2a-2022-sep-10/subspace-farmer-ubuntu-x86_64-gemini-2a-2022-sep-10"

FARMER_RUN_FILE = "subspace-farmer"
NODE_RUN_FILE = "subspace-node"

def get_home():
    return os.path.expanduser('~')


def get_ip():
    return socket.gethostbyname_ex(socket.gethostname())[-1][0]


def get_last_2digit_ip():
    return str(get_ip()).split(".")[-2] + "_" + str(get_ip()).split(".")[-1]


def get_host_name():
    return socket.gethostname()


def get_arr_addrs(file_addr="addr.txt"):
    if os.path.exists(file_addr):
        with open(file_addr, "r") as f:
            addrs = [line.rstrip() for line in f]
    return addrs


def download_file(url):
    print("Downloading from " + url)
    file_name = url.split("/")[-1]
    shorter_filename = file_name.split("-")[0] + "-" + file_name.split("-")[1]
    if os.path.exists(shorter_filename):
        print(shorter_filename + " already exists! Nothing need to be done")
    else:
        with urlopen(url) as webpage:
            content = webpage.read()
        with open(shorter_filename, 'wb') as download:
            download.write(content)
        change_permission_file(shorter_filename)




def create_node_farmer_script(reward_address="dummy"):
    name_id = HOST_PREFIX + "_" + get_host_name().replace("tung", "").replace("-", "") + "_" + reward_address[-4:]
    node_script_name = "run_node.sh"
    farmer_script_name = "run_farmer.sh"
    # last_4digit_reward_addr = reward_address[-4:]
    global FIRST_NODE
    global WS_PORT_START
    global RPC_PORT_START
    global PORT_START
    # if os.path.exists(node_script_name):
    #    print("remove " + node_script_name)
    #    os.remove(node_script_name)
    if FIRST_NODE:
        with open(node_script_name, "w") as f:
            print("Write first node")
            f.write(TMP_NODE_CMD0.replace("<NAME_ID>", name_id))
        with open(farmer_script_name, "w") as f:
            f.write(TMP_FARMER_CMD0.replace("<REWARD_ADDR>", reward_address))
        FIRST_NODE = False
    else:

        with open(node_script_name, "w") as f:
            f.write(TMP_NODE_CMD1_NO_RESERVE.replace("<NAME_ID>", name_id).replace("<WS_PORT>", str(WS_PORT_START)) \
                    .replace("<RPC_PORT>", str(RPC_PORT_START)).replace("<PORT>", str(PORT_START)))
        with open(farmer_script_name, "w") as f:
            f.write(TMP_FARMER_CMD1.replace("<REWARD_ADDR>", reward_address).replace("<WS_PORT>", str(RPC_PORT_START)) \
                    .replace("<RPC_PORT>", str(WS_PORT_START)))

        WS_PORT_START = WS_PORT_START + 1
        RPC_PORT_START = RPC_PORT_START + 1
        PORT_START = PORT_START + 1

    change_permission_file(node_script_name)
    change_permission_file(farmer_script_name)
    return node_script_name, farmer_script_name


def create_farmer_script():
    pass


def change_permission_file(path):
    try:
        # print("Change file permission " + str(path))
        if os.path.exists(path):
            out, err = Popen(["sudo", "chmod", "+x", path], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE).communicate()
            if out and err:
                print(out)
                print(err)
        else:
            print(path + " not existed!")
    except:
        pass

def change_owner(path,owner="tung"):
    try:
        # print("Change file permission " + str(path))
        if os.path.exists(path):
            out, err = Popen(["sudo", "chown", "-R", owner, path], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE).communicate()
            if out and err:
                print(out)
                print(err)
        else:
            print(path + " not existed!")
    except:
        pass
def copy_file(src, destination):
    try:
        print("copy " + src + " to " + destination)
        shutil.copy2(src, destination)
    except:
        print("Exception happened")
        traceback.print_exc()


def create_folder(path):
    try:
        # print("Create folder " + str(path))
        if not os.path.exists(path):
            out, err = Popen(["sudo", "mkdir", path], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE).communicate()
            if out and err:
                print(out)
                print(err)
            change_owner(path)
        else:
            pass
            # print(path + " already existed!")
    except:
        pass


def create_scripts_at_location(reward_addrs, arr_location=["/home/tung", "/mnt/nvme1"], arr_number_folder=[5, 6]):
    counter = 0
    for location, val_number in zip(arr_location, arr_number_folder):
        if counter > len(reward_addrs):
            print("Reward address less then number of script. Exiting")
            return

        sub_path = os.path.join(location, "subspace")
        if not os.path.exists(sub_path):
            create_folder(sub_path)
        for i in range(1, val_number + 1):
            reward_address = reward_addrs[counter]
            subsub_path = os.path.join(sub_path, "sub" + str(i))
            create_folder(subsub_path)
            subsub_path_chain = os.path.join(subsub_path, "chain")
            create_folder(subsub_path_chain)
            subsub_path_node = os.path.join(subsub_path, "node")
            create_folder(subsub_path_node)
            subsub_path_farmer = os.path.join(subsub_path, "farmer")
            create_folder(subsub_path_farmer)
            subsub_path_data = os.path.join(subsub_path, "data")
            create_folder(subsub_path_data)
            subsub_path_meta = os.path.join(subsub_path, "meta")
            create_folder(subsub_path_meta)

            # Create script

            node_script_file, farmer_script_file = create_node_farmer_script(reward_address=reward_address)
            copy_file(node_script_file, subsub_path_node)
            if os.path.exists(NODE_RUN_FILE):
                copy_file(NODE_RUN_FILE,subsub_path_node)

            copy_file(farmer_script_file, subsub_path_farmer)
            if os.path.exists(FARMER_RUN_FILE):
                copy_file(FARMER_RUN_FILE,subsub_path_farmer)
            counter = counter + 1



def main():
    #print(get_home())
    download_file(NODE_FILE)
    download_file(FARMER_FILE)
    reward_address = get_arr_addrs()
    create_scripts_at_location(reward_addrs=reward_address)

if __name__ == '__main__':
    main()
