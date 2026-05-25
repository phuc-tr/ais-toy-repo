import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")
suite = context.suites.get("expectation_suite")

# billing_history.id - required (multiple rules collapsed to one expectation)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_history:not_null:id"},
        column="id"
    )
)

# billing_history.billAction - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_history:not_null:billAction"},
        column="billAction"
    )
)

# billing_history.paymentmethod - accepted_values
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_history:domain:paymentmethod"},
        column="paymentmethod",
        value_set=["PrePaid", "PostPaid"]
    )
)

# billing_plans.planName - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_plans:not_null:planName"},
        column="planName"
    )
)

# billing_plans.planActive - accepted_values
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_plans:domain:planActive"},
        column="planActive",
        value_set=["yes", "no"]
    )
)

# billing_plans.planRecurringBillingSchedule - accepted_values
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_plans:domain:planRecurringBillingSchedule"},
        column="planRecurringBillingSchedule",
        value_set=["Fixed", "Dynamic"]
    )
)

# financial_summary.finDate - regex
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "financial_summary:format:finDate"},
        column="finDate",
        regex=r"^\d{4}/\d{2}$"
    )
)

# financial_summary.finDate - unique
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "financial_summary:unique:finDate"},
        column="finDate"
    )
)

# invoice.date - required (collapsed)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:not_null:date"},
        column="date"
    )
)

# invoice.amount - required (collapsed)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:not_null:amount"},
        column="amount"
    )
)

# invoice.amount - custom amount > 0 (as range > 0)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "invoice:range:amount"},
        column="amount",
        min_value=0,
        strict_min=True
    )
)

# invoice.tax_amount - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:not_null:tax_amount"},
        column="tax_amount"
    )
)

# invoice.total - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:not_null:total"},
        column="total"
    )
)

# invoice.statusId - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:not_null:statusId"},
        column="statusId"
    )
)

# invoice.discount - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:not_null:discount"},
        column="discount"
    )
)

# invoice_status.value - required (first block)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice_status:not_null:value"},
        column="value"
    )
)

# invoice_status.value - accepted_values (status set)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "invoice_status:domain_status:value"},
        column="value",
        value_set=["open", "disputed", "draft", "sent", "paid", "partial"]
    )
)

# invoice_status.value - accepted_values (payment type set)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "invoice_status:domain_payment_type:value"},
        column="value",
        value_set=[
            "PostPaid",
            "PrePaid_TOPUP",
            "PrePaid_CARD",
            "PostPaid_RollBack"
        ]
    )
)

# invoice_status.notes - required (collapsed)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice_status:not_null:notes"},
        column="notes"
    )
)

# payment.invoice_id - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:not_null:invoice_id"},
        column="invoice_id"
    )
)

# payment.type_id - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:not_null:type_id"},
        column="type_id"
    )
)

# prepaid_transaction.balance_before - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:balance_before"},
        column="balance_before"
    )
)

# prepaid_transaction.bounce - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:bounce"},
        column="bounce"
    )
)

# prepaid_transaction.allowance - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:allowance"},
        column="allowance"
    )
)

# prepaid_transaction.balance_current - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:balance_current"},
        column="balance_current"
    )
)

# prepaid_transaction.due_date - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:due_date"},
        column="due_date"
    )
)

# prepaid_transaction.userID - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:userID"},
        column="userID"
    )
)

# prepaid_transaction.trans_status - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:trans_status"},
        column="trans_status"
    )
)

# prepaid_transaction.creationdate - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:creationdate"},
        column="creationdate"
    )
)

# prepaid_transaction.type - accepted_values
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "prepaid_transaction:domain:type"},
        column="type",
        value_set=[1, 2, 3, 4, 5]
    )
)

# tblcampaign.Name - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblcampaign:not_null:Name"},
        column="Name"
    )
)

# tblcampaign.description - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblcampaign:not_null:description"},
        column="description"
    )
)

# tblcampaign.cstatus - accepted_values
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "tblcampaign:domain:cstatus"},
        column="cstatus",
        value_set=["Active", "InActive"]
    )
)

# tblgeneration.gid - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblgeneration:not_null:gid"},
        column="gid"
    )
)

# tblgeneration.month - regex
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "tblgeneration:format:month"},
        column="month",
        regex=r"^\d{4}-\d{2}$"
    )
)

# tblgeneration.month - unique
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "tblgeneration:unique:month"},
        column="month"
    )
)

# tbllinetransactions.transdate - required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tbllinetransactions:not_null:transdate"},
        column="transdate"
    )
)