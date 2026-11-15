---- MODULE CleanPolicy ----
\* Translation of new-format/seeded-clean/model.py (defects fixed). One order, one conversation.
\* The Python state S is the record s; Python replace(s, ...) is [s EXCEPT ...].
\* brk holds the step rules broken by the step just taken, as <<rule id, reason>>: the Python
\* checker tests step rules on each (state, step, next state), and a TLA+ invariant sees only a
\* state, so the step that reaches a state records what it broke.

EXTENDS Integers, Sequences

VARIABLES s, brk
vars == <<s, brk>>

ASKS == {"number", "unnamed", "unknown", "partial", "other_method", "other_amount"}

SETUPS == { <<"open", "none", FALSE>>, <<"open", "none", TRUE>>, <<"shipped", "none", FALSE>>,
            <<"cancelled", "ok", FALSE>>, <<"cancelled", "failed", FALSE>> }

FINAL(r) == IF r = "cancellation_unknown" THEN {"cancel_unknown"}
            ELSE IF r = "refund_not_issued" THEN {"cancelled", "refund_not_issued"}
            ELSE {"cancelled", "refund_unknown"}

Init ==
    /\ s = [loc |-> "setup", pending |-> "", order |-> "", refund |-> "none", task |-> FALSE,
            other_open |-> FALSE, request |-> "", named |-> FALSE, asked_whole |-> FALSE,
            change |-> "", seen |-> "", seen_refund |-> "", method |-> "", ever_proposed |-> FALSE,
            confirmed |-> FALSE, cancel_n |-> 0, cancel_last |-> "", after_cancel |-> "",
            cancel_seen |-> FALSE, refund_n |-> 0, refund_last |-> "", after_refund |-> "",
            fu_n |-> 0, fu_last |-> "", fu_reason |-> "", told |-> {}]
    /\ brk = {}

\* ------------------------------------------------------------------ rule helpers (on s)

