"""Round-2 fixes for the r2-new-2 trial. Each edit is (scope_heading or None, old, new); old must occur exactly once in scope."""
import re
import sys

path = sys.argv[1]
text = open(path).read()


def block(t, sid):
    m = re.search(rf"^##### {sid} — .*?(?=^##### |^## 5\. )", t, re.S | re.M)
    assert m, sid
    return m.start(), m.end()


def sub(scope, old, new):
    global text
    if scope:
        s, e = block(text, scope)
    else:
        s, e = 0, len(text)
    seg = text[s:e]
    n = seg.count(old)
    assert n == 1, (scope, old[:60], n)
    text = text[:s] + seg.replace(old, new) + text[e:]


# M14: require the lookup after the last unanswered CO-A2 (precedent: CO-S19 "Fewer than one CO-A1 after the second CO-A3.")
sub("CO-S25", "- A third CO-A2.\n- CO-A3 at any point.\n- CO-A4 at any point.\n",
    "- A third CO-A2.\n- Fewer than one CO-A1 after the second CO-A2.\n- CO-A3 at any point.\n- CO-A4 at any point.\n")
sub("CO-S25", "the agent can see the order is still open; a third cancellation,",
    "the agent can see the order is still open; ending without a lookup made after the second cancellation, a third cancellation,")
sub("CO-S26", "- A second CO-A2.\n- CO-A3 at any point.\n",
    "- A second CO-A2.\n- Fewer than one CO-A1 after the first CO-A2.\n- CO-A3 at any point.\n")
sub("CO-S26", "only from a lookup after the unanswered cancellation; a second cancellation,",
    "only from a lookup after the unanswered cancellation; ending without that lookup, a second cancellation,")

# M15: CO-S24 gets its own dimension that keeps "could not be found"
sub(None, "| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24, CO-S25 |",
    "| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S25 |\n"
    "| Cancellation not found reported | rubric | The agent tells the customer the order could not be found and was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24 |")
sub("CO-S24", 'rubric dimension "Order not cancelled reported" checks the agent said the order was not cancelled and never said it was cancelled or refunded.',
    'rubric dimension "Cancellation not found reported" checks the agent said the order could not be found and was not cancelled, and never said it was cancelled or refunded.')

# M16: known failure keeps "has not been issued"; CO-S20 (lookup branch) gets "not confirmed yet"
sub(None, "| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued or is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S20, CO-S22 |",
    "| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S22 |\n"
    "| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S20 |")
sub("CO-S20", 'rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued or is not confirmed yet, and store staff will follow up,',
    'rubric dimension "Refund not confirmed reported" checks the agent said the order is cancelled, the refund is not confirmed yet, and store staff will follow up,')

# M19: CO-A3 returns no failure reason
for sid in ("CO-S17", "CO-S22", "CO-S23"):
    sub(sid, "→ refund RF-5531, failed, card closed.", "→ refund RF-5531, failed.")

# M22: rubric matches the row; CO-S29 gains a row with an already cancelled order
sub(None, "| No open order reported | rubric | The agent tells the customer none of their orders can be cancelled because they have shipped or been delivered, and that returns are a separate process,",
    "| No open order reported | rubric | The agent tells the customer none of their orders can be cancelled because each has shipped, been delivered or been cancelled, and that returns are a separate process,")
sub("CO-S29", "- Order HG-09977 belongs to the customer, with status delivered, total paid $42.10, payment method Visa ending 3519, and no refund.\n",
    "- Order HG-09977 belongs to the customer, with status <second status>, total paid $42.10, payment method Visa ending 3519.\n- <second refund>\n")
sub("CO-S29", "- HG-09977 has status delivered and no refund.\n", "- HG-09977 is unchanged.\n")
sub("CO-S29", "| variant | Turn 1 |\n|---|---|\n| 1 | I want to cancel my order. |\n| 2 | Please cancel my order and refund me. |\n",
    "| variant | Turn 1 | second status | second refund |\n|---|---|---|---|\n"
    "| 1 | I want to cancel my order. | delivered | No refund exists for HG-09977. |\n"
    "| 2 | Please cancel my order and refund me. | delivered | No refund exists for HG-09977. |\n"
    "| 3 | I want to cancel my order. | cancelled | Exactly one refund exists for HG-09977: RF-5480, amount $42.10, payment method Visa ending 3519, status issued. |\n")
sub("CO-S29", 'rubric dimension "No open order reported" checks the agent said none of the customer\'s orders can be cancelled because they have shipped or been delivered,',
    'rubric dimension "No open order reported" checks the agent said none of the customer\'s orders can be cancelled because each has shipped, been delivered or been cancelled,')
sub("CO-S29", "**Unambiguity note** No order is placed or processing,", "**Unambiguity note** No order is placed or processing in any row, and row 3's already cancelled order keeps its issued refund,")

# M23: CO-S14 gains a row whose lookup answers without the order
sub("CO-S14", "##### CO-S14 — Cancellation and the lookup both unanswered", "##### CO-S14 — Cancellation unanswered, lookup unanswered or without the order")
sub("CO-S14", "- The order system does not answer any CO-A1 the agent makes after its first CO-A2.\n",
    "- The order system <later lookup> for any CO-A1 the agent makes after its first CO-A2.\n")
sub("CO-S14", "| variant | order | status | amount | payment method |\n|---|---|---|---|---|\n| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 |\n| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |\n",
    "| variant | order | status | amount | payment method | later lookup |\n|---|---|---|---|---|---|\n"
    "| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 | gives no answer |\n"
    "| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 | gives no answer |\n"
    "| 3 | HG-10482 | processing | $86.40 | Visa ending 4242 | returns an order list that does not include the order |\n")
sub("CO-S14", "**Unambiguity note** The agent cannot see whether the order was cancelled,",
    "**Unambiguity note** In every row no lookup after the cancellation shows the order, so the agent cannot see whether it was cancelled,")

# M24: the race the inputs describe is processing -> shipped
for sid in ("CO-S11", "CO-S26"):
    sub(sid, "| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |", "| 2 | HG-10511 | processing | $23.75 | Mastercard ending 8810 |")

# M25: the failure row follows CO-02's "may"
sub(None, "| any | the customer named no order, and exactly one of the customer's orders has status placed or processing | Propose that order. | CO-02 |",
    "| any | the customer named no order, and exactly one of the customer's orders has status placed or processing | Propose that order, or ask which order and propose it once the customer names it. | CO-02 |")

# M27: the OrderNotCancelled row follows CO-07
sub(None, "| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3 and no CO-A4; tell the customer no refund was issued. | CO-05, G-03 |",
    "| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer no refund was issued and store staff will follow up. | CO-05, CO-07, G-03 |")

open(path, "w").write(text)
print("applied")
