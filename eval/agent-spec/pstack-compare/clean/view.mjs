// View for CleanPolicy.tla (and SeededPolicy.tla), per pstack's statechart SKILL.md.
// State and step labels are the Python model's own: chart() and the Step labels in
// new-format/seeded-clean/model.py. The parent-state names are added here.

const BEFORE = "Before the cancel call";
const AFTER = "After the customer says yes";
const OVER = "Conversation over";

export const title = "Harbor Goods: cancel an order (clean policy)";

// chart(s) from model.py, with a parent state for each phase.
export const state = ({ s }) => {
  if (s.loc === "setup" || s.loc === "turn1") return ["Start"];
  if (s.loc === "end") {
    if (s.told.includes("refund_ok")) return [OVER, "Cancelled and refunded"];
    if (s.told.includes("staff_will_follow")) return [OVER, "Handed to store staff"];
    if (s.told.includes("staff_unconfirmed")) return [OVER, "Customer sent to support"];
    return [OVER, "Nothing cancelled, customer told"];
  }
  if (s.loc === "ask_which") return [BEFORE, "Asked which order"];
  if (s.loc === "whole_only") return [BEFORE, "Told only the whole order can be cancelled"];
  if (s.loc === "proposed") return [BEFORE, "Proposal waiting for yes"];
  if (!s.confirmed) return [BEFORE, s.ever_proposed ? "Proposal waiting for yes" : "Looking up orders"];
  if (s.fu_n) return [AFTER, "Handing to store staff"];
  if (s.refund_n) return [AFTER, "Refunding"];
  if (s.cancel_last === "timeout") return [AFTER, "Cancel unanswered, checking"];
  return [AFTER, "Cancelling"];
};

// Phase colors: where the conversation is, and how it ended.
export const group = ({ s }) => {
  if (s.loc === "end") {
    if (s.told.includes("refund_ok")) return "refunded";
    if (s.told.includes("staff_will_follow") || s.told.includes("staff_unconfirmed")) return "handed off";
    return "nothing cancelled";
  }
  if (s.loc === "setup" || s.loc === "turn1") return "start";
  return s.confirmed ? "after yes" : "before cancel";
};

export const colors = {
  start: "tan",
  "before cancel": "blue",
  "after yes": "orange",
  refunded: "teal",
  "handed off": "yellow",
  "nothing cancelled": "pink",
};

// ------------------------------------------------------------ step labels from model.py

const SAYS = {
  orders_unavailable: "your orders cannot be checked right now",
  no_such_order: "no order with that number is on your account",
  shipped_returns: "the order has shipped and cannot be cancelled; returns are a separate process",
  already_cancelled: "the order is already cancelled",
  whole_only: "only the whole order can be cancelled",
  refund_terms: "the refund is the total paid, to the order's payment method",
  cancelled: "the order is cancelled",
  not_cancelled: "the order was not cancelled",
  cancel_unknown: "it is not known whether the order was cancelled",
  refund_ok: "the refund is pending or issued, with its id",
  refund_not_issued: "the refund has not been issued",
  refund_unknown: "the refund's status is unknown",
  staff_will_follow: "store staff will follow up",
  staff_unconfirmed: "it could not confirm store staff were told; contact Harbor Goods support",
};

const ASKS = {
  number: "customer asks to cancel the order by its number",
  unnamed: "customer asks to cancel 'my order' without saying which",
  unknown: "customer gives an order number not on the account",
  partial: "customer asks to cancel only some items",
  other_method: "customer asks for the refund to go to another payment method",
  other_amount: "customer asks for a different refund amount",
};

const REASON = {
  refund_not_issued: "refund not issued",
  refund_status_unknown: "refund status unknown",
  cancellation_unknown: "cancellation unknown",
};

const setupLabel = (t) => {
  if (t.order === "open") return t.other_open
    ? "The order is placed or processing, and a second open order exists"
    : "The order is placed or processing";
  if (t.order === "shipped") return "The order has shipped or been delivered";
  return t.refund === "ok"
    ? "The order is already cancelled, refund pending or issued"
    : "The order is already cancelled, its refund failed";
};

const WORDS = { open: "placed or processing", shipped: "shipped", cancelled: "cancelled" };

