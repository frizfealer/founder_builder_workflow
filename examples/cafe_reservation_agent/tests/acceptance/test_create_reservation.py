"""Steps for the Create Reservation executable specifications."""

from pytest_bdd import given, parsers, scenarios, then, when

scenarios("features/create_reservation.feature")

# Test data the scenarios leave open, taken from other scenarios in the spec.
BOOKING_REQUEST = "Book Cafe Roma this Friday at 7pm for two under Alex."  # CR-S01
CONFIRMATION = "Yes, book it."  # CR-S04


def booked(controls):
    return [reservation for reservation in controls.records() if not reservation.cancelled]


def created(controls):
    """Every reservation made during the conversation."""
    return [reservation for reservation in controls.records() if not reservation.seeded]


@given(parsers.parse("{date} {time} is available"))
def slot_is_available(controls, date, time):
    controls.make_available(date, time)


@given(parsers.parse("{date} {time} is unavailable"))
def slot_is_unavailable(controls, date, time):
    controls.make_unavailable(date, time)


@given("no matching reservation exists")
@given("no matching reservation is known to exist")
def no_matching_reservation(controls):
    assert not controls.records()


@given(parsers.parse("the agent has proposed {proposal}"))
def agent_has_proposed(say, judge, proposal):
    say(BOOKING_REQUEST)
    verdict = judge(f"Proposal: {proposal}")
    assert verdict.shown, verdict.reason


@given("the booking request will time out after it is sent")
def booking_request_times_out(controls):
    controls.time_out_creates()


@given("the booking is found")
def booking_is_found(controls):
    controls.time_out_creates(takes_effect=True)


@given("the outcome cannot be determined")
def outcome_cannot_be_determined(controls):
    controls.time_out_lookups()


@given("the agent has sent the booking request")
def agent_has_sent_booking_request(say, controls):
    say(BOOKING_REQUEST)
    say(CONFIRMATION)
    assert "create" in controls.calls()


@when("the user confirms the current proposal")
def user_confirms_current_proposal(say):
    say(CONFIRMATION)


@then("exactly one reservation exists")
def exactly_one_reservation_exists(controls):
    assert len(booked(controls)) == 1


@then(parsers.parse("the reservation's {field} is {value}"))
def reservation_field_is(controls, field, value):
    [reservation] = booked(controls)
    attribute = {"café": "cafe", "party size": "party_size"}.get(field, field)
    assert str(getattr(reservation, attribute)) == value


@then("no duplicate reservation was created")
def no_duplicate_reservation(controls):
    details = [(r.cafe, r.date, r.time, r.party_size, r.name) for r in created(controls)]
    assert len(details) == len(set(details))


@then(parsers.parse("no reservation was made for a time other than {time}"))
def no_reservation_at_other_time(controls, time):
    assert all(reservation.time == time for reservation in created(controls))


@then("no reservation was created")
def no_reservation_created(controls):
    assert not created(controls)


@then(parsers.parse("no reservation was created for a party of {party_size:d}"))
def no_reservation_for_party(controls, party_size):
    assert all(reservation.party_size != party_size for reservation in created(controls))


@then(parsers.parse("{time} was not booked"))
def time_was_not_booked(controls, time):
    assert all(reservation.time != time for reservation in created(controls))


@then("the agent checks reservation state or transaction status")
def agent_checks_reservation_state(controls):
    calls = controls.calls()
    assert "lookup" in calls[calls.index("create") + 1 :]


@then("the booking is not retried")
@then("another booking is not blindly created")
def booking_is_not_repeated(controls):
    assert controls.calls().count("create") == 1
