from tqdm import tqdm
import time
import random

"""
测试文件
"""
print(time.time())

id = str(time.time())
print(id)


print(str(random.randint(1, 100000000)) + str(time.time()).split(".")[1].strip())
