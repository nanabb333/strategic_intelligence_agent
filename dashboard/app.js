const scenarioRules = {
  "Export Controls": ["export control", "entity list", "license", "licensing", "restricted access"],
  "Industrial Policy": ["chips act", "industrial policy", "subsidy", "domestic manufacturing", "incentive"],
  "Sanctions": ["sanctions", "asset freeze", "embargo"],
  "Supply Chain Disruption": ["supply chain", "shipping", "logistics", "shortage", "disruption", "rerouting"],
  "Regulatory Action": ["regulation", "regulatory", "compliance", "rule", "enforcement"],
  "Military / Security Shock": ["military", "security", "red sea", "strait", "conflict"],
  "Earnings / Corporate Disclosure": ["earnings", "guidance", "quarter", "margin", "revenue", "disclosure", "deposit"],
  "Strategic Investment": ["investment", "capex", "facility", "plant", "partnership"],
  "Trade Policy": ["tariff", "trade", "customs", "import"],
};

const historicalCases = [
  { title: "CHIPS and Science Act", source: "Historical Database", scenario: "Industrial Policy", relevance: "shares characteristics with subsidy-backed semiconductor capacity planning" },
  { title: "Huawei Entity List", source: "Historical Database", scenario: "Export Controls", relevance: "may resemble technology-access restrictions and compliance screening" },
  { title: "Russia Sanctions After Ukraine Invasion", source: "Historical Database", scenario: "Sanctions", relevance: "shares characteristics with sanctions-driven counterparty review" },
  { title: "COVID Supply Chain Disruption", source: "Historical Database", scenario: "Supply Chain Disruption", relevance: "may resemble supplier continuity and logistics stress" },
  { title: "Red Sea Shipping Disruption", source: "Historical Database", scenario: "Supply Chain Disruption", relevance: "shares characteristics with route disruption and delivery monitoring" },
  { title: "Major Earnings Guidance Withdrawal During COVID", source: "Historical Database", scenario: "Earnings / Corporate Disclosure", relevance: "may resemble disclosure under operational uncertainty" },
];

const contextFindings = [
  { industry: "Semiconductors", source: "Context Knowledge Base", keywords: ["semiconductor", "chips", "ai", "fabrication"], text: "Semiconductor strategy requires monitoring licensing, supplier concentration, fabrication capacity, and government incentive requirements." },
  { industry: "Banking", source: "Context Knowledge Base", keywords: ["bank", "deposit", "credit", "liquidity", "capital"], text: "Banking analysis often requires monitoring deposit trends, credit quality, liquidity planning, regulatory engagement, and capital levels." },
  { industry: "Supply Chain", source: "Context Knowledge Base", keywords: ["supply chain", "shipping", "logistics", "inventory", "supplier"], text: "Supply chain disruptions can affect routing, lead times, inventory planning, supplier communication, and customer commitments." },
  { industry: "Trade Policy", source: "Context Knowledge Base", keywords: ["trade", "tariff", "customs", "export control", "sanctions"], text: "Trade policy context requires monitoring customs rules, sanctions lists, control lists, eligibility rules, and compliance guidance." },
  { industry: "Energy", source: "Context Knowledge Base", keywords: ["energy", "oil", "gas", "battery", "grid"], text: "Energy context can involve sanctions, industrial incentives, shipping chokepoints, permitting, and equipment lead times." },
];

let currentBrief = "";

function textIncludes(text, keyword) {
  return text.toLowerCase().includes(keyword.toLowerCase());
}

function classifyScenario(text) {
  let best = { scenario: "Other", matches: [] };
  for (const [scenario, keywords] of Object.entries(scenarioRules)) {
    const matches = keywords.filter((keyword) => textIncludes(text, keyword));
    if (matches.length > best.matches.length) {
      best = { scenario, matches };
    }
  }
  const confidence = best.matches.length >= 3 ? "High" : best.matches.length >= 1 ? "Medium" : "Low";
  return { ...best, confidence };
}

function summarizeDocument(text) {
  const clean = text.trim().replace(/\s+/g, " ");
  return clean.slice(0, 420) + (clean.length > 420 ? "..." : "");
}

function extractEntities(text) {
  const industries = ["semiconductor", "banking", "supply chain", "shipping", "energy", "trade policy", "AI", "cloud"].filter((item) => textIncludes(text, item));
  const policyTerms = ["export control", "industrial policy", "sanctions", "CHIPS Act", "tariff", "regulatory", "compliance"].filter((item) => textIncludes(text, item));
  return { industries, policyTerms };
}

function retrieveAnalogues(classification) {
  const exact = historicalCases.filter((item) => item.scenario === classification.scenario);
  const fallback = historicalCases.filter((item) => item.scenario !== classification.scenario);
  return [...exact, ...fallback].slice(0, 3);
}

