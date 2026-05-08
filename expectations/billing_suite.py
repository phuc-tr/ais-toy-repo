import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")

suite_name = "expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

now = datetime.utcnow()
freshness_cutoff = (now - timedelta(hours=24)).date().isoformat()

# ---------- billing_history ----------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:billing_history:paymentmethod_exists"},
        column="paymentmethod"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:billing_history:paymentmethod_accepted_values"},
        column="paymentmethod",
        value_set=["PrePaid", "PostPaid"]
    )
)

# ---------- billing_plans ----------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:billing_plans:planActive_exists"},
        column="planActive"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:billing_plans:planActive_accepted_values"},
        column="planActive",
        value_set=["yes", "no"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:billing_plans:planRecurringBillingSchedule_exists"},
        column="planRecurringBillingSchedule"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:billing_plans:planRecurringBillingSchedule_accepted_values"},
        column="planRecurringBillingSchedule",
        value_set=["Fixed", "Dynamic"]
    )
)

# ---------- financial_summary ----------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:financial_summary:finDate_exists"},
        column="finDate"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "contract:financial_summary:finDate_regex"},
        column="finDate",
        regex=r"^\d{4}/\d{2}$"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:financial_summary:finDate_unique"},
        column="finDate"
    )
)

# ---------- invoice ----------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:invoice:total_consistency_exists"},
        column="total"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:invoice:amount_exists"},
        column="amount"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:invoice:tax_amount_exists"},
        column="tax_amount"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:invoice:discount_exists"},
        column="discount"
    )
)

suite.add_expectation(
    gx.expectations.ExpectMulticolumnSumToEqual(
        meta={"check_id": "contract:invoice:total_equals_amount_plus_tax_minus_discount"},
        column_list=["amount", "tax_amount", "discount", "total"],
        sum_total=None
    )
)

# ---------- invoice_status ----------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:invoice_status:value_exists"},
        column="value"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:invoice_status:value_accepted_values"},
        column="value",
        value_set=["open", "disputed", "draft", "sent", "paid", "partial"]
    )
)

# ---------- payment ----------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:payment:invoice_id_exists"},
        column="invoice_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeNotNull(
        meta={"check_id": "contract:payment:invoice_id_not_null"},
        column="invoice_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:payment:amount_exists"},
        column="amount"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:payment:amount_positive"},
        column="amount",
        min_value=0,
        strictly_minimum=True
    )
)

# ---------- payment_type ----------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:payment_type:value_exists"},
        column="value"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:payment_type:value_accepted_values"},
        column="value",
        value_set=["PostPaid", "PrePaid_TOPUP", "PrePaid_CARD", "PostPaid_RollBack"]
    )
)

# ---------- prepaid_transaction ----------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:prepaid_transaction:type_exists"},
        column="type"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:prepaid_transaction:type_accepted_values"},
        column="type",
        value_set=[1, 2, 3, 4, 5]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:prepaid_transaction:due_date_exists"},
        column="due_date"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:prepaid_transaction:creationdate_exists"},
        column="creationdate"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "contract:prepaid_transaction:due_date_after_creationdate"},
        column_A="due_date",
        column_B="creationdate",
        or_equal=True
    )
)

# ---------- tblcampaign ----------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tblcampaign:cstatus_exists"},
        column="cstatus"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:tblcampaign:cstatus_accepted_values"},
        column="cstatus",
        value_set=["Active", "InActive"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tblcampaign:cstart_exists"},
        column="cstart"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tblcampaign:cend_exists"},
        column="cend"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "contract:tblcampaign:cend_after_cstart"},
        column_A="cend",
        column_B="cstart",
        or_equal=True
    )
)

# ---------- tblgeneration ----------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tblgeneration:month_exists"},
        column="month"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "contract:tblgeneration:month_regex"},
        column="month",
        regex=r"^\d{4}-\d{2}$"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:tblgeneration:month_unique"},
        column="month"
    )
)

# ---------- tbllinetransactions ----------
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:tbllinetransactions:typeid_exists"},
        column="typeid"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:tbllinetransactions:typeid_not_null"},
        column="typeid"
    )
)

# ---------- Freshness (generic, using creation/update dates where present) ----------
for model, date_col in [
    ("billing_history", "creationdate"),
    ("invoice", "creationdate"),
    ("payment", "creationdate"),
    ("prepaid_transaction", "creationdate"),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"contract:{model}:{date_col}_exists"},
            column=date_col
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            meta={"check_id": f"contract:{model}:{date_col}_fresh_within_24h"},
            column=date_col,
            min_value=freshness_cutoff,
            max_value=None
        )
    )