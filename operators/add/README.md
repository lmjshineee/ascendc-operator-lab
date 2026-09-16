# Add 设备开发任务

状态：未实现、未编译、未注册、未运行。这里的 `#error` 用来防止骨架被误判为可用实现。

1. 先读根目录 `docs/ACCEPTANCE.md` 中输入契约，保存匹配 CANN 的官方样例 commit。
2. 从官方工程补齐构建配置、调用程序和设备测试；不能只删除 `#error`。
3. 按 Host → Tiling → Kernel 顺序填写各文件，先通过最小单核例子。
4. 将根目录 `configs/cases.json` 中适用的候选输入接到真实 NPU runner，补拒绝测试。
5. 保留基础实现 commit，再优化 tile/核数/缓冲；每次先精度再计时。

关联 TODO：A01–A06。设备参考答案暂不提供，因为芯片、CANN 和工程版本尚未确定；本机数学/分块答案位于 `exercises/`，不替代设备实现。