function retrieveContext(text) {
  const matches = contextFindings.filter((item) => item.keywords.some((keyword) => textIncludes(text, keyword)));
  return (matches.length ? matches : contextFindings).slice(0, 3);
}

function buildBrief(text, classification, entities, analogues, contexts) {
  const analogueLines = analogues.map((item) => `- ${item.title}: ${item.relevance} (Source: ${item.source})`).join("\n");
  const contextLines = contexts.map((item) => `- ${item.industry}: ${item.text} (Source: ${item.source})`).join("\n");
  return `# Executive Intelligence Brief

This output is for decision-support and analyst productivity only. It does not provide forecasts, probabilities, trading advice, or investment recommendations.

## Executive Summary

- The document describes a ${classification.scenario} issue.
- Historical analogues and current context are used for comparison, not prediction.
- Evidence references identify source origins.

## Key Issue

${summarizeDocument(text)}

Source: Input Document

## Scenario Classification

- Primary scenario: ${classification.scenario}
- Matched keywords: ${classification.matches.join(", ") || "None"}
- Classification confidence: ${classification.confidence}
- Source: Input Document

## Extracted Entities

- Industries: ${entities.industries.join(", ") || "None detected"}
- Policy terms: ${entities.policyTerms.join(", ") || "None detected"}
- Source: Input Document

## Historical Analogues

${analogueLines}

## Current Context

${contextLines}

## Implications

- The issue may resemble selected historical cases while differing in current actors, timing, and implementation details.
- Current context requires monitoring of stakeholders, operational constraints, and source updates.
- Analysts should separate observed facts from interpretation.

## Strategic Questions

- Which stakeholders are most exposed?
- Which evidence should be verified against primary sources?
- Which current-context findings require continued monitoring?

## Evidence Trace

- Source: Input Document
- Source: Historical Database
- Source: Context Knowledge Base
`;
}

function renderFindingList(element, items, renderItem) {
  element.innerHTML = "";
  if (!items.length) {
    element.innerHTML = '<div class="empty">No findings generated.</div>';
    return;
  }
  for (const item of items) {
    const div = document.createElement("div");
    div.className = "finding";
    div.innerHTML = renderItem(item);
    element.appendChild(div);
  }
}

function runAnalysis() {
  const text = document.getElementById("document-input").value.trim();
  if (!text) {
    document.getElementById("summary-section").innerHTML = '<div class="empty">Paste or upload a document to analyze.</div>';
    return;
  }
  const classification = classifyScenario(text);
  const entities = extractEntities(text);
  const analogues = retrieveAnalogues(classification);
  const contexts = retrieveContext(text);
  currentBrief = buildBrief(text, classification, entities, analogues, contexts);

  document.getElementById("summary-section").innerHTML = `<p>${summarizeDocument(text)}</p><p><span class="evidence">Source: Input Document</span></p>`;
  document.getElementById("classification-section").innerHTML = `<ul><li>Primary scenario: ${classification.scenario}</li><li>Matched keywords: ${classification.matches.join(", ") || "None"}</li><li>Confidence: ${classification.confidence}</li></ul><p><span class="evidence">Source: Input Document</span></p>`;
  renderFindingList(document.getElementById("analogues-section"), analogues, (item) => `<h3>${item.title}</h3><p>${item.relevance}</p><span class="evidence">Source: ${item.source}</span>`);
  renderFindingList(document.getElementById("context-section"), contexts, (item) => `<h3>${item.industry}</h3><p>${item.text}</p><span class="evidence">Source: ${item.source}</span>`);
  document.getElementById("implications-section").innerHTML = `<ul><li>The issue may resemble selected historical cases, but differences in current actors and timing require monitoring.</li><li>Current context adds stakeholder and operating constraints that historical analogues alone cannot provide.</li></ul><p><span class="evidence">Source: Synthesis from all evidence</span></p>`;
  document.getElementById("brief-section").textContent = currentBrief;
}

function exportBrief(format) {
  if (!currentBrief) {
    runAnalysis();
  }
  const content = format === "txt" ? currentBrief.replace(/^#+\s/gm, "") : currentBrief;
  const type = format === "txt" ? "text/plain" : "text/markdown";
  const blob = new Blob([content], { type });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `strategic_intelligence_brief.${format}`;
  link.click();
  URL.revokeObjectURL(link.href);
}

document.getElementById("file-input").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  document.getElementById("document-input").value = await file.text();
  runAnalysis();
});

document.getElementById("analyze-button").addEventListener("click", runAnalysis);
document.getElementById("export-md").addEventListener("click", () => exportBrief("md"));
document.getElementById("export-txt").addEventListener("click", () => exportBrief("txt"));

runAnalysis();
