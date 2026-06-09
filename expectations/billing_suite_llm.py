import great_expectations as gx

context = gx.get_context(mode="file")
suite = context.suites.get("expectation_suite")

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_history:domain:paymentmethod"},
        column="paymentmethod",
        value_set=["PrePaid", "PostPaid"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_plans:domain:planRecurringBillingSchedule"},
        column="planRecurringBillingSchedule",
        value_set=["Fixed", "Dynamic"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_plans:domain:planActive"},
        column="planActive",
        value_set=["yes", "no"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "financial_summary:format:finDate"},
        column="finDate",
        regex=r"^\d{4}/\d{2}$"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "financial_summary:unique:finDate"},
        column="finDate"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesToBeEqual(
        meta={"check_id": "invoice:custom:total"},
        column_A="total",
        column_B="amount_plus_tax_minus_discount",
        ignore_row_if="either_value_is_missing"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "payment:range:amount"},
        column="amount",
        min_value=0,
        strict_min=True
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "invoice_status:domain:value"},
        column="value",
        value_set=["open", "disputed", "draft", "sent", "paid", "partial"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "prepaid_transaction:range:due_date"},
        column_A="due_date",
        column_B="creationdate"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "prepaid_transaction:domain:type"},
        column="type",
        value_set=[1, 2, 3, 4, 5]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "payment_type:domain:value"},
        column="value",
        value_set=["PostPaid", "PrePaid_TOPUP", "PrePaid_CARD", "PostPaid_RollBack"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "tblcampaign:domain:cstatus"},
        column="cstatus",
        value_set=["Active", "InActive"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "tblcampaign:range:cend"},
        column_A="cend",
        column_B="cstart"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "tblgeneration:format:month"},
        column="month",
        regex=r"^\d{4}-\d{2}$"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tblgeneration:unique:month"},
        column="month"
    )
)