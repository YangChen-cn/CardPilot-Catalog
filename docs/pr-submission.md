# Catalog PR 提交注意事项

更新：2026-10-27。适用于银行、产品、活动、卡面、Logo、Schema 和校验器的修改。

## 提交前先确认

- 从最新 `main` 开始，复用已有银行、产品、活动 ID。不同等级或用户版本是不同产品；不要按名称合并。
- 先看当前 `docs/catalog.json`、`docs/schema.json` 和 App 的实际解码类型。**JSON 语法正确、Schema 文件通过审阅，都不等于客户端能读取。** 本仓库校验器只覆盖显式检查的约束，不代表已完整执行 JSON Schema。
- 涉及字段类型、必填项、枚举或新增协议字段时，同时检查 CardPilot 的 `RemoteCatalogDocument`、`CatalogCard`、`CatalogRule`、`WelcomePlan`、`RuleExtras` 和 `CatalogImporter`。不要为通过一次 PR 随意放宽约束；兼容性应通过客户端定向测试确认。
- 只使用公开官方资料，保留官方来源及真正核实日期。不要把活动宣传标题、核实日期或个人推测写成规则事实。

## 常见字段错误

| 字段 | 正确写法 | 易错写法／注意事项 |
| --- | --- | --- |
| `merchantKeywords` | `"HKT,The Club,csl,1O1O"` | **不是** `["HKT", "The Club"]`。当前 Swift 类型是 `String?`；数组会使整份快照解码失败。 |
| `searchTerms`、`ruleIDs`、`applicationChannels` | 字符串数组 | 不要与 `merchantKeywords` 混用类型。 |
| `logo`、`artwork` | `{ "path": "images/...png", "sha256": "真实哈希", "contentType": "image/png" }` | 没有文件时不得造路径、占位哈希；`null` 只适用于已经支持可选图片的客户端。Schema 允许 null 不代表所有旧版 App 支持。 |
| `sourceURL` | 可核实的 HTTPS 官方链接 | 不使用搜索结果页、带凭据 URL 或第三方宣传替代官方条款。 |
| `startsOn`、`endsOn` | `"2026-10-01"` 或未知时 `null` | 不填中文日期、时间戳、空字符串或猜测日期。 |
| `verifiedOn` | 实际核实日 | 不能代替活动生效日期或个人消费期。 |
| `products[].usageGuide` | 可选对象，省略或 `null` 表示未提供 | 见[推荐用法接口](usage-guide.md)。不放到 `catalog.rules`；`relatedOfferIDs` 仅引用同产品活动/迎新计划；旧客户端会拒绝此新字段，即使为 `null`。当前唯一用户已明确无需旧版兼容；本轮验证当前客户端即可。 |
| `group` | `daily` / `limited` / `merchant` / `welcome` | 显式填写，不依赖活动标题猜分组。 |
| `kind`（活动） | `cashback` / `welcome` | 不随意增加客户端不认识的值。 |
| `paymentMethod` 及相关数组 | 校验器列出的 canonical 值 | 云闪付相关统一用 `UnionPay`；不能用 `UnionPay App`。Google Pay 等尚无 canonical 值的条件写入自然语言说明，不能擅造枚举。 |
| `ratePercent` | `1.5` 表示 1.5% | 不填 `"1.5%"` 或 `0.015`；“最高”必须保留条件，不能当普通消费无条件比例。 |
| `capHKD` / `capPeriod` | 金额数字及 `monthly` / `campaign` | 每月、整期、每人、共享额度不同；混合积分和现金上限不能随意换算为一个保证回赠值。 |
| 布尔值 | `true` / `false` | 不填 `"true"`、`0`、`1`。 |

2026-10-27 的实际教训：Schema 曾把 `merchantKeywords` 写成数组，与已发布客户端的字符串类型不一致；原校验器也未检查该类型。新卡一项写错就可能使全部银行资料无法更新。本轮已对齐 Schema、校验器和数据，并加入负向回归测试。

## 活动内容

