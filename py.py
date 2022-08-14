import time
from threading import Thread

def some_func(i,dest):
    print(f"i is ",i," and dest is ",dest)
    # simulating complicated calculation
    time.sleep(10)
    print(f"going to append",i,"dest is ",dest," before appending")
    dest.append(i)
    print(f"going to append",i,"dest is ",dest," after appending")
    return dest

for i in range(1,3):
    arr = []
    for i in range(1,5):
        t = Thread(target=some_func,args=(i,arr))
        t.start()
    print(f"arr from the ",i,"th loop is ",arr)    