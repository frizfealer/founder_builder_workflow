# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Customer asked to cancel | The customer's order is placed or processing |
|  |  |  | The customer's order is placed or processing, and they have another open order |
|  |  |  | The customer's order is shipped or delivered |
|  |  |  | The customer's order is shipped or delivered, and they have another open order |
|  |  |  | The customer's order is already cancelled |
|  |  |  | The customer's order is already cancelled, and they have another open order |
| A2 | Customer asked to cancel | Reading the orders | customer asks to cancel the order by its number |
|  |  |  | customer asks to cancel an order number that is none of theirs |
|  |  |  | customer asks to cancel "my order" without a number |
| A3 | Reading the orders | Proposal waiting for yes | agent states the proposal: order number, refund amount and payment method, and asks for a yes |
|  |  |  | agent states the changed proposal and asks for a yes |
| A4 | Reading the orders | Nothing changed, customer told | agent tells the customer: it cannot see your orders right now; nothing was changed |
|  |  |  | agent tells the customer: no order of yours has that number; nothing was changed |
|  |  |  | agent tells the customer: the order has shipped and cannot be cancelled; returns are a separate process |
|  |  |  | agent tells the customer: the order is already cancelled; nothing was changed |
|  |  |  | agent tells the customer: nothing was changed |
| A5 | Reading the orders | Asked which order | agent asks which order, and proposes nothing |
| A6 | Proposal waiting for yes | Reading the orders | customer says yes and names their other open order |
| A7 | Proposal waiting for yes | Reading the orders | customer says no |
| A8 | Proposal waiting for yes | Cancelling | customer says yes |
| A9 | Proposal waiting for yes | Customer left | customer stops answering |
| A10 | Asked which order | Reading the orders | customer names the order |
| A11 | Asked which order | Customer left | customer stops answering |
| A12 | Cancelling | Nothing changed, customer told | agent tells the customer: the order shipped before it could be cancelled; it was not cancelled and no refund was made; returns are a separate process |
| A13 | Cancelling | Refunding | agent issues the refund |
| A14 | Cancelling | Asking staff to follow up | agent asks staff to follow up: the order was not found |
|  |  |  | agent asks staff to follow up: it is not known whether the order was cancelled |
| A15 | Refunding | Cancelled and refunded, customer told | agent tells the customer: the order is cancelled and the refund was made, with its amount, payment method and status |
| A16 | Refunding | Asking staff to follow up | agent asks staff to follow up: the refund amount differs |
|  |  |  | agent asks staff to follow up: the refund was not issued; issue it by the manual refund process |
|  |  |  | agent asks staff to follow up: the refund status is unknown |
| A17 | Asking staff to follow up | Handed to staff, customer told | agent tells the customer: the order could not be cancelled; nothing was changed; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, and the refund was made for a different amount, the amount the order system returned; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; staff will follow up |
|  |  |  | agent tells the customer: the order could not be cancelled; nothing was changed; please contact Harbor Goods support |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled, and no refund was made; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, and the refund was made for a different amount, the amount the order system returned; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled, and no refund was made; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, and it is not known whether the refund was made; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, and it is not known whether the refund was made; please contact Harbor Goods support |

## Breaks

None.
