## 修改内容

说明新增／更新的银行、产品、活动或素材，以及 contentVersion。

## 来源与素材

列出官方来源；若使用生成横版示意，明确说明并链接素材记录。

## 提交前检查

- [ ] 已阅读 [PR 提交注意事项](https://github.com/YangChen-cn/CardPilot-Catalog/blob/main/docs/pr-submission.md)。
- [ ] 稳定 ID、字段类型／枚举与当前客户端一致；merchantKeywords 为逗号分隔字符串。
- [ ] 日期、门槛、上限、登记与排除条件可核实，未知资料保持未知。
- [ ] 卡面 1200×756，图片／Logo 引用、SHA-256、contentType 对应真实文件，无个人字段。
- [ ] contentVersion 已递增；没有意外删除旧资料或改变无关活动。
- [ ] 已运行目录回归测试、validator（与 main 比较）和 git diff --check。
- [ ] 若改动可能影响客户端解码，已运行主 App 资料库／Catalog 定向测试；空图有明确客户端兼容边界。

## 实际验证结果

写出实际执行的命令与结果；未执行的检查不要勾选或声称通过。构建／启动不等于用户 UI 验收。
