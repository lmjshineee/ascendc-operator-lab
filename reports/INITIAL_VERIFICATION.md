# 初始化验证记录

日期：2026-09-17。阶段：M0 初始仓库。环境：Darwin arm64、Python 3.14.7、Git 2.55.0；未找到 npu-smi，用户确认当前无设备。

| 检查 | 命令 | 实际结果 |
|---|---|---|
| 数学/分块/集成参考答案 | `python3 run.py test all --solution` | 14 个测试通过，含 128 组边界分块组合及 60 组固定种子组合 |
| 本机端到端演示 | `python3 run.py demo --solution` | Add 8 个、Softmax 4 个形状通过；对所选数学基准 max abs error 均为 0 |
| 环境诊断 | `python3 scripts/doctor.py` | Python 可用；NPU validation 明确为 not_performed |
| 三组题目状态 | `python3 run.py test 01`（以及 02、03） | 均按预期因 TODO / NotImplementedError 非零退出 |
| 未完成集成 | `python3 run.py demo` | 按预期被 TODO 阻断 |
| NPU 脚本语法 | `bash -n scripts/npu.sh` | 通过 |
| NPU 占位入口 | `bash scripts/npu.sh build`（以及 install、test、bench） | 均以退出码 2 提示未接入，没有假成功 |
| Python / JSON | AST 解析 / JSON 解析 | 通过 |
| Markdown 本地链接 | 文件目标存在性检查 | 通过；不代表所有外部网页可用 |

原始输出保存在 [initial-logs](initial-logs/) 中。个人练习尚未完成；以上正确结果来自参考答案。Python 数学模拟没有验证 FP16/FP32 硬件舍入、CANN API、设备编译、注册、执行、内存安全、异步同步或性能。

设备文件含有显式 `#error`，尚未编译。不把“骨架创建”和“算子实现完成”混为一谈。仓库没有记录任何 NPU 时延或加速比。
