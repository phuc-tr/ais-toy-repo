import datetime as dt
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

today = dt.date.today()
now = dt.datetime.now()

# -----------------------------
# billing_history
# -----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:billing_history:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:billing_history:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:billing_history:id:unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:billing_history:id:minimum"},
        column="id",
        min_value=1,
        max_value=None,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:billing_history:phone:exists"},
        column="phone",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:billing_history:phone:max_length"},
        column="phone",
        min_value=0,
        max_value=200,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:billing_history:billAction:exists"},
        column="billAction",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:billing_history:billAction:not_null"},
        column="billAction",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:billing_history:billAction:max_length"},
        column="billAction",
        min_value=0,
        max_value=128,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:billing_history:paymentmethod:exists"},
        column="paymentmethod",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:billing_history:paymentmethod:max_length"},
        column="paymentmethod",
        min_value=0,
        max_value=200,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:billing_history:paymentmethod:accepted_values"},
        column="paymentmethod",
        value_set=["PrePaid", "PostPaid"],
    )
)

# Freshness (24h) using creationdate
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:billing_history:creationdate:exists"},
        column="creationdate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:billing_history:creationdate:freshness_24h"},
        column="creationdate",
        min_value=now - dt.timedelta(hours=24),
        max_value=now,
    )
)

# Length constraints
for col, mx in [
    ("billAmount", 200),
    ("billPerformer", 200),
    ("billReason", 200),
    ("notes", 200),
    ("creationby", 128),
    ("updateby", 128),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:billing_history:{col}:exists"},
            column=col,
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValueLengthsToBeBetween(
            meta={"check_id": f"contract:billing_history:{col}:max_length"},
            column=col,
            min_value=0,
            max_value=mx,
        )
    )

# -----------------------------
# billing_plans
# -----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:billing_plans:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:billing_plans:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:billing_plans:id:unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:billing_plans:id:minimum"},
        column="id",
        min_value=1,
        max_value=None,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:billing_plans:planName:exists"},
        column="planName",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:billing_plans:planName:not_null"},
        column="planName",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:billing_plans:planName:unique"},
        column="planName",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:billing_plans:planName:max_length"},
        column="planName",
        min_value=0,
        max_value=128,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:billing_plans:planRecurringBillingSchedule:exists"},
        column="planRecurringBillingSchedule",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:billing_plans:planRecurringBillingSchedule:max_length"},
        column="planRecurringBillingSchedule",
        min_value=0,
        max_value=128,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:billing_plans:planRecurringBillingSchedule:accepted_values"},
        column="planRecurringBillingSchedule",
        value_set=["Fixed", "Dynamic"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:billing_plans:planActive:exists"},
        column="planActive",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:billing_plans:planActive:max_length"},
        column="planActive",
        min_value=0,
        max_value=32,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:billing_plans:planActive:accepted_values"},
        column="planActive",
        value_set=["yes", "no"],
    )
)

# Generic length constraints for billing_plans string fields with maxLength
for col, mx in [
    ("planType", 128),
    ("planBandwidthUp", 128),
    ("planBandwidthDown", 128),
    ("planTrafficTotal", 128),
    ("planTrafficUp", 128),
    ("planTrafficDown", 128),
    ("planTrafficRefillCost", 128),
    ("planRecurring", 128),
    ("planRecurringPeriod", 128),
    ("planCost", 128),
    ("planSetupCost", 128),
    ("planTax", 128),
    ("planCurrency", 128),
    ("notes", 200),
    ("creationby", 128),
    ("updateby", 128),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:billing_plans:{col}:exists"},
            column=col,
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValueLengthsToBeBetween(
            meta={"check_id": f"contract:billing_plans:{col}:max_length"},
            column=col,
            min_value=0,
            max_value=mx,
        )
    )

# -----------------------------
# financial_summary
# -----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:financial_summary:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:financial_summary:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:financial_summary:id:unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:financial_summary:id:minimum"},
        column="id",
        min_value=1,
        max_value=None,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:financial_summary:finDate:exists"},
        column="finDate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:financial_summary:finDate:max_length"},
        column="finDate",
        min_value=0,
        max_value=50,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "contract:financial_summary:finDate:regex"},
        column="finDate",
        regex=r"^\d{4}/\d{2}$",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:financial_summary:finDate:unique"},
        column="finDate",
    )
)

