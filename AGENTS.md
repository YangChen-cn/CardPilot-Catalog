# AGENTS.md — CardPilot-Catalog editorial and publishing contract

> Applies to this repository and all subdirectories. Read this file, `docs/usage-guide.md` and `docs/pr-submission.md` before editing Catalog content.

## Goal and language
- Write for a cardholder making a payment decision, not for a developer auditing a database.
- Use concise, plain Chinese in user-facing fields. Lead with **how to use**, **reward**, **threshold**, **cap**, **registration**, and **expiry**.
- Never put internal status such as "尚待完整核实", "本次整理", "此处不自动计算", "不视为免年费", schema history, or AI/artwork production notes in `catalog.caveats`, `catalog.rules[].notes` or `usageGuide`.
- Do not repeat an umbrella disclaimer ("以银行为准") in each field. Provide the actual official sourceURL, and preserve material eligibility/uncertainty in a precise, actionable phrase only where needed.
- Never hide an important exclusion, enrollment requirement, shared cap, transaction method, currency requirement, period, new-customer condition or reward form just to shorten copy.
- Separate a **confirmed negative condition** ("微信支付不适用") from **missing data** ("未收录外币手续费"). Missing fee information is not permission to claim zero fees. Keep unknown facts out of positive recommendations.
- The official card face provenance belongs in artwork documentation, not the spending guide.

## Structured fact protection
- For copy-only work, do **not** change `id`, `kind`, `group`, `ratePercent`, `bonusHKD`, `capHKD`, dates, `calculation`, `sourceURL`, `verifiedOn`, `welcomePlans[].ruleIDs` or other calculation/eligibility fields. Require a separate official evidence check and explicitly reviewed diff to change them.
- Do not pretend all point equivalents are cash. Label approximate points-to-cash equivalents, total vs extra reward, monthly vs campaign limits, and shared caps.
- New cards and offers require exact product-grade matching (Diamond/Platinum/Signature, student/general, Visa/UnionPay); don't borrow terms from a sibling card.
- Unknown start dates remain null; `verifiedOn` or guide `reviewedOn` is NOT an effective date. Expired offers must not be advertised as current.
- Maintain stable IDs for revisions; a distinct promotion round needs a new ID. Keep historical records navigable.
- `usageGuide` is editorial only. NEVER inject its prose into the reward engine or eligibility calculations.

## Size and quality limits (enforced by validator/schema)
- `catalog.caveats` <= 180 Chinese characters; `annualFeeNote` <= 110; `rules[].notes` <= 300; `welcomePlans[].details` <= 250.
- `usageGuide.summary` <= 90; 1–4 truly useful scenarios, not one for every offer by default.
- Scenario `title` <= 64, `whenToUse` <= 130, `howToUse` <= 220; `capNote` and `stopAfter` <= 120 each.
- At most **2** scenario warnings, <= 100 characters each. If there are no genuinely important warnings, omit the field.
- Avoid mechanically filling `capNote`, `stopAfter` or `warnings`. Only calculate spend-to-cap when the rate, scope and reward period are unambiguous and no shared/used cap is assumed.
- Every guide scenario includes official HTTPS source(s) and IDs from the *same product*. Avoid invented dates, rewards, or links. Historical benefits should not be included as present-day scenarios.
- Re-evaluate guides when a referenced offer changes. All linked IDs still existing is necessary but **not sufficient** for semantic correctness.

## Research and review
1. Read the exact card and rules in `docs/catalog.json`; inspect each linked official page/PDF. Record what was actually verified. Do not claim to have checked a link you did not open.
2. Preserve facts in the structured model, simplify only user-visible prose. If bank sources conflict, STOP on factual change and create a small follow-up Issue listing the exact product/rule and two sources.
3. Compare before/after IDs, rates, cap, amounts, periods, merchant lists, calculation conditions, sources and image hashes. A copy-only PR must have a zero non-editorial diff.
4. Run `python3 scripts/test_validate_catalog.py`, `python3 scripts/validate_catalog.py docs/catalog.json`, and `git diff --check`. With a changed catalog, pass `--base` pointing to main's prior snapshot to verify contentVersion increase.
5. **Publishing compatibility gate:** a client older than the `usageGuide` change rejects the new field. Do not merge or publish new guides until a compatible CardPilot client is shipped or compatibility is explicitly resolved. Keep this PR as draft until then.
6. Summarize what was code-verified versus what still needs bank-side manual evidence. Never mark schema validation as independent confirmation of bank terms.
