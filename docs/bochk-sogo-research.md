# BOCHK SOGO Visa（2026-10-29 核实）

独立产品：`bochk.sogo.visa.platinum`、`bochk.sogo.visa.signature`。不合并不同等级。8家银行／24款产品，版本2026102902。

来源：
- [官方产品页](https://www.bochk.com/tc/creditcard/details/cobrand/cobrand/sogo.html)
- [2026迎新及产品条款](https://www.bochk.com/dam/boccreditcard/sogo_doc/sogocard_tnc_tc.pdf)
- [电子生日奖赏条款](https://www.bochk.com/dam/boccreditcard/cbc_pdf/sogoebday_TC.pdf)
- [官方新产品展示页](https://www.bochk.com/dam/boccreditcard/sogocard/chi/index.html)

以PDF为准，未照搬产品页可能令人误解的“HK$500现金”标题：礼券与手机回赠为二选一。迎新个人期按发卡当月及后两个月，申请截止2026-12-31；新客与多卡限制只描述，不限制个人追踪。Signature手机额外5%每月HK$100主附卡共享，白金没有此权益。Freshmart为折扣，积分不自动折算现金，未知开始日期保持null。

卡面来源：
- https://www.bochk.com/dam/boccreditcard/sogocard/images/Cardface-VP.png
- https://www.bochk.com/dam/boccreditcard/sogocard/images/Cardface-VS.png

用户明确要求真正横版，2026102902取代2026102901的竖图透明画布方案。使用内置imagegen分别参考官方竖版重排为横版示意，再标准化1200×756、去元数据和更新SHA-256。保留白金银白彩带、Signature蓝底银色飘带及银行、SOGO、Visa等级，无个人字段。产品说明明确标记AI示意，不称官方发行版；官方Logo资源未改。原始生成文件保留在本机generated_images目录，最终资源在docs/images/cards。

## 生图提示词

### platinum

```text
Use case: product-mockup. Transform the referenced official BOCHK SOGO Visa platinum vertical card into a true HORIZONTAL landscape credit card illustration, width:height 1.587:1. The entire output canvas MUST be the card front edge-to-edge, no surrounding space, no portrait card pasted inside landscape, no mockup background, no perspective, shadow, reflection or padding. Recompose the design horizontally rather than rotating lettering. Preserve BANK OF CHINA branding upper left and SOGO HONG KONG upper right, Visa Platinum lower right, metallic chip on left. Preserve silver-white background and colorful teal red pink blue orange curved stripes from reference. Crisp restrained faithful flat card illustration. No account numbers, names, expiry, security codes or invented benefits. All writing upright and readable. Output single horizontal card only.
```

### signature

```text
Use case: product-mockup. Transform the referenced official BOCHK SOGO Visa signature vertical card into a true HORIZONTAL landscape credit card illustration, width:height 1.587:1. The entire output canvas MUST be the card front edge-to-edge, no surrounding space, no portrait card pasted inside landscape, no mockup background, no perspective, shadow, reflection or padding. Recompose the design horizontally rather than rotating lettering. Preserve BANK OF CHINA branding upper left and SOGO HONG KONG upper right, Visa Signature lower right, metallic chip on left. Preserve deep blue background and white silver cyan curved stripes from reference. Crisp restrained faithful flat card illustration. No account numbers, names, expiry, security codes or invented benefits. All writing upright and readable. Output single horizontal card only.
```
