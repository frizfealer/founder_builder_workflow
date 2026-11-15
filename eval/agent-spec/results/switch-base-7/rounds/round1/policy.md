# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Customer asked | The order is placed or processing |
|  |  |  | The order has shipped or been delivered |
|  |  |  | The order is already cancelled |
|  |  |  | No order of the customer's has that number |
|  |  |  | The customer has two open orders |
| A2 | Customer asked | Looking up orders | customer asks to cancel an order by its number |
|  |  |  | customer asks to cancel "my order" without saying which |
| A3 | Handing off to staff | Handed to staff, customer told | agent tells the customer: the order is cancelled; the refund the order system shows is for the amount it returned, not the amount the customer confirmed; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, but the refund is not issued and not confirmed yet; store staff will follow up |
|  |  |  | agent tells the customer: the order system says the order is not cancelled, so no refund was issued; store staff will follow up |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled; no refund was issued; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled; it is not known whether the refund was issued; store staff will follow up |
| A4 | Handing off to staff | Staff not reached, customer told | agent tells the customer: the order is cancelled; the refund the order system shows is for the amount it returned, not the amount the customer confirmed; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, but the refund is not issued and not confirmed yet; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order system says the order is not cancelled, so no refund was issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled; no refund was issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled; it is not known whether the refund was issued; please contact Harbor Goods support |
| A5 | Looking up orders | Proposal waiting for yes | agent proposes: cancel this order and refund the total paid to the order's payment method |
| A6 | Looking up orders | Nothing changed, customer told | agent tells the customer: it could not look up the orders now; nothing was changed |
|  |  |  | agent tells the customer: the order has shipped, so it cannot be cancelled; returns are a separate process; nothing was changed |
|  |  |  | agent tells the customer: the order is already cancelled; nothing was changed |
|  |  |  | agent tells the customer: none of the customer's orders has that number; nothing was changed |
| A7 | Looking up orders | Asked which order | agent asks which order, naming each open order's number |
| A8 | Proposal waiting for yes | Nothing changed, customer told | agent tells the customer: nothing was changed |
| A9 | Proposal waiting for yes | Cancelling | customer says yes |
| A10 | Proposal waiting for yes | Customer left | customer stops answering |
| A11 | Asked which order | Looking up orders | customer names one of the open orders |
| A12 | Asked which order | Customer left | customer stops answering |
| A13 | Cancelling | Handing off to staff | agent creates a follow-up task for staff (cancellation_unknown) |
| A14 | Cancelling | Nothing changed, customer told | agent tells the customer: the order system does not find that order; nothing was changed |
| A15 | Cancelling | Refunding | agent issues the refund |
| A16 | Cancelling | Order shipped first, customer told | agent tells the customer: the order shipped before it could be cancelled, so it was not cancelled and no refund was issued; returns are a separate process |
| A17 | Refunding | Cancelled and refunded, customer told | agent tells the customer: the order is cancelled and the refund is pending or issued, with its amount and payment method |
| A18 | Refunding | Handing off to staff | agent creates a follow-up task for staff (refund_status_unknown) |
|  |  |  | agent creates a follow-up task for staff (refund_not_issued) |

## Breaks

None.
