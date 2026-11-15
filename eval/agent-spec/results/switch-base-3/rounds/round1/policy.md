# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Customer asked | The customer has one open order |
|  |  |  | The customer has two open orders |
|  |  |  | The customer's order has shipped or been delivered |
|  |  |  | The customer's order is already cancelled |
|  |  |  | The customer has no orders |
| A2 | Customer asked | Looking up orders | customer asks to cancel an order, naming it |
|  |  |  | customer says "cancel my order" without naming it |
|  |  |  | customer gives an order number that matches none of their orders |
|  |  |  | customer asks to cancel some items of an order |
| A3 | Refunding | Cancelled and refunded, customer told | agent tells the customer: the order is cancelled and the refund of the total paid to the payment method is pending or issued, as the order system shows it, with no promise of when it arrives |
| A4 | Refunding | Handing to staff | agent hands the case to staff as "refund amount differs" |
|  |  |  | agent hands the case to staff as "refund not issued" |
| A5 | Refunding | Checking the refund | agent looks up the order and its refund again |
| A6 | Checking the order | Refunding | order lookup shows the order cancelled |
| A7 | Checking the order | Handing to staff | agent hands the case to staff as "cancellation unknown" |
| A8 | Checking the order | Nothing changed, customer told | agent tells the customer: the order has shipped and cannot be cancelled; returns are a separate process; no refund was issued |
| A9 | Checking the order | Cancelling | agent cancels the order once more |
| A10 | Handing to staff | Handed to staff, customer told | agent tells the customer: the order is cancelled and the refund call returned an amount different from the one agreed, which it states; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled and the refund was not issued; store staff will follow up |
|  |  |  | agent tells the customer: the outcome is unknown; no refund was issued; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled and the refund call returned an amount different from the one agreed, which it states; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled and the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the outcome is unknown; no refund was issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled and the refund status is unknown; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled and the refund shown is for an amount different from the one agreed, which it states; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled and the refund is not confirmed yet; store staff will follow up |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled; no refund was issued; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled and the refund status is unknown; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled and the refund shown is for an amount different from the one agreed, which it states; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled and the refund is not confirmed yet; please contact Harbor Goods support |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled; no refund was issued; please contact Harbor Goods support |
| A11 | Checking the refund | Cancelled and refunded, customer told | agent tells the customer: the order is cancelled and the refund of the total paid to the payment method is pending or issued, as the order system shows it, with no promise of when it arrives |
| A12 | Checking the refund | Handing to staff | agent hands the case to staff as "refund status unknown" |
|  |  |  | agent hands the case to staff as "refund amount differs" |
|  |  |  | agent hands the case to staff as "refund not issued" |
| A13 | Looking up orders | Proposal waiting for yes | agent proposes: cancel order <number> and refund <total paid> to <payment method>, and asks for a yes |
| A14 | Looking up orders | Nothing changed, customer told | agent tells the customer: no order of theirs has that number; nothing changed |
|  |  |  | agent tells the customer: the order has shipped and cannot be cancelled; returns are a separate process; nothing changed |
|  |  |  | agent tells the customer: the order is already cancelled; nothing changed |
|  |  |  | agent tells the customer: it found no order to cancel; nothing changed |
| A15 | Looking up orders | Asked about the whole order | agent tells the customer: only the whole order can be cancelled |
| A16 | Looking up orders | Asked which order | agent asks which order to cancel |
| A17 | Proposal waiting for yes | Nothing changed, customer told | agent tells the customer: the order was not cancelled; nothing changed |
| A18 | Proposal waiting for yes | Cancelling | customer says yes |
| A19 | Proposal waiting for yes | Customer left | customer stops answering |
| A20 | Proposal waiting for yes | Asked instead or as well | agent asks whether the customer means the other order instead of the first, or as well |
| A21 | Asked about the whole order | Looking up orders | customer asks to cancel the whole order |
| A22 | Asked about the whole order | Customer left | customer stops answering |
| A23 | Asked which order | Looking up orders | customer names one of the open orders |
| A24 | Asked which order | Customer left | customer stops answering |
| A25 | Cancelling | Refunding | cancel call answers cancelled |
| A26 | Cancelling | Checking the order | agent looks up the order |
| A27 | Cancelling | Nothing changed, customer told | agent tells the customer: the order has shipped and cannot be cancelled; returns are a separate process; no refund was issued |
|  |  |  | agent tells the customer: it could not find the order; nothing changed |
| A28 | Asked instead or as well | Proposal waiting for yes | customer means the other order instead |
| A29 | Asked instead or as well | Cancelling | customer means the other order as well |
| A30 | Asked instead or as well | Customer left | customer stops answering |

## Breaks

None.
