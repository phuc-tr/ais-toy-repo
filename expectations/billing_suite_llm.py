import great_expectations as gx

context = gx.get_context(mode="file")
suite = context.suites.get("expectation_suite")

import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")
suite = context.suites.get("expectation_suite")

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_history:not_null:id"},
        column="id",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_history:not_null:billAction"},
        column="billAction",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_history:domain:paymentmethod"},
        column="paymentmethod",
        value_set=["PrePaid", "PostPaid"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_plans:not_null:id"},
        column="id",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "billing_plans:not_null:planName"},
        column="planName",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_plans:domain:planActive"},
        column="planActive",
        value_set=["yes", "no"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "billing_plans:domain:planRecurringBillingSchedule"},
        column="planRecurringBillingSchedule",
        value_set=["Fixed", "Dynamic"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "financial_summary:not_null:id"},
        column="id",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "financial_summary:format:finDate"},
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
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:not_null:id"},
        column="id",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:not_null:date"},
        column="date",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:not_null:amount"},
        column="amount",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:not_null:tax_amount"},
        column="tax_amount",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:not_null:total"},
        column="total",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:not_null:statusId"},
        column="statusId",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice:not_null:discount"},
        column="discount",
    )
)

suite.add_expectation(
    gx.expectations.ExpectMulticolumnSumToEqual(
        meta={"check_id": "invoice:consistency:total"},
        column_list=["amount", "tax_amount", "discount"],
        sum_total={"column": "total"},
        ignore_row_if="any_value_is_missing",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice_status:not_null:id"},
        column="id",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "invoice_status:not_null:value"},
        column="value",
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
        meta={"check_id": "invoice_status:not_null:notes"},
        column="notes",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:not_null:id"},
        column="id",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:not_null:invoice_id"},
        column="invoice_id",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:not_null:amount"},
        column="amount",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "payment:range:amount"},
        column="amount",
        min_value=0,
        max_value=None,
        strict_min=True,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:not_null:date"},
        column="date",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:not_null:type_id"},
        column="type_id",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment:not_null:notes"},
        column="notes",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment_type:not_null:id"},
        column="id",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "payment_type:not_null:value"},
        column="value",
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
        meta={"check_id": "payment_type:not_null:notes"},
        column="notes",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:id"},
        column="id",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:balance_before"},
        column="balance_before",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:amount"},
        column="amount",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:bounce"},
        column="bounce",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:allowance"},
        column="allowance",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:balance_current"},
        column="balance_current",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:due_date"},
        column="due_date",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:userID"},
        column="userID",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:trans_status"},
        column="trans_status",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "prepaid_transaction:not_null:creationdate"},
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
        meta={"check_id": "prepaid_transaction:range:due_date"},
        column_A="due_date",
        column_B="creationdate",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblcampaign:not_null:id"},
        column="id",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblcampaign:not_null:Name"},
        column="Name",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblcampaign:not_null:value"},
        column="value",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblcampaign:not_null:description"},
        column="description",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "tblcampaign:domain:cstatus"},
        column="cstatus",
        value_set=["Active", "InActive"],
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "tblcampaign:range:cend"},
        column_A="cend",
        column_B="cstart",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tblgeneration:not_null:gid"},
        column="gid",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "tblgeneration:format:month"},
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

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tbllinetype:not_null:id"},
        column="id",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tbllinetransactions:not_null:id"},
        column="id",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "tbllinetransactions:not_null:transdate"},
        column="transdate",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "global:freshness:transactions"},
        column="creationdate",
        min_value=(datetime.utcnow() - timedelta(hours=24)).isoformat(),
        max_value=datetime.utcnow().isoformat(),
    )
)