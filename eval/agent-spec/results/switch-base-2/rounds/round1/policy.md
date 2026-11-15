# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Customer asked | The customer has one open order |
|  |  |  | The customer has two open orders |
|  |  |  | The customer's order has shipped |
|  |  |  | The customer's order is already cancelled |
| A2 | Customer asked | Reading the orders | customer asks to cancel an order by its number |
|  |  |  | customer asks to cancel their order without a number |
|  |  |  | customer asks to cancel an order number that matches none of their orders |
|  |  |  | customer asks to cancel only some items of an order |
| A3 | Handing to staff | Handed to staff, customer told | agent tells the customer: the order is cancelled; the order system reported a refund of a different amount, which it names; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled; the refund was not issued; staff will follow up |
|  |  |  | agent tells the customer: the refund was not issued; staff will follow up |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled; no refund was issued; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled; the order system reported a refund of a different amount, which it names; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled; the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled; no refund was issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled; the refund status is unknown; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled; the refund is not confirmed yet; staff will follow up |
|  |  |  | agent tells the customer: the order was not cancelled; no refund was issued; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled; the refund status is unknown; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled; the refund is not confirmed yet; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order was not cancelled; no refund was issued; please contact Harbor Goods support |
| A4 | Reading the orders | Proposal waiting for yes | agent proposes: cancel this order and refund the order total to its payment method |
|  |  |  | agent states the changed proposal and asks again |
| A5 | Reading the orders | Nothing changed, customer told | agent tells the customer: I cannot see your orders right now; nothing was changed; please try again later |
|  |  |  | agent tells the customer: the order number matches none of your orders; nothing was changed |
|  |  |  | agent tells the customer: only the whole order can be cancelled |
|  |  |  | agent tells the customer: the order has shipped and cannot be cancelled; returns are a separate process |
|  |  |  | agent tells the customer: the order is already cancelled; nothing was changed |
|  |  |  | agent tells the customer: nothing was changed |
| A6 | Reading the orders | Asked which order | agent asks which order |
| A7 | Proposal waiting for yes | Reading the orders | customer withdraws |
|  |  |  | customer says yes and names the other open order |
| A8 | Proposal waiting for yes | Cancelling | customer says yes |
| A9 | Proposal waiting for yes | Customer left | customer stops answering |
| A10 | Asked which order | Reading the orders | customer names one of the open orders |
| A11 | Asked which order | Customer left | customer stops answering |
| A12 | Cancelling | Handing to staff | agent asks staff to follow up: cancellation unknown |
|  |  |  | agent asks staff to follow up: order not cancelled |
| A13 | Cancelling | Nothing changed, customer told | agent tells the customer: the order has shipped and was not cancelled; returns are a separate process; no refund was issued |
|  |  |  | agent tells the customer: I cannot find that order; nothing was changed; no refund was issued |
| A14 | Cancelling | Refunding | cancel call answers cancelled |
|  |  |  | read shows the order cancelled |
| A15 | Refunding | Handing to staff | agent asks staff to follow up: refund differs |
|  |  |  | agent asks staff to follow up: refund not issued |
|  |  |  | agent asks staff to follow up: refund status unknown |
| A16 | Refunding | Cancelled and refund pending or issued, customer told | agent tells the customer: the order is cancelled and the refund of the order total to its payment method is pending or issued |

## Breaks

None.
