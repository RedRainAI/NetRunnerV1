import multiprocessing
import os
import sys

def run_script(script_name):
    os.system(f"python {script_name}")

if __name__ == "__main__":
    # Check if the scripts exist in the current directory
    if not os.path.isfile('Test1.py') or not os.path.isfile('test2.py'):
        print("The required scripts Test1.py and test2.py are not in the current directory.")
        sys.exit(1)

    # Create two processes
    process1 = multiprocessing.Process(target=run_script, args=('Test1.py',))
    process2 = multiprocessing.Process(target=run_script, args=('test2.py',))

    # Start the processes
    process1.start()
    process2.start()

    # Wait for both scripts to finish
    process1.join()
    process2.join()
