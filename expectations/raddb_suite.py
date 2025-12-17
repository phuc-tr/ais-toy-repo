import datetime
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# radacctid unique (PK)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "radacctid_unique"},
        column="radacctid"
    )
)

# acctsessionid not_null (required)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid"
    )
)

# acctuniqueid unique + not_null (required + unique)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctuniqueid_not_null"},
        column="acctuniqueid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "acctuniqueid_unique"},
        column="acctuniqueid"
    )
)

# realm: allow nulls (not required) but constrain cardinality
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfUniqueValuesToBeBetween(
        meta={"check_id": "realm_cardinality"},
        column="realm",
        min_value=0.0,
        max_value=0.5
    )
)

# nasportid format: "Uniq-Sess-IDXX" (simple prefix check)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_format_uniq_sess_id"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID.*$",
        mostly=1.0
    )
)

# nasporttype domain: valid values Virtual, ISDN; mustBeLessThan 1 invalid
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_valid_values"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.99
    )
)

# acctstarttime, acctupdatetime, acctstoptime are timestamps; no strict not_null (not required in contract)
# acctstoptime must be later than acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_gt_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=False,
        mostly=0.99
    )
)

# acctinterval integer; not required, keep as-is but non-null if present is not mandated -> skip not_null

# acctsessiontime: 95% < 30000; also non-negative
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_non_negative"},
        column="acctsessiontime",
        min_value=0,
        max_value=None
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_95pct_lt_30000"},
        column="acctsessiontime",
        min_value=0,
        max_value=30000,
        mostly=0.95
    )
)

# acctauthentic optional; no contract quality rules -> leave unconstrained

# connectinfo_start / connectinfo_stop optional; no explicit rules

# acctinputoctets, acctoutputoctets: non-negative
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinputoctets_non_negative"},
        column="acctinputoctets",
        min_value=0,
        max_value=None
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctoutputoctets_non_negative"},
        column="acctoutputoctets",
        min_value=0,
        max_value=None
    )
)

# calledstationid not null: nullValues mustBeLessThan 10 percent
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "calledstationid_not_null_90pct"},
        column="calledstationid",
        mostly=0.90
    )
)

# callingstationid not null: nullValues mustBeLessThan 10 percent
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "callingstationid_not_null_90pct"},
        column="callingstationid",
        mostly=0.90
    )
)

# acctterminatecause valid values; invalidValues mustBeLessThan 1 -> mostly >= 0.99
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "acctterminatecause_valid_values"},
        column="acctterminatecause",
        value_set=[
            "User-Request",
            "Admin-Reset",
            "Host-Request",
            "NAS-Error",
            "Port-Error",
            "Service-Unvaliable"
        ],
        mostly=0.99
    )
)

# servicetype, framedprotocol, IPv6-related fields: contract does not require non-null, keep unconstrained

# created_at required: not_null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "created_at_not_null"},
        column="created_at"
    )
)

# table freshness based on created_at: youngest row <= 25h old
suite.add_expectation(
    gx.expectations.ExpectTableRowCountToBeBetween(
        meta={"check_id": "table_not_empty_for_freshness"},
        min_value=1,
        max_value=None
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "created_at_freshness_25h"},
        column="created_at",
        min_value=None,
        max_value=datetime.datetime.utcnow() - datetime.timedelta(hours=25)
    )
)