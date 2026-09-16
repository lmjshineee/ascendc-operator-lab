# TODO 与验收证据

状态规则：`[x]` 只表示该事项已有证据；参考答案、个人练习和设备验收分别记录。每项完成后补充日期、命令、Git commit 与日志路径。

## M0 仓库起步（本次交付）

- [x] 本地独立 Git 仓库骨架、中文指南和题目验收映射。
- [x] 明确无昇腾设备的学习路线，默认算子 Add + 行级 Softmax。
- [x] 三组本机 TODO 练习与独立参考答案、测试、集成演示。
- [x] 设备侧开发位置、环境模板、性能记录格式、报告模板。
- [x] 本机初始化验证；详见 reports/INITIAL_VERIFICATION.md。

## M1 数学与 C/C++ 基础（本机，第 1 周）

- [ ] L01 独立完成 `exercises/01_golden/problem/ops.py`，执行 `python3 run.py test 01`。
- [ ] L02 用 `[1000,1001,1002]` 解释 Softmax 为什么减去最大值；补一个自己的边界测试。
- [ ] L03 用 C++ 写一个连续数组 Add 小程序并本机编译，解释指针、索引、字节数、元素数和越界；文件放 `work/cpp-warmup.cpp`。
- [ ] L04 解释 FP16/FP32 与 Python 浮点基准的差别，写入周报。

## M2 分块与边界（本机，第 2 周）

- [ ] L05 独立完成 `exercises/02_tiling/problem/tiling.py`，执行 `python3 run.py test 02`。
- [ ] L06 手画 N=17、cores=4、tile=3 的覆盖图；说明为什么无重叠、无遗漏。
- [ ] L07 检查 N=0、N<cores、tile>N、非法参数；补一个性质测试。
- [ ] L08 用元素数和 dtype 字节数估算 Add 的单/双缓冲内存需求，明确预留空间。

## M3 模拟集成与设计（本机，第 3–4 周）

- [ ] L09 独立完成 `exercises/03_pipeline/problem/pipeline.py`，执行 `python3 run.py test 03`。
- [ ] L10 执行 `python3 run.py test all` 与 `python3 run.py demo`，保留个人实现日志。
- [ ] L11 讲清 Softmax 的整行归约为何不能被独立的列分块归一化替代。
- [ ] L12 阅读官方编程模型与 Add 样例，画 Host→Tiling→Kernel 数据流，记录样例版本。
- [ ] L13 为 Add 和 Softmax 写支持/拒绝矩阵、精度阈值草案与至少一个负例。
- [ ] L14 写第一版实验假设：tile/core/buffer_count 改变什么、怎样控制变量。

## M4 接入设备（拿到设备后，第 1 周）

- [ ] D01 填 `configs/environment.example.json` 的副本 `environment.local.json`：芯片、OS、驱动、固件、CANN、工具链、样例 commit。
- [ ] D02 按对应版本官方说明安装或加载环境；`npu-smi info` 与官方 Add 样例通过，保存完整日志。
- [ ] D03 按选定 SDK 样例生成工程，补真实构建文件及 `scripts/npu.sh` 的 build/install/test/bench 入口。
- [ ] D04 扩展 doctor 的版本采集；做注册与调用 smoke test；形成可重复命令。

## M5 Add（拿到设备后，第 2 周）

- [ ] A01 完成 op_host/add.cpp：Host schema、shape/dtype 检查、输出推导、注册。
- [ ] A02 完成 op_host/add_tiling.h 与 tiling.cpp：元数据、UB 预算、单核/多核划分。
- [ ] A03 完成 op_kernel/add.cpp：初始化、搬入、向量加、搬出、尾部与同步。
- [ ] A04 先通过 FP32 单核基线，再加入多核和 FP16；不支持的组合明确拒绝。
- [ ] A05 验证随机、非对齐、极小、非整除形状；空输入由 Host 处理；保存正确性日志。
- [ ] A06 测单核基线与多核版本；扫 tile，尝试双缓冲，逐项消融。

## M6 Softmax（拿到设备后，第 3 周）

- [ ] S01 完成 Host 注册、二维连续输入约束、末轴推导、最大可支持行宽校验。
- [ ] S02 完成按行分配 Tiling、UB 预算、尾行处理及必要的 scratch 预算。
- [ ] S03 实现 max→减 max→exp→sum→除法；FP16 输入计划采用 FP32 中间归约，按 SDK 支持核实。
- [ ] S04 验证等值、大幅值、负值、非对齐列宽；对比基准，单独检查行和。
- [ ] S05 测行数/行宽与核数关系；对一个优化变量做消融，记录回退情形。

## M7 实验与结题（拿到设备后，第 4 周）

- [ ] R01 两个算子各自有同设备基础实现或内置算子对比，明确计时边界。
- [ ] R02 正确性先通过，再收集预热后多组计时；保留原始记录、环境和 commit。
- [ ] R03 至少一项优化有可复现改善、适用 shape、资源代价与退化边界。
- [ ] R04 填 `reports/EXPERIMENT_TEMPLATE.md`，以图表或表格说明原因，区分推测与 profiler 证据。
- [ ] R05 按 `docs/ACCEPTANCE.md` 勾选至少四项环节，准备复现脚本和 5 分钟讲解。

## 可选扩展（完成最低验收后）

- [ ] 长行多遍归约、非连续输入、动态策略表、框架接入、模型局部集成。
- [ ] 工程研究方向：为 tile/core 选择建立可解释规则，在未参与调参的形状上验证泛化。
