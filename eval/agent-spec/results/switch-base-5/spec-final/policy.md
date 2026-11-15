# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Customer asked | The customer's order is placed or processing |
|  |  |  | The customer's order has shipped |
|  |  |  | The customer's order has been delivered |
|  |  |  | The customer's order is already cancelled |
|  |  |  | The customer has more than one order placed or processing |
| A2 | Customer asked | Looking up the orders | customer asks to cancel the order by its number |
|  |  |  | customer asks to cancel an order number that matches none of their orders |
|  |  |  | customer asks to cancel their order without giving a number |
| A3 | Handing to staff | Not settled, handed to staff, customer told | agent tells the customer: the order is cancelled and the refund came back with another amount than agreed, giving that amount; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; staff will follow up |
|  |  |  | agent tells the customer: the order system did not confirm the order is cancelled, and the refund was not issued; staff will follow up |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled, and no refund was issued; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled and the refund came back with another amount than agreed, giving that amount; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order system did not confirm the order is cancelled, and the refund was not issued; please contact Harbor Goods support |
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
| A6 | Looking up the orders | Asked which order | agent asks which of the open orders to cancel |
| A7 | Proposal waiting for yes | Nothing changed, customer told | agent tells the customer: nothing was changed |
| A8 | Proposal waiting for yes | Cancelling | customer says yes |
| A9 | Proposal waiting for yes | Customer left | customer stops answering |
| A10 | Asked which order | Looking up the orders | customer names one of the open orders |
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

### R-11: the refund came back with another amount and the customer was not told that amount

1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. agent lists the customer's orders
4. order list answers
5. agent proposes cancelling the order and refunding its total to the payment method it was paid with, and asks for a yes
6. customer says yes
7. agent cancels the order
8. cancel call answers cancelled
9. agent issues the refund
10. refund call gets no answer (nothing created)
11. agent sends the refund call once more
12. refund call answers issued with another amount
13. agent reads the refund again
14. refund read again answers an error
15. agent creates a staff task: refund status unknown
16. staff task call answers created
17. agent tells the customer: the order is cancelled but the refund's status is not known; staff will follow up
