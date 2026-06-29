# Failure Modes

This document records known failure-mode categories for future research validation.

The categories below do not mean the platform is unsuitable for decision support. They define where reviewers should pay attention and where future research can improve the system. The current product remains a local decision-support tool that requires human review.

## Weak Source Material

**Description:** The input is too short, vague, incomplete, or unsupported to produce a strong decision brief.

**Impact:** The system may generate a structurally complete brief while the evidence base remains thin.

**Mitigation:** Keep evidence limitations visible, avoid high confidence, and ask users to provide better source material when needed.

**Future research opportunity:** Study how source quality affects decision-support usefulness and when the product should decline to infer more.

## Ambiguous Decision Questions

**Description:** The user question does not specify the decision, objective, stakeholder, or time horizon.

**Impact:** The system may frame a generic decision rather than the user's actual decision.

**Mitigation:** Preserve the extracted decision question, expose assumptions, and use the Decision Case to make framing visible.

**Future research opportunity:** Develop review protocols for decision-question clarity and human correction.

## Poor Historical Analogue Coverage

**Description:** The local historical records do not contain close or useful analogues for the current case.

**Impact:** Historical comparison may become generic, weak, or misleading if not clearly limited.

**Mitigation:** State analogue limitations, distinguish mechanism similarity from outcome prediction, and keep confidence qualitative.

**Future research opportunity:** Evaluate analogue relevance with human reviewers and build clearer transferability rubrics.

## Over-Generalization

**Description:** The system treats broad historical or strategic patterns as more applicable than the evidence supports.

**Impact:** Recommendations may appear more grounded than they are.

**Mitigation:** Show differences, assumptions, and change triggers. Avoid claims that history determines the current case.

**Future research opportunity:** Track where reviewers identify over-broad analogies or unsupported mechanisms.

## Confidence Mismatch

**Description:** Confidence language is stronger or weaker than the evidence quality justifies.

**Impact:** Users may over-trust or under-use the decision-support output.

**Mitigation:** Use qualitative confidence only, expose limitations, and prevent high confidence where evidence is limited.

**Future research opportunity:** Compare confidence labels against human evidence-quality judgments.

## Missing Evidence

**Description:** Important evidence is absent from the source material or local records.

**Impact:** The brief may omit key risks, stakeholders, constraints, or alternatives.

**Mitigation:** Name missing evidence and include it in uncertainty, monitoring, and change-trigger sections.

**Future research opportunity:** Create rubrics for missing-evidence detection by scenario type.

## Unsupported Assumptions

**Description:** The system relies on assumptions that are not visible or not sufficiently tied to evidence.

**Impact:** Recommendations may appear more direct than the evidence warrants.

**Mitigation:** Keep assumptions explicit in the Confidence Assessment and brief.

**Future research opportunity:** Evaluate assumption quality and reviewer disagreement across cases.

## Localization Drift

**Description:** Localized output preserves labels but weakens analytical meaning, caution, or decision logic.

**Impact:** Non-English reviewers may receive less precise decision support.

**Mitigation:** Preserve structure across languages and include localization quality in deterministic evaluation.

**Future research opportunity:** Add human review of localized decision-support artifacts.

## Evaluation Overreach

**Description:** Deterministic product-quality scores are misread as scientific validation or factual accuracy.

**Impact:** Reviewers may infer stronger claims than the product supports.

**Mitigation:** Label deterministic scores as product-quality review aids and avoid benchmark superiority claims.

**Future research opportunity:** Design protocols that clearly separate product QA, research validation, and academic benchmarking.
