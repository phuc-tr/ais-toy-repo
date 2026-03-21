import great_expectations as gx
from datetime import date

context = gx.get_context(mode="file")

suite_name = "expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# -------------------------
# Table: ticket
# -------------------------
# Required columns exist
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

# Required fields not null
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
            meta={"check_id": f"contract:ticket:{col}:not_null"},
            column=col,
        )
    )

# Types / parseability
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket:ticket_id:type"},
        column="ticket_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket:ticket_customer_id:type"},
        column="ticket_customer_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket:ticket_status_id:type"},
        column="ticket_status_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket:ticket_type_id:type"},
        column="ticket_type_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket:ticket_priority_id:type"},
        column="ticket_priority_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket:ticket_owner_id:type"},
        column="ticket_owner_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeDateutilParseable(
        meta={"check_id": "contract:ticket:ticket_creationdate:date_parseable"},
        column="ticket_creationdate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "contract:ticket:ticket_creationtime:time_format"},
        column="ticket_creationtime",
        regex=r"^(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?$",
    )
)

# ticket_note maxLength 1000
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:ticket:ticket_note:max_length"},
        column="ticket_note",
        min_value=0,
        max_value=1000,
    )
)

# Quality rule: ticket must have valid creation date and time (already covered by not_null + parse/format)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket:ticket_creation_datetime_valid:creationdate_not_null"},
        column="ticket_creationdate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket:ticket_creation_datetime_valid:creationtime_not_null"},
        column="ticket_creationtime",
    )
)

# Quality rule: Closed tickets must have a close date
# (Using row-conditional expectation via "row_condition" and "condition_parser")
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket:closed_ticket_has_close_date"},
        column="ticket_closedate",
        row_condition="ticket_status_id == 2",
        condition_parser="great_expectations__experimental__condition_parser",
    )
)

# Freshness-ish: creation date should not be in the future (compare against current date)
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "contract:ticket:ticket_creationdate:not_in_future"},
        column="ticket_creationdate",
        min_value=None,
        max_value=date.today().isoformat(),
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
            meta={"check_id": f"contract:ticket_status:{col}:not_null"},
            column=col,
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
            meta={"check_id": f"contract:ticket_type:{col}:not_null"},
            column=col,
        )
    )

# -------------------------
# Table: ticket_priority
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:ticket_priority:ticket_priority_id:exists"},
        column="ticket_priority_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_priority:ticket_priority_id:not_null"},
        column="ticket_priority_id",
    )
)

# -------------------------
# Table: ticket_followup
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:ticket_followup:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_followup:id:not_null"},
        column="id",
    )
)

# -------------------------
# Table: ticket_note
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:ticket_note:ticket_note_id:exists"},
        column="ticket_note_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_note:ticket_note_id:not_null"},
        column="ticket_note_id",
    )
)

# -------------------------
# Table: ticket_note_type
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:ticket_note_type:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_note_type:id:not_null"},
        column="id",
    )
)

# -------------------------
# Table: ticket_transactions
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:ticket_transactions:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_transactions:id:not_null"},
        column="id",
    )
)

# -------------------------
# Contract quality rules that reference other tables (FK validity)
# Implemented as "column values in set" expectations; populate sets at runtime if available.
# These placeholders should be replaced with sets computed from the referenced tables.
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:ticket:valid_foreign_keys_ticket_status"},
        column="ticket_status_id",
        value_set=[],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:ticket:valid_foreign_keys_ticket_type"},
        column="ticket_type_id",
        value_set=[],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:ticket:valid_foreign_keys_ticket_priority"},
        column="ticket_priority_id",
        value_set=[],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:ticket_note:note_type_valid"},
        column="note_type",
        value_set=[],
    )
)