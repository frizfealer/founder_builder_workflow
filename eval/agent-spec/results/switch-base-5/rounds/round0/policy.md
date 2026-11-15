# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Customer asked | The customer's order is placed or processing |
|  |  |  | The customer's order has shipped |
|  |  |  | The customer's order has been delivered |
|  |  |  | The customer's order is already cancelled |
|  |  |  | The customer has two orders placed or processing |
| A2 | Customer asked | Looking up the orders | customer asks to cancel the order by its number |
|  |  |  | customer asks to cancel an order number that matches none of their orders |
|  |  |  | customer asks to cancel their order without giving a number |
| A3 | Handing to staff | Not settled, handed to staff, customer told | agent tells the customer: the order is cancelled and the refund came back with another amount than agreed, giving that amount; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; staff will follow up |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled, and no refund was issued; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled and the refund came back with another amount than agreed, giving that amount; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled, and no refund was issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund's status is not known; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund is not confirmed yet; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund's status is not known; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund is not confirmed yet; please contact Harbor Goods support |
| A4 | Looking up the orders | Proposal waiting for yes | agent proposes cancelling the order and refunding its total to the payment method it was paid with, and asks for a yes |
| A5 | Looking up the orders | Nothing changed, customer told | agent tells the customer: it cannot look up your orders right now, so nothing was changed |
|  |  |  | agent tells the customer: no order with that number is among your orders, so nothing was changed |
|  |  |  | agent tells the customer: the order has shipped, so it cannot be cancelled; returns are a separate process |
|  |  |  | agent tells the customer: the order has been delivered, so it cannot be cancelled; returns are a separate process |
|  |  |  | agent tells the customer: the order is already cancelled, so nothing was changed |
| A6 | Looking up the orders | Asked which order | agent asks which of the two orders to cancel |
| A7 | Proposal waiting for yes | Nothing changed, customer told | agent tells the customer: nothing was changed |
| A8 | Proposal waiting for yes | Cancelling | customer says yes |
| A9 | Proposal waiting for yes | Customer left | customer stops answering |
| A10 | Asked which order | Looking up the orders | customer names one of the two orders |
| A11 | Asked which order | Customer left | customer stops answering |
| A12 | Cancelling | Handing to staff | agent creates a staff task: cancellation unknown |
| A13 | Cancelling | Nothing changed, customer told | agent tells the customer: the order has shipped or been delivered and can no longer be cancelled, and no refund was issued; returns are a separate process |
|  |  |  | agent tells the customer: the order could not be found, so nothing was changed |
| A14 | Cancelling | Refunding | cancel call answers cancelled |
|  |  |  | order read again shows it cancelled |
| A15 | Refunding | Handing to staff | agent creates a staff task: refund amount differs |
|  |  |  | agent creates a staff task: refund not issued |
|  |  |  | agent creates a staff task: refund status unknown |
| A16 | Refunding | Cancelled and refunded, customer told | agent tells the customer: the order is cancelled and the amount was refunded to the payment method it was paid with; nothing is promised about when the money arrives |
|  |  |  | agent tells the customer: the order is cancelled and a refund of the amount to the payment method it was paid with is pending; nothing is promised about when the money arrives |

## Breaks

None.
