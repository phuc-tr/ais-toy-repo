import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# billing_history
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_history:domain:paymentmethod"},
        column="paymentmethod",
        value_set=["PrePaid", "PostPaid"]
    )
)

# billing_plans
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_plans:domain:planActive"},
        column="planActive",
        value_set=["yes", "no"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_plans:domain:planRecurringBillingSchedule"},
        column="planRecurringBillingSchedule",
        value_set=["Fixed", "Dynamic"]
    )
)

# financial_summary
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "financial_summary:regex:finDate"},
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

# invoice
suite.add_expectation(
    gx.expectations.ExpectMulticolumnSumToEqual(
        meta={"check_id": "invoice:custom:total_formula"},
        column_list=["amount", "tax_amount", "discount"],
        sum_total=0.0,
        ignore_row_if="any_value_is_missing"
    )
)

# invoice_status
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "invoice_status:domain:value"},
        column="value",
        value_set=["open", "disputed", "draft", "sent", "paid", "partial"]
    )
)

# payment
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "payment:custom:amount"},
        column="amount",
        min_value=0,
        strict_min=True
    )
)

# payment_type
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "payment_type:domain:value"},
        column="value",
        value_set=["PostPaid", "PrePaid_TOPUP", "PrePaid_CARD", "PostPaid_RollBack"]
    )
)

# prepaid_transaction
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "prepaid_transaction:domain:type"},
        column="type",
        value_set=[1, 2, 3, 4, 5]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "prepaid_transaction:custom:due_date"},
        column_A="due_date",
        column_B="creationdate",
        or_equal=True
    )
)

# tblcampaign
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "tblcampaign:domain:cstatus"},
        column="cstatus",
        value_set=["Active", "InActive"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "tblcampaign:custom:cend_after_cstart"},
        column_A="cend",
        column_B="cstart",
        or_equal=True
    )
)

# tblgeneration
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "tblgeneration:regex:month"},
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

# tbllinetype
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tbllinetype:completeness:transtype"},
        column="transtype"
    )
)