# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Customer asked | The customer has one order that has not shipped |
|  |  |  | The customer has two orders that have not shipped |
|  |  |  | The customer's order has shipped or been delivered |
|  |  |  | The customer's order is already cancelled |
| A2 | Customer asked | Looking up the orders | customer asks to cancel an order, naming it |
|  |  |  | customer asks to cancel only some items of an order |
|  |  |  | customer names an order number that matches none of their orders |
|  |  |  | customer asks to cancel "my order" without saying which |
| A3 | Handing to staff | Handed to staff, customer told | agent tells the customer: the order is cancelled, and the refund amount the refund call returned; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, and the refund was not issued; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, and the refund is not confirmed yet; store staff will follow up |
|  |  |  | agent tells the customer: the outcome of the cancellation is unknown, and no refund was made; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, and the refund status is unknown; store staff will follow up |
|  |  |  | agent tells the customer: the order is not cancelled yet; store staff will follow up |
| A4 | Handing to staff | Staff not reached, customer told | agent tells the customer: the order is cancelled, and the refund amount the refund call returned; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, and the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, and the refund is not confirmed yet; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the outcome of the cancellation is unknown, and no refund was made; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, and the refund status is unknown; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is not cancelled yet; please contact Harbor Goods support |
| A5 | Looking up the orders | Proposal waiting for yes | agent proposes: cancel this order and refund its total paid to the payment method it was paid with; asks for a yes |
|  |  |  | agent proposes the other order and asks for a new yes |
| A6 | Looking up the orders | Nothing changed, customer told | agent tells the customer: it cannot look up the orders right now, and nothing was changed |
|  |  |  | agent tells the customer: no order of theirs has that number, and nothing was changed |
|  |  |  | agent tells the customer: the order has shipped or been delivered and cannot be cancelled; returns are a separate process |
|  |  |  | agent tells the customer: the order is already cancelled, and nothing was changed |
|  |  |  | agent tells the customer: nothing was changed |
| A7 | Looking up the orders | Told only whole orders | agent tells the customer: only the whole order can be cancelled |
| A8 | Looking up the orders | Asked which order | agent lists the orders that have not shipped and asks which one |
| A9 | Proposal waiting for yes | Looking up the orders | customer says no |
| A10 | Proposal waiting for yes | Looking up the orders | customer says yes, but for their other order |
| A11 | Proposal waiting for yes | Cancelling | customer says yes |
| A12 | Proposal waiting for yes | Customer left | customer stops answering |
| A13 | Told only whole orders | Looking up the orders | customer asks to cancel the whole order |
| A14 | Told only whole orders | Customer left | customer stops answering |
| A15 | Asked which order | Looking up the orders | customer names one of the orders |
| A16 | Asked which order | Customer left | customer stops answering |
| A17 | Cancelling | Handing to staff | agent creates a staff follow-up task: cancellation unknown |
| A18 | Cancelling | Nothing changed, customer told | agent tells the customer: the order shipped before it could be cancelled, so it is not cancelled and no refund is made |
|  |  |  | agent tells the customer: the order was not found, and nothing was changed |
| A19 | Cancelling | Refunding | cancel call answers cancelled |
|  |  |  | order read shows the order cancelled |
| A20 | Refunding | Cancelled and refunded, customer told | agent tells the customer: the order is cancelled, and the refund's amount, payment method and status as the order system shows it, with no promise of when the money arrives |
| A21 | Refunding | Handing to staff | agent creates a staff follow-up task: refund status unknown |
|  |  |  | agent creates a staff follow-up task: refund not issued |

## Breaks

None.
