
import subprocess
import time
import atexit
import signal

# Global variables for the subprocesses
api_process = None
main_process = None

def cleanup_processes():
    # Terminate the processes gracefully when the script exits
    if api_process:
        api_process.terminate()
    if main_process:
        main_process.terminate()

# Register the cleanup_processes function to be called on script exit
atexit.register(cleanup_processes)

try:
    # Start the API project in a separate process
    api_process = subprocess.Popen(["python", "api_project.py"])

    # Wait for a few seconds to allow the API to start (you can adjust the duration if needed)
    time.sleep(5)

    # Start the main website in another process
    main_process = subprocess.Popen(["python", "main.py"])

    # Wait for both processes to finish (this will keep the script running)
    api_process.wait()
    main_process.wait()

except KeyboardInterrupt:
    # If a KeyboardInterrupt (e.g., Ctrl+C) is received, cleanup the processes before exiting
    cleanup_processes()

# import subprocess
# import time
# import atexit
# import signal
#
# def cleanup_processes():
#     # Terminate the processes gracefully when the script exits
#     api_process.terminate()
#     main_process.terminate()
#
# # Register the cleanup_processes function to be called on script exit
# atexit.register(cleanup_processes)
#
# # Start the API project in a separate process
# api_process = subprocess.Popen(["python", "api_project.py"])
#
# # Wait for a few seconds to allow the API to start (you can adjust the duration if needed)
# time.sleep(5)
#
# # Start the main website in another process
# main_process = subprocess.Popen(["python", "main.py"])
#
# # Wait for both processes to finish (this will keep the script running)
# api_process.wait()
# main_process.wait()
#




# import subprocess
# import time
# import signal
# import os
#
# # Start the API project in a separate process
# api_process = subprocess.Popen(["python", "api_project.py"])
#
# # Wait for a few seconds to allow the API to start (you can adjust the duration if needed)
# time.sleep(5)
#
# # Start the main website in another process
# main_process = subprocess.Popen(["python", "main.py"])
#
# # Function to handle termination of the processes
# def terminate_processes(signum, frame):
#     api_process.terminate()
#     main_process.terminate()
#     exit(0)
#
# # Register the signal handler for termination
# signal.signal(signal.SIGINT, terminate_processes)
#
# # Wait for the main website process to finish
# main_process.wait()
#
# # If the website process is closed, terminate both processes
# terminate_processes(None, None)
#
#
