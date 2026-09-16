# 03 集成：模拟搬运、计算、写回

完成 `problem/pipeline.py`。测试会提供已验证的 partition 作为依赖，以独立检查本题；根目录 demo 则串联你选择的 problem 或 solution 的三组实现。

1. 先实现 tiled_add：按区间复制 x/y 到局部列表、相加、写回全局输出。
2. 再实现 row_softmax：分配的是整行，归约范围不能变成每个列 tile。
3. 运行 `python3 run.py test 03`，再运行 `python3 run.py test all` 和 `python3 run.py demo`。

不变量：输入不修改；每个结果位置被正确覆盖；Softmax 每行独立、非负且行和约为 1。相同输出之外，还需阅读/解释分块与拷贝过程。

自问：这个 Python 循环中搬运和计算会真正并行吗？两个 buffer 本身能保证硬件流水化吗？将一行分成两个独立 Softmax 会丢失什么统计量？

答案：`solution/pipeline.py`；验证答案：`python3 run.py test 03 --solution`。
