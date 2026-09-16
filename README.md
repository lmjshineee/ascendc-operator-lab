# Ascend C 高性能算子开发与优化研究

以 **Add + 行级 Softmax** 为两条主线，先建立可解释、可复现的正确性基准，再完成 Ascend C 实现和性能优化。

**当前阶段：初始学习仓库。用户暂时没有昇腾设备，先在 macOS 本机学习。**
本机练习使用 Python 标准库（3.11+），无需下载依赖。设备侧 Host / Kernel / Tiling 是带 TODO 的开发位置，尚不能编译或运行。CPU 数学模型不模拟 AI Core 指令、队列和时序，不能作为 NPU 性能证据。

## 1. 从这里开始

在本仓库根目录执行：

```bash
python3 scripts/doctor.py
python3 run.py test 01
# 初始状态会报 NotImplementedError；完成 exercises/01_golden/problem/ops.py 后重试。
python3 run.py test 02
python3 run.py test 03
python3 run.py demo
```

卡住后再看相应 `solution/`。可用以下命令确认学习包本身可用：

```bash
python3 run.py test all --solution
python3 run.py demo --solution
```

参考答案通过不代表个人练习完成。`demo` 会串联分块、模拟搬运、计算与数学基准比较，不产生 NPU 跑分。

## 2. 阅读顺序

1. [任务清单](TODO.md)：逐项勾选，并填写证据路径。
2. [学习计划](docs/LEARNING_PLAN.md)：本机 4 周 + 有设备后 4 周，每周建议 6–8 小时。
3. [环境准备](docs/ENVIRONMENT.md)：本机与昇腾服务器的职责、版本记录、排错。
4. [原理与项目结构](docs/ARCHITECTURE.md)：公式、内存、Tiling、流水线。
5. [算子契约与验收](docs/ACCEPTANCE.md)：输入约束、测试矩阵、题目要求映射。
6. [性能实验设计](docs/BENCHMARK.md)：基线、同步、统计和消融实验。
7. [资料入口](docs/RESOURCES.md)：官方文档与样例的使用方法。

## 3. 目录

```text
exercises/01_golden/     数学基准：Add、稳定 Softmax
exercises/02_tiling/     核间切分、核内分块、尾部覆盖
exercises/03_pipeline/   集成：分块 Add、按行 Softmax 模拟
operators/add/          Ascend C Add 开发位置和任务说明
operators/softmax/      Ascend C Softmax 开发位置和任务说明
tests/                  三组本机学习测试
scripts/doctor.py        环境只读检查
scripts/npu.sh          设备工作流待接入入口（未接入时明确失败）
configs/                测试形状、版本记录模板
benchmarks/             设备实验记录格式
reports/                周报、实验报告、初始化验证记录
```

## 4. 交付目标

- 两个算子均有自定义实现、正确性测试、编译和运行入口。
- 至少四项环节有代码和运行证据；本项目计划覆盖 Host 注册、Kernel、Tiling、内存搬运、向量化、多核并行六项。
- 两个算子均与同设备基础实现或 CANN 内置实现对比；至少一项优化有修改前后及适用范围说明。
- 初始仓库不承诺比内置算子快。失败的优化实验也必须保留，但最终优化成果应有可复现的有效条件。

无设备阶段完成到本机 M3 即可；NPU 编译、注册、数值精度、内存安全、性能数据仍需真实环境验证。进度以 [TODO](TODO.md) 和 [验证记录](reports/INITIAL_VERIFICATION.md) 为准。
