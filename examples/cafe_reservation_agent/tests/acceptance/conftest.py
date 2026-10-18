"""Harness for the executable specifications generated from agent_spec.md."""

import datetime
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import pytest
from pytest_bdd import given, parsers, then, when

from executable_spec import ExecutableSpec, SpecQuestion
from judge import judge_reply

AGENT_SPEC_PATH = Path(__file__).parents[2] / "agent_spec.md"
SPEC = ExecutableSpec(AGENT_SPEC_PATH, Path(__file__).parent / "features")


def pytest_configure(config):
    config.pluginmanager.register(SPEC)


# Today in every scenario, so "this Friday" is the same day on every run.
# The agent under test uses it as its current date.
TODAY = datetime.date(2026, 10, 19)  # a Monday
_WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
_TIME_WORDS = re.compile(r"(\d{1,2})(?::(\d{2}))?(am|pm)")


def date_from_spec(day: str) -> datetime.date:
    """The first date from TODAY that falls on `day`, such as "Friday"."""
    return TODAY + datetime.timedelta(days=(_WEEKDAYS.index(day) - TODAY.weekday()) % 7)


def date_to_spec(value: datetime.date) -> str:
    """The weekday name for a date in TODAY's week, else the ISO date, so a later week never reads as this one."""
    return _WEEKDAYS[value.weekday()] if 0 <= (value - TODAY).days < 7 else value.isoformat()


def time_from_spec(text: str) -> datetime.time:
    """The time for words such as "7pm" or "7:30pm"."""
    match = _TIME_WORDS.fullmatch(text)
    assert match, f"not a time in the spec's words: {text!r}"
    hour, minute, half = match.groups()
    return datetime.time(int(hour) % 12 + (12 if half == "pm" else 0), int(minute or 0))


def time_to_spec(value: datetime.time) -> str:
    hour, half = value.hour % 12 or 12, "pm" if value.hour >= 12 else "am"
    return f"{hour}{half}" if value.minute == 0 else f"{hour}:{value.minute:02d}{half}"


SUCCEEDED = "succeeded"
REJECTED = "rejected"
UNKNOWN = "unknown"


@dataclass(frozen=True)
class Reservation:
    """A reservation as steps read it, in the spec's words."""

    cafe: str
    date: str  # such as "Friday"
    time: str  # such as "7pm"
    party_size: int
    name: str
    confirmation: str
    seeded: bool  # it existed before the conversation started
    cancelled: bool


class ReservationControls(Protocol):
    """The test controls: how steps set up and read the systems behind the Reservation Gateway.

    Steps call only these, so a real implementation can replace the fake without
    changing a step. Days and times are in the spec's words, translated by the
    functions above.
    """

    implementation: str  # what stands behind the gateway, as the run summary names it
    gateway: object  # the Reservation Gateway the agent under test calls

    def make_available(self, day: str, time: str) -> None: ...

    def make_unavailable(self, day: str, time: str) -> None: ...

    def seed(self, cafe: str, day: str, time: str, party_size: int, name: str, confirmation: str) -> None:
        """Add a reservation that exists before the conversation starts.

        `confirmation` is the code the scenario uses, such as "ABC123". A real
        implementation maps it to the code the system assigns.
        """

    def time_out_creates(self, *, takes_effect: bool = False) -> None:
        """Make every later create report unknown. If `takes_effect`, the reservation is still made."""

    def time_out_lookups(self) -> None:
        """Make every later lookup report unknown."""

    def records(self) -> list[Reservation]:
        """Every reservation in the store, cancelled ones included, read directly rather than through the gateway."""

    def calls(self) -> list[str]:
        """The gateway operations the agent called, in order, under the Architecture Notes' names:
        "availability", "create", "lookup", and "cancel"."""


@dataclass(frozen=True)
class StoredReservation:
    """A reservation as the fake gateway stores and returns it."""

    cafe: str
    date: datetime.date
    time: datetime.time
    party_size: int
    name: str
    confirmation: str