- 基础权益、限时活动、指定商户、迎新分别维护，避免把额外回赠当总回赠、把最高比例当通用比例。
- 记录消费门槛、排除类别、登记要求、适用支付方式、上限和有效期。难以表达的条件写自然语言，不为了展示而扩展精确奖励计算。
- 迎新申请期与个人消费期分开；互斥方案的银行条件可说明，但不阻止用户手动记录个人状态。
- 已结束活动保留真实日期，不改成新一期；延期或新批次按已有稳定 ID 约定处理。
- 未确认的事实保持未知，不能默认 0% 手续费、1:1 汇率、Apple Pay 或合资格。
- 推荐用法属于 agent 编辑建议，必须记录真实 `reviewedOn`、相关活动 ID 和官方来源；上限及“刷多少可停”写清币种、周期、共享范围与推导前提，不生成个人额度追踪或精确结算模型。未填写时省略字段，不能发布虚构模板。

## 图片与 Logo

- 卡面固定为 **1200×756**；银行 Logo 不要求此比例。图片边长不超过 2400px、文件不超过 4MB。
- 优先官方公开单卡素材。裁掉外部透明／白色空白，保持卡面完整，不把宣传页、手机截图或多卡拼图直接当产品卡面。
- 没有合适横版时，生成横版示意须有用户授权；参考官方图核对银行、卡组织和等级，按用户2026-10-29自用约定，只在素材文档保留生成示意来源和提示词，不在产品说明及App界面显示卡面制作标注。
- 不提交姓名、卡号／尾号、有效期、CVV 或其他个人字段，包括未经处理的示例个人字段。个人卡面不进入公开 Catalog。
- 不用 AI 生成替代真实银行 Logo。可按官方 SVG 路径栅格化，再去元数据重编码。
- 在素材文档记录官方产品页、原始资源 URL、获取日期、处理方式；生成图另记录工具和提示词。图片变更同步更新引用和真实 SHA-256。

```sh
python3 scripts/catalog_asset.py /path/to/prepared-card.png docs/images/cards/example-card.png
```

该工具负责去元数据和重编码，**不会替你把任意图片自动变成 1200×756**。运行前应准备好固定画布的图片。把输出的相对路径、哈希和类型写入对应产品；从仓库根目录运行，避免把本机绝对路径或 `build/...` 写进 JSON。

## 必做验证

从 Catalog 仓库根目录运行：

```sh
git fetch origin
git show origin/main:docs/catalog.json > /tmp/cardpilot-catalog-base.json
python3 scripts/test_validate_catalog.py
python3 scripts/validate_catalog.py docs/catalog.json --base /tmp/cardpilot-catalog-base.json
git diff --check
```

每次发布文档内容或图片时提高 `contentVersion`，相同版本不能悄悄更换正文。`publishedAt` 写真实发布日期。PR 中同时列明银行数、产品数和新增 ID；检查旧产品没有意外删除、活动没有无关改动。

首次新增产品、改字段类型／必填项或准备合并可能影响解码的资料时，在 CardPilot 主仓库继续验证（不改真实账本）：

```sh
python3 script/import_catalog_snapshot.py --source build/CardPilot-Catalog/docs
./script/test.sh -quiet \
  -only-testing:CardPilotTests/BankLibraryTests \
  -only-testing:CardPilotTests/CatalogV2Tests
```

上例默认 Catalog checkout 位于 App 的 `build/CardPilot-Catalog`，其他位置请替换路径。按实际快照更新测试中的银行／产品数量，不能删掉解码和离线图片断言以逃避失败。Mac 测试使用项目现有独立 DerivedData 和维护者自己的签名身份；不要重签用户运行中的 App。

小型素材变更不需要重复全量测试或 UI 自动化；字段／存储协议大改按主项目规则扩大验证范围。报告区分目录校验、客户端解码测试、构建、启动和用户 UI 验收。

## PR 与合并发布

1. 先暂存、提交、推送到功能分支，确认 PR 确实已经创建。只有远端分支不等于已有 PR。
2. 描述最终内容：新增产品、素材来源、生成示意、兼容边界和实际验证结果。删掉已失效的“图片待补”“必须先合并另一个 PR”等说明。
3. 等**当前 head SHA** 的 CI 通过；旧提交的绿色检查不能代替最新版本。草稿完成后再标记 ready；按已获授权合并，避免合并到检查后意外移动的 head。
4. 等 Pages 部署完成，再读取线上 `catalog.json` 检查版本、数量及本轮新图片的字节哈希。合并成功不等于线上已经发布。
5. 按需要同步 App 内置离线快照；只更新只读资源，不覆盖持卡人、账本、偏好、同步目录或钥匙串。
6. 更新项目交接记录，写明提交／PR、版本、真实验证结果及仍待用户确认的事项，不记入私人数据。
