# 官方资料入口

检查日期：2026-09-17。以下用于查找资料，不代表本仓库采用了网页上的最新版本。设备到位后必须选择与实际 CANN/芯片匹配的文档和样例。

1. [CANN 官方文档入口](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920beta2/index/index.html)：本次可读取的版本入口，包含安装、Ascend C、API 和工具分类。按设备选择版本；不默认安装 beta。
2. [CANN samples](https://atomgit.com/cann/cann-samples)：由上述官方入口链接到的样例仓库，用于定位匹配版本的算子示例。
3. [Ascend/samples](https://github.com/Ascend/samples)：历史样例资料和版本匹配说明。各样例支持的产品与版本不同，不能因为仓库能打开就认为适用于目标设备。

阅读顺序：编程模型与硬件抽象→Add 样例的 Host/Kernel/Tiling→搬运与向量 API→归约/Softmax 相关 API→性能调优工具。

每次读样例记录：URL、commit/tag、CANN 版本、芯片支持、入口文件、编译命令、运行命令、预期结果。目录和网页可能迁移，本次部分旧路径返回 404 或非预期正文，因此不把未经核实的深层路径作为构建依据。

资料阅读任务：在周报中用自己的话回答“shape 在哪里变成 Tiling 参数”“谁分配 Local Memory”“队列/事件解决哪种依赖”“示例是否只支持整除长度”。资料引用与运行验证分别记录。
