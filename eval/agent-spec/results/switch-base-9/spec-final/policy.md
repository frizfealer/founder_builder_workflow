# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Customer asked | The customer has one open order |
|  |  |  | The customer has two open orders |
|  |  |  | The customer's order has shipped or been delivered |
|  |  |  | The customer's order is already cancelled |
| A2 | Customer asked | Reading the orders | customer asks to cancel an order, naming it |
|  |  |  | customer asks to cancel an order number that is not theirs |
|  |  |  | customer asks to cancel their order without saying which |
| A3 | Handing to staff | Handed to staff, customer told | agent tells the customer: the order is cancelled, and the refund the order system returned is not the amount confirmed; it gives that amount; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, but the refund was not issued; store staff will follow up |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled, and no refund was issued; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, and the refund the order system returned is not the amount confirmed; it gives that amount; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, but the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled, and no refund was issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, and the refund's status is not known; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, but the refund is not confirmed yet; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, and the refund's status is not known; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, but the refund is not confirmed yet; please contact Harbor Goods support |
| A4 | Reading the orders | Proposal waiting for yes | agent proposes cancelling the order and refunding its total paid to its payment method, and asks for a yes |
| A5 | Reading the orders | Nothing changed, customer told | agent tells the customer: it cannot see their orders right now; nothing was changed |
|  |  |  | agent tells the customer: no order with that number is among their orders; nothing was changed |
|  |  |  | agent tells the customer: the order has shipped, so it cannot be cancelled here; returns are a separate process |
|  |  |  | agent tells the customer: the order is already cancelled; nothing was changed |
| A6 | Reading the orders | Asked which order | agent asks which open order to cancel |
| A7 | Proposal waiting for yes | Nothing changed, customer told | agent tells the customer: nothing was changed |
| A8 | Proposal waiting for yes | Cancelling | customer says yes |
| A9 | Proposal waiting for yes | Customer left | customer stops answering |
| A10 | Asked which order | Reading the orders | customer names one of their open orders |
| A11 | Asked which order | Customer left | customer stops answering |
| A12 | Cancelling | Nothing changed, customer told | agent tells the customer: the order has shipped, so it cannot be cancelled here; returns are a separate process |
|  |  |  | agent tells the customer: the order could not be found; nothing was changed |
| A13 | Cancelling | Refunding | agent issues the refund |
| A14 | Cancelling | Checking the records | agent re-reads the order |
| A15 | Refunding | Cancelled and refunded, customer told | agent tells the customer: the order is cancelled and the refund of the total paid is pending or issued to the order's payment method |
| A16 | Refunding | Handing to staff | agent asks staff to follow up: refund amount differs |
|  |  |  | agent asks staff to follow up: refund not issued |
| A17 | Refunding | Checking the records | agent re-reads the order's refund |
| A18 | Checking the records | Cancelled and refunded, customer told | agent tells the customer: the order is cancelled and the refund of the total paid is pending or issued to the order's payment method |
| A19 | Checking the records | Handing to staff | agent asks staff to follow up: cancellation unknown |
|  |  |  | agent asks staff to follow up: refund status unknown |
|  |  |  | agent asks staff to follow up: refund amount differs |
|  |  |  | agent asks staff to follow up: refund not issued |
| A20 | Checking the records | Nothing changed, customer told | agent tells the customer: the order has shipped, so it cannot be cancelled here; returns are a separate process |
|  |  |  | agent tells the customer: the order could not be cancelled; nothing was changed |
| A21 | Checking the records | Cancelling | agent sends the cancel call once more under the same yes |
| A22 | Checking the records | Refunding | agent issues the refund |

## Breaks

None.
