import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# radacctid unique and non-null (required, PK, unique)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacctid_not_null"},
        column="radacctid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "radacctid_unique"},
        column="radacctid"
    )
)

# acctsessionid required: no nulls allowed
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid"
    )
)

# acctuniqueid required + unique
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

# nasportid text format: "Uniq-Sess-IDXX" (XX = 2 digits)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_format"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID\d{2}$",
        mostly=0.95
    )
)

# nasporttype domain
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.99
    )
)

# acctstoptime must be later than acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_after_start"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        mostly=0.99
    )
)

# acctsessiontime distribution rule: 95% < 30000
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_95pct_lt_30000"},
        column="acctsessiontime",
        min_value=0,
        max_value=30000,
        mostly=0.95
    )
)

# calledstationid not_null with <10% nulls
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "calledstationid_not_null"},
        column="calledstationid",
        min_value=0.90,
        max_value=1.0
    )
)

# callingstationid not_null with <10% nulls
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "callingstationid_not_null"},
        column="callingstationid",
        min_value=0.90,
        max_value=1.0
    )
)

# acctterminatecause domain
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "acctterminatecause_domain"},
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

# created_at required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "created_at_not_null"},
        column="created_at"
    )
)

# table-level freshness: youngest row created_at within 25h
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "created_at_freshness_min"},
        column="created_at",
        min_value=(datetime.utcnow() - timedelta(hours=25)).isoformat(),
        max_value=datetime.utcnow().isoformat()
    )
)