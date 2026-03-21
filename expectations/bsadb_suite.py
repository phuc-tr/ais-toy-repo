import datetime
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# -------------------------
# ticket table expectations
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

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket:ticket_id:type"},
        column="ticket_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "LongType", "IntegerType", "int"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket:ticket_customer_id:type"},
        column="ticket_customer_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "LongType", "IntegerType", "int"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket:ticket_status_id:type"},
        column="ticket_status_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "LongType", "IntegerType", "int"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket:ticket_type_id:type"},
        column="ticket_type_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "LongType", "IntegerType", "int"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket:ticket_priority_id:type"},
        column="ticket_priority_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "LongType", "IntegerType", "int"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket:ticket_owner_id:type"},
        column="ticket_owner_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "LongType", "IntegerType", "int"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeDateutilParseable(
        meta={"check_id": "contract:ticket:ticket_creationdate:date_parseable"},
        column="ticket_creationdate",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeDateutilParseable(
        meta={"check_id": "contract:ticket:ticket_creationtime:time_parseable"},
        column="ticket_creationtime",
    )
)

# ticket_note maxLength: 1000
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:ticket:ticket_note:exists"},
        column="ticket_note",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:ticket:ticket_note:max_length"},
        column="ticket_note",
        max_value=1000,
        min_value=0,
    )
)

# Quality rule: Ticket must have valid creation date and time (both not null)
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

# Quality rule: Closed tickets must have a close date (ticket_status_id = 2 => ticket_closedate not null)
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:ticket:ticket_closedate:exists"},
        column="ticket_closedate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket:closed_ticket_has_close_date"},
        column="ticket_closedate",
        row_condition='col("ticket_status_id") == 2',
        condition_parser="great_expectations",
    )
)

# ------------------------------
# ticket_status table expectations
# ------------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:ticket_status:ticket_status_id:exists"},
        column="ticket_status_id",
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

# ----------------------------
# ticket_type table expectations
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:ticket_type:ticket_type_id:exists"},
        column="ticket_type_id",
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
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:ticket_type:ticket_type_name:exists"},
        column="ticket_type_name",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_type:ticket_type_name:not_null"},
        column="ticket_type_name",
    )
)

# --------------------------------
# ticket_priority table expectations
# --------------------------------
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
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:ticket_priority:ticket_priority_id:unique"},
        column="ticket_priority_id",
    )
)

# -------------------------------
# ticket_note_type table expectations
# -------------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:ticket_note_type:note_type:exists"},
        column="note_type",
    )
)

# --------------------------
# ticket_note table expectations
# --------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:ticket_note:note_type:exists"},
        column="note_type",
    )
)

# Quality rule: note_type must exist in ticket_note_type.note_type (represented as allowed set check)
# (Populate allowed_note_types from the reference table at runtime in your pipeline)
allowed_note_types = []
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:ticket_note:note_type_valid"},
        column="note_type",
        value_set=allowed_note_types,
    )
)

# -------------------------
# Foreign key quality rules
# -------------------------
# Represented as allowed-set checks; populate these lists from the referenced tables at runtime.
allowed_ticket_status_ids = []
allowed_ticket_type_ids = []
allowed_ticket_priority_ids = []

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:ticket:valid_foreign_keys_ticket_status"},
        column="ticket_status_id",
        value_set=allowed_ticket_status_ids,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:ticket:valid_foreign_keys_ticket_type"},
        column="ticket_type_id",
        value_set=allowed_ticket_type_ids,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:ticket:valid_foreign_keys_ticket_priority"},
        column="ticket_priority_id",
        value_set=allowed_ticket_priority_ids,
    )
)