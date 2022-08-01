''' room status case 
최초 room 생성시 : running
한명/두명 연결 되어 있을 때 : running
한명이 창을 닫거나, 두명이 창을 닫으면 : stop => 메시지 보내기 가능 
한명이 삭제를 했음 : pending => 추가 메시지 보내기는 안되고 읽기만 가능한 상태.
두명이 삭제를 했음 : 현재 상태가 pending일 떄 remove 요청시 삭제
'''
STATUS_CHOICE = (
    ("running", "Running"),
    ("pending", "Pending"),
    ("stop", "Stop"),
)

ROOM_STATUS_RUNNING = 'running'
ROOM_STATUS_PENDING = 'pending'
ROOM_STATUS_STOP = 'stop'
