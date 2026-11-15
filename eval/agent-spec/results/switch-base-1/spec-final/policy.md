# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Conversation started | The customer has one open order |
|  |  |  | The customer has two open orders |
|  |  |  | The customer's order has shipped or been delivered |
|  |  |  | The customer's order is already cancelled |
| A2 | Conversation started | Finding the order | customer asks to cancel an order by its number |
|  |  |  | customer asks to cancel my order |
|  |  |  | customer asks to cancel an order number that matches none of their orders |
|  |  |  | customer asks to cancel some items of an order |
| A3 | Finding the order | Proposal waiting for yes | agent proposes: cancel the order and refund its total paid to its payment method, and asks for a yes |
| A4 | Finding the order | Nothing changed, customer told | agent tells the customer: it cannot look up your orders right now; nothing was changed |
|  |  |  | agent tells the customer: the order has shipped and cannot be cancelled; returns are a separate process |
|  |  |  | agent tells the customer: the order is already cancelled; nothing was changed |
|  |  |  | agent tells the customer: it cannot find that order; please contact Harbor Goods support |
| A5 | Finding the order | Waiting for the customer's answer | agent tells the customer: that order number matches none of your orders; which order do you mean? |
|  |  |  | agent tells the customer: only the whole order can be cancelled |
|  |  |  | agent tells the customer: which order do you mean? please give its order number |
| A6 | Proposal waiting for yes | Nothing changed, customer told | agent tells the customer: nothing was changed |
| A7 | Proposal waiting for yes | Cancelling | customer says yes |
| A8 | Proposal waiting for yes | Customer left | customer stops answering |
| A9 | Waiting for the customer's answer | Finding the order | customer names one of their orders by its number |
|  |  |  | customer names another order number that matches none of their orders |
|  |  |  | customer asks to cancel the whole order |
| A10 | Waiting for the customer's answer | Customer left | customer stops answering |
| A11 | Cancelling | Nothing changed, customer told | agent tells the customer: the order has shipped or been delivered, so it could not be cancelled; returns are a separate process; no refund was issued |
|  |  |  | agent tells the customer: the order could not be cancelled; no refund was issued |
| A12 | Cancelling | Refunding | agent issues the refund |
| A13 | Cancelling | Handing to staff | agent creates a follow-up task for staff: cancellation_unknown |
| A14 | Refunding | Refunded, customer told | agent tells the customer: the order is cancelled and the total paid is refunded to the payment method |
| A15 | Refunding | Refund pending, customer told | agent tells the customer: the order is cancelled and the refund of the total paid to the payment method is pending |
| A16 | Refunding | Handing to staff | agent creates a follow-up task for staff: refund_amount_differs |
|  |  |  | agent creates a follow-up task for staff: refund_not_issued |
|  |  |  | agent creates a follow-up task for staff: refund_status_unknown |
| A17 | Handing to staff | Cancel outcome unknown, customer told | agent tells the customer: it could not cancel the order; no refund was issued; store staff will follow up |
|  |  |  | agent tells the customer: it could not cancel the order; no refund was issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled; no refund was issued; store staff will follow up |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled; no refund was issued; please contact Harbor Goods support |
| A18 | Handing to staff | Cancelled, refund not confirmed, customer told | agent tells the customer: the order is cancelled; the order system reports a refund of the amount it returned, not the amount you confirmed; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, but the refund was not issued; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled; the order system reports a refund of the amount it returned, not the amount you confirmed; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, but the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, but the refund's status is unknown; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, but the refund is not confirmed yet; store staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled, but the refund's status is unknown; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled, but the refund is not confirmed yet; please contact Harbor Goods support |

## Breaks

### R-11: the refund amount differs and the customer was not told, or staff were not given the case

1. The customer has one open order
2. customer asks to cancel an order by its number
3. agent lists the customer's orders
4. list call answers with the customer's orders
5. agent proposes: cancel the order and refund its total paid to its payment method, and asks for a yes
6. customer says yes
7. agent cancels the order
8. cancel call answers cancelled
9. agent issues the refund
10. refund call gets no answer (no refund created)
11. agent issues the refund again
12. refund call returns a refund for a different amount
13. agent lists the order and its refund again
14. list call fails
15. agent creates a follow-up task for staff: refund_status_unknown
16. follow-up call answers created
17. agent tells the customer: the order is cancelled, but the refund's status is unknown; store staff will follow up
