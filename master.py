import os
import multiprocessing
import glob
import subprocess

NUM_PROCESSES = 20
NUMBERS_FOLDER = "group1"
SCRIPT_NAME = "otp_sender.py"

def load_keys():
    keys_path = os.path.join(NUMBERS_FOLDER, "captcha_keys.txt")
    if not os.path.exists(keys_path):
        raise FileNotFoundError("captcha_keys.txt not found in group1")
    with open(keys_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def run_process(numbers_file, captcha_key):
    env = os.environ.copy()
    env["CAPTCHA_KEY"] = captcha_key
    print(f"[MASTER] Starting process for {numbers_file} with key {captcha_key}")
    subprocess.run(["python3", SCRIPT_NAME, numbers_file], env=env)

def worker_task(file_queue, captcha_keys):
    key_index = 0
    while not file_queue.empty():
        try:
            numbers_file = file_queue.get_nowait()
        except:
            break
        captcha_key = captcha_keys[key_index % len(captcha_keys)]
        key_index += 1
        run_process(numbers_file, captcha_key)

def main():
    captcha_keys = load_keys()
    number_files = sorted(glob.glob(os.path.join(NUMBERS_FOLDER, "*.txt")))
    number_files = [f for f in number_files if "numbers" in os.path.basename(f)]

    if not number_files:
        print("[MASTER] No number files found!")
        return

    file_queue = multiprocessing.Queue()
    for file in number_files:
        file_queue.put(file)

    processes = []
    for _ in range(NUM_PROCESSES):
        p = multiprocessing.Process(target=worker_task, args=(file_queue, captcha_keys))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
