import random
import pandas as pd
import numpy as np

eff_case1 = 0.64*1.21/1.9   #对照组1：文学少女の普攻
eff_case2 = 0.64*1.08/1.9   #对照组2：jk少女の普攻
eff_case3 = 0.64*1.34/1.9   #对照组3：办公室女郎の技能
eff_case4 = 0.744/1.9       #对照组4：地质专家の普攻
eff_case5 = 0.744/1.4       #对照组5：地质专家の技能
eff_case6 = 0.8             #对照组6：满额停顿效果
eff_case7 = 0.54            #对照组7：时天使领域
eff_case8 = 0.8/3           #对照组8：小企鹅的常态控制
eff_case9 = 2.5/3           #对照组9：小企鹅的冰结领域

eff_case = eff_case7        #选择参考的对照组
n = 1000000                 #测试次数
l_path = 10                 #设置敌人行进的距离，单位米，1格=2米
v_emeny = 1.4               #设置敌人行进的速度，单位米/秒
atk_speed_add = 100         #设置技能开启后增加的攻速（1攻速=1%基础）
t_skill = 30                #设置技能持续时间
atk_speed_normal = 108      #设置图内攻速，即包含加速力场buff下的攻速
atk_time_default = 1.3      #设置默认攻击间隔


s = []                      #样本集
atk_time_normal = atk_time_default*100/atk_speed_normal                 #图内基础攻击间隔
atk_time_skill = atk_time_default*100/(atk_speed_normal+atk_speed_add)  #技能持续时间内攻击间隔
c_skill = t_skill//atk_time_skill + 1                                   #技能持续时间内攻击次数
better = 0                  #优化计数器
for i in range(n):
    m = 0           #初始化攻击次数
    t_sluggish = 0  #初始化停顿持续时间
    t_stun = 0      #初始化眩晕持续时间
    distance = 0    #初始化敌人移动距离
    dis_old = 0     #初始化参考移动距离
    atk_time_real = atk_time_skill  #初始化攻击间隔为技能释放时攻击间隔
    while distance < l_path:
        m = m + 1
        dis_move = 0                        #初始化当前行动周期的移动距离
        if m >= c_skill:
            atk_time_real = atk_time_normal #当攻击次数超过技能持续时间时，攻击间隔变更为图内基础攻击间隔
        type_eff = random.randint(1,4)      #抽取天赋效果
        if type_eff == 3:                    #抽到停顿
            t_sluggish = 1.4                #重置停顿持续时间
        if type_eff == 4:                    #抽到眩晕
            t_stun = 1                      #重置眩晕持续时间
            t_sluggish = 0                  #如果眩晕与停顿重合，眩晕状态覆盖停顿状态
        if (t_sluggish==0)and(t_stun==0):   #如果当前眩晕与停顿时间均为0
            dis_move = atk_time_real*v_emeny#敌人原速前进
        if t_sluggish > atk_time_real:      #如果当前停顿时间比攻击间隔长
            dis_move = 0.2*atk_time_real*v_emeny    #当前攻击间隔的移动距离为停顿状态
            t_sluggish = t_sluggish - atk_time_real #停顿时间消耗掉一个攻击间隔
        elif t_sluggish > 0:                #如果当前存在停顿时间但不满一次攻击间隔
            dis_move = 0.2*t_sluggish*v_emeny + (atk_time_real-t_sluggish)*v_emeny  #行走完剩余停顿时间，接着以常速行进
            t_sluggish = 0                  #停顿时间清零
        if t_stun > atk_time_real:          #如果当前眩晕时间比攻击间隔长
            dis_move = 0                    #敌人不行动
            t_stun = t_stun - atk_time_real #眩晕时间消耗掉一个攻击间隔
        elif t_stun > 0:                    #如果当前存在眩晕时间但不满一次攻击间隔
            dis_move = (atk_time_real-t_stun)*v_emeny   #眩晕期间不行动，剩余时间原速行进
            t_stun = 0                      #眩晕时间清零
        distance = distance + dis_move      #计算敌人行进情况
        dis_old = dis_old + atk_time_real*v_emeny
        #eff = 1-(distance/dis_old)          #调试用，计算减速效果
        #print(m,type_eff,distance,eff)      #调试用语句
    eff_final = 1-(distance/dis_old)            #计算最终减速效果
    if  eff_final > eff_case:
        better = better + 1                 #统计优于参考减速的情况
    s.append(eff_final)                     #添加减速效果至样本中

res=pd.value_counts(s)                  #统计每个抽数出现的次数
print("E = ", np.mean(s))               #打印期望
print("ES = ",np.std(s))                #打印标准差
print(better/n)                         #打印比参考减速标准强的频率
#print(np.sum(res[:case])/n)             #比参考减速标准弱的频率

        