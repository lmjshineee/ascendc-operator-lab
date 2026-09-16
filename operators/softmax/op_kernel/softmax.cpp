// 行级 Softmax Kernel 开发位置，不是已经验证的 Ascend C 代码。
// TODO: 按匹配 SDK 添加头文件、设备入口、初始化、队列/事件和内存声明。
// TODO: 按核分配整行；max -> sub -> exp -> sum -> div；搬出结果。
// TODO: 核实 FP32 中间归约与 scratch；处理尾行/尾列；超行宽拒绝。
#error "TODO: implement Ascend C kernel on the selected target"