CancelledKnown == s.cancel_seen \/ (s.seen = "cancelled" /\ s.request # "unknown")
RefundShownOk == s.refund_last = "ok" \/ s.after_refund = "ok" \/ s.seen_refund = "ok"
FurtherRefundAllowed ==
    IF ~(s.confirmed /\ CancelledKnown) THEN FALSE
    ELSE s.refund_n = 0 \/ (s.refund_n = 1 /\ s.refund_last \in {"unavailable", "timeout"})
RefundUnfinished == s.cancel_seen /\ ~RefundShownOk /\ ~FurtherRefundAllowed
CannotTellCancelled ==
    /\ s.cancel_n # 0 /\ s.cancel_last = "timeout" /\ ~s.cancel_seen
    /\ s.after_cancel \in {"", "timeout", "missing"}

\* ------------------------------------------------------------------ step rules ("" = holds)

ReasonSays(r) == IF r = "refund_not_issued" THEN "refund not issued"
                 ELSE IF r = "refund_status_unknown" THEN "refund status unknown"
                 ELSE "cancellation unknown"

R01Step(k, t) == IF k = "propose" /\ s.seen # "open"
                 THEN "proposed without a lookup showing the order placed or processing" ELSE ""
R02Step(k) == IF k # "propose" THEN ""
              ELSE IF s.request = "unknown" THEN "proposed for an order number not on the account"
              ELSE IF s.other_open /\ s.request = "unnamed" /\ ~s.named
                   THEN "proposed while two orders are open and the customer has not said which"
              ELSE ""
R03Step(k, t) == IF k # "propose" THEN ""
                 ELSE IF t.method # "original" THEN "proposed a refund to another payment method"
                 ELSE IF s.request = "partial" /\ ~s.asked_whole
                      THEN "proposed after a part-order request before the customer asked for the whole order"
                 ELSE IF s.request \in {"other_method", "other_amount"} /\ "refund_terms" \notin t.told
                      THEN "proposed after a request for another refund without stating the refund terms"
                 ELSE ""
R04Step(k) == IF k \in {"call_cancel", "call_refund"} /\ ~s.confirmed
              THEN "cancel or refund sent without a confirmation of the full proposal" ELSE ""
R05Step(k) == IF k = "call_refund" /\ ~CancelledKnown
              THEN "refund sent for an order not returned or shown cancelled" ELSE ""
R06Step(k, out) ==
    IF k = "call_cancel" /\ s.cancel_n >= 2 THEN "third cancel"
    ELSE IF k = "call_cancel" /\ s.cancel_n = 1 /\ ~(s.cancel_last = "timeout" /\ s.after_cancel = "open")
         THEN "second cancel without a lookup after the first showing the order still open"
    ELSE IF k = "call_refund" /\ s.refund_n >= 2 THEN "third refund"
    ELSE IF k = "call_refund" /\ s.refund_n = 1 /\ s.refund_last \notin {"unavailable", "timeout"}
         THEN "second refund after an answer that forbids it"
    ELSE IF k = "call_followup" /\ s.fu_n >= 2 THEN "third hand-off"
    ELSE IF k = "call_followup" /\ s.fu_n = 1 /\ ~(s.fu_last = "timeout" /\ out = s.fu_reason)
         THEN "second hand-off without the first going unanswered, or with another reason"
    ELSE ""
R07Step(k, out) ==
    IF k # "call_followup" \/ s.fu_n # 0 THEN ""
    ELSE IF RefundUnfinished /\ out \in {"refund_not_issued", "refund_status_unknown"} THEN ""
    ELSE IF CannotTellCancelled /\ out = "cancellation_unknown" THEN ""
    ELSE "hand-off (" \o ReasonSays(out) \o ") in a situation the rule does not name"

StepBreaks(k, out, t) ==
    LET all == { <<"R-01", R01Step(k, t)>>, <<"R-02", R02Step(k)>>, <<"R-03", R03Step(k, t)>>,
                 <<"R-04", R04Step(k)>>, <<"R-05", R05Step(k)>>, <<"R-06", R06Step(k, out)>>,
                 <<"R-07", R07Step(k, out)>> }
    IN {b \in all : b[2] # ""}

\* Every step: the next state is t, and brk records the step rules it broke.
Go(k, out, t) == s' = t /\ brk' = StepBreaks(k, out, t)

\* ------------------------------------------------------------------ outside world

Setup == s.loc = "setup" /\ \E x \in SETUPS :
    Go("setup", "", [s EXCEPT !.loc = "turn1", !.order = x[1], !.refund = x[2], !.other_open = x[3]])

OrderShips == s.order = "open" /\ (s.loc = "proposed" \/ s.pending = "cancel")
              /\ Go("ship", "", [s EXCEPT !.order = "shipped"])

LookupResult(answer) ==
    LET t == [s EXCEPT !.pending = ""] IN
    IF s.cancel_n = 0 THEN
        IF answer = "timeout" THEN [t EXCEPT !.seen = "timeout"]
        ELSE [t EXCEPT !.seen = s.order, !.seen_refund = s.refund]
    ELSE IF s.refund_n = 0 THEN
        LET seen == IF answer = "shown" THEN s.order ELSE answer IN
        [t EXCEPT !.after_cancel = seen, !.cancel_seen = (s.cancel_seen \/ seen = "cancelled")]
    ELSE [t EXCEPT !.after_refund = IF answer = "shown" THEN s.refund ELSE "timeout"]

LookupShows == s.pending = "lookup" /\ Go("lookup", "shown", LookupResult("shown"))
LookupGetsNoAnswer == s.pending = "lookup" /\ Go("lookup", "timeout", LookupResult("timeout"))
LookupAnswersWithoutOrder == s.pending = "lookup" /\ s.cancel_n # 0 /\ s.refund_n = 0
                             /\ Go("lookup", "missing", LookupResult("missing"))

CancelOutcomes == IF s.order = "open" THEN {"cancelled", "timeout_done", "timeout_none"}
                  ELSE IF s.order = "shipped" THEN {"not_cancellable", "timeout_none"}
                  ELSE {"cancelled", "timeout_none"}

CancelAnswers == s.pending = "cancel" /\ \E o \in CancelOutcomes :
    LET t0 == [s EXCEPT !.pending = "",
                        !.cancel_last = IF o \in {"timeout_done", "timeout_none"} THEN "timeout" ELSE o]
        t == IF o = "cancelled" THEN [t0 EXCEPT !.order = "cancelled", !.cancel_seen = TRUE]
             ELSE IF o = "timeout_done" THEN [t0 EXCEPT !.order = "cancelled"]
             ELSE t0
    IN Go("cancel", o, t)

RefundOutcomes == IF s.refund = "ok" THEN {"ok", "timeout_none"}
                  ELSE IF s.refund = "failed" THEN {"failed", "timeout_none"}
                  ELSE IF s.order = "cancelled"
                       THEN {"ok", "failed", "unavailable", "timeout_ok", "timeout_failed", "timeout_none"}
                  ELSE {"not_cancelled", "timeout_none"}

RefundAnswers == s.pending = "refund" /\ \E o \in RefundOutcomes :
    LET t0 == [s EXCEPT !.pending = "",
                        !.refund_last = IF o \in {"timeout_ok", "timeout_failed", "timeout_none"}
                                        THEN "timeout" ELSE o]
        t == IF o \in {"ok", "timeout_ok"} THEN [t0 EXCEPT !.refund = "ok"]
             ELSE IF o \in {"failed", "timeout_failed"} THEN [t0 EXCEPT !.refund = "failed"]
             ELSE t0
    IN Go("refund", o, t)

FollowupOutcomes == IF s.task THEN {"created", "timeout_none"}
                    ELSE {"created", "timeout_created", "timeout_none"}

FollowupAnswers == s.pending = "followup" /\ \E o \in FollowupOutcomes :
    Go("followup", o, [s EXCEPT !.pending = "",
                                !.fu_last = IF o = "created" THEN "created" ELSE "timeout",
                                !.task = (s.task \/ o \in {"created", "timeout_created"})])

\* ------------------------------------------------------------------ the customer

CustomerAsks == s.loc = "turn1" /\ \E req \in ASKS :
    /\ (req # "unnamed" \/ s.order = "open")
    /\ Go("ask", req, [s EXCEPT !.loc = "agent", !.request = req, !.named = (req # "unnamed")])

CustomerNamesOrder == s.loc = "ask_which" /\ Go("which", "", [s EXCEPT !.loc = "agent", !.named = TRUE])
CustomerAsksWhole == s.loc = "whole_only" /\ Go("whole", "", [s EXCEPT !.loc = "agent", !.asked_whole = TRUE])
CustomerKeepsOrder == s.loc = "whole_only" /\ Go("whole", "", [s EXCEPT !.loc = "end"])
CustomerSaysYes == s.loc = "proposed" /\ Go("reply", "", [s EXCEPT !.loc = "agent", !.confirmed = TRUE])
CustomerNamesOtherOrder == s.loc = "proposed" /\ s.other_open
                           /\ Go("reply", "", [s EXCEPT !.loc = "agent", !.change = "switch"])
CustomerSaysYesButNamesOther == s.loc = "proposed" /\ s.other_open
                                /\ Go("reply", "", [s EXCEPT !.loc = "agent", !.change = "switch"])
CustomerAsksOtherMethod == s.loc = "proposed" /\ Go("reply", "", [s EXCEPT !.loc = "agent", !.change = "method"])
CustomerWithdraws == s.loc = "proposed" /\ Go("reply", "", [s EXCEPT !.loc = "end"])
CustomerStopsAnswering == s.loc \in {"ask_which", "proposed"} /\ Go("reply", "", [s EXCEPT !.loc = "end"])

\* ------------------------------------------------------------------ the agent (rules.md)

Tell(claims) == [k |-> "tell", out |-> "", t |-> [s EXCEPT !.loc = "end", !.told = s.told \cup claims]]
CallLookup == [k |-> "call_lookup", out |-> "", t |-> [s EXCEPT !.pending = "lookup"]]
CallCancel(n) == [k |-> "call_cancel", out |-> "",
                  t |-> [s EXCEPT !.pending = "cancel", !.cancel_n = n, !.after_cancel = ""]]
CallRefund == [k |-> "call_refund", out |-> "", t |-> [s EXCEPT !.pending = "refund", !.refund_n = 1]]
CallRefundAgain == [k |-> "call_refund", out |-> "",
                    t |-> [s EXCEPT !.pending = "refund", !.refund_n = 2, !.after_refund = ""]]
Followup(r) == [k |-> "call_followup", out |-> r,
                t |-> [s EXCEPT !.pending = "followup", !.fu_n = s.fu_n + 1, !.fu_reason = r]]
Propose(m, extra) == [k |-> "propose", out |-> "",
                      t |-> [s EXCEPT !.loc = "proposed", !.ever_proposed = TRUE, !.method = m,
                                      !.change = "", !.told = s.told \cup extra]]
AskWhich == [k |-> "ask_which", out |-> "", t |-> [s EXCEPT !.loc = "ask_which"]]
WholeOnly == [k |-> "whole_only", out |-> "",
              t |-> [s EXCEPT !.loc = "whole_only", !.told = s.told \cup {"whole_only"}]]

BeforeCancel ==
    LET extra == IF s.request = "partial" THEN {"whole_only"}
                 ELSE IF s.request \in {"other_method", "other_amount"} THEN {"refund_terms"}
                 ELSE {}
    IN
    IF s.seen = "" THEN CallLookup
    ELSE IF s.seen = "timeout" THEN Tell({"orders_unavailable"})
    ELSE IF s.request = "unknown" THEN Tell({"no_such_order"})
    ELSE IF s.seen = "shipped" THEN Tell({"shipped_returns"} \cup extra)
    ELSE IF s.seen = "cancelled" THEN Tell({"already_cancelled"} \cup extra)
    ELSE IF s.change = "switch" THEN Propose("original", {})
    ELSE IF s.change = "method" THEN Propose("original", {"refund_terms"})
    ELSE IF s.request = "unnamed" /\ ~s.named THEN (IF s.other_open THEN AskWhich ELSE Propose("original", {}))
    ELSE IF s.request = "partial" /\ ~s.asked_whole THEN WholeOnly
    ELSE IF s.request \in {"other_method", "other_amount"} THEN Propose("original", {"refund_terms"})
    ELSE Propose("original", {})

AfterCancel ==
    IF s.cancel_last = "cancelled" THEN {CallRefund}
    ELSE IF s.cancel_last = "not_cancellable" THEN {Tell({"shipped_returns", "not_cancelled"})}
    ELSE IF s.cancel_last = "not_found" THEN {Tell({"not_cancelled"})}
    ELSE IF s.cancel_n = 2 THEN {Followup("cancellation_unknown")}
    ELSE IF s.after_cancel = "" THEN {CallLookup}
    ELSE IF s.after_cancel = "cancelled" THEN {CallRefund}
    ELSE IF s.after_cancel = "open" THEN {CallCancel(2)}
    ELSE IF s.after_cancel = "shipped" THEN {Tell({"shipped_returns", "not_cancelled"})}
    ELSE {Followup("cancellation_unknown")}

AfterRefund ==
    IF s.refund_last = "ok" THEN {Tell({"cancelled", "refund_ok"})}
    ELSE IF s.refund_last \in {"failed", "not_cancelled"} THEN {Followup("refund_not_issued")}
    ELSE IF s.refund_last = "unavailable"
         THEN (IF s.refund_n = 1 THEN {CallRefundAgain} ELSE {Followup("refund_not_issued")})
    ELSE IF s.refund_n = 1 THEN {CallRefundAgain}
    ELSE IF s.after_refund = "" THEN {CallLookup}
    ELSE IF s.after_refund = "ok" THEN {Tell({"cancelled", "refund_ok"})}
    ELSE IF s.after_refund \in {"failed", "none"} THEN {Followup("refund_not_issued")}
    ELSE {Followup("refund_status_unknown")}

\* The agent's steps in this state: one, or none (a state where the table has no row).
AgentChoices ==
    IF s.loc # "agent" \/ s.pending # "" THEN {}
    ELSE IF s.cancel_n = 0 /\ ~s.confirmed THEN {BeforeCancel}
    ELSE IF s.cancel_n = 0 THEN {CallCancel(1)}
    ELSE IF s.refund_n = 0 /\ s.fu_n = 0 THEN AfterCancel
    ELSE IF s.fu_n = 0 THEN AfterRefund
    ELSE IF s.fu_last = "created" THEN {Tell(FINAL(s.fu_reason) \cup {"staff_will_follow"})}
    ELSE IF s.fu_n = 1 THEN {Followup(s.fu_reason)}
    ELSE {Tell(FINAL(s.fu_reason) \cup {"staff_unconfirmed"})}

AgentActs == \E c \in AgentChoices : Go(c.k, c.out, c.t)

\* The conversation is over: no step out, and not a deadlock.
Done == s.loc = "end" /\ UNCHANGED vars

Next ==
    \/ Setup \/ OrderShips
    \/ LookupShows \/ LookupGetsNoAnswer \/ LookupAnswersWithoutOrder
    \/ CancelAnswers \/ RefundAnswers \/ FollowupAnswers
    \/ CustomerAsks \/ CustomerNamesOrder \/ CustomerAsksWhole \/ CustomerKeepsOrder
    \/ CustomerSaysYes \/ CustomerNamesOtherOrder \/ CustomerSaysYesButNamesOther
    \/ CustomerAsksOtherMethod \/ CustomerWithdraws \/ CustomerStopsAnswering
    \/ AgentActs
    \/ Done

Spec == Init /\ [][Next]_vars

\* ------------------------------------------------------------------ rules as invariants

IsEnd == s.loc = "end"
NoStepBreak(id) == \A b \in brk : b[1] # id

R01End ==
    IF s.request = "unknown" THEN ""
    ELSE IF s.seen = "shipped" /\ ("shipped_returns" \notin s.told \/ s.ever_proposed)
         THEN "shipped order: customer not told it shipped and returns are separate, or something proposed"
    ELSE IF s.seen = "cancelled" /\ ("already_cancelled" \notin s.told \/ s.ever_proposed)
         THEN "cancelled order: customer not told it is already cancelled, or something proposed"
    ELSE IF s.seen = "timeout" /\ s.ever_proposed THEN "proposed although no lookup answered"
    ELSE ""
R02End ==
    IF s.request = "unknown" /\ s.seen \notin {"", "timeout"}
       /\ ("no_such_order" \notin s.told \/ s.ever_proposed)
    THEN "unknown order number: customer not told no such order is on the account" ELSE ""
R03End ==
    IF s.seen \in {"", "timeout"} THEN ""
    ELSE IF s.request = "partial" /\ "whole_only" \notin s.told
         THEN "part-order request: customer never told only the whole order can be cancelled"
    ELSE IF s.request \in {"other_method", "other_amount"} /\ "refund_terms" \notin s.told
         THEN "request for another refund: customer never told the refund terms"
    ELSE ""
R05End ==
    IF (s.cancel_last = "not_cancellable" \/ s.after_cancel = "shipped")
       /\ (~({"shipped_returns", "not_cancelled"} \subseteq s.told) \/ s.refund_n # 0)
    THEN "order shipped after the proposal: customer not told it shipped and was not cancelled"
    ELSE IF s.cancel_last = "not_found" /\ ("not_cancelled" \notin s.told \/ s.refund_n # 0)
    THEN "order not found by the cancel: customer not told it was not cancelled"
    ELSE ""
R07End ==
    IF (RefundUnfinished \/ CannotTellCancelled) /\ s.fu_n = 0
    THEN "order cancelled with no refund shown, or cancellation unknown, and no hand-off made"
    ELSE IF "staff_will_follow" \in s.told /\ s.fu_last # "created"
    THEN "told store staff will follow up before the task was created"
    ELSE ""

\* R-01 Only open orders are proposed
R01 == NoStepBreak("R-01") /\ (IsEnd => R01End = "")
\* R-02 The customer's own order, by number
R02 == NoStepBreak("R-02") /\ (IsEnd => R02End = "")
\* R-03 Whole order, full refund, original payment method
R03 == NoStepBreak("R-03") /\ (IsEnd => R03End = "")
\* R-04 Confirmation precedes cancellation
R04 == NoStepBreak("R-04")
\* R-05 Refund only for a cancelled order
R05 == NoStepBreak("R-05") /\ (IsEnd => R05End = "")
\* R-06 Limited retries
R06 == NoStepBreak("R-06")
\* R-07 Unfinished orders go to store staff
R07 == NoStepBreak("R-07") /\ (IsEnd => R07End = "")

====
