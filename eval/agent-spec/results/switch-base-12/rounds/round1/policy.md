# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Customer asked | The order is placed or processing |
|  |  |  | The order has shipped or been delivered |
|  |  |  | The order is already cancelled |
|  |  |  | The customer has two open orders |
| A2 | Customer asked | Looking up orders | customer asks to cancel the order by its number |
|  |  |  | customer asks to cancel an order number that is none of theirs |
|  |  |  | customer asks to cancel only some items of the order |
|  |  |  | customer asks to cancel "my order" without saying which |
| A3 | Handing to staff | Handed to staff, customer told | agent tells the customer: the order is cancelled; the order system returned a refund of <the amount it returned>, which differs from the total you agreed; store staff will follow up on the order |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; store staff will follow up on the order |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled; no refund was issued; store staff will follow up on the order |
|  |  |  | agent tells the customer: the order is cancelled; the order system returned a refund of <the amount it returned>, which differs from the total you agreed; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund was not issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: it is not known whether the order was cancelled; no refund was issued; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund's status is unknown; store staff will follow up on the order |
|  |  |  | agent tells the customer: the order is cancelled but the refund is not confirmed yet; store staff will follow up on the order |
|  |  |  | agent tells the customer: the order is cancelled but the refund's status is unknown; please contact Harbor Goods support |
|  |  |  | agent tells the customer: the order is cancelled but the refund is not confirmed yet; please contact Harbor Goods support |
| A4 | Looking up orders | Proposal waiting for yes | agent proposes cancelling the order and refunding its total paid to its payment method |
|  |  |  | agent says the refund is the total paid to the order's payment method, and proposes again |
| A5 | Looking up orders | Nothing changed, customer told | agent tells the customer: it cannot see your orders right now; nothing was changed |
|  |  |  | agent tells the customer: no order with that number is among your orders; nothing was changed |
|  |  |  | agent tells the customer: the order has shipped or been delivered, so it cannot be cancelled; returns are a separate process |
|  |  |  | agent tells the customer: the order is already cancelled; nothing was changed |
|  |  |  | agent tells the customer: nothing was changed |
| A6 | Looking up orders | Asked about the whole order | agent tells the customer only the whole order can be cancelled |
| A7 | Looking up orders | Asked which order | agent asks which order to cancel |
| A8 | Proposal waiting for yes | Looking up orders | customer says no |
| A9 | Proposal waiting for yes | Looking up orders | customer says yes, then asks for a different refund amount or payment method |
| A10 | Proposal waiting for yes | Cancelling | customer says yes |
| A11 | Proposal waiting for yes | Customer left | customer stops answering |
| A12 | Asked about the whole order | Looking up orders | customer asks to cancel the whole order |
| A13 | Asked about the whole order | Customer left | customer stops answering |
| A14 | Asked which order | Looking up orders | customer names the order to cancel |
| A15 | Asked which order | Customer left | customer stops answering |
| A16 | Cancelling | Handing to staff | agent creates a follow-up task: cancellation unknown |
| A17 | Cancelling | Nothing changed, customer told | agent tells the customer: the order shipped before it could be cancelled, so nothing was cancelled or refunded |
|  |  |  | agent tells the customer: the order was not cancelled and no refund was issued |
| A18 | Cancelling | Refunding | agent sends the refund call |
| A19 | Refunding | Cancelled and refunded, customer told | agent tells the customer: the order is cancelled and the refund of its total to its payment method is issued, with the refund id |
|  |  |  | agent tells the customer: the order is cancelled and the refund of its total to its payment method is pending, with the refund id |
| A20 | Refunding | Handing to staff | agent creates a follow-up task: refund status unknown |
|  |  |  | agent creates a follow-up task: refund not issued |
|  |  |  | agent creates a follow-up task: cancellation unknown |

## Breaks

None.
