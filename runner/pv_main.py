
import os
import time
def run_main():
	print("ciao")

if __name__ == "__main__":
	#run_main()
	print("qua")
	os.system("run_meter.py &")
	time.sleep(5)
	print("la")
	os.system("run_PV_simulator.py &")
	print("nein")