for col in ["total", "num_trans", "num_customers"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:financial_summary:{col}:exists"},
            column=col,
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            meta={"check_id": f"contract:financial_summary:{col}:minimum"},
            column=col,
            min_value=0,
            max_value=None,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:financial_summary:note:exists"},
        column="note",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:financial_summary:note:max_length"},
        column="note",
        min_value=0,
        max_value=200,
    )
)

# -----------------------------
# invoice
# -----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:invoice:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:invoice:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:invoice:id:unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:invoice:id:minimum"},
        column="id",
        min_value=1,
        max_value=None,
    )
)

for col in ["date", "amount", "tax_amount", "total", "statusId", "discount"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:invoice:{col}:exists"},
            column=col,
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            meta={"check_id": f"contract:invoice:{col}:not_null"},
            column=col,
        )
    )

for col in ["amount", "tax_amount", "total", "discount"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            meta={"check_id": f"contract:invoice:{col}:minimum"},
            column=col,
            min_value=0,
            max_value=None,
        )
    )

# Custom: total = amount + tax_amount - discount (tolerance ±0.01)
suite.add_expectation(
    gx.expectations.ExpectMulticolumnSumToEqual(
        meta={"check_id": "contract:invoice:total:equals_amount_plus_tax_minus_discount"},
        column_list=["amount", "tax_amount", "discount"],
        sum_total="total",
        # Use atol to represent tolerance
        atol=0.01,
    )
)

for col, mx in [
    ("notes", 128),
    ("creationby", 128),
    ("updateby", 128),
    ("btype", 3),
    ("prefix", 2),
    ("offerName", 150),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:invoice:{col}:exists"},
            column=col,
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValueLengthsToBeBetween(
            meta={"check_id": f"contract:invoice:{col}:max_length"},
            column=col,
            min_value=0,
            max_value=mx,
        )
    )

# Freshness (24h) using invoice.date
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:invoice:date:freshness_24h"},
        column="date",
        min_value=now - dt.timedelta(hours=24),
        max_value=now,
    )
)

# -----------------------------
# invoice_status
# -----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:invoice_status:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:invoice_status:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:invoice_status:id:unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:invoice_status:id:minimum"},
        column="id",
        min_value=1,
        max_value=None,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:invoice_status:value:exists"},
        column="value",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:invoice_status:value:not_null"},
        column="value",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:invoice_status:value:max_length"},
        column="value",
        min_value=0,
        max_value=32,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:invoice_status:value:accepted_values"},
        column="value",
        value_set=["open", "disputed", "draft", "sent", "paid", "partial"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:invoice_status:notes:exists"},
        column="notes",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:invoice_status:notes:not_null"},
        column="notes",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:invoice_status:notes:max_length"},
        column="notes",
        min_value=0,
        max_value=128,
    )
)

for col in ["creationby", "updateby"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:invoice_status:{col}:exists"},
            column=col,
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValueLengthsToBeBetween(
            meta={"check_id": f"contract:invoice_status:{col}:max_length"},
            column=col,
            min_value=0,
            max_value=128,
        )
    )

# -----------------------------
# payment
# -----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:payment:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:payment:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:payment:id:unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:payment:id:minimum"},
        column="id",
        min_value=1,
        max_value=None,
    )
)

for col in ["invoice_id", "amount", "date", "type_id", "notes"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:payment:{col}:exists"},
            column=col,
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            meta={"check_id": f"contract:payment:{col}:not_null"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:payment:amount:greater_than_zero"},
        column="amount",
        min_value=1e-12,
        max_value=None,
        strict_min=True,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:payment:notes:max_length"},
        column="notes",
        min_value=0,
        max_value=128,
    )
)

for col in ["creationby", "updateby"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:payment:{col}:exists"},
            column=col,
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValueLengthsToBeBetween(
            meta={"check_id": f"contract:payment:{col}:max_length"},
            column=col,
            min_value=0,
            max_value=128,
        )
    )

