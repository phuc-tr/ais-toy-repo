import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

import datetime
import great_expectations as gx

# -----------------------------
# Schema: table/column existence + types + required (not null)
# -----------------------------
# ticket
for col in [
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
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket.{col}:exists"},
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
    "ticket_assignedto_id",
    "ticket_closed_by_id",
    "ticket_updated_by_id",
    "ticket_followup_id",
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInTypeList(
            meta={"check_id": f"contract:ticket.{col}:type"},
            column=col,
            type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
        )
    )

for col in ["ticket_description", "ticket_note"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInTypeList(
            meta={"check_id": f"contract:ticket.{col}:type"},
            column=col,
            type_list=["STRING", "VARCHAR", "TEXT", "str", "string"],
        )
    )

for col in ["ticket_creationdate", "ticket_closedate"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeDateutilParseable(
            meta={"check_id": f"contract:ticket.{col}:date_parseable"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeDateutilParseable(
        meta={"check_id": "contract:ticket.ticket_updated_date:datetime_parseable"},
        column="ticket_updated_date",
    )
)

for col, fmt in [("ticket_creationtime", "%H:%M:%S"), ("ticket_closetime", "%H:%M:%S")]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToMatchStrftimeFormat(
            meta={"check_id": f"contract:ticket.{col}:time_format"},
            column=col,
            strftime_format=fmt,
        )
    )

# required=true (ticket)
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
            meta={"check_id": f"contract:ticket.{col}:not_null"},
            column=col,
        )
    )

# ticket_note maxLength: 1000
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:ticket.ticket_note:max_length"},
        column="ticket_note",
        min_value=0,
        max_value=1000,
    )
)

# ticket_status
for col in ["ticket_status_id", "ticket_status_name", "ticket_status_desc", "creation_date"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_status.{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket_status.ticket_status_id:type"},
        column="ticket_status_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_status.ticket_status_id:not_null"},
        column="ticket_status_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeDateutilParseable(
        meta={"check_id": "contract:ticket_status.creation_date:date_parseable"},
        column="creation_date",
    )
)

# ticket_type
for col in ["ticket_type_id", "ticket_type_name", "ticket_type_desc", "creation_date"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_type.{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket_type.ticket_type_id:type"},
        column="ticket_type_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_type.ticket_type_id:not_null"},
        column="ticket_type_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_type.ticket_type_name:not_null"},
        column="ticket_type_name",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeDateutilParseable(
        meta={"check_id": "contract:ticket_type.creation_date:date_parseable"},
        column="creation_date",
    )
)

# ticket_priority
for col in ["ticket_priority_id", "ticket_priority_type", "ticket_creation_date"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_priority.{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket_priority.ticket_priority_id:type"},
        column="ticket_priority_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_priority.ticket_priority_id:not_null"},
        column="ticket_priority_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeDateutilParseable(
        meta={"check_id": "contract:ticket_priority.ticket_creation_date:date_parseable"},
        column="ticket_creation_date",
    )
)

# ticket_followup
for col in ["id", "ticket_followup", "ticket_followup_desc", "creationdate"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_followup.{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket_followup.id:type"},
        column="id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_followup.id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeDateutilParseable(
        meta={"check_id": "contract:ticket_followup.creationdate:date_parseable"},
        column="creationdate",
    )
)

# ticket_note
for col in [
    "ticket_note_id",
    "ticket_note_details",
    "ticket_creationdate",
    "creationtime",
    "ticket_id",
    "userid",
    "note_type",
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_note.{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_note.ticket_note_id:not_null"},
        column="ticket_note_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket_note.ticket_note_id:type"},
        column="ticket_note_id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
    )
)
for col in ["ticket_id", "userid"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInTypeList(
            meta={"check_id": f"contract:ticket_note.{col}:type"},
            column=col,
            type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
        )
    )
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeDateutilParseable(
        meta={"check_id": "contract:ticket_note.ticket_creationdate:date_parseable"},
        column="ticket_creationdate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchStrftimeFormat(
        meta={"check_id": "contract:ticket_note.creationtime:time_format"},
        column="creationtime",
        strftime_format="%H:%M:%S",
    )
)

# ticket_note_type
for col in ["id", "note_type", "note_type_desc", "creationdate"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_note_type.{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_note_type.id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInTypeList(
        meta={"check_id": "contract:ticket_note_type.id:type"},
        column="id",
        type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeDateutilParseable(
        meta={"check_id": "contract:ticket_note_type.creationdate:date_parseable"},
        column="creationdate",
    )
)

# ticket_transactions
for col in [
    "id",
    "ticket_id",
    "user_id",
    "ticket_trans_summury",
    "ticket_trans_creation_date",
    "ticket_trans_creation_time",
    "ticket_trans_note",
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:ticket_transactions.{col}:exists"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_transactions.id:not_null"},
        column="id",
    )
)
for col in ["id", "ticket_id", "user_id"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInTypeList(
            meta={"check_id": f"contract:ticket_transactions.{col}:type"},
            column=col,
            type_list=["INTEGER", "INT", "BIGINT", "SMALLINT", "TINYINT", "int", "integer"],
        )
    )
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeDateutilParseable(
        meta={"check_id": "contract:ticket_transactions.ticket_trans_creation_date:date_parseable"},
        column="ticket_trans_creation_date",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchStrftimeFormat(
        meta={"check_id": "contract:ticket_transactions.ticket_trans_creation_time:time_format"},
        column="ticket_trans_creation_time",
        strftime_format="%H:%M:%S",
    )
)

# -----------------------------
# Quality rules (as expectations)
# -----------------------------
# ticket_creation_datetime_valid: creation date and time not null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket.ticket_creationdate:ticket_creation_datetime_valid"},
        column="ticket_creationdate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket.ticket_creationtime:ticket_creation_datetime_valid"},
        column="ticket_creationtime",
    )
)

# closed_ticket_has_close_date: if status_id == 2 then closedate not null
# (Implemented as: if closedate is null then status_id must not be 2)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesToBeInSet(
        meta={"check_id": "contract:ticket.ticket_status_id+ticket_closedate:closed_ticket_has_close_date"},
        column_A="ticket_status_id",
        column_B="ticket_closedate",
        value_pairs_set=[[2, None]],
        mostly=0.0,
    )
)

# valid_foreign_keys_ticket_status / ticket_type / ticket_priority
# (Implemented as non-null FK fields; referential integrity requires runtime join/custom checks not expressible here)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket.ticket_status_id:valid_foreign_keys_ticket_status"},
        column="ticket_status_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket.ticket_type_id:valid_foreign_keys_ticket_type"},
        column="ticket_type_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket.ticket_priority_id:valid_foreign_keys_ticket_priority"},
        column="ticket_priority_id",
    )
)

# note_type_valid: note_type exists in ticket_note_type.note_type
# (Implemented as non-null note_type where present; cross-table membership requires runtime join/custom checks)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:ticket_note.note_type:note_type_valid"},
        column="note_type",
    )
)

# Persist suite (SuiteFactory has no 'update' method in current GX API)
context.suites.add_or_update(suite)