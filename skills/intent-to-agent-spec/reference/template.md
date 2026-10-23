# Agent Spec — output template

Copy the Purpose / Writing Guide section verbatim into every spec. Replace `<…>` placeholders. Delete bracketed guidance.

---

# Agent Spec

## 目的

Agent Spec 是 **Agent 的行為與驗收規格（WHAT）**。它定義 Agent 在其能力範圍內：

- 可以與不可以執行哪些行動，以及何時擁有執行權限；
- 在不同使用者請求、對話歷史與外部世界狀態下，必須滿足哪些行為規則（Contract / invariants）；
- 在代表性的情境中，哪些結果是 **Expected**、哪些行為是 **Forbidden**；
- 必要時，以附屬 **Evaluation Criteria（Rubrics）** 定義語意或品質判斷的合格標準；
- 透過 **Evaluation Policy** 定義單次執行、重複執行與 Quality Gate 的通過條件。

Agent Spec **不規定 HOW**：例如使用哪個 agent framework、怎麼寫 pytest assertions、如何讀取工具呼叫紀錄、使用哪個 LLM judge 或如何實作測試資料。這些由架構、測試與 evaluation implementation 決定；實作不可擅自增加或放寬 Spec 的產品要求。

## 寫作原則

- **Contract**：寫跨多個情境都成立的規則。只有真正跨 capabilities 共用的規則才放在 Global Contract。
- **Scenarios**：用少量具體的 specification examples 說明規則。每個情境描述已知狀態、使用者行為、Expected 與必要的 Forbidden；`may` 是允許行為，不是必須通過的檢查。
- **Attached Rubrics（optional）**：僅在某個 Expected／Forbidden 的合格界線需要澄清時，寫在該 statement 旁邊。預設每條 criterion 為 yes/no。若需要分數制，才明確定義分數尺度、各分數的判準與 pass threshold。
- **Evaluation Policy**：只放共通的判定與 Quality Gate 規則；某個情境偏離預設時，才在該情境說明例外。
- **Ownership**：Rubric 中的每一條合格條件都是產品要求，須由 spec owner 決定。產生測試的 skill 不能自行添加條件；遇到無法可靠判斷的文字，應回報 spec issue。
- **Examples**：valid／invalid responses 是判準的例子，除非規格另有明確要求，不能將例子當成唯一可接受的措辭。

在需求探索時可以使用 **Rules ↔ Examples ↔ Questions** 與暫時性的 rough examples。只有經確認的情境才進入正式 `Scenarios`；草稿討論不自動成為可執行的驗收要求。

---

# <Agent Name> — Agent Spec

Status: <Draft — N open issues | Confirmed>  
Owner: <name>  
Source: `product-sense.md` (claims cited as `[PS §n: "…"]`) · owner confirmations in `example-map.md` (cited as `[EM: id]`) · issues in `phase-result.yaml`

## 0. Agent Requirements

### Goal & outcome

- <what the agent does for the user> [PS §1: "…"]
- <business outcome / quality bar it serves> [PS §7: "…"]

### Actors & authority

| Actor | Agent may do alone | Requires confirmation from this actor | Needs a human |
|---|---|---|---|
| <actor> | <actions> [PS §3: "…"] | <actions> [PS §3: "…"] | <actions> [PS §3: "…"] |

[Irreversible or record-changing actions are `requires confirmation` unless §3 says otherwise.]

### Capabilities, prioritized

1. <Capability A> — <one line> [PS §2: "…"] [PS §4: "…"]
2. <Capability B> — … 
[Committed future scope, not specified in this version:] <…> [PS §2: "…"]

### World requirements

| Entity / affordance | Material fields or behavior | Status | Source |
|---|---|---|---|
| <entity> | <fields the agent must resolve> | confirmed | [PS §5: "…"] |
| <affordance: observe / change / check status of …> | <what it must return> | assumed | needed by <XX-Snn> |

[`assumed` = required of the world, not yet confirmed by Product Sense; architecture must honor or reject via Issue.]

## 1. Global Contract

[Only rules that hold unchanged for ≥2 capabilities. Typical candidates, include only if evidenced by this product's examples: truthful outcomes, no unrelated changes, current authorization, uncertain execution.]

**G-01 — <Title>**

<1–3 sentences, must / must not.>

## 2. Evaluation Policy

### Judgment — per execution

- Every required **Expected** statement must hold, and every applicable **Forbidden** behavior must not occur.
- A statement that says **may** describes permitted behavior, not a required check. Explicit constraints on that permission, if any, still apply.
- A statement is assessed on its own, even when it has no attached rubric.
- Attached rubric criteria are **yes/no** by default. A statement with an attached rubric passes only if the statement itself is satisfied **and** every attached criterion is yes.
- An illustrative response is not required verbatim; semantically equivalent wording can pass.
- An execution **fails** if any required check establishes a violation. Otherwise, if a required check cannot reach a verdict, the execution is **inconclusive**. Otherwise, it **passes**.
- A scenario with mutually exclusive world states is evaluated separately for each applicable **scenario variant**.

### Quality Gate

- Each scenario variant must pass **k = <5> independent Agent executions** with fresh conversation and test state.
- The Quality Gate passes only if all <k> executions pass. A confirmed violation fails the gate; otherwise, an inconclusive execution makes the gate inconclusive.
- Runs with fewer executions are diagnostic and do not satisfy this gate.

[If the owner chose an average-pass-rate criterion instead, state: k, the minimum passes, and that any confirmed violation of a Forbidden still fails.]

## 3. Capability: <Capability A>

### Scope & Authority

The agent may:

- <action>;
- <action, "after confirmation of the current proposal" when authorization is required>.

The agent must not:

- <action>. [PS §3: "…"]

Clarify when:

- <condition under which the agent asks before acting>. [PS / EM]

Abstain / escalate when:

- <condition>; the agent <what it does instead: refuses / hands off to …>. [PS / EM]

### Contract

#### <XX>-01 — <Rule title>

<Rule. Name the material information / authorization / outcome condition it governs.>

[Optional:]
**Illustrative conversation (not a separately approved scenario):**

> Agent: …
> User: …

### Scenarios

These are **Specification by Example** examples of the Contract. Attached rubrics, when present, refine the evaluation of the statement immediately above them.

#### <XX>-S01 — <Scenario name>

**Initial state**  [or **Existing state**]

<External world facts. One fact per line.>

**Conversation**  [only when prior turns matter]

<Prior turns.>

**User**

"<verbatim user message>"

**Expected**

[Mark each statement's kind: (state) world-state fact · (order) ordering constraint on the trace · (comm) communication requirement, always with a rubric.]

- (state) <after valid authorization: exactly one reservation exists; field = value>;
- (order) <Y does not happen until X>;
- (comm) <what the message must contain / omit> — rubric below.

[Judgment statement with rubric:]
- <statement>

  **Attached Rubric (yes/no):**

  - <criterion the owner confirmed>.
  - <criterion>.

  **Calibration set (owner-labelled; illustrative, no exact wording required):**

  - PASS — > <text>
  - PASS (boundary) — > <text>
  - FAIL — > <text>
  [3–5 entries]

[Variants, when outcomes are mutually exclusive:]
**If <condition A>:**
- …

**If <condition B>:**
- …

**Forbidden**

- <behavior>;
- <behavior>.

This scenario illustrates **<XX>-01** [and **G-xx**]. [EM: <card-id>]

## 4. Capability: <Capability B>

[Same structure.]