# Freshness (24h) using payment.date
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:payment:date:freshness_24h"},
        column="date",
        min_value=now - dt.timedelta(hours=24),
        max_value=now,
    )
)

# Referential integrity (payment.invoice_id -> invoice.id) via query expectation (SQL capable execution engine)
suite.add_expectation(
    gx.expectations.ExpectQueryResultsToMatchComparison(
        meta={"check_id": "contract:payment:invoice_id:referential_integrity"},
        query="""
            SELECT COUNT(*) AS missing_fk_count
            FROM payment p
            LEFT JOIN invoice i ON p.invoice_id = i.id
            WHERE p.invoice_id IS NOT NULL AND i.id IS NULL
        """,
        comparison_operator="=",
        comparison_value=0,
    )
)

# -----------------------------
# payment_type
# -----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:payment_type:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:payment_type:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:payment_type:id:unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:payment_type:id:minimum"},
        column="id",
        min_value=1,
        max_value=None,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:payment_type:value:exists"},
        column="value",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:payment_type:value:not_null"},
        column="value",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:payment_type:value:max_length"},
        column="value",
        min_value=0,
        max_value=32,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:payment_type:value:accepted_values"},
        column="value",
        value_set=["PostPaid", "PrePaid_TOPUP", "PrePaid_CARD", "PostPaid_RollBack"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:payment_type:notes:exists"},
        column="notes",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:payment_type:notes:not_null"},
        column="notes",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:payment_type:notes:max_length"},
        column="notes",
        min_value=0,
        max_value=128,
    )
)

for col in ["creationby", "updateby"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:payment_type:{col}:exists"},
            column=col,
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValueLengthsToBeBetween(
            meta={"check_id": f"contract:payment_type:{col}:max_length"},
            column=col,
            min_value=0,
            max_value=128,
        )
    )

# -----------------------------
# prepaid_transaction
# -----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:prepaid_transaction:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:prepaid_transaction:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:prepaid_transaction:id:unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:prepaid_transaction:id:minimum"},
        column="id",
        min_value=1,
        max_value=None,
    )
)

for col in [
    "balance_before",
    "amount",
    "bounce",
    "allowance",
    "balance_current",
    "due_date",
    "userID",
    "trans_status",
    "creationdate",
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:prepaid_transaction:{col}:exists"},
            column=col,
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            meta={"check_id": f"contract:prepaid_transaction:{col}:not_null"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:prepaid_transaction:bounce:minimum"},
        column="bounce",
        min_value=0,
        max_value=None,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:prepaid_transaction:type:exists"},
        column="type",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:prepaid_transaction:type:accepted_values"},
        column="type",
        value_set=[1, 2, 3, 4, 5],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:prepaid_transaction:note:exists"},
        column="note",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:prepaid_transaction:note:max_length"},
        column="note",
        min_value=0,
        max_value=250,
    )
)

# Custom: due_date >= DATE(creationdate) (use query-based comparison)
suite.add_expectation(
    gx.expectations.ExpectQueryResultsToMatchComparison(
        meta={"check_id": "contract:prepaid_transaction:due_date:gte_creationdate"},
        query="""
            SELECT COUNT(*) AS bad_count
            FROM prepaid_transaction
            WHERE due_date IS NOT NULL
              AND creationdate IS NOT NULL
              AND due_date < DATE(creationdate)
        """,
        comparison_operator="=",
        comparison_value=0,
    )
)

# Freshness (24h) using prepaid_transaction.creationdate
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:prepaid_transaction:creationdate:freshness_24h"},
        column="creationdate",
        min_value=now - dt.timedelta(hours=24),
        max_value=now,
    )
)

