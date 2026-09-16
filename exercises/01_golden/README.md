# 01 数学基准：先确定“算对”是什么意思

目标：独立完成 `problem/ops.py` 的 Add 与稳定 Softmax。输入是 Python 数值列表，类型转换不在本题范围内；NaN/Inf、形状不符必须抛 ValueError。

1. 先手算 `add([1,-2],[3,4])` 与 `softmax([[0,0],[1000,1001]])`。
2. 执行根目录命令 `python3 run.py test 01`，定位 TODO。
3. 实现后再跑测试，补一条不同于已有用例的边界案例。

提示：Softmax 对每行减去同一个最大值再 exp；sum 的归约范围是整行。空 batch 返回 []，含空行或行长不一致要报错。不要修改输入。

自问：直接 exp(1000) 为什么可能失败？输出和为 1 能否单独证明结果正确？Python float 通过为什么还要测试 FP16？

卡住再看 `solution/ops.py`；验证答案用 `python3 run.py test 01 --solution`。
