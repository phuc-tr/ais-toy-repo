import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# ----------------------------
# billing_history
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_history.id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "billing_history.id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "billing_history.id_min_1"},
        column="id",
        min_value=1,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_history.billAction_not_null"},
        column="billAction",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "billing_history.billAction_max_len_128"},
        column="billAction",
        max_value=128,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "billing_history.phone_max_len_200"},
        column="phone",
        max_value=200,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "billing_history.planId_min_1_if_present"},
        column="planId",
        min_value=1,
        mostly=1.0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "billing_history.billAmount_max_len_200"},
        column="billAmount",
        max_value=200,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "billing_history.billPerformer_max_len_200"},
        column="billPerformer",
        max_value=200,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "billing_history.billReason_max_len_200"},
        column="billReason",
        max_value=200,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_history.paymentmethod_domain_prepaid_postpaid"},
        column="paymentmethod",
        value_set=["PrePaid", "PostPaid"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "billing_history.bounce_min_0_if_present"},
        column="bounce",
        min_value=0,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "billing_history.notes_max_len_200"},
        column="notes",
        max_value=200,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "billing_history.creationby_max_len_128"},
        column="creationby",
        max_value=128,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "billing_history.updateby_max_len_128"},
        column="updateby",
        max_value=128,
    )
)

# ----------------------------
# billing_plans
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_plans.id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "billing_plans.id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "billing_plans.id_min_1"},
        column="id",
        min_value=1,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_plans.planName_not_null"},
        column="planName",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "billing_plans.planName_unique"},
        column="planName",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "billing_plans.planName_max_len_128"},
        column="planName",
        max_value=128,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_plans.planActive_domain_yes_no"},
        column="planActive",
        value_set=["yes", "no"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_plans.planRecurringBillingSchedule_domain_fixed_dynamic"},
        column="planRecurringBillingSchedule",
        value_set=["Fixed", "Dynamic"],
    )
)

# ----------------------------
# financial_summary
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "financial_summary.id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "financial_summary.id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "financial_summary.id_min_1"},
        column="id",
        min_value=1,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "financial_summary.finDate_regex_yyyy_mm_slash"},
        column="finDate",
        regex=r"^\d{4}/\d{2}$",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "financial_summary.finDate_unique"},
        column="finDate",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "financial_summary.total_min_0"},
        column="total",
        min_value=0,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "financial_summary.num_trans_min_0"},
        column="num_trans",
        min_value=0,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "financial_summary.num_customers_min_0"},
        column="num_customers",
        min_value=0,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "financial_summary.note_max_len_200"},
        column="note",
        max_value=200,
    )
)

# ----------------------------
# invoice
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice.id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "invoice.id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice.id_min_1"},
        column="id",
        min_value=1,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice.date_not_null"},
        column="date",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice.amount_not_null"},
        column="amount",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice.amount_min_0"},
        column="amount",
        min_value=0,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice.tax_amount_not_null"},
        column="tax_amount",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice.tax_amount_min_0"},
        column="tax_amount",
        min_value=0,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice.total_not_null"},
        column="total",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice.total_min_0"},
        column="total",
        min_value=0,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice.discount_not_null"},
        column="discount",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice.discount_min_0"},
        column="discount",
        min_value=0,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice.statusId_not_null"},
        column="statusId",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "invoice.notes_max_len_128"},
        column="notes",
        max_value=128,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "invoice.creationby_max_len_128"},
        column="creationby",
        max_value=128,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "invoice.updateby_max_len_128"},
        column="updateby",
        max_value=128,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "invoice.btype_max_len_3"},
        column="btype",
        max_value=3,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "invoice.prefix_max_len_2"},
        column="prefix",
        max_value=2,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "invoice.offerName_max_len_150"},
        column="offerName",
        max_value=150,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice.user_id_min_1_if_present"},
        column="user_id",
        min_value=1,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice.plan_id_min_1_if_present"},
        column="plan_id",
        min_value=1,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice.nid_min_1_if_present"},
        column="nid",
        min_value=1,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice.generationid_min_1_if_present"},
        column="generationid",
        min_value=1,
        mostly=1.0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectTableRowCountToBeBetween(
        meta={"check_id": "invoice.row_count_gt_0"},
        min_value=1,
    )
)

# ----------------------------
# invoice_status
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice_status.id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "invoice_status.id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice_status.id_min_1"},
        column="id",
        min_value=1,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice_status.value_not_null"},
        column="value",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "invoice_status.value_domain"},
        column="value",
        value_set=["open", "disputed", "draft", "sent", "paid", "partial"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice_status.notes_not_null"},
        column="notes",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "invoice_status.value_max_len_32"},
        column="value",
        max_value=32,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "invoice_status.notes_max_len_128"},
        column="notes",
        max_value=128,
    )
)