# -----------------------------
# tblcampaign
# -----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tblcampaign:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:tblcampaign:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:tblcampaign:id:unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:tblcampaign:id:minimum"},
        column="id",
        min_value=1,
        max_value=None,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tblcampaign:Name:exists"},
        column="Name",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:tblcampaign:Name:not_null"},
        column="Name",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:tblcampaign:Name:unique"},
        column="Name",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:tblcampaign:Name:max_length"},
        column="Name",
        min_value=0,
        max_value=255,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tblcampaign:value:exists"},
        column="value",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:tblcampaign:value:not_null"},
        column="value",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:tblcampaign:value:range_0_1"},
        column="value",
        min_value=0,
        max_value=1,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tblcampaign:cstatus:exists"},
        column="cstatus",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:tblcampaign:cstatus:max_length"},
        column="cstatus",
        min_value=0,
        max_value=200,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:tblcampaign:cstatus:accepted_values"},
        column="cstatus",
        value_set=["Active", "InActive"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tblcampaign:description:exists"},
        column="description",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:tblcampaign:description:not_null"},
        column="description",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:tblcampaign:description:max_length"},
        column="description",
        min_value=0,
        max_value=255,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tblcampaign:period:exists"},
        column="period",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:tblcampaign:period:minimum"},
        column="period",
        min_value=0,
        max_value=None,
    )
)

# Custom: cend >= cstart when both populated (or either NULL)
suite.add_expectation(
    gx.expectations.ExpectQueryResultsToMatchComparison(
        meta={"check_id": "contract:tblcampaign:cend:gte_cstart_when_populated"},
        query="""
            SELECT COUNT(*) AS bad_count
            FROM tblcampaign
            WHERE cend IS NOT NULL AND cstart IS NOT NULL AND cend < cstart
        """,
        comparison_operator="=",
        comparison_value=0,
    )
)

for col in ["creationby", "updateby"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:tblcampaign:{col}:exists"},
            column=col,
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValueLengthsToBeBetween(
            meta={"check_id": f"contract:tblcampaign:{col}:max_length"},
            column=col,
            min_value=0,
            max_value=128,
        )
    )

# -----------------------------
# tblgeneration
# -----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tblgeneration:gid:exists"},
        column="gid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:tblgeneration:gid:not_null"},
        column="gid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:tblgeneration:gid:unique"},
        column="gid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:tblgeneration:gid:minimum"},
        column="gid",
        min_value=1,
        max_value=None,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tblgeneration:month:exists"},
        column="month",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:tblgeneration:month:max_length"},
        column="month",
        min_value=0,
        max_value=10,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "contract:tblgeneration:month:regex"},
        column="month",
        regex=r"^\d{4}-\d{2}$",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:tblgeneration:month:unique"},
        column="month",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tblgeneration:note:exists"},
        column="note",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:tblgeneration:note:max_length"},
        column="note",
        min_value=0,
        max_value=250,
    )
)

# -----------------------------
# tbllinetype
# -----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tbllinetype:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:tbllinetype:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:tbllinetype:id:unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:tbllinetype:id:minimum"},
        column="id",
        min_value=1,
        max_value=None,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tbllinetype:transtype:exists"},
        column="transtype",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:tbllinetype:transtype:max_length"},
        column="transtype",
        min_value=0,
        max_value=50,
    )
)

# -----------------------------
# tbllinetransactions
# -----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tbllinetransactions:id:exists"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:tbllinetransactions:id:not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:tbllinetransactions:id:unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:tbllinetransactions:id:minimum"},
        column="id",
        min_value=1,
        max_value=None,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tbllinetransactions:transdate:exists"},
        column="transdate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:tbllinetransactions:transdate:not_null"},
        column="transdate",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tbllinetransactions:description:exists"},
        column="description",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:tbllinetransactions:description:max_length"},
        column="description",
        min_value=0,
        max_value=255,
    )
)

# Referential integrity (tbllinetransactions.typeid -> tbllinetype.id) via query expectation
suite.add_expectation(
    gx.expectations.ExpectQueryResultsToMatchComparison(
        meta={"check_id": "contract:tbllinetransactions:typeid:referential_integrity"},
        query="""
            SELECT COUNT(*) AS missing_fk_count
            FROM tbllinetransactions t
            LEFT JOIN tbllinetype lt ON t.typeid = lt.id
            WHERE t.typeid IS NOT NULL AND lt.id IS NULL
        """,
        comparison_operator="=",
        comparison_value=0,
    )
)

# Freshness (24h) using tbllinetransactions.transdate (date-based)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:tbllinetransactions:transdate:freshness_24h"},
        column="transdate",
        min_value=today - dt.timedelta(days=1),
        max_value=today,
    )
)

context.suites.save(suite)