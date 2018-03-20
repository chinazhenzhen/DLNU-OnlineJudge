import time
import subprocess
import psutil
import os

class MyConfig():
    """
    配置文件
    """
    dir_work = "./"

    ans_in_file = "./ans.in"

    ans_out_file = "./ans.out"
    user_out_file = "./user.out"




def compile(language):
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
    p = subprocess.Popen(build_cmd[language], shell=True, cwd=MyConfig.dir_work, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)  # cwd设置工作目录
    out, err = p.communicate()  # 获取编译错误信息
    if p.returncode == 0:  # 返回值为0,编译成功
        return True
    # update_compile_info(solution_id,err+out) #编译失败，更新题目编译错误信息
    print(err, out)
    return False


def judge_result():
    '''对输出数据进行评测'''
    currect_result = os.path.join(MyConfig.ans_out_file)
    user_result = os.path.join(MyConfig.user_out_file)
    try:
        curr = open(currect_result).read().replace('\r','').rstrip()#删除\r,删除行末的空格和换行
        #print(curr) #debug
        user = open(user_result).read().replace('\r','').rstrip()  #python2中使用file函数
        #print(user) #debug
    except:
        return False
    if curr == user:       #完全相同:AC
        return "Accepted"
    if curr.split() == user.split(): #除去空格,tab,换行相同:PE
        return "Presentation Error"
    if curr in user:  #输出多了
        return "Output limit"
    return "Wrong Answer"  #其他WA



def time_mem(language):
    """
    执行程序获取执行时间与内存
    """
    fin = open(MyConfig.ans_in_file, "r+")
    fout = open(MyConfig.user_out_file, "w+")

    p_cmd = {  # 运行程序的命令,这里以C++、C语言为例
        "gcc": "./main",
        "g++": "./main",
    }

    time_limit = 1  #second
    mem_limit = 128 * 1024 #kb
    max_rss = 0
    problem_info = {} #时间单位ms 内存单位kb
    p = subprocess.Popen(p_cmd[language],shell=True,cwd=MyConfig.dir_work, stdin=fin, stdout=fout,
                         stderr=subprocess.PIPE)  # cwd设置工作目录
    start = time.time()  #开始时间
    print("程序开始运行的时间是%s" % start)
    pid = p.pid
    glan = psutil.Process(pid) #监听控制进程

    while True:
        time_now = time.time() - start  # ??
        if psutil.pid_exists(pid) is False:   #运行错误
            problem_info['time'] = time_now*1000
            problem_info['memory'] = max_rss/1024.0
            problem_info['result'] = "Runtime Error"
            return problem_info
        m_infor = glan.memory_info()
        #print(m_infor) #debug
        rss = m_infor[0] #获取程序占用内存空间 rss
        if p.poll() == 0:  #运行正常结束，跳出循环，继续判断
            end = time.time()
            break
        if max_rss < rss:
            max_rss = rss
            #print("max_rss=%s" % max_rss)  #debug
        if time_now > time_limit:  #时间超限
            problem_info['time'] = time_now*1000
            problem_info['memory'] = max_rss/1024.0
            problem_info['result'] = "Time Limit Exceeded"
            glan.terminate()
            return problem_info
        if max_rss > mem_limit: #内存超限
            problem_info['time'] = time_now*1000
            problem_info['memory'] = max_rss/1024.0
            problem_info['result'] = "Memery Limit Exceeded"

    problem_info['time'] = time_now*1000
    problem_info['memory'] = max_rss/1024.0
    problem_info['result'] = judge_result()
    return problem_info


if __name__ == '__main__':
    language = input("输入编译环境")
    if compile(language):
        judge_code = time_mem(language)
        print(judge_code)
    else:
        print("compile failed")