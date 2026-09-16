// Add Kernel 开发位置，不是已经验证的 Ascend C 代码。
// TODO: 按匹配 SDK 添加头文件、设备入口、初始化、队列/事件和内存声明。
// TODO: 按核索引定位区间；CopyIn 搬入 x/y；向量 Add；CopyOut 写回。
// TODO: 检查尾部有效长度和对齐；先单缓冲，再验证双缓冲同步。
#error "TODO: implement Ascend C kernel on the selected target"
