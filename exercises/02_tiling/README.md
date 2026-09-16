# 02 分核、分块和尾部

目标：完成 `problem/tiling.py`，把 N 个逻辑工作项均衡分给 cores，再在每核范围内分 tile。返回 `(core,start,end)` 列表，区间为左闭右开。

1. 手画 N=17、cores=4、tile=3。先分核，各核元素数最多相差 1，再切 tile。
2. 根目录执行 `python3 run.py test 02`，实现函数并新增边界测试。
3. 解释 n=0、n<cores、tile>n 的行为，保证没有空 tile。

提示：先用商和余数决定每核长度；start 由前面核已经领取的数量决定。测试要求每个元素恰好出现一次，不能用重复覆盖后相同数值碰巧正确来蒙混过关。

自问：为什么不能每核都从 0 开始？这里的 tile 是有效元素数还是分配容量？转到真实设备后还缺哪些对齐与内存约束？

答案：`solution/tiling.py`；验证答案：`python3 run.py test 02 --solution`。
