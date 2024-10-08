from flask import Flask, request, jsonify, render_template, session
from openai import OpenAI
####님아 이거 OPENAI 부르는 변수가 client임 그리고 밑줄 indy 불러오는 변수도 client그래서 겹칠거임
from indy_utils import indydcp_client as client
from indy_utils.indy_program_maker import JsonProgramComponent
    
import json
import threading
from time import sleep

import random

import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'worldcoin'  # 안전한 방식으로 시크릿 키 생성

############################## Database ##############################

object = {'사과':'A1_point', '일자 드라이버':'A2_point', '십자 드라이버':'A3_point'} # 물체 위치
empty_space = { # 빈 공간
    'A구역':[],
    'B구역':['B1_point', 'B2_point', 'B3_point'],
    'C구역':['C1_point', 'C2_point', 'C3_point'],
    'D구역':['D1_point', 'D2_point', 'D3_point']
}
coordinate = { # 좌표
    'A1_point' : [0.32330491015684665, -0.38516933935970177-0.1, 0.5963410135877879, 0.6072558201308853, -179.65762323742186, 0.23112312512849534],
    'B1_point' : [0.3232633009302702, 0.014763603588633295-0.1, 0.5963698945196607, 0.6080781294125118, -179.6616462395533, 0.224564545080794],
    'C1_point' : [0.45327059164574024, -0.18519738259145058-0.1, 0.5963772082243386, 0.6076548882427718, -179.66383284573266, 0.22876034164273226], # 미완
    'D1_point' : [0.5832683231757283, 0.014748593474563282-0.1, 0.5963415258302244, 0.6079806728648356, -179.65794963509427, 0.2228538311511681],
    'A2_point' : [0.32330491015684665, -0.38516933935970177, 0.5963410135877879, 0.6072558201308853, -179.65762323742186, 0.23112312512849534],
    'B2_point' : [0.3232633009302702, 0.014763603588633295, 0.5963698945196607, 0.6080781294125118, -179.6616462395533, 0.224564545080794],
    'C2_point' : [0.45327059164574024, -0.18519738259145058, 0.5963772082243386, 0.6076548882427718, -179.66383284573266, 0.22876034164273226], # 미완
    'D2_point' : [0.5832683231757283, 0.014748593474563282, 0.5963415258302244, 0.6079806728648356, -179.65794963509427, 0.2228538311511681],
    'A3_point' : [0.32330491015684665, -0.38516933935970177+0.1, 0.5963410135877879, 0.6072558201308853, -179.65762323742186, 0.23112312512849534],
    'B3_point' : [0.3232633009302702, 0.014763603588633295+0.1, 0.5963698945196607, 0.6080781294125118, -179.6616462395533, 0.224564545080794],
    'C3_point' : [0.45327059164574024, -0.18519738259145058+0.1, 0.5963772082243386, 0.6076548882427718, -179.66383284573266, 0.22876034164273226], # 미완
    'D3_point' : [0.5832683231757283, 0.014748593474563282+0.1, 0.5963415258302244, 0.6079806728648356, -179.65794963509427, 0.2228538311511681]
}

obj_dest = {
    'A구역':['사과', '일자 드라이버', '십자 드라이버'],
    'B구역':[],
    'C구역':[],
    'D구역':[]
}

############################## MOVEMENT FUNCTION ##############################