# ----------------------------
# payment
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment.id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "payment.id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "payment.id_min_1"},
        column="id",
        min_value=1,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment.invoice_id_not_null"},
        column="invoice_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "payment.invoice_id_min_1"},
        column="invoice_id",
        min_value=1,
        mostly=1.0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment.amount_not_null"},
        column="amount",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "payment.amount_gt_0"},
        column="amount",
        min_value=0,
        strict_min=True,
        mostly=1.0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment.date_not_null"},
        column="date",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment.type_id_not_null"},
        column="type_id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment.notes_not_null"},
        column="notes",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "payment.notes_max_len_128"},
        column="notes",
        max_value=128,
    )
)

# ----------------------------
# payment_type
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment_type.id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "payment_type.id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "payment_type.id_min_1"},
        column="id",
        min_value=1,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment_type.value_not_null"},
        column="value",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "payment_type.value_domain"},
        column="value",
        value_set=["PostPaid", "PrePaid_TOPUP", "PrePaid_CARD", "PostPaid_RollBack"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment_type.notes_not_null"},
        column="notes",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "payment_type.value_max_len_32"},
        column="value",
        max_value=32,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "payment_type.notes_max_len_128"},
        column="notes",
        max_value=128,
    )
)

# ----------------------------
# prepaid_transaction
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction.id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "prepaid_transaction.id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "prepaid_transaction.id_min_1"},
        column="id",
        min_value=1,
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
        gx.expectations.ExpectColumnValuesToNotBeNull(
            meta={"check_id": f"prepaid_transaction.{col}_not_null"},
            column=col,
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "prepaid_transaction.bounce_min_0"},
        column="bounce",
        min_value=0,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "prepaid_transaction.type_domain_1_5"},
        column="type",
        value_set=[1, 2, 3, 4, 5],
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "prepaid_transaction.due_date_on_or_after_creationdate"},
        column_A="due_date",
        column_B="creationdate",
        or_equal=True,
        ignore_row_if="either_value_is_missing",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "prepaid_transaction.note_max_len_250"},
        column="note",
        max_value=250,
    )
)

# ----------------------------
# tblcampaign
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblcampaign.id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tblcampaign.id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "tblcampaign.id_min_1"},
        column="id",
        min_value=1,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblcampaign.Name_not_null"},
        column="Name",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tblcampaign.Name_unique"},
        column="Name",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "tblcampaign.Name_max_len_255"},
        column="Name",
        max_value=255,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblcampaign.value_not_null"},
        column="value",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "tblcampaign.value_between_0_1"},
        column="value",
        min_value=0,
        max_value=1,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "tblcampaign.cstatus_domain"},
        column="cstatus",
        value_set=["Active", "InActive"],
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "tblcampaign.period_min_0_if_present"},
        column="period",
        min_value=0,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblcampaign.description_not_null"},
        column="description",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "tblcampaign.description_max_len_255"},
        column="description",
        max_value=255,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "tblcampaign.cend_on_or_after_cstart_if_present"},
        column_A="cend",
        column_B="cstart",
        or_equal=True,
        ignore_row_if="either_value_is_missing",
    )
)

# ----------------------------
# tblgeneration
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblgeneration.gid_not_null"},
        column="gid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tblgeneration.gid_unique"},
        column="gid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "tblgeneration.gid_min_1"},
        column="gid",
        min_value=1,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "tblgeneration.month_regex_yyyy_mm_dash"},
        column="month",
        regex=r"^\d{4}-\d{2}$",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tblgeneration.month_unique"},
        column="month",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "tblgeneration.note_max_len_250"},
        column="note",
        max_value=250,
    )
)

# ----------------------------
# tbllinetype
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tbllinetype.id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tbllinetype.id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "tbllinetype.id_min_1"},
        column="id",
        min_value=1,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "tbllinetype.transtype_max_len_50"},
        column="transtype",
        max_value=50,
    )
)

# ----------------------------
# tbllinetransactions
# ----------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tbllinetransactions.id_not_null"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tbllinetransactions.id_unique"},
        column="id",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "tbllinetransactions.id_min_1"},
        column="id",
        min_value=1,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tbllinetransactions.transdate_not_null"},
        column="transdate",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "tbllinetransactions.typeid_min_1_if_present"},
        column="typeid",
        min_value=1,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "tbllinetransactions.billid_min_1_if_present"},
        column="billid",
        min_value=1,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "tbllinetransactions.description_max_len_255"},
        column="description",
        max_value=255,
    )
)

context.suites.add_or_update(suite)