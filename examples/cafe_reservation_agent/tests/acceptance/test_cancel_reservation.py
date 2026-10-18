"""Steps for the Cancel Reservation executable specifications."""

from pytest_bdd import given, parsers, scenarios, then, when

from executable_spec import SpecQuestion

scenarios("features/cancel_reservation.feature")


@given(
    parsers.parse(
        "a reservation at {cafe} on {date} at {time:S} for a party of {party_size:d} with confirmation {confirmation}"
    )
)
def reservation_with_confirmation(controls, cafe, date, time, party_size, confirmation):
    controls.seed(cafe, date, time, party_size, name="Alex", confirmation=confirmation)


@given(parsers.parse("a reservation at {cafe} on {date} at {time:S}"))
def reservation_at(controls, cafe, date, time):
    controls.seed(cafe, date, time, party_size=2, name="Alex", confirmation=f"{date}-{time}".upper())


@given("only one reservation matches")
def only_one_reservation_matches(controls):
    # A reservation that does not match, so cancelling the wrong one is observable.
    controls.seed("Cafe Roma", "Saturday", "7pm", party_size=2, name="Alex", confirmation="DEF456")


@when("the user gives valid cancellation authorization")
def user_gives_cancellation_authorization():
    raise SpecQuestion("I-04")


@then(parsers.parse("{confirmation} is cancelled"))
def reservation_is_cancelled(controls, confirmation):
    assert any(r.confirmation == confirmation and r.cancelled for r in controls.records())


@then(parsers.parse("no reservation other than {confirmation} changes"))
def no_other_reservation_changes(controls, confirmation):
    assert not any(r.cancelled for r in controls.records() if r.confirmation != confirmation)


@then("no reservation was cancelled")
def no_reservation_cancelled(controls):
    assert not any(reservation.cancelled for reservation in controls.records())
