import multiprocessing
import subprocess
import platform
import os

#To run Jarvis
def startJarvis():
        # Code for process 1
        print("Process 1 is running.")
        from main import start
        start()

#To run hotword
def listenHotword():
        # Code for process 2
        print("Process 2 s running.")
        from engine.features import hotword
        hotword()

#start both process
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startJarvis)
        p2 = multiprocessing.Process(target=listenHotword)
        p1.start()
        
        # Detect OS and run appropriate device script
        if platform.system() == 'Windows':
                subprocess.call([r'device.bat'])
        else:  # Linux/Ubuntu
                device_script = os.path.join(os.path.dirname(__file__), 'device.sh')
                subprocess.call(['bash', device_script])
        
        p2.start()
        p1.join()

        if p2.is_alive():
                p2.terminate()
                p2.join()
        
        print("system stop")
    
    