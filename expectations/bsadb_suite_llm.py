import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")
suite = context.suites.get("expectation_suite")

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "ticket:reference:tickets.ticket_status_id"},
        column="ticket.ticket_status_id",
        value_set=[]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "ticket:reference:tickets.ticket_type_id"},
        column="ticket.ticket_type_id",
        value_set=[]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "ticket:reference:tickets.ticket_priority_id"},
        column="ticket.ticket_priority_id",
        value_set=[]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket:not_null:ticket_creationdate"},
        column="ticket.ticket_creationdate"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket:not_null:ticket_creationtime"},
        column="ticket.ticket_creationtime"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeNull(
        meta={"check_id": "ticket:conditional_required:ticket_closedate"},
        column="ticket.ticket_closedate",
        mostly=1.0
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "ticket:freshness:ticket_updated_date"},
        column="ticket.ticket_updated_date",
        min_value=(datetime.utcnow() - timedelta(hours=25)).isoformat(),
        max_value=datetime.utcnow().isoformat()
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "ticket_note:reference:ticket_note.note_type"},
        column="ticket_note.note_type",
        value_set=[]
    )
)