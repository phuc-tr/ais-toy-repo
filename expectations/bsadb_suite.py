import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# ----------------------------------------------------------------------
# Table-level sanity: expected columns present (ticket table)
# ----------------------------------------------------------------------
suite.add_expectation(
    gx.expectations.ExpectTableColumnsToMatchSet(
        meta={"check_id": "ticket:columns_match_set"},
        column_set=[
            "ticket_id",
            "ticket_customer_id",
            "ticket_status_id",
            "ticket_type_id",
            "ticket_description",
            "ticket_priority_id",
            "ticket_owner_id",
            "ticket_assignedto_id",
            "ticket_creationdate",
            "ticket_creationtime",
            "ticket_closed_by_id",
            "ticket_closedate",
            "ticket_closetime",
            "ticket_updated_by_id",
            "ticket_updated_date",
            "ticket_note",
            "ticket_followup_id",
        ],
        exact_match=True,
    )
)

# ----------------------------------------------------------------------
# Required vs optional columns (align to data contract)
# ----------------------------------------------------------------------
# Required (NOT NULL)
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
        gx.expectations.ExpectColumnValuesToNotBeNull(
            meta={"check_id": f"{col}:not_null"},
            column=col,
        )
    )

# Optional (allow NULLs) - no not-null expectations
# ticket_description, ticket_assignedto_id, ticket_closed_by_id, ticket_closedate,
# ticket_closetime, ticket_updated_by_id, ticket_updated_date, ticket_note, ticket_followup_id

# ----------------------------------------------------------------------
# Type expectations (align to data contract)
# NOTE: Great Expectations type strings can vary by backend; these are common for SQL.
# ----------------------------------------------------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "ticket_id:type"},
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
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"{col}:type"},
            column=col,
            type_="INTEGER",
        )
    )

for col in ["ticket_description", "ticket_note"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"{col}:type"},
            column=col,
            type_="STRING",
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "ticket_creationdate:type"},
        column="ticket_creationdate",
        type_="DATE",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "ticket_creationtime:type"},
        column="ticket_creationtime",
        type_="TIME",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "ticket_closedate:type"},
        column="ticket_closedate",
        type_="DATE",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "ticket_closetime:type"},
        column="ticket_closetime",
        type_="TIME",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "ticket_updated_date:type"},
        column="ticket_updated_date",
        type_="DATETIME",
    )
)

# ----------------------------------------------------------------------
# Contract rule: Ticket must have valid creation date and time
# (already enforced via not-null; keep as explicit multi-column rule)
# ----------------------------------------------------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket_creation_datetime_valid:ticket_creationdate_not_null"},
        column="ticket_creationdate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket_creation_datetime_valid:ticket_creationtime_not_null"},
        column="ticket_creationtime",
    )
)

# ----------------------------------------------------------------------
# Contract rule: Closed tickets (status_id=2) must have a close date
# Implemented as conditional expectation.
# ----------------------------------------------------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "closed_ticket_has_close_date"},
        column="ticket_closedate",
        row_condition='col("ticket_status_id") == 2',
        condition_parser="great_expectations",
    )
)

# ----------------------------------------------------------------------
# Length constraint: ticket_note maxLength 1000
# ----------------------------------------------------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "ticket_note:max_length_1000"},
        column="ticket_note",
        min_value=0,
        max_value=1000,
        mostly=1.0,
    )
)

# ----------------------------------------------------------------------
# Foreign key checks
# NOTE: These are represented as set-membership expectations; populate value_set at runtime.
# ----------------------------------------------------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "ticket_status_id:foreign_key"},
        column="ticket_status_id",
        value_set=[],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "ticket_type_id:foreign_key"},
        column="ticket_type_id",
        value_set=[],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "ticket_priority_id:foreign_key"},
        column="ticket_priority_id",
        value_set=[],
    )
)

# For note_type rule, it applies to ticket_note.note_type (different table).
# Kept here as a placeholder only if validating a dataset containing note_type.
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "note_type:foreign_key"},
        column="note_type",
        value_set=[],
        mostly=1.0,
    )
)