class FakeReservationGateway:
    """The Reservation Gateway, held in memory.

    Provisional: these operations follow the Architecture Notes' sketch. When the
    product code defines the gateway's interface, change them to match it. Every
    slot is available unless `unavailable` lists it, and every write reports
    succeeded, rejected, or unknown. Lookups are not limited to the requesting
    user (AD-3).
    """

    def __init__(self) -> None:
        self.stored: list[StoredReservation] = []
        self.cancelled: set[str] = set()  # confirmation codes
        self.unavailable: set[tuple[datetime.date, datetime.time]] = set()
        self.calls: list[str] = []
        self.creates_time_out = False  # create reports unknown
        self.timed_out_creates_take_effect = False  # ...although it made the reservation
        self.lookups_time_out = False  # find_reservations reports unknown

    def check_availability(self, cafe: str, date: datetime.date, time: datetime.time) -> bool:
        self.calls.append("availability")
        return (date, time) not in self.unavailable

    def create(self, cafe: str, date: datetime.date, time: datetime.time, party_size: int, name: str) -> str:
        self.calls.append("create")
        if (date, time) in self.unavailable:
            return REJECTED
        if self.creates_time_out and not self.timed_out_creates_take_effect:
            return UNKNOWN
        confirmation = f"R{len(self.stored) + 1}"
        self.stored.append(StoredReservation(cafe, date, time, party_size, name, confirmation))
        return UNKNOWN if self.creates_time_out else SUCCEEDED

    def find_reservations(self) -> list[StoredReservation] | str:
        """The reservations that are not cancelled."""
        self.calls.append("lookup")
        if self.lookups_time_out:
            return UNKNOWN
        return [stored for stored in self.stored if stored.confirmation not in self.cancelled]

    def cancel(self, confirmation: str) -> str:
        self.calls.append("cancel")
        if confirmation in self.cancelled or all(stored.confirmation != confirmation for stored in self.stored):
            return REJECTED
        self.cancelled.add(confirmation)
        return SUCCEEDED


class FakeReservationControls:
    """The test controls for the in-memory fake gateway."""

    implementation = "in-memory fake"

    def __init__(self) -> None:
        self.gateway = FakeReservationGateway()
        self._seeded: set[str] = set()  # confirmation codes

    def make_available(self, day: str, time: str) -> None:
        self.gateway.unavailable.discard((date_from_spec(day), time_from_spec(time)))

    def make_unavailable(self, day: str, time: str) -> None:
        self.gateway.unavailable.add((date_from_spec(day), time_from_spec(time)))

    def seed(self, cafe: str, day: str, time: str, party_size: int, name: str, confirmation: str) -> None:
        stored = StoredReservation(cafe, date_from_spec(day), time_from_spec(time), party_size, name, confirmation)
        self.gateway.stored.append(stored)
        self._seeded.add(confirmation)

    def time_out_creates(self, *, takes_effect: bool = False) -> None:
        self.gateway.creates_time_out = True
        self.gateway.timed_out_creates_take_effect = takes_effect

    def time_out_lookups(self) -> None:
        self.gateway.lookups_time_out = True

    def records(self) -> list[Reservation]:
        return [
            Reservation(
                stored.cafe,
                date_to_spec(stored.date),
                time_to_spec(stored.time),
                stored.party_size,
                stored.name,
                stored.confirmation,
                seeded=stored.confirmation in self._seeded,
                cancelled=stored.confirmation in self.gateway.cancelled,
            )
            for stored in self.gateway.stored
        ]

    def calls(self) -> list[str]:
        return list(self.gateway.calls)


@pytest.fixture
def controls() -> ReservationControls:
    controls = FakeReservationControls()
    SPEC.record_boundary("Reservation Gateway", controls.implementation)
    return controls


@pytest.fixture
def agent(controls):
    raise NotImplementedError(
        "Connect the agent under test: the Cafe Reservation Agent built on `controls.gateway`, "
        "using TODAY as the current date, with a send(text) -> reply method."
    )


@pytest.fixture
def conversation():
    """The conversation so far, as (speaker, text) pairs."""
    return []


@pytest.fixture
def say(agent, conversation):
    """Send a user turn to the agent and record both turns."""

    def say(text):
        conversation.append(("User", text))
        conversation.append(("Agent", agent.send(text)))

    return say


@pytest.fixture
def judge(request, conversation):
    """Judge the agent's latest reply against one statement quoted from the scenario."""

    def judge(statement):
        return judge_reply(statement, conversation=conversation, scenario_text=SPEC.scenario_for(request.node).text)

    return judge


@given(parsers.parse("the spec answers {issue}"))
def spec_answers(issue):
    raise SpecQuestion(issue)


@when(parsers.parse('the user says "{text}"'))
def user_says(say, text):
    say(text)


@then(parsers.parse('the agent\'s reply meets "{statement}"'))
def reply_meets(judge, statement):
    verdict = judge(statement)
    assert verdict.shown, verdict.reason


@then(parsers.parse('the agent\'s reply avoids "{statement}"'))
def reply_avoids(judge, statement):
    verdict = judge(statement)
    assert not verdict.shown, verdict.reason
