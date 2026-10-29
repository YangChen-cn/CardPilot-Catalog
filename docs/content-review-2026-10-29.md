# Catalog 文案清洗与用卡指南复核 — 2026-10-29

## 原 PR 自报范围（复核前）
- 8 家银行、24 款产品、91 条现有权益逐条遍历；24 款产品的 `catalog.caveats` 全部改写，31 条 `rules[].notes` 清除了重复的维护话术或冗长段落，其他简明、有效的规则说明保留。
- 补充 24 份 `usageGuide`，共 50 个精选场景；指南只用于阅读，不参与回赠计算、选卡排序或账本资格判断。
- 新增编辑长度限制与测试，并以 `AGENTS.md` 要求后续 Agent 延续精简风格。
- 保留全部原有卡片/规则 ID、活动类别、奖励率、金额、上限、申请时间、结算条件、商户关键词、官方 URL、个人资料隔离及卡面 SHA-256。只改用户可读文案、可选 usageGuide 与快照版本。

## 原 PR 复核边界（复核前）
- 结构及原字段核对：完成。除编辑文案、指南和发布版本外，原有数字与计算条件保持不变。
- 官方网页抽样：CNCBI GBA 的 4%（含基础）、额外 6%、HK$150/HK$250 月上限，与工银亚洲星座 Visa Signature/银联钻石的 1.5% 无上限回赠均和官方公开页一致。公开页近期内容可能更新，合并时再次检查。
- **未完成的核对：** 其余所有 91 项官方 PDF 的逐项重新打开/阅读，以及确实存在冲突的活动起始日、历史旧规则与用户设备显示/排序。无法将这批工作标为「已认证」。
- 所有新 `usageGuide.reviewedOn` 表示本次文本整理日期，不应被视为银行承诺、活动开始日期或逐条官方条款验证通过。

## 原 PR 合并前阻断项（历史；已被本轮决定替代）
1. 先发布支持 `usageGuide` 的新版 CardPilot App，否则旧客户端会拒绝含有 `usageGuide` 的新 Catalog；见 `docs/usage-guide.md`。
2. 由另一 Agent / 维护者打开高风险活动原始 PDF，逐条核对优惠汇总、活动起始日期和共享封顶。优先：BOCHK GO Q4、Chill & 大湾区青年「即日起」、CNCBI 4%+6% 资格、工银亚洲年费与外币手续费、建行 eye 分段现金/积分。
3. 运行 Catalog CI 与全量校验；新 App 需通过实际解码、展示及离线缓存回归。

## 不在本 PR 范围
- App 中对每条建议固定追加「合资格签账、推广登记及其他限制以银行条款为准」的冗余提示。
- App 将产品级 caveats 与动态资格提示混合展示的界面问题。
- 日期原值涉嫌用资料核实日代替真实活动起始日，以及年费/手续费等未知事实；需要正式官方来源后才能改结构字段。


## 2026-10-29 复核增补（本轮实际范围）

已对照下列银行原始条款或银行官方页面的对应要点；这些仅为本次检查范围，不代表已对 91 条活动的所有字段、排除交易及同期其他优惠逐一核验，也不构成未来活动资格保证。

