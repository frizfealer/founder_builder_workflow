# Generated from agent_spec.md by agent-spec-to-pytest-bdd. Edit the Agent Spec, then regenerate.
Feature: Create Reservation

  # Source: CR-S01 sha256:f2565818acab
  @CR-S01 @planned
  Scenario: CR-S01 Complete request, available
    Given Friday 7pm is available
    And no matching reservation exists
    When the user says "Book Cafe Roma this Friday at 7pm for two under Alex."
    And the user confirms the current proposal
    Then exactly one reservation exists
    And the reservation's café is Cafe Roma
    And the reservation's date is Friday
    And the reservation's time is 7pm
    And the reservation's party size is 2
    And the reservation's name is Alex
    And no duplicate reservation was created
    And no reservation was made for a time other than 7pm

  # Source: CR-S02 sha256:58fce0b51dc3
  @CR-S02 @CR-01 @planned
  Scenario: CR-S02 Missing party size
    When the user says "Book Cafe Roma Friday at 7pm under Alex."
    Then no reservation was created
    And the agent's reply meets "The agent resolves the party size before booking."
    And no reservation was created for a party of 2

  # Source: CR-S03 sha256:483299d6c28d
  @CR-S03 @CR-02 @planned
  Scenario: CR-S03 Requested time unavailable
    Given Friday 7pm is unavailable
    And Friday 7:30pm is available
    When the user says "Book Cafe Roma Friday at 7pm for two."
    Then the agent's reply meets "The agent informs the user that 7pm is unavailable"
    And 7:30pm was not booked

  # Source: CR-S04 sha256:c59eef270d1f
  @CR-S04 @CR-04 @planned
  Scenario: CR-S04 User changes party size after authorization
    Given the agent has proposed Friday 7pm, party of 2
    When the user says "Yes, book it."
    And the user says "Actually, make it four people."
    Then the agent's reply meets "The agent treats the new four-person reservation as a changed proposal."
    And no reservation was created for a party of 4

  # Source: CR-S05 sha256:296e08b05769
  @CR-S05 @CR-05 @G-04 @planned
  Scenario: CR-S05 Booking request times out — If the booking is found
    Given no matching reservation is known to exist
    And the booking request will time out after it is sent
    And the booking is found
    And the agent has sent the booking request
    Then the agent checks reservation state or transaction status
    And the booking is not retried
    And the agent's reply meets "report the verified booking"

  # Source: CR-S05 sha256:296e08b05769
  @CR-S05 @CR-05 @G-04 @planned
  Scenario: CR-S05 Booking request times out — If the outcome cannot be determined
    Given no matching reservation is known to exist
    And the booking request will time out after it is sent
    And the outcome cannot be determined
    And the agent has sent the booking request
    Then the agent checks reservation state or transaction status
    And the agent's reply avoids "claim success"
    And another booking is not blindly created
    And the agent's reply meets "communicate the uncertainty appropriately"
