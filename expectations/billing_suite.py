import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# -------------------------
# billing_history
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "billing_history:key:id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_history:key:id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_history:domain:paymentmethod"},
        column="paymentmethod",
        value_set=["PrePaid", "PostPaid"],
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotMatchRegex(
        meta={"check_id": "billing_history:pii:phone_masking_check"},
        column="phone",
        regex="^[Xx*]+$",
        mostly=0.0,
    )
)

# -------------------------
# billing_plans
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "billing_plans:key:id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_plans:key:id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "billing_plans:business:planName_unique"},
        column="planName",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_plans:business:planName_not_null"},
        column="planName",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_plans:domain:planActive"},
        column="planActive",
        value_set=["yes", "no"],
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_plans:domain:planRecurringBillingSchedule"},
        column="planRecurringBillingSchedule",
        value_set=["Fixed", "Dynamic"],
        mostly=1.0,
    )
)

# -------------------------
# financial_summary
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "financial_summary:key:id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "financial_summary:key:id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "financial_summary:format:finDate_regex"},
        column="finDate",
        regex=r"^\d{4}/\d{2}$",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "financial_summary:unique:finDate"},
        column="finDate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "financial_summary:range:total_non_negative"},
        column="total",
        min_value=0,
        max_value=None,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "financial_summary:range:num_trans_non_negative"},
        column="num_trans",
        min_value=0,
        max_value=None,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "financial_summary:range:num_customers_non_negative"},
        column="num_customers",
        min_value=0,
        max_value=None,
    )
)

# -------------------------
# invoice
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "invoice:key:id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:key:id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:required:date_not_null"},
        column="date",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:required:amount_not_null"},
        column="amount",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:required:tax_amount_not_null"},
        column="tax_amount",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:required:total_not_null"},
        column="total",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:required:statusId_not_null"},
        column="statusId",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:required:discount_not_null"},
        column="discount",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice:range:amount_non_negative"},
        column="amount",
        min_value=0,
        max_value=None,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice:range:tax_amount_non_negative"},
        column="tax_amount",
        min_value=0,
        max_value=None,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice:range:total_non_negative"},
        column="total",
        min_value=0,
        max_value=None,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice:range:discount_non_negative"},
        column="discount",
        min_value=0,
        max_value=None,
    )
)
suite.add_expectation(
    gx.expectations.ExpectMulticolumnSumToEqual(
        meta={"check_id": "invoice:custom:total"},
        column_list=["amount", "tax_amount", "discount"],
        sum_total=1.0,
        ignore_row_if="any_value_is_missing",
    )
)

# -------------------------
# invoice_status
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "invoice_status:key:id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice_status:key:id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "invoice_status:domain:value"},
        column="value",
        value_set=["open", "disputed", "draft", "sent", "paid", "partial"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice_status:required:value_not_null"},
        column="value",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice_status:required:notes_not_null"},
        column="notes",
    )
)

# -------------------------
# payment
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "payment:key:id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:key:id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:required:invoice_id_not_null"},
        column="invoice_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:required:amount_not_null"},
        column="amount",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:required:date_not_null"},
        column="date",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:required:type_id_not_null"},
        column="type_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:required:notes_not_null"},
        column="notes",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "payment:custom:amount_gt_zero"},
        column="amount",
        min_value=0,
        max_value=None,
    )
)

# -------------------------
# payment_type
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "payment_type:key:id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment_type:key:id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "payment_type:domain:value"},
        column="value",
        value_set=["PostPaid", "PrePaid_TOPUP", "PrePaid_CARD", "PostPaid_RollBack"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment_type:required:value_not_null"},
        column="value",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment_type:required:notes_not_null"},
        column="notes",
    )
)

# -------------------------
# prepaid_transaction
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "prepaid_transaction:key:id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:key:id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:required:balance_before_not_null"},
        column="balance_before",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:required:amount_not_null"},
        column="amount",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:required:bounce_not_null"},
        column="bounce",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "prepaid_transaction:range:bounce_non_negative"},
        column="bounce",
        min_value=0,
        max_value=None,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:required:allowance_not_null"},
        column="allowance",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:required:balance_current_not_null"},
        column="balance_current",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:required:due_date_not_null"},
        column="due_date",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:required:userID_not_null"},
        column="userID",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:required:trans_status_not_null"},
        column="trans_status",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:required:creationdate_not_null"},
        column="creationdate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "prepaid_transaction:domain:type"},
        column="type",
        value_set=[1, 2, 3, 4, 5],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "prepaid_transaction:custom:due_date"},
        column_A="due_date",
        column_B="creationdate",
        or_equal=True,
    )
)

# -------------------------
# tblcampaign
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tblcampaign:key:id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblcampaign:key:id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tblcampaign:business:Name_unique"},
        column="Name",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblcampaign:business:Name_not_null"},
        column="Name",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "tblcampaign:range:value_0_1"},
        column="value",
        min_value=0,
        max_value=1,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "tblcampaign:domain:cstatus"},
        column="cstatus",
        value_set=["Active", "InActive"],
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblcampaign:required:description_not_null"},
        column="description",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "tblcampaign:range:period_non_negative"},
        column="period",
        min_value=0,
        max_value=None,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "tblcampaign:custom:cend"},
        column_A="cend",
        column_B="cstart",
        or_equal=True,
    )
)

# -------------------------
# tblgeneration
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tblgeneration:key:gid_unique"},
        column="gid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblgeneration:key:gid_not_null"},
        column="gid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "tblgeneration:format:month_regex"},
        column="month",
        regex=r"^\d{4}-\d{2}$",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tblgeneration:unique:month"},
        column="month",
    )
)

# -------------------------
# tbllinetype
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tbllinetype:key:id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tbllinetype:key:id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tbllinetype:required:transtype_not_null"},
        column="transtype",
    )
)

# -------------------------
# tbllinetransactions
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tbllinetransactions:key:id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tbllinetransactions:key:id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tbllinetransactions:required:transdate_not_null"},
        column="transdate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tbllinetransactions:referential_integrity:typeid"},
        column="typeid",
    )
)

context.suites.add_or_update(suite)