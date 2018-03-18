import queue
import pymysql
import time
pymysql.install_as_MySQLdb()


q = queue.Queue(20) #queue_size = 20


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



def run():
    pass