// lookup_says(s) from model.py
const lookupSays = (f) => {
  if (f.cancel_n && !f.refund_n) return "lookup shows the order " + WORDS[f.order];
  if (f.refund_n) return {
    none: "lookup shows no refund for the order",
    ok: "lookup shows the order's refund pending or issued",
    failed: "lookup shows the order's refund failed",
  }[f.refund];
  let w = WORDS[f.order];
  if (f.order === "cancelled")
    w += { ok: ", refund pending or issued", failed: ", refund failed", none: ", no refund" }[f.refund];
  return "lookup shows the order " + w;
};

const cancelLabel = (f, t) => {
  if (t.cancel_last === "cancelled") return "cancel call returns cancelled";
  if (t.cancel_last === "not_cancellable") return "cancel call rejected: the order has shipped";
  if (t.cancel_last === "not_found") return "cancel call reports the order not found";
  return t.order === "cancelled" && f.order !== "cancelled"
    ? "cancel call times out (it did cancel)"
    : "cancel call times out (nothing changed)";
};

const refundLabel = (f, t) => {
  const r = t.refund_last;
  if (r === "ok") return "refund call returns the refund pending or issued";
  if (r === "failed") return "refund call returns the refund failed";
  if (r === "unavailable") return "refund call: payment provider temporarily unavailable";
  if (r === "not_cancelled") return "refund call: the order is not cancelled";
  if (t.refund === "ok" && f.refund !== "ok") return "refund call times out (refund created, pending or issued)";
  if (t.refund === "failed" && f.refund !== "failed") return "refund call times out (refund created, failed)";
  return "refund call times out (nothing created)";
};

const followupLabel = (f, t) => {
  if (t.fu_last === "created") return "follow-up task created";
  return t.task && !f.task ? "follow-up call times out (task created)" : "follow-up call times out (no task)";
};

const TERMS = "agent states the refund terms and proposes the whole order, refund to its payment method";

// The agent's one step: which Python label it carries, from what it changed.
const agentLabel = (f, t) => {
  if (t.loc === "end") {
    const claims = t.told.filter((c) => !f.told.includes(c)).sort();
    return "agent tells the customer: " + claims.map((c) => SAYS[c]).join("; ");
  }
  if (t.pending === "lookup") return "agent looks up the customer's orders";
  if (t.pending === "cancel") return t.cancel_n === 1 ? "agent sends the cancel" : "agent sends the cancel again";
  if (t.pending === "refund") return t.refund_n === 1 ? "agent sends the refund" : "agent sends the refund again";
  if (t.pending === "followup")
    return `agent asks store staff to follow up${f.fu_n ? " again" : ""} (${REASON[t.fu_reason]})`;
  if (t.loc === "ask_which") return "agent asks which order";
  if (t.loc === "whole_only") return "agent says only the whole order can be cancelled";
  // propose: the branch of before_cancel() that fired
  if (t.method === "other") return "agent proposes the changed proposal: refund to the other payment method";
  if (f.change === "switch") return "agent proposes: cancel the whole order, refund the total to its payment method";
  if (f.change === "method") return TERMS;
  if (f.request === "unnamed" && !f.named) return "agent proposes the only open order";
  if (f.request === "other_method" || f.request === "other_amount") return TERMS;
  return "agent proposes: cancel the whole order, refund the total to its payment method";
};

const FIXED = {
  OrderShips: "order ships",
  LookupGetsNoAnswer: "lookup gets no answer",
  LookupAnswersWithoutOrder: "lookup answers without the order",
  CustomerNamesOrder: "customer names the order",
  CustomerAsksWhole: "customer asks to cancel the whole order",
  CustomerKeepsOrder: "customer keeps the order",
  CustomerSaysYes: "customer says yes",
  CustomerNamesOtherOrder: "customer names the other open order instead",
  CustomerSaysYesButNamesOther: "customer says yes but names the other open order",
  CustomerAsksOtherMethod: "customer asks for the refund to go to another payment method instead",
  CustomerWithdraws: "customer withdraws",
  CustomerStopsAnswering: "customer stops answering",
  Done: "the conversation is over",
};

export const step = (action, { s: f }, { s: t }) => {
  if (action in FIXED) return FIXED[action];
  if (action === "Setup") return setupLabel(t);
  if (action === "LookupShows") return lookupSays(f);
  if (action === "CancelAnswers") return cancelLabel(f, t);
  if (action === "RefundAnswers") return refundLabel(f, t);
  if (action === "FollowupAnswers") return followupLabel(f, t);
  if (action === "CustomerAsks") return ASKS[t.request];
  if (action === "AgentActs") return agentLabel(f, t);
  throw new Error(`no label for ${action}`);
};
