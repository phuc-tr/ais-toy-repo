import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# ----------------------------
# Required (NOT NULL) columns
# ----------------------------
for check_id, column in [
    ("ticket_id_not_null", "ticket_id"),
    ("ticket_customer_id_not_null", "ticket_customer_id"),
    ("ticket_status_id_not_null", "ticket_status_id"),
    ("ticket_type_id_not_null", "ticket_type_id"),
    ("ticket_priority_id_not_null", "ticket_priority_id"),
    ("ticket_owner_id_not_null", "ticket_owner_id"),
    ("ticket_creationdate_not_null", "ticket_creationdate"),
    ("ticket_creationtime_not_null", "ticket_creationtime"),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            meta={"check_id": check_id},
            column=column,
        )
    )

# ----------------------------
# Type expectations (contract)
# ----------------------------
for check_id, column, t in [
    ("ticket_id_type_integer", "ticket_id", "INTEGER"),
    ("ticket_customer_id_type_integer", "ticket_customer_id", "INTEGER"),
    ("ticket_status_id_type_integer", "ticket_status_id", "INTEGER"),
    ("ticket_type_id_type_integer", "ticket_type_id", "INTEGER"),
    ("ticket_priority_id_type_integer", "ticket_priority_id", "INTEGER"),
    ("ticket_owner_id_type_integer", "ticket_owner_id", "INTEGER"),
    ("ticket_assignedto_id_type_integer", "ticket_assignedto_id", "INTEGER"),
    ("ticket_closed_by_id_type_integer", "ticket_closed_by_id", "INTEGER"),
    ("ticket_updated_by_id_type_integer", "ticket_updated_by_id", "INTEGER"),
    ("ticket_followup_id_type_integer", "ticket_followup_id", "INTEGER"),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": check_id},
            column=column,
            type_=t,
        )
    )

for check_id, column, t in [
    ("ticket_creationdate_type_date", "ticket_creationdate", "DATE"),
    ("ticket_closedate_type_date", "ticket_closedate", "DATE"),
    ("ticket_updated_date_type_datetime", "ticket_updated_date", "DATETIME"),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": check_id},
            column=column,
            type_=t,
        )
    )

for check_id, column, t in [
    ("ticket_creationtime_type_time", "ticket_creationtime", "TIME"),
    ("ticket_closetime_type_time", "ticket_closetime", "TIME"),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": check_id},
            column=column,
            type_=t,
        )
    )

# ----------------------------
# Length constraints
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "ticket_note_max_length_1000"},
        column="ticket_note",
        min_value=0,
        max_value=1000,
        mostly=1.0,
    )
)

# ------------------------------------
# Row-level quality rules from contract
# ------------------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket_creation_datetime_valid"},
        column="ticket_creationdate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "ticket_creation_datetime_valid_time"},
        column="ticket_creationtime",
    )
)

# If ticket_status_id == 2 (closed), then ticket_closedate must not be null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "closed_ticket_has_close_date"},
        column="ticket_closedate",
        row_condition='col("ticket_status_id") == 2',
        condition_parser="great_expectations",
    )
)

# ------------------------------------
# Foreign key / relationship validations
# (validate that IDs exist in reference tables)
# ------------------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "valid_foreign_keys_ticket_status"},
        column="ticket_status_id",
        value_set=[
            1,
            2,
            3,
            4,
            5,
        ],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "valid_foreign_keys_ticket_type"},
        column="ticket_type_id",
        value_set=[
            1,
            2,
            3,
            4,
            5,
        ],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "valid_foreign_keys_ticket_priority"},
        column="ticket_priority_id",
        value_set=[
            1,
            2,
            3,
            4,
            5,
        ],
    )
)

# Note type validity (applies to ticket_note table, included here for completeness
# if validating a joined/denormalized dataset that contains note_type)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "note_type_valid"},
        column="note_type",
        value_set=["normal", "internal", "system"],
        mostly=1.0,
    )
)