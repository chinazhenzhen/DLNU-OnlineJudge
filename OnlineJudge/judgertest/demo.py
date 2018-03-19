import queue
import time
import threading
import subprocess
import os
import pymysql
pymysql.install_as_MySQLdb()


q = queue.Queue(20) #queue_size = 20

dblock = threading.Lock()#创建数据库进程锁，保证同一个时间只能一个程序写进数据库


def run_sql(sql):
    """
    进行连接数据库等操作
    :return:
    """
    con = None
    while True:
        try:
            con = pymysql.connect(host='127.0.0.1',port=3306,user="root",password="123456",db = "test")
            break

        except:
            print('cannot connect to databases')

    cur = con.cursor()



def put_task_into_queue():
    """
    循环扫描素和据库，将任务添加到队列
    :return:
    """
    while True:
        q.join()#阻塞程序，一直到队列里面的任务全部完成
        sql = "#####"
        data = run_sql(sql)
        for i in data:
            solution_id = i["solution_id"]
            problem_id = i["user_id"]

            task={
                "solution_id":solution_id,
                "problem_id":problem_id
            }
            q.put(task)#将任务写入队列

    time.sleep(1)


#队列中获取任务，然后完成任务
def worker():
    while True:
        #获取队列中的任务
        task = q.get()
        #获取题目信息
        solution_id = task['solution_id']
        problem_id = task['problem_id']

        #评测
        result = run(solution_id,problem_id)

        #将结果写入数据库


        #标记一个任务完成
        q.task_done()


def start_work_thread():
    '''
    开启工作线程
    :return:
    '''
    for i in range(10): #config.count_thread  这里的数字要做出相应的改变
        t = threading.Thread(target=worker)
        t.daemon = True  #当主进程退出的时候，评测进程也会跟着退出，不在后台继续进行
        t.start()

#编译
def compile(solution_id,language):
    build_cmd = {
        "gcc": "gcc main.c -o main -Wall -lm -O2 -std=c99 --static -DONLINE_JUDGE",
        "g++": "g++ main.cpp -O2 -Wall -lm --static -DONLINE_JUDGE -o main",
        "java": "javac Main.java",
        "ruby": "ruby -c main.rb",
        "perl": "perl -c main.pl",
        "pascal": 'fpc main.pas -O2 -Co -Ct -Ci',
        "go": '/opt/golang/bin/go build -ldflags "-s -w"  main.go',
        "lua": 'luac -o main main.lua',
        "python2": 'python2 -m py_compile main.py',
        "python3": 'python3 -m py_compile main.py',
        "haskell": "ghc -o main main.hs",
    }
    p = subprocess.Popen(build_cmd[language],shell=True,cwd=dir_work,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = p.communicate()#获取编译错误信息
    if p.returncode == 0: #返回值为0,编译成功
        return True
    dblock.acquire() # ???
    update_compile_info(solution_id,err+out) #编译失败，更新题目编译错误信息
    dblock.release()#???
    return False


#判断结果
def judge_result(problem_id,solution_id,data_num):
    '''对输出数据进行评测'''
    currect_result = os.path.join(config.data_dir,str(problem_id),'data%s.out'%data_num)
    user_result = os.path.join(config.work_dir,str(solution_id),'out%s.txt'%data_num)
    try:
        curr = file(currect_result).read().replace('\r','').rstrip()#删除\r,删除行末的空格和换行
        user = file(user_result).read().replace('\r','').rstrip()
    except:
        return False
    if curr == user:       #完全相同:AC
        return "Accepted"
    if curr.split() == user.split(): #除去空格,tab,换行相同:PE
        return "Presentation Error"
    if curr in user:  #输出多了
        return "Output limit"
    return "Wrong Answer"  #其他WA

def get_max_mem(pid):
    '''获取进程号为pid的程序的最大内存'''
    glan = psutil.Process(pid)
    max = 0
    while True:
        try:
            rss,vms = glan.get_memory_info()
            if rss > max:
                max = rss
        except:
            print("max rss = %s"%max)
            return max



#工作函数
def run(problem_id,solution_id,language,data_count,user_id):
    '''获取程序执行时间和内存'''
    time_limit = (time_limit+10)/1000.0
    mem_limit = mem_limit * 1024
    max_rss = 0
    max_vms = 0
    total_time = 0
    for i in range(data_count):
        '''依次测试各组测试数据'''
        args = shlex.split(cmd)
        p = subprocess.Popen(args,env={"PATH":"/nonexistent"},cwd=work_dir,stdout=output_data,stdin=input_data,stderr=run_err_data)
        start = time.time()
        pid = p.pid
        glan = psutil.Process(pid)
        while True:
            time_to_now = time.time()-start + total_time
            if psutil.pid_exists(pid) is False:
                program_info['take_time'] = time_to_now*1000
                program_info['take_memory'] = max_rss/1024.0
                program_info['result'] = result_code["Runtime Error"]
                return program_info
            rss,vms = glan.get_memory_info()
            if p.poll() == 0:
                end = time.time()
                break
            if max_rss < rss:
                max_rss = rss
                print 'max_rss=%s'%max_rss
            if max_vms < vms:
                max_vms = vms
            if time_to_now > time_limit:
                program_info['take_time'] = time_to_now*1000
                program_info['take_memory'] = max_rss/1024.0
                program_info['result'] = result_code["Time Limit Exceeded"]
                glan.terminate()
                return program_info
            if max_rss > mem_limit:
                program_info['take_time'] = time_to_now*1000
                program_info['take_memory'] = max_rss/1024.0
                program_info['result'] =result_code["Memory Limit Exceeded"]
                glan.terminate()
                return program_info

        logging.debug("max_rss = %s"%max_rss)
#        print "max_rss=",max_rss
        logging.debug("max_vms = %s"%max_vms)
#        logging.debug("take time = %s"%(end - start))
    program_info['take_time'] = total_time*1000
    program_info['take_memory'] = max_rss/1024.0
    program_info['result'] = result_code[program_info['result']]
    return program_info
