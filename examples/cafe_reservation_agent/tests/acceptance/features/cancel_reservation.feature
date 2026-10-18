# Generated from agent_spec.md by agent-spec-to-pytest-bdd. Edit the Agent Spec, then regenerate.
Feature: Cancel Reservation

  # Source: CA-S01 sha256:abb701643dea
  @CA-S01 @planned
  Scenario: CA-S01 One matching reservation
    Given the spec answers I-04
    And a reservation at Cafe Roma on Friday at 7pm for a party of 2 with confirmation ABC123
    And only one reservation matches
    When the user says "Cancel my Cafe Roma reservation Friday."
    And the user gives valid cancellation authorization
    Then ABC123 is cancelled
    And no reservation other than ABC123 changes

  # Source: CA-S02 sha256:b2991053e4c2
  @CA-S02 @planned
  Scenario: CA-S02 Multiple matching reservations
    Given a reservation at Cafe Roma on Friday at 6pm
    And a reservation at Cafe Roma on Friday at 8pm
    When the user says "Cancel my Cafe Roma reservation Friday."
    Then the agent's reply meets "The agent asks which reservation the user means."
    And no reservation was cancelled
    And the agent's reply avoids "choosing one of the two reservations itself"
