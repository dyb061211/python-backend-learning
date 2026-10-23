import time
from datetime import datetime

def sync_request(request_id):
    print('request_id:', request_id)
    print("start:",datetime.now())
    time.sleep(2)
    print("end:",datetime.now())



if __name__=='__main__':
    start=time.perf_counter()
    sync_request(1)
    sync_request(2)
    sync_request(3)
    elapsed=time.perf_counter()-start
    print("total_time:",elapsed)