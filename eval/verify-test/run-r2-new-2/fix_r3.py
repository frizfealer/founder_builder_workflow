"""Round-3 fixes for the r2-new-2 trial. Same mechanics as fix_r2.py."""
import re
import sys

path = sys.argv[1]
round1 = open(sys.argv[2]).read()
text = open(path).read()


def span(t, sid):
    m = re.search(rf"^##### {sid} — .*?(?=^##### |^## 5\. )", t, re.S | re.M)
    assert m, sid
    return m.start(), m.end()


def sub(scope, old, new):
    global text
    s, e = span(text, scope) if scope else (0, len(text))
    seg = text[s:e]
    assert seg.count(old) == 1, (scope, old[:60], seg.count(old))
    text = text[:s] + seg.replace(old, new) + text[e:]


# M28: the ask-first path gets an optional answer in CO-S28
sub("CO-S28", "- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.\n",
    "- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.\n- Q: Which order would you like to cancel? A: <order>. (optional)\n")
sub("CO-S28", "so the agent may propose it without asking which;",
    "so the agent may propose it without asking which, and a which-order question is answered with that order;")

# M29: revert the OrderNotCancelled row to its round-1 text; its handling is the user's open question
sub(None, "| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer no refund was issued and store staff will follow up. | CO-05, CO-07, G-03 |",
    "| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3 and no CO-A4; tell the customer no refund was issued. | CO-05, G-03 |")

# M30: CO-S14 back to its round-1 block (the list_orders contract cannot omit an owned order)
s1, e1 = span(round1, "CO-S14")
s, e = span(text, "CO-S14")
text = text[:s] + round1[s1:e1] + text[e:]

# M31: reporting an already cancelled order is not claiming to have cancelled it
sub(None, "proposes no cancellation, and never says an order was cancelled. | CO-S29 |",
    "proposes no cancellation, and never says it cancelled an order in this conversation. | CO-S29 |")
sub("CO-S29", "that returns are a separate process, and never said an order was cancelled.",
    "that returns are a separate process, and never said it cancelled an order in this conversation.")

open(path, "w").write(text)
print("applied")