def letsMove(result_dict):

    ############################## INDYDCP CREATE ############################## 
    
    # Set robot (server) IP 
    robot_ip = "192.168.0.145"  # Robot (Indy) IP
    
    # Set robot name
    name = "NRMK-Indy7"  # Robot name (Indy7)
    # name = "NRMK-IndyRP2"  # Robot name (IndyRP2)
    
    # Create class object
    indy = client.IndyDCPClient(robot_ip, name)

    print(result_dict['출발지'] + '에서 ' + result_dict['목적지'] + '으로 ' + result_dict['물체'] + '을/를 옮기겠습니다.')
    
    endtool_type = 0

    start_point = object[result_dict['물체']]
    dest_point = random.choice(empty_space[result_dict['목적지']])

    start = coordinate[start_point]
    dest = coordinate[dest_point]

    # 로봇팔 이동
    indy.connect()
    
    indy.go_home()
    
    status = indy.get_robot_status()
    t_pos = indy.get_task_pos()
    print(t_pos)
    
    if status['ready'] == 1:
        # 출발지
        indy.task_move_to(start)
        indy.wait_for_move_finish()
        start[2] -= 0.14
        indy.task_move_to(start)
        indy.wait_for_move_finish()

        indy.set_endtool_do(endtool_type, 0)  # val: 0(off), 1(on)
        sleep(1)

        start[2] += 0.14
        indy.task_move_to(start)
        indy.wait_for_move_finish()
        
        # 목적지
        indy.task_move_to(dest)
        indy.wait_for_move_finish()
        dest[2] -= 0.14
        indy.task_move_to(dest)
        indy.wait_for_move_finish()

        indy.set_endtool_do(endtool_type, 1)  # val: 0(off), 1(on)
        sleep(1)

        dest[2] += 0.14
        indy.task_move_to(dest)
        indy.wait_for_move_finish()
        indy.go_home()
        
    #indy disconnect
    indy.disconnect()

    return [start_point, dest_point]


# 로봇팔 작동에 필요한 데이터 초기화
obj_dest = {
    'A구역': '사과',
    'B구역': '일자 드라이버',
    'C구역': '십자 드라이버',
    'D구역': 'X'
}

client_gpt = OpenAI()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():


    ###이게 원래 의도 코드임 우리가 지피터 엥꼬나서 직접 운전한다고 꺼놓은거임

    user_content = request.json['message']
    if 'messages' not in session:
        session['messages'] = [
            {"role": "system", "content": f"너는 공손한 Pick&Place 로봇팔이고, 너의 앞에는 {str(obj_dest)}이 있어."},
            {"role": "system", "content": "사용자의 명령 속에서 모호한 부분을 너의 앞에 있는 '목적지:물체'를 확인해서 질문을 통해 구체화 해야 돼."},
            {"role": "system", "content": "모호한 부분을 구체화 시켰을 때 너의 앞에 있기에 실행 가능하다면, result: {출발지:?,목적지:?,물체:?}만을 출력해줘야 해."},
            {"role": "system", "content": "모호한 부분을 구체화 시켰을 때 실행 불가능하다면, result: '실행 불가능'만을 출력해줘."}
        ]

    messages = session['messages']
    messages.append({"role": "user", "content": user_content})
    session['messages'] = messages  # 세션 업데이트

    completion = client_gpt.chat.completions.create(model="gpt-4", messages=messages)
    assistant_content = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_content})
    session['messages'] = messages  # 세션 업데이트



    '''
    ###이게 직접 야옹 한거임. 이 부분의 원본이 아래쪽 주석처리된 부분임
    test="result: {'출발지':'A구역','목적지':'D구역','물체':'사과'}"
    print("1")
    if test.startswith('result: '):
        result = test[len('result: '):]
        if not result.startswith('실행 불가능'):
            result_dict = eval(result)
            print("2")
            update = letsMove(result_dict)
            object[result_dict['물체']] = update[1]
            empty_space[result_dict['출발지']].append(update[0])
            empty_space[result_dict['목적지']].remove(update[1])
            obj_dest[result_dict['출발지']].remove(result_dict['물체'])
            obj_dest[result_dict['목적지']].append(result_dict['물체'])
            print(object)
            print(empty_space)

    return jsonify({"GPT": test})
    '''

    if assistant_content.startswith('result: '):
        result = assistant_content[len('result: '):]
        if not result.startswith('실행 불가능'):
            result_dict = eval(result)
            update = letsMove(result_dict)
            
            # object[result_dict['물체']] = update[1]
            # empty_space[result_dict['출발지']].append(update[0])
            # empty_space[result_dict['목적지']].remove(update[1])
            # obj_dest[result_dict['출발지']].remove(result_dict['물체'])
            # obj_dest[result_dict['목적지']].append(result_dict['물체'])
            print(object)
            print(empty_space)

    return jsonify({"GPT": assistant_content})

if __name__ == '__main__':
    app.run(debug=True)
