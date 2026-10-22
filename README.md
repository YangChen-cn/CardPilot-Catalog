# CardPilot 官方银行卡资料库

这是 CardPilot App 的公开静态资料源，只包含银行官方产品、权益与活动资料。App 通过 GitHub Pages 读取经过校验的版本化 JSON，不需要重新安装即可获得新增或修订的活动。

- 资料地址：<https://yangchen-cn.github.io/CardPilot-Catalog/catalog.json>
- App：<https://github.com/YangChen-cn/CardPilot>
- 当前结构版本：`schemaVersion: 1`

## 这里绝不存放

个人持卡信息、银行卡号/尾号、交易账本、姓名、邮箱、短信内容、连接码、Keychain 凭据、私人备注或任何访问令牌。此仓库是公开仓库，提交前请检查 diff。

## 文件

```
docs/catalog.json           App 使用的当前快照
docs/schema.json            字段说明与校验约束
scripts/validate_catalog.py 无第三方依赖的发布前校验
archive/                    历史快照（按 contentVersion 命名）
```

## 更新资料

1. 在 CardPilot 主仓库修订 `App/Resources/` 下的官方产品/活动资料，保留稳定 ID。
2. 生成新快照，`contentVersion` 必须大于上一版；建议使用 `YYYYMMDDNN`：

   ```bash
   python3 script/build_catalog_snapshot.py \
     --output ../CardPilot-Catalog/docs/catalog.json \
     --content-version 2026102301 --published-at 2026-10-23
   ```

3. 运行校验：

   ```bash
   python3 scripts/validate_catalog.py docs/catalog.json
   ```

4. 将上一版复制到 `archive/catalog-<旧contentVersion>.json`，提交并推送 `main`。GitHub Pages 会发布 `docs/`。
5. 用 `curl -sS https://yangchen-cn.github.io/CardPilot-Catalog/catalog.json | head` 确认线上内容。

`contentVersion` 只能递增。App 会拒绝低于本地版本的资料；同样的版本不会重复应用。

## 活动更新约定

- **修订**：保持产品 ID 和活动 ID 不变，更新条款并提高产品 `verifiedOn` 或活动日期。用户手改过的活动会进入待确认，不会被静默覆盖。
- **延期 / 新批次**：新增活动 ID，不要复用旧 ID 或按名称模糊匹配。旧活动保留在用户本地历史中。
- **到期**：保留活动并更新 `endsOn`，或从新快照移除；移除只会让 App 把官方活动标记为已下架，不删除个人迎新记录。
- **下架产品**：从快照移除产品不会删除用户已添加的卡；App 会继续保留本地资料。
- **新增产品**：当前 App 只允许使用内置卡面资源。新增产品必须同时随 App 发布卡面，否则应先在 App 中准备资源，再写入快照。

## 字段

顶层：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `schemaVersion` | Int | 当前为 `1`，不兼容结构必须提升版本 |
| `contentVersion` | Int | 单调递增的快照版本，例如 `2026102201` |
| `publishedAt` | `YYYY-MM-DD` | 发布日期，不是活动有效期 |
| `products` | Array | 当前可分发产品快照，至少一项 |

每个产品：

| 字段 | 说明 |
| --- | --- |
| `id` | 稳定产品 ID，与 App 现有 `catalogID` 一致 |
| `bankID` | `hsbc`、`bochk` 或 `bea` |
| `imageResource` | App 内置卡面文件名，远程不传图片 |
| `baseRewardVerified` | 基础权益是否已核实；未核实不参与展示金额 |
| `welcomePlans` | 官方迎新方案，沿用 App 的 `WelcomePlan` 结构 |
| `catalog` | 官方产品与活动条款，沿用 App 的 `CatalogCard` / `CatalogRule` 结构 |

`catalog` 中不得包含 `imageURL` 或 `imageBase64`；卡面由 App 内置。所有 `sourceURL` 必须为银行官方 HTTPS 地址。未知字段会被 App 拒绝，复杂条件写入 `notes` 并停用活动，不扩展计算字段。

App 展示的资料修订日期来自产品 `verifiedOn`，云端发布日期来自 `publishedAt`。
