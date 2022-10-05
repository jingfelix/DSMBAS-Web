from time import sleep
import requests
import secret
import os
import func_timeout


def mainloop():

    while True:
        try:
            response = requests.get(
                "http://192.168.56.1:5000/e/gettask",
                data={
                    "key": secret.SECERT_KEY,
                },
            )

            status = response.json().get("status", None)
            id = response.json().get("task", None)
            print(status, id)
            if status == None or id == None:
                sleep(5)
                continue
            try:
                
                response = requests.get(
                    "http://192.168.56.1:5000/e/download",
                    data={
                        "key": secret.SECERT_KEY,
                        "task": id,
                    },
                )
                print(response.status_code)
                if response.status_code != 200:
                    sleep(5)
                    continue
                else:
                    with open(os.path.join(secret.SAVE_PATH, str(id)) + ".exe", "wb") as f:
                        f.write(response.content)
            except Exception as e:
                requests.get(
                    "http://192.168.56.1:5000/e/errortask",
                    data={
                        "key": secret.SECERT_KEY,
                        "task": id,
                        "error": str(e),
                    },
                )
                sleep(5)
                continue

            # 执行注入
            # 考虑记录log的方式
            # 注意执行的路径
            try:
                run(id)
            except func_timeout.exceptions.FunfTimeoutOut:
                raise Exception("timeout")

            # 清理文件
            for file in os.listdir(secret.SAVE_PATH):
                os.remove(os.path.join(secret.SAVE_PATH, file))
        except Exception as e:
            requests.get(f"http://192.168.56.1:5000/e/endtask?id={str(id)}")
            print(e)
            sleep(5)
            continue
        pass


@func_timeout.func_set_timeout(60)
def run(id):
    try:
        cmd = (f" .\\Injector.exe .\\download\\{str(id)}.exe")
        os.popen(cmd)
        
    except Exception as e:
        # 这里用来处理执行失败的情况
        # 需要发送endtask给后端，并标记报错
        requests.get(f"http://192.168.56.1:5000/e/endtask?id={str(id)}&error=1")
        print(e)


if __name__ == "__main__":
    mainloop()
