import pynput
from pynput.keyboard import Key, Controller

# 키 입력 이벤트를 처리하는 핸들러 함수
def on_key_input(key):
    # 키 입력 처리 코드
    print(key)

# 서비스의 시작 함수
def on_start():
    # 키 입력 이벤트 핸들러 등록
    keyboard = Controller()
    keyboard.on_press(on_key_input)

# 서비스의 이벤트 처리 함수
def on_event(event):
    # 키 입력 이벤트 처리
    print("키 입력 이벤트 수신")

if __name__ == "__main__":
    # 서비스 등록
    from win32serviceutil import RegisterServiceCtrlHandlerEx
    from win32service import Service

    class MyService(Service):
        def __init__(self, name, description):
            super().__init__(name, description)

        def on_start(self):
            on_start()

        def on_stop(self):
            pass

    service_name = "pynput_service"
    service_description = "pynput service"
    RegisterServiceCtrlHandlerEx(service_name, on_event, None)
    MyService(service_name, service_description).start()