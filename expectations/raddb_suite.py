import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# Primary key & uniqueness
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "radacct:unique:radacctid"},
        column="radacctid",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct:not_null:radacctid"},
        column="radacctid",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "radacct:unique:acctuniqueid"},
        column="acctuniqueid",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct:not_null:acctuniqueid"},
        column="acctuniqueid",
    )
)

# Required fields
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct:not_null:acctsessionid"},
        column="acctsessionid",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct:not_null:created_at"},
        column="created_at",
    )
)

# Numeric ranges / distributions
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct:range:acctsessiontime"},
        column="acctsessiontime",
        min_value=0,
        max_value=30000,
        mostly=0.95,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct:range:acctinterval"},
        column="acctinterval",
        min_value=0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct:range:acctinputoctets"},
        column="acctinputoctets",
        min_value=0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct:range:acctoutputoctets"},
        column="acctoutputoctets",
        min_value=0,
    )
)

# Domain / categorical constraints
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "radacct:domain:nasporttype"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.99,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "radacct:domain:acctterminatecause"},
        column="acctterminatecause",
        value_set=[
            "User-Request",
            "Admin-Reset",
            "Host-Request",
            "NAS-Error",
            "Port-Error",
            "Service-Unvaliable",
        ],
        mostly=0.99,
    )
)

# Null thresholds (<= 10% nulls)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct:not_null:calledstationid"},
        column="calledstationid",
        mostly=0.90,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct:not_null:callingstationid"},
        column="callingstationid",
        mostly=0.90,
    )
)

# Text / pattern constraints
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "radacct:format:nasportid"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID\d{2}$",
        mostly=0.99,
    )
)

# Temporal relationships
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "radacct:temporal:acctstart_before_stoptime"},
        column_A="acctstarttime",
        column_B="acctstoptime",
        mostly=0.99,
    )
)