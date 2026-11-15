# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Customer asked | The customer has one order, not yet shipped |
|  |  |  | The customer has one order, already shipped or delivered |
|  |  |  | The customer has one order, already cancelled |
|  |  |  | The customer has two or more orders, none shipped |
|  |  |  | The customer has one order not yet shipped and one shipped |
|  |  |  | The customer has no orders |
| A2 | Customer asked | Looking up orders | customer asks to cancel an order, naming its number |
|  |  |  | customer asks to cancel their order without naming one |
|  |  |  | customer asks to cancel an order number that is not one of theirs |
| A3 | Looking up orders | Proposal waiting for yes | agent proposes cancelling the whole order, with the full refund to its payment method, and asks for a yes |
| A4 | Looking up orders | Nothing changed, customer told | agent tells the customer: it could not look up their orders just now, and nothing was changed |
|  |  |  | agent tells the customer: it cannot find that order among their orders, and nothing was changed |
|  |  |  | agent tells the customer: the order has shipped, so it cannot be cancelled; returns are a separate process |
|  |  |  | agent tells the customer: the order is already cancelled, and nothing was changed |
|  |  |  | agent tells the customer: it finds no orders for them, and nothing was changed |
| A5 | Looking up orders | Asked which order | agent asks which order the customer means |
| A6 | Proposal waiting for yes | Nothing changed, customer told | agent tells the customer: nothing was changed |
| A7 | Proposal waiting for yes | Cancelling | customer says yes |
| A8 | Proposal waiting for yes | Customer left | customer stops answering |
| A9 | Asked which order | Looking up orders | customer names an order not yet shipped |
|  |  |  | customer names the shipped order |
| A10 | Asked which order | Customer left | customer stops answering |
| A11 | Cancelling | Nothing changed, customer told | agent tells the customer: the order has shipped or been delivered, so it was not cancelled and no refund was made; returns are a separate process |
| A12 | Cancelling | Refunding | agent asks the order system to refund the order |
| A13 | Cancelling | Handing to staff | agent creates a staff follow-up task: cancellation unknown |
| A14 | Refunding | Cancelled and refunded, customer told | agent tells the customer: the order is cancelled and the refund of the total paid to the payment method used is pending or issued, as the order system reported it |
| A15 | Refunding | Handing to staff | agent creates a staff follow-up task: refund differs |
|  |  |  | agent creates a staff follow-up task: refund not issued |
|  |  |  | agent creates a staff follow-up task: cancellation unknown |
|  |  |  | agent creates a staff follow-up task: refund status unknown |
| A16 | Handing to staff | Handed to staff, customer told | agent tells the customer: it could not find the order to cancel it, and nothing was changed; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled and the refund the order system made has the amount and payment method it returned, which differ from what the customer agreed; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; store staff will follow up |
|  |  |  | agent tells the customer: the cancellation could not be confirmed, and no refund was made; store staff will follow up |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled, and no refund was made; store staff will follow up |
|  |  |  | agent tells the customer: it could not find the order to cancel it, and nothing was changed; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled and the refund the order system made has the amount and payment method it returned, which differ from what the customer agreed; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the cancellation could not be confirmed, and no refund was made; please contact Harbor Goods support |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled, and no refund was made; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund's status is not known; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund is not confirmed yet; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund's status is not known; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund is not confirmed yet; please contact Harbor Goods support |

## Breaks

None.
