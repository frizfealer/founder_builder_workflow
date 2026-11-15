# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Customer asked | The order is placed or processing |
|  |  |  | The order has shipped or been delivered |
|  |  |  | The order is already cancelled |
| A2 | Customer asked | Reading the orders | customer asks to cancel the order, naming it |
|  |  |  | customer gives an order number that matches none of their orders |
|  |  |  | customer says cancel my order, and has two open orders |
| A3 | Handing to staff | Passed to staff, customer told | agent tells the customer: the order is cancelled, with the refund's amount and payment method as the order system returned them |
|  |  |  | agent tells the customer: the order is cancelled, but the refund was not issued |
|  |  |  | agent tells the customer: the refund was not issued |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled; no refund was issued |
|  |  |  | agent tells the customer: the order is cancelled, but the refund's status is not known |
|  |  |  | agent tells the customer: the order is cancelled, but the refund is not confirmed yet |
|  |  |  | agent tells the customer: the order could not be cancelled right now; no refund was issued |
| A4 | Handing to staff | Customer told to contact support | agent tells the customer: the order is cancelled, with the refund's amount and payment method as the order system returned them; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, but the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled; no refund was issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, but the refund's status is not known; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, but the refund is not confirmed yet; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order could not be cancelled right now; no refund was issued; please contact Harbor Goods support |
| A5 | Reading the orders | Proposal waiting for yes | agent proposes: cancel this order and refund its total paid to its payment method, and asks for a yes |
| A6 | Reading the orders | Proposal waiting for yes | agent treats the yes as void, sends no cancel call, says what the change means, and proposes again |
| A7 | Reading the orders | Nothing changed, customer told | agent tells the customer: it cannot see their orders right now; nothing was changed |
|  |  |  | agent tells the customer: that order number matches none of their orders; nothing was changed |
|  |  |  | agent tells the customer: the order has shipped, so it cannot be cancelled here; returns are a separate process |
|  |  |  | agent tells the customer: the order is already cancelled; nothing was changed |
|  |  |  | agent tells the customer: nothing was changed |
| A8 | Reading the orders | Asked which order | agent asks which order to cancel |
| A9 | Reading the orders | Cancelling | agent cancels the order |
| A10 | Proposal waiting for yes | Reading the orders | customer says yes |
| A11 | Proposal waiting for yes | Reading the orders | customer says yes with a change to the proposal |
| A12 | Proposal waiting for yes | Reading the orders | customer says no |
| A13 | Proposal waiting for yes | Customer left | customer stops answering |
| A14 | Asked which order | Reading the orders | customer names the order |
| A15 | Asked which order | Customer left | customer stops answering |
| A16 | Cancelling | Handing to staff | agent hands the case to staff (cancellation unknown) |
| A17 | Cancelling | Nothing changed, customer told | agent tells the customer: the order shipped before it could be cancelled; it was not cancelled and no refund was issued |
|  |  |  | agent tells the customer: it could not find that order; no refund was issued |
| A18 | Cancelling | Refunding | agent issues the refund |
| A19 | Refunding | Handing to staff | agent hands the case to staff (refund status unknown) |
|  |  |  | agent hands the case to staff (refund not issued) |
| A20 | Refunding | Cancelled and refunded, customer told | agent tells the customer: the order is cancelled, with the refund's amount, payment method, status and refund id as the order system returned them |

## Breaks

None.