- [中银 GO 第四季指定手机签账 PDF](https://www.bochk.com/dam/boccreditcard/gopmq126/tnc_tc.pdf) 第 1–11、19–20 条：2026-10-01 至 12-31；限前 35,000 人登记；成功登记的**当月及其后月份**的合资格消费计入，登记月较早交易并非自动排除。钻石/白金内地分别 20X/10X，本地及海外分别 10X/5X，额外积分整期各卡账户共享上限 75,000，主附卡合并；同一笔符合指定 Go 商户优惠时只计商户优惠。修正原六项 `notes` 中“登记后的”错误，六项 `sourceURL` 及四项指南链接改为直接 PDF；加入名额、七天入账与不叠加提醒，不改倍率和上限。
- [中银 GO 产品优惠 PDF](https://www.bochk.com/dam/boccreditcard/gocard/gocardoffer_TC.pdf) 第 28–35 条：指定 Go 商户每月 HK$100 **包括**基础积分及额外回赠；2026 年底前豁免每月本地 HK$1,500 门槛。指南标注主附卡合并、上限构成，并在额度未用的前提下给出约 HK$2,000 的参考。
- [中银 GO 迎新 PDF](https://www.bochk.com/dam/boccreditcard/gocard/Go_WG_TC.pdf) 第 21–25 条：2026 年下半年申请的合资格 GO 钻石/白金手机迎新为 10%、上限由 HK$300 提高至 HK$800，不是固定加 HK$500；另核对 [限时双重迎新 PDF](https://www.bochk.com/dam/creditcard/banner/GoCard/DoubleWG_TC.pdf) 第 1–4 条，符合指定新客户条件并于 2026-10-01 至 12-31 同日申请 GO 与另一指定卡、于 2027-01-31 或之前获批，才有双迎新例外。修正白金欢迎活动中“同批只能领一项”的绝对说法；不更改用户手动追踪或锁定资格。
- [Chill 活动 PDF](https://www.bochk.com/dam/boccreditcard/chillcard/chill_offer_tnc_tc.pdf) 第 16–18、21、25 条：白金网上/海外 4% 和指定商户 8% 额外部分共用每历月 HK$150 上限，基础积分另计；商户优惠要求实体零售 HK$1,000。已修正两条指南的上限含义。其活动期写“即日起至 2026-12-31”；[Chill 迎新 PDF](https://www.bochk.com/dam/boccreditcard/chillcard/chill_wg_tc.pdf) 与[大湾区青年卡活动 PDF](https://www.bochk.com/dam/boccreditcard/cbc_pdf/gba_product_tnc_tc.pdf) / [迎新 PDF](https://www.bochk.com/dam/boccreditcard/cbc_pdf/gba_welcome_tnc.pdf) 同样仅写“即日起”。依据已有研究记录可知原 `2026-10-21` 只是人为选取的保守日期，故 Chill 三条和青年卡两条 `startsOn` 改为 null；不把核实日当生效日。青年卡 5% 按 PDF 第 3 条是每月最多 HK$100，补 `regional.capPeriod=monthly` 并给出额度未使用时约 HK$2,000 的参考。
- [东亚 UDC 奖赏 PDF](https://www.hkbea.com/pdf/en/credit-card/master-reward-tnc_en.pdf) 第 9 页：额外奖励每账户每历月最多 100,000 积分，餐饮、本地、云闪付、外币与人民币的额外积分共用；基础积分另计。六条普通/学生版指南原来把它写成不明周期的 HK$400 总回赠上限，已改为额外积分并说明兑换约值、相关排除。
- [信银国际大湾区活动页](https://www.cncbinternational.com/personal/promotions/credit-card/tc/index.html?SOURCE=ATJ15) 优惠 1、注 1–3：4%包含基础，额外部分 HK$150；合资格单笔人民币满 CNY4,000 的额外 6% 每月上限 HK$250，微信/支付宝/PayMe交易不享额外6%；合资格云闪付需商户扫描用户付款码，用户扫商户码不适用。指南说明满足两项条件时最高 10%，两个上限分别列示。迎新 PDF 的个人消费期与网页存在表述差异，未擅自统一。
- [建行 eye+ 官方活动页](https://www.asia.ccb.com/hongkong_sc/personal/credit_cards/eye_credit_card.html) 注 2–4：2026-10-01 至 2027-03-31；每月合资格零售 HK$3,000 门槛；网购 7.5X（含基础）加 2% 现金、拍卡 7.5X；额外 52,000 分共享及 HK$160 现金月上限。补足指南中的网购/拍卡范围与两个上限，不把积分等值当纯现金。
- [工银星座产品页](https://www.icbcasia.com/hk/tc/personal/credit-cards/type-of-cards/icbc-horoscope-card.html) 和[工银大湾区产品页](https://www.icbcasia.com/hk/sc/personal/credit-cards/type-of-cards/icbc-greater-bay-area-credit-cards.html)：钻石/Signature 1.5% 适用本地及海外合资格消费，原三条指南误仅写海外，已修正。产品页没有在本次找到足以确认的年费/外币手续费完整条款，未填“免费”。页面经搜索索引可读，部分请求返回 403，仍须人工打开产品资料概要复核。
- [汇丰学生卡迎新 PDF](https://www.hsbc.com.hk/content/dam/hsbc/hk/tc/docs/credit-cards/student/terms-and-conditions.pdf)、[学生学费 PDF](https://www.hsbc.com.hk/content/dam/hsbc/hk/docs/credit-cards/tc/tuition-fee-payment-tcs1.pdf)、[Pulse 活动 PDF](https://www.hsbc.com.hk/content/dam/hsbc/hk/docs/credit-cards/unionpay-dual-currency/diamond-card-terms-and-conditions.pdf)、[迎新 PDF](https://www.hsbc.com.hk/content/dam/hsbc/hk/tc/docs/credit-cards/offers/welcome-terms-and-conditions.pdf)：学生新客迎新 60 日 HK$2,000、Pulse 网申新客迎新 60 日 HK$8,000；学生学费整期 $200，按 2.4% 在额度未用的假设下约 HK$8,333 接近上限；Pulse 指定支付在内地/澳门人民币或澳门元皆适用，首 HK$80,000 合资格签账享额外奖赏。指南已补门槛和渠道、不再把澳门元排除。
- [Mox 信用卡官方产品页](https://mox.com/zh/features/mox-credit/) 注 2–4：1%/Mox+ 2% 自 2026-09-01 起，添加这两条活动及对应指南的真实生效日；0%外币及跨境港币费须选里数，非 Mox+ 转换奖励计划收费 HK$50，恢复产品说明中的条件。
- [交银 Go-Goal 官方产品页](https://www.bankcomm.com.hk/hk/shtml/hk/cn/2005276/2005302/2005325/2500923/2007907/list.shtml?channelId=2005276)：合资格首 12 历月每月首 HK$2,000 享额外 5.6%、最高 HK$112，基础 0.4% 积分另计；指南说明额外部分用满后可以比较其他卡。迎新、学费及特定申请渠道 PDF 未在本次成功读取并逐项核验，不把产品页视为完整迎新条款。
- [SOGO 官方条款 PDF](https://www.bochk.com/dam/boccreditcard/sogo_doc/sogocard_tnc_tc.pdf)：迎新两方案分别为 HK$500 购物礼券或手机 10% 上限 HK$300，须分清形式及资格。Signature 手机优惠指南改写现金上限及额度未使用时约 HK$2,000 的参考；仍需对产品优惠页具体条目逐字段复核。

卡面：按用户最新要求，产品界面不展示 AI 素材说明；卡面来源、生成提示词和非发行版本身份保留于素材记录。汇丰扣账卡指南删除无法由该产品页支持的“基础方案赚奖赏钱”表述。

### 按产品列出尚需逐字段核验的活动

下面“已抽查”只表示对上面列出的特定要点检查过，不代表该规则所有字段已核实；“未逐项核对”是本轮未对该规则内容做完整条款核验的明确列表。无活动的产品未列；迎新方案及申请渠道仍需另核。

- **hsbc.student.visa.gold**：已抽查 `hsbc.student.welcome.new.2026`、`hsbc.student.welcome.existing.2026`、`hsbc.student.tuition.2026h2`；未逐项核对 无。
- **hsbc.pulse.unionpay.diamond**：已抽查 `hsbc.pulse.cn-mo.mobile.2026h2`、`hsbc.pulse.welcome.new.online.2026`、`hsbc.pulse.welcome.new.other.2026`、`hsbc.pulse.welcome.existing.2026`；未逐项核对 无。
- **bochk.chill.platinum**：已抽查 `chill.platinum.online-overseas.2026`、`chill.platinum.merchants.2026`、`chill.platinum.welcome.2026`；未逐项核对 无。
- **bochk.go.diamond**：已抽查 `mobile`、`go.welcome.mobile.2026`、`go.diamond.mobile.mainland.2026q4`、`go.diamond.mobile.local.2026q4`、`go.diamond.mobile.overseas.2026q4`、`go.diamond.selected-go-merchants.2026`；未逐项核对 `go.diamond.fx.fee-waiver.2026q4`。
- **bochk.go.platinum**：已抽查 `mobile`、`go.platinum.welcome.mobile.2026`、`go.platinum.mobile.mainland.2026q4`、`go.platinum.mobile.local.2026q4`、`go.platinum.mobile.overseas.2026q4`、`go.platinum.selected-go-merchants.2026`；未逐项核对 `go.platinum.fx.fee-waiver.2026q4`。
- **bochk.gba.youth**：已抽查 `regional`、`welcome`；未逐项核对 无。
- **bea.hku.student.visa**：已抽查 `hku.student.welcome.2026`；未逐项核对 无。
- **bea.udc.diamond**：已抽查 `dining`、`local`、`cny`、`usd`、`unionpay-app`；未逐项核对 `udc.existing.welcome.2026`。
- **bea.udc.diamond.student**：已抽查 `dining`、`local`、`cny`、`usd`、`unionpay-app`；未逐项核对 无。
- **cncbi.gba.dual**：已抽查 `cny4`、`cny6`、`cncbi.gba.unionpay.app.merchantqr.2026h2`；未逐项核对 `welcome600`、`cncbi.gba.welcome.fx10.2026h2`。
- **bocom.go-goal.visa.platinum**：已抽查 无；未逐项核对 `bocom.go-goal.points`、`bocom.go-goal.first-year.rebate.2026`、`bocom.go-goal.tuition.points.2026`、`bocom.go-goal.welcome.2026`、`bocom.spending-rewards.2026q4`。
- **bocom.gba.unionpay.diamond**：已抽查 无；未逐项核对 `bocom.gba.dual-account`、`bocom.gba.points`、`bocom.unionpay.cny-mop.rebate.2026`、`bocom.unionpay.gba-transport.rebate.2026`、`bocom.gba.welcome.2026h2`、`bocom.spending-rewards.2026q4`。
- **mox.credit.mastercard**：已抽查 `mox.credit.mastercard.cashback.base`、`mox.credit.mastercard.cashback.plus`、`mox.credit.mastercard.supermarket`；未逐项核对 `mox.credit.mastercard.phone.2026`、`mox.credit.mastercard.moxcash.welcome.2026`。
- **icbcasia.horoscope.unionpay.diamond**：已抽查 `icbcasia.horoscope.unionpay.diamond.cashback.1_5`；未逐项核对 `icbcasia.horoscope.unionpay.diamond.tax.2026q4`、`icbcasia.horoscope.unionpay.diamond.unionpay.mobile.2026q3`。
- **icbcasia.horoscope.visa.signature**：已抽查 `icbcasia.horoscope.visa.signature.cashback.1_5`；未逐项核对 `icbcasia.horoscope.visa.signature.tax.2026q4`。
- **icbcasia.gba.unionpay.diamond**：已抽查 `icbcasia.gba.unionpay.diamond.cashback.1_5`；未逐项核对 `icbcasia.gba.unionpay.diamond.tax.2026q4`、`icbcasia.gba.unionpay.diamond.unionpay.mobile.2026q3`。
- **ccbasia.eye.visa.signature**：已抽查 `ccbasia.eye.visa.signature.online.contactless`；未逐项核对 `ccbasia.eye.visa.signature.points.base`、`ccbasia.eye.visa.signature.dining.2026q3`、`ccbasia.eye.visa.signature.welcome.cash`。
- **ccbasia.travo.world.mastercard**：已抽查 无；未逐项核对 `ccbasia.travo.world.mastercard.overseas.2026`、`ccbasia.travo.world.mastercard.dining.2026`、`ccbasia.travo.world.mastercard.overseas.bonus.2026sep`、`ccbasia.travo.world.mastercard.welcome.cash`。
- **ccbasia.unionpay.dual.currency**：已抽查 无；未逐项核对 `ccbasia.unionpay.dual.currency.points`、`ccbasia.unionpay.dual.currency.overseas.2026sep`、`ccbasia.unionpay.dual.currency.welcome.cash`。
- **bochk.sogo.visa.platinum**：已抽查 无；未逐项核对 `bochk.sogo.visa.platinum.shopping.2026`、`bochk.sogo.visa.platinum.freshmart.2026`、`bochk.sogo.visa.platinum.japan.2026`、`bochk.sogo.visa.platinum.dining.2026`、`bochk.sogo.visa.platinum.points`、`bochk.sogo.visa.platinum.birthday.2026`。
- **bochk.sogo.visa.signature**：已抽查 无；未逐项核对 `bochk.sogo.visa.signature.mobile.2026`、`bochk.sogo.visa.signature.shopping.2026`、`bochk.sogo.visa.signature.freshmart.2026`、`bochk.sogo.visa.signature.japan.2026`、`bochk.sogo.visa.signature.dining.2026`、`bochk.sogo.visa.signature.points`、`bochk.sogo.visa.signature.birthday.2026`。

以上“已抽查”的字段之外也都仍需逐项核验，包括 91 条活动中其他所有比例、金额、申请期、消费期、商户限制、排除条件、费用与来源；尤其交银欢迎/交通 PDF、工银年费/跨境费、所有尚未点开原始条款的产品。资料通过 JSON/schema 校验不等于已证实银行事实，Catalog #7 应保持开放并明确记录剩余工作。

## 当前发布决定

唯一使用者于2026-10-29明确不要求旧版兼容，并要求删除用户界面的AI卡面标注；按当前客户端验证后发布。本轮提交是文案精简与已证实事实修正，不声称91条全部银行条件重新认证。尚未完整核验的字段继续在 Catalog #7 跟进，不把其余内容的发布写成该 issue 已完成。

补充建行[飞常赏官方条款](https://www.asia.ccb.com/hongkong_tc/personal/credit_cards/promotions/overseas_spending/index.html)第3–5条：登记一张卡后名下其余卡自动登记，签账及上限按持卡人合并；已补 TRAVO 和银联两条 notes 及银联指南上限。TRAVO 登记可经网银或手机银行，不限 App，已纠正文案。

### 收口补查

另打开 SOGO 产品条款第 II–V 项及[生日条款](https://www.bochk.com/dam/boccreditcard/cbc_pdf/sogoebday_TC.pdf)，对购物/Freshmart/日本/餐饮、Signature手机5%及生日会员/直销/每年一次条件作补查。Freshmart措辞明确为“付款前出示手机应用内已加入的卡”，不要求拿出实体卡。TRAVO[产品页](https://www.asia.ccb.com/hongkong_tc/personal/credit_cards/travoworld.html)可读，登记渠道已修正；本轮不是全部字段审计。

无法读取的来源：工银缴税 PDF https://v.icbc.com.cn/userfiles/resources/icbc/haiwai/asia/download/tc/2026/tax_payment_cash_rebate_tnc_2610_tc.pdf 返回403；交银 Go-Goal/大湾区迎新、学费、交通及季度奖赏的 catalog.sourceURL 多份 PDF 返回 TLS EOF。可读 Go-Goal 产品页只支持5.6%及首HK$2,000等要点，不能代替完整条款。工银费用和这些活动的剩余排除项未证实，保留未知并在 #7 跟进。
