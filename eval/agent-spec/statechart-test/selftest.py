"""Self-test: a deliberately broken CO-06 ("at most one CO-A2") must report the known shortest path.

The real policy sends a second cancel only after an unanswered first one and a lookup showing the
order still open (CO-S13), so the broken rule must fire there, and nowhere sooner.
Run:  python3 selftest.py
"""
import check
import model

EXPECTED = [
    "The order is placed or processing",
    "customer asks to cancel the order by its number",
    "agent looks up the customer's orders",
    "lookup shows the order placed or processing",
    "agent proposes: cancel the whole order, refund the total to its payment method",
    "customer says yes",
    "agent sends the cancel",
    "cancel call times out (nothing changed)",
    "agent looks up the customer's orders",
    "lookup shows the order placed or processing",
    "agent sends the cancel again",
]


def broken_co06_step(s, st, t):
    if st.kind == "call_cancel" and s.cancel_n >= 1:
        return "second cancel (broken rule: at most one)"


def main():
    parent, edges = check.explore()
    broken = dict(id="CO-06-broken", title="at most one CO-A2", state=None, step=broken_co06_step)
    found = check.check(parent, edges, [broken])["CO-06-broken"]
    assert list(found) == ["second cancel (broken rule: at most one)"], found
    got = check.fmt_path(next(iter(found.values())))
    for i, lab in enumerate(got, 1):
        print(f"  {i:2d}. {lab}")
    assert got == EXPECTED, "shortest path differs from the expected one"
    real = check.check(parent, edges, [r for r in model.RULES if r["id"] == "CO-06"])["CO-06"]
    assert not real, real
    print("selftest passed: broken CO-06 caught with the expected 11-step path; real CO-06 holds")


if __name__ == "__main__":
    main()
