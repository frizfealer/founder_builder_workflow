# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Customer asked | The customer has one open order |
|  |  |  | The customer has two or more open orders |
|  |  |  | The customer's order has shipped or been delivered |
|  |  |  | The customer's order is already cancelled |
| A2 | Customer asked | Looking up orders | customer asks to cancel an order, naming its number |
|  |  |  | customer asks to cancel an order number that is not theirs |
|  |  |  | customer asks to cancel "my order" without a number |
| A3 | Looking up orders | Proposal waiting for yes | agent proposes: cancel this order and refund its total to its payment method; asks for a yes |
| A4 | Looking up orders | Nothing changed, customer told | agent tells the customer: it cannot look up the orders right now, and nothing was changed |
|  |  |  | agent tells the customer: that order number matches none of the customer's orders, and nothing was changed |
|  |  |  | agent tells the customer: the order has shipped or been delivered and cannot be cancelled; returns are a separate process |
|  |  |  | agent tells the customer: the order is already cancelled, and nothing was changed |
|  |  |  | agent tells the customer: nothing was changed |
| A5 | Looking up orders | Asked which order | agent asks which order, by its number |
| A6 | Looking up orders | Cancelling | agent cancels the order |
| A7 | Proposal waiting for yes | Looking up orders | customer says yes |
| A8 | Proposal waiting for yes | Looking up orders | customer says yes, then asks to cancel their other order instead |
| A9 | Proposal waiting for yes | Looking up orders | customer says no |
| A10 | Proposal waiting for yes | Customer left | customer stops answering |
| A11 | Asked which order | Looking up orders | customer names one order by its number |
| A12 | Asked which order | Customer left | customer stops answering |
| A13 | Cancelling | Nothing changed, customer told | agent tells the customer: the order has shipped or been delivered; it was not cancelled and no refund was issued |
| A14 | Cancelling | Refunding | agent asks for the refund of the total paid |
| A15 | Cancelling | Handing to staff | agent creates a follow-up task for staff |
| A16 | Refunding | Cancelled and refunded, customer told | agent tells the customer: the order is cancelled and the refund of the total paid to the order's payment method is pending |
|  |  |  | agent tells the customer: the order is cancelled and the refund of the total paid to the order's payment method is issued |
| A17 | Refunding | Handing to staff | agent creates a follow-up task for staff |
| A18 | Handing to staff | Outcome unclear, staff will follow up | agent tells the customer: the order could not be cancelled, and no refund was issued; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled and the refund system returned a different amount, which it states; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; staff will follow up |
|  |  |  | agent tells the customer: the order could not be cancelled, and no refund was issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled, and no refund was issued; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled and the refund system returned a different amount, which it states; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled, and no refund was issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund's status is unknown; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund is not confirmed yet; staff will follow up |
|  |  |  | agent tells the customer: the order is cancelled but the refund's status is unknown; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund is not confirmed yet; please contact Harbor Goods support |

## Breaks

None.
