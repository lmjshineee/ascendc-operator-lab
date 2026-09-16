# 环境准备与迁移

## 1. 本机现在要做的事

Python 3.11+、Git 即可启动本机学习；不需要安装 PyTorch、torch_npu 或 CANN。当前验证环境见 `reports/INITIAL_VERIFICATION.md`。

```bash
python3 scripts/doctor.py
python3 run.py test all --solution
python3 run.py demo --solution
```

可选虚拟环境：`python3 -m venv .venv`，然后 `source .venv/bin/activate`。此阶段没有第三方依赖，也不会用本机 CPU 时间代表 NPU 性能。

## 2. 拿到昇腾服务器后的顺序

1. 向提供方确认访问方式、芯片完整型号、可用 AI Core 数、OS/架构、驱动与固件、CANN 与配套开发组件、设备使用权限。不凭芯片系列名推断每个 API 都可用。
2. 根据该硬件的官方支持矩阵选择软件组合，固定实际版本。复制 `configs/environment.example.json` 为仓库根目录 `environment.local.json` 并填写。这个文件默认被 Git 忽略；提交脱敏版本到报告目录作为复现证据。
3. 运行 `npu-smi info`；按该版本文档加载实际 `set_env.sh`。常见安装路径不作为默认真值；保留实际路径和命令。版本字段必须来自安装记录或命令输出，不根据目录名猜测。
4. 选取同版本官方 Ascend C Add 样例，固定样例 commit，先独立编译运行。把调用方式、生成工程方式、编译工具与目标 SoC 参数写进报告。
5. 以样例的工程文件为基础接入本项目的 Host/Kernel/Tiling；保留借用代码的许可证与来源。补齐 `scripts/npu.sh` 和构建文件，再替换明确的 TODO 阻断点。
6. 执行注册/调用 smoke test、完整精度测试，最后才执行性能测试。

先学官方 Kernel 直调样例有助于理解执行流程，最终计划采用能提供 Host 注册证据的自定义算子工程。若选择其他工程路径，验收映射必须据实调整；一个 kernel 源文件不代表注册成功。

`scripts/npu.sh build|install|test|bench` 当前一律非零退出并解释缺项。没有设备/版本信息时，不拼接一条声称通用的 msOpGen、编译或注册命令。

## 3. 排错记录：位置 → 原因 → 修复 → 验证

| 位置 / 症状 | 优先排查 | 修复方向 | 验证 |
|---|---|---|---|
| 本机练习 NotImplementedError | 对应 problem 中 TODO 未写 | 完成本阶段题目，不改测试绕过 | 运行该组 problem 测试 |
| NPU 不可见 | 设备分配、驱动、权限或容器透传 | 使用提供方支持的环境配置 | `npu-smi info` + 官方样例 |
| 编译缺头文件/工具 | SDK 环境未加载或版本不匹配 | 核对真实安装路径及样例要求 | 干净构建官方样例 |
| 注册成功但无法调用 | 算子包路径、schema、调用签名 | 核对生成工程的部署与调用流程 | 最小 Add 一次调用 |
| 大 shape 出错或越界 | Tiling 覆盖、长度单位、尾部、UB | 单核小输入定位，再加入边界 | 固定种子复现 + 工具支持时内存检查 |
| 精度错误 | dtype 转换、归约范围、同步、尾块无效值 | 小矩阵逐阶段比较 | 元素比较 + Softmax 行和 |
| 测速异常快/波动 | 异步未完成、首次编译、共用卡 | 正确同步、预热、记录设备负载 | 多组独立重复 |

不在共享服务器上擅自替换驱动/固件；若环境已由学校维护，优先匹配已有版本。
