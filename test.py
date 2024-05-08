from tqdm import tqdm
import time

global_progress_bar = tqdm(total=7, desc="progress", unit="page", colour='GREEN')

for i in range(8):
    time.sleep(0.1)
    global_progress_bar.update(round(1/7,2))
global_progress_bar.close()