import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")
suite = context.suites.get("expectation_suite")

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket:not_null:ticket_id"},
        column="ticket_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket:not_null:ticket_customer_id"},
        column="ticket_customer_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket:not_null:ticket_status_id"},
        column="ticket_status_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket:not_null:ticket_type_id"},
        column="ticket_type_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket:not_null:ticket_priority_id"},
        column="ticket_priority_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket:not_null:ticket_owner_id"},
        column="ticket_owner_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket:not_null:ticket_creationdate"},
        column="ticket_creationdate"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket:not_null:ticket_creationtime"},
        column="ticket_creationtime"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "ticket:freshness:ticket.ticket_updated_date"},
        column="ticket.ticket_updated_date",
        min_value=(datetime.utcnow() - timedelta(hours=25)).isoformat(),
        max_value=datetime.utcnow().isoformat()
    )
)