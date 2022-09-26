import time
import threading
import random
from to_class.get_cam_num import camera_num
states = []
# "temp : {1}\nvolt1 : {2}\nvolt2 : {3}\nvolt : {0}\nvolt : {0}\nvolt : {0}\nvolt : {0}\nvolt : {0}\nvolt : {0}\nvolt : {0}\nvolt : {0}\nvolt : {0}\n")

values = []

temp_outputs = []
volt1_outputs = []
volt2_outputs = []
volt3_outputs = []
current_outputs = []

class Worker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.temp = []
        self.volt1 = []
        self.volt2 = []
        self.volt3 = []
        self.current = []

    def run(self):
        global values
        global temp_outputs
        global volt1_outputs
        global volt2_outputs
        global volt3_outputs
        global current_outputs

        while True:
            # print("prevalues : ", values)

            time.sleep(2)
            self.temp = []
            self.volt1 = []
            self.volt2 = []
            self.volt3 = []
            self.current = []
            states = []
            temp_list = [random.randint(0,34) for i in range(camera_num)] # 16은 카메라 개수
            volt1_list = [random.randint(0, 34) for i in range(camera_num)]
            volt2_list = [random.randint(0, 34) for i in range(camera_num)]
            volt3_list = [random.randint(16, 34) for i in range(camera_num)]
            current_list = [random.randint(16, 34) for i in range(camera_num)]
            for i in range(camera_num):
                self.temp.append(temp_list[i])
                self.volt1.append(volt1_list[i])
                self.volt2.append(volt2_list[i])
                self.volt3.append(volt3_list[i])
                self.current.append(current_list[i])
                states.append(
                    "temp : {temp}\nvolt1 : {volt1}\nvolt2 : {volt2}\nvolt3 : {volt3}\ncurrent : {current}\nhi\nbye\nnew\nln1\nln2\nln3\nln4\nln5\n\n\n".format(
                        temp=self.temp[i], volt1=self.volt1[i], volt2=self.volt2[i], volt3=self.volt3[i],
                        current=self.current[i]))
                values = states
            # print("states" ,states)

            temp_outputs = self.temp
            volt1_outputs = self.volt1
            volt2_outputs = self.volt2
            volt3_outputs = self.volt3
            current_outputs = self.current
            # print("values : ", values)

print("main thread start")
t = Worker()                # sub thread 생성
t.start()                       # sub thread의 run 메서드를 호출

print("main thread end")
