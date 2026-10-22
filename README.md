# CardPilot 官方银行卡资料库

[CardPilot](https://github.com/YangChen-cn/CardPilot) 的公开、版本化银行资料源。App 通过 GitHub Pages 获取银行、官方产品、权益活动和卡面，新增银行或产品不再需要发布新版 App。

- 资料地址：<https://yangchen-cn.github.io/CardPilot-Catalog/catalog.json>
- JSON Schema：<https://yangchen-cn.github.io/CardPilot-Catalog/schema.json>
- 当前结构版本：`schemaVersion: 2`

## 数据边界

这里只存放公开的银行官方资料：

- 银行名称、简称、Logo 和搜索关键词。
- 官方银行卡的产品信息、费率、来源、核实日期和活动条款。
- 银行 Logo 与官方卡面，路径相对资料根目录，并由 SHA-256 固定内容。

这里绝不存放个人持卡信息、卡号/尾号、姓名、邮箱、短信、交易账本、个人备注、Keychain 凭据、连接码或访问令牌。用户自己的卡面只保存在 CardPilot 的个人数据中，不会被上传到本仓库。

## 目录

```text
docs/catalog.json                 当前公开快照
docs/schema.json                  Schema V2
docs/images/banks/<name>.webp     银行 Logo
docs/images/cards/<name>.webp     官方卡面
scripts/validate_catalog.py       发布前校验（无第三方依赖）
.github/workflows/validate.yml    CI：结构、引用、图片和版本校验
archive/                          历史快照（可选）
```

## 结构

```json
{
  "schemaVersion": 2,
  "contentVersion": 2026102302,
  "publishedAt": "2026-10-23",
  "banks": [
    {
      "id": "example-bank",
      "name": "示例银行",
      "shortName": "示例",
      "logo": { "path": "images/banks/example-bank.webp", "sha256": "...", "contentType": "image/webp" },
      "searchTerms": ["示例", "example"]
    }
  ],
  "products": [
    {
      "id": "example-bank.card",
      "bankID": "example-bank",
      "artwork": { "path": "images/cards/example-card.webp", "sha256": "...", "contentType": "image/webp" },
      "baseRewardVerified": true,
      "welcomePlans": [],
      "catalog": { "...": "官方产品与活动条款" },
      "searchTerms": ["示例卡"]
    }
  ]
}
```

`bankID` 必须引用同一快照中的银行。图片路径只能是相对路径，不能是绝对 URL、跨域地址或包含 `..`；App 会拒绝不符合规则的资源。图片格式支持 PNG、JPEG 和 WebP，单张不超过 4 MB、边长不超过 2400 px。

## 新增银行或产品

1. 在 CardPilot 主仓库准备官方 JSON 与图片，更新 `App/Resources/Catalog/catalog.json`。保持银行、产品、活动的稳定 ID。
2. 将图片处理为无 EXIF 的公开资源，计算路径与 SHA-256。可使用主仓库工具：

   ```bash
   python3 scripts/catalog_asset.py ~/Downloads/new-card.png docs/images/cards/new-card.webp
   ```

   将输出的 `path`、`sha256`、`contentType` 填进 Catalog 的 `artwork`。

3. 从主仓库生成公开快照并复制图片：

   ```bash
   python3 script/build_catalog_snapshot.py \
     --output ../CardPilot-Catalog/docs/catalog.json \
     --content-version 2026102401 --published-at 2026-10-24
   ```

   `contentVersion` 必须大于线上版本，建议使用 `YYYYMMDDNN`。脚本会验证每张图片存在且 SHA-256 与 JSON 一致，并以原子方式写出快照。

4. 在公开仓库运行校验：

   ```bash
   python3 scripts/validate_catalog.py docs/catalog.json --base /tmp/previous-catalog.json
   ```

   没有旧版时可省略 `--base`。校验会检查 Schema、ID 唯一性与引用、图片路径/格式/尺寸/体积/hash、活动日期与 URL、隐私字段和版本递增。

5. 提交 `docs/catalog.json`、`docs/images/` 相关变更并推送 `main`。GitHub Actions 会自动复跑校验，GitHub Pages 随后发布 `docs/`。
6. 用 `curl` 确认线上版本：

   ```bash
   curl -sS https://yangchen-cn.github.io/CardPilot-Catalog/catalog.json | head
   ```

## 版本与离线

- App 每 6 小时检查一次，也支持启动、回到前台和设置页手动检查。
- 使用 ETag / Last-Modified 和 `contentVersion`，304 或同版本不会重复应用。
- 快照本地原子保存；网络失败不会清空上一次有效资料。
- 卡面按 SHA-256 独立下载、校验和缓存；单张图片失败不会让整份权益资料不可用。离线时优先使用已校验缓存，再回退 App 内置的基础资料和占位图。
- 卡面内容变化必须同时提升对应资源的 SHA-256；更新后的卡面会自动切换，不依赖清空全部缓存。

## 活动更新约定

- **修订**：保持产品 ID 和活动 ID 不变，更新条款并提高 `verifiedOn` 或活动日期。
- **延期 / 新批次**：新增活动 ID，不要复用旧 ID 或按名称模糊匹配。
- **到期**：保留活动并更新 `endsOn`，或从新快照移除；移除只会让 App 把官方活动标记为已下架，不删除个人迎新记录。
- **下架产品**：从快照移除产品不会删除用户已添加的卡；App 会保留本地历史。
- **新增产品**：银行和产品都由快照定义，App 不需要为新增银行或卡面发版。缺少图片时仍应保留产品资料，App 会显示占位图并允许稍后重试。

## 隐私与安全

提交前请检查 diff，确认没有个人信息或凭据。若发现误提交，请立即移除数据并轮换相关凭据；仅删除文件不能清除 Git 历史。安全问题请通过主仓库的 [SECURITY.md](https://github.com/YangChen-cn/CardPilot/blob/main/SECURITY.md) 报告。
