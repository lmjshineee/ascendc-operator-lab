# 项目协作约定

- 默认中文；这是无设备起步的 Ascend C 学习仓库。
- 用户练习位于 exercises/*/problem；未明确要求时不要替用户填完全部答案。答案单独放 solution。
- 核心算子是 Add 和行级 Softmax；先正确性，后性能，每次优化保留基线。
- 当前 NPU 文件是 TODO 骨架，禁止把 CPU 模拟、静态检查或答案通过描述成设备验收。
- 接入 CANN 前先记录硬件和软件版本，采用匹配版本官方工程，避免猜测 SDK API。
- 本机验证：python3 run.py test all --solution；python3 run.py demo --solution。
- 初始 problem 测试失败是预期；不要删测试或伪造输出让它通过。
- 修改完成后报告改动、验证范围和未验证边界；不自动发布远程仓库或写入凭据。
