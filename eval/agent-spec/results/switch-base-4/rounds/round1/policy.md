# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Customer asked | The order is placed or processing |
|  |  |  | The order is placed or processing, and the customer has a second open order |
|  |  |  | The order has shipped or been delivered |
|  |  |  | The order is already cancelled |
| A2 | Customer asked | Reading the orders | customer asks to cancel the order, naming it |
|  |  |  | customer asks to cancel an order without naming it |
|  |  |  | customer asks to cancel an order number that matches none of their orders |
| A3 | Reading the orders | Proposal waiting for yes | agent proposes: cancel the whole order, naming its number, and refund its total paid to its payment method, and asks for a yes |
| A4 | Reading the orders | Nothing changed, customer told | agent tells the customer: it cannot see your orders right now, and nothing was changed |
|  |  |  | agent tells the customer: no order of yours has that number, and nothing was changed |
|  |  |  | agent tells the customer: the order has shipped, so it cannot be cancelled; returns are a separate process |
|  |  |  | agent tells the customer: the order is already cancelled, and nothing was changed |
| A5 | Reading the orders | Asked which order | agent asks which order to cancel |
| A6 | Proposal waiting for yes | Nothing changed, customer told | agent tells the customer: nothing was changed |
| A7 | Proposal waiting for yes | Cancelling the order | customer says yes |
| A8 | Proposal waiting for yes | Customer left | customer stops answering |
| A9 | Asked which order | Reading the orders | customer names the order |
| A10 | Asked which order | Customer left | customer stops answering |
| A11 | Cancelling the order | Nothing changed, customer told | agent tells the customer: the order has shipped, so it cannot be cancelled; returns are a separate process |
| A12 | Cancelling the order | Refunding | agent issues the refund |
| A13 | Cancelling the order | Handing to staff | agent asks staff to follow up: cancellation unknown |
| A14 | Refunding | Cancelled and refunded, customer told | agent tells the customer: the order is cancelled, and the refund of the confirmed amount to the order's payment method is pending or issued, with its refund id |
| A15 | Refunding | Handing to staff | agent asks staff to follow up: refund amount differs |
|  |  |  | agent asks staff to follow up: refund not issued |
|  |  |  | agent asks staff to follow up: refund status unknown |
| A16 | Handing to staff | Handed to staff, customer told | agent tells the customer: the order could not be cancelled; staff will follow up |
|  |  |  | agent tells the customer: the refund amount the order system returned, which differs from the amount you confirmed; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; staff will follow up |
|  |  |  | agent tells the customer: the order could not be cancelled; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the outcome is unknown; staff will follow up |
|  |  |  | agent tells the customer: the refund amount the order system returned, which differs from the amount you confirmed; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the outcome is unknown; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund's status is unknown; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund is not confirmed yet; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund's status is unknown; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund is not confirmed yet; please contact Harbor Goods support |

## Breaks

None.
