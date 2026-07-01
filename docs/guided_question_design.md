# Guided Question Design

Guided questions convert a prompt-writing task into a product workflow. Users choose a business question, and the system maps it to an internal analysis goal and recommended tools.

## Question Set

The knowledge base includes eight English question types:

- What does this issue mean?
- What past events does this resemble?
- What mechanisms may be operating?
- What have actors done in similar situations?
- Who may be affected?
- What should I monitor next?
- What are competing interpretations?
- What is missing from the evidence?

## Implementation

The question definitions are stored in `knowledge_base/guided_questions.csv` with user-facing text, internal analysis goals, recommended tools, and output focus.

## Product Rationale

The design reduces prompt burden, improves repeatability, and makes the reviewer workflow easier to demonstrate to non-technical stakeholders.
