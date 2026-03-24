import great_expectations as gx
from datetime import datetime, timedelta, timezone

context = gx.get_context(mode="file")

suite_name = "expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# -------------------------
# Table: ticket
# -------------------------
for col in [
    "ticket_id",
    "ticket_customer_id",
    "ticket_status_id",
    "ticket_type_id",
    "ticket_priority_id",
    "ticket_owner_id",
    "ticket_creationdate",
    "ticket_creationtime",
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket:{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket:ticket_id:not_null"},
        column="ticket_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:ticket:ticket_id:unique"},
        column="ticket_id",
    )
)

for col in [
    "ticket_customer_id",
    "ticket_status_id",
    "ticket_type_id",
    "ticket_priority_id",
    "ticket_owner_id",
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            meta={"check_id": f"contract:ticket:{col}:not_null"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket:ticket_creationdate:not_null"},
        column="ticket_creationdate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket:ticket_creationtime:not_null"},
        column="ticket_creationtime",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:ticket:ticket_id:type"},
        column="ticket_id",
        type_="INTEGER",
    )
)
for col in [
    "ticket_customer_id",
    "ticket_status_id",
    "ticket_type_id",
    "ticket_priority_id",
    "ticket_owner_id",
    "ticket_assignedto_id",
    "ticket_closed_by_id",
    "ticket_updated_by_id",
    "ticket_followup_id",
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInTypeList(
            meta={"check_id": f"contract:ticket:{col}:type"},
            column=col,
            type_list=["INTEGER", "INT", "BIGINT", "SMALLINT"],
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:ticket:ticket_description:length"},
        column="ticket_description",
        min_value=0,
        max_value=1000,
        mostly=1.0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:ticket:ticket_note:length"},
        column="ticket_note",
        min_value=0,
        max_value=1000,
        mostly=1.0,
    )
)

# Conditional requirement: ticket_closedate must be present when ticket_status_id = 2
suite.add_expectation(
    gx.expectations.ExpectQueryResultsToMatchComparison(
        meta={"check_id": "contract:ticket:ticket_closedate:required_when_closed"},
        query="""
            SELECT
              SUM(CASE WHEN ticket_status_id = 2 AND ticket_closedate IS NULL THEN 1 ELSE 0 END) AS invalid_count
            FROM ticket
        """,
        comparison_operator="=",
        comparison_value=0,
    )
)

# Freshness: ticket.ticket_updated_date no older than 25 hours (compare against current datetime)
freshness_cutoff = datetime.now(timezone.utc) - timedelta(hours=25)
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "contract:ticket:ticket_updated_date:freshness_25h"},
        column="ticket_updated_date",
        min_value=freshness_cutoff,
        max_value=datetime.now(timezone.utc),
    )
)

# -------------------------
# Table: ticket_status
# -------------------------
for col in ["ticket_status_id"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_status:{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_status:ticket_status_id:not_null"},
        column="ticket_status_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:ticket_status:ticket_status_id:unique"},
        column="ticket_status_id",
    )
)

# -------------------------
# Table: ticket_type
# -------------------------
for col in ["ticket_type_id", "ticket_type_name"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_type:{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_type:ticket_type_id:not_null"},
        column="ticket_type_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:ticket_type:ticket_type_id:unique"},
        column="ticket_type_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_type:ticket_type_name:not_null"},
        column="ticket_type_name",
    )
)

# -------------------------
# Table: ticket_priority
# -------------------------
for col in ["ticket_priority_id"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_priority:{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_priority:ticket_priority_id:not_null"},
        column="ticket_priority_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:ticket_priority:ticket_priority_id:unique"},
        column="ticket_priority_id",
    )
)

# -------------------------
# Table: ticket_followup
# -------------------------
for col in ["id"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_followup:{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_followup:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:ticket_followup:id:unique"},
        column="id",
    )
)

# -------------------------
# Table: ticket_note
# -------------------------
for col in ["ticket_note_id"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_note:{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_note:ticket_note_id:not_null"},
        column="ticket_note_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:ticket_note:ticket_note_id:unique"},
        column="ticket_note_id",
    )
)

# -------------------------
# Table: ticket_note_type
# -------------------------
for col in ["id"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_note_type:{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_note_type:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:ticket_note_type:id:unique"},
        column="id",
    )
)

# -------------------------
# Table: ticket_transactions
# -------------------------
for col in ["id"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_transactions:{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_transactions:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:ticket_transactions:id:unique"},
        column="id",
    )
)

# -------------------------
# Reference integrity checks (via SQL)
# -------------------------

# ticket.ticket_status_id must exist in ticket_status
suite.add_expectation(
    gx.expectations.ExpectQueryResultsToMatchComparison(
        meta={"check_id": "contract:ticket:ticket_status_id:fk_ticket_status"},
        query="""
            SELECT COUNT(*) AS invalid_count
            FROM ticket t
            LEFT JOIN ticket_status s
              ON t.ticket_status_id = s.ticket_status_id
            WHERE t.ticket_status_id IS NOT NULL
              AND s.ticket_status_id IS NULL
        """,
        comparison_operator="=",
        comparison_value=0,
    )
)

# ticket.ticket_type_id must exist in ticket_type
suite.add_expectation(
    gx.expectations.ExpectQueryResultsToMatchComparison(
        meta={"check_id": "contract:ticket:ticket_type_id:fk_ticket_type"},
        query="""
            SELECT COUNT(*) AS invalid_count
            FROM ticket t
            LEFT JOIN ticket_type tt
              ON t.ticket_type_id = tt.ticket_type_id
            WHERE t.ticket_type_id IS NOT NULL
              AND tt.ticket_type_id IS NULL
        """,
        comparison_operator="=",
        comparison_value=0,
    )
)

# ticket.ticket_priority_id must exist in ticket_priority
suite.add_expectation(
    gx.expectations.ExpectQueryResultsToMatchComparison(
        meta={"check_id": "contract:ticket:ticket_priority_id:fk_ticket_priority"},
        query="""
            SELECT COUNT(*) AS invalid_count
            FROM ticket t
            LEFT JOIN ticket_priority tp
              ON t.ticket_priority_id = tp.ticket_priority_id
            WHERE t.ticket_priority_id IS NOT NULL
              AND tp.ticket_priority_id IS NULL
        """,
        comparison_operator="=",
        comparison_value=0,
    )
)

# ticket_note.note_type must exist in ticket_note_type.note_type
suite.add_expectation(
    gx.expectations.ExpectQueryResultsToMatchComparison(
        meta={"check_id": "contract:ticket_note:note_type:fk_ticket_note_type"},
        query="""
            SELECT COUNT(*) AS invalid_count
            FROM ticket_note n
            LEFT JOIN ticket_note_type nt
              ON n.note_type = nt.note_type
            WHERE n.note_type IS NOT NULL
              AND nt.note_type IS NULL
        """,
        comparison_operator="=",
        comparison_value=0,
    )
)