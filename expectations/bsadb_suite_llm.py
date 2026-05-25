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
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "ticket:domain:ticket_status_id"},
        column="ticket_status_id",
        value_set=[1, 2, 3, 4]
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
    gx.expectations.ExpectColumnValuesToBeNull(
        meta={"check_id": "ticket:conditional_not_null:ticket_closedate"},
        column="ticket_closedate",
        row_condition="ticket_status_id != 2"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket_status:not_null:ticket_status_id"},
        column="ticket_status_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket_type:not_null:ticket_type_id"},
        column="ticket_type_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket_type:not_null:ticket_type_name"},
        column="ticket_type_name"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket_priority:not_null:ticket_priority_id"},
        column="ticket_priority_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket_followup:not_null:id"},
        column="id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket_note:not_null:ticket_note_id"},
        column="ticket_note_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "ticket_note:domain:note_type"},
        column="note_type",
        value_set=["normal", "system", "internal"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket_note_type:not_null:id"},
        column="id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket_transactions:not_null:id"},
        column="id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "ticket:freshness:ticket_updated_date"},
        column="ticket_updated_date",
        min_value=(datetime.utcnow() - timedelta(hours=25)).isoformat(),
        max_value=datetime.utcnow().isoformat()
    )
)