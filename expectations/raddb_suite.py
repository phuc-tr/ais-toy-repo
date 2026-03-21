import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")

suite_name = "expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# --- Schema / required / uniqueness ---
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:radacctid:exists"},
        column="radacctid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:radacctid:not_null"},
        column="radacctid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:radacctid:unique"},
        column="radacctid",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:acctsessionid:exists"},
        column="acctsessionid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:acctsessionid:not_null"},
        column="acctsessionid",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:acctuniqueid:exists"},
        column="acctuniqueid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:acctuniqueid:not_null"},
        column="acctuniqueid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:acctuniqueid:unique"},
        column="acctuniqueid",
    )
)

# --- Field-specific quality rules ---
# nasportid format: "Uniq-Sess-ID<id>" where <id> are numerics
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "contract:nasportid:format_regex"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID\d+$",
    )
)

# nasporttype valid values, invalid < 1%  -> mostly in set
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:nasporttype:valid_values"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.99,
    )
)

# acctstoptime must be >= acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "contract:acctstoptime:gte_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
    )
)

# acctsessiontime 95% should be less than 30000 seconds
suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={"check_id": "contract:acctsessiontime:p95_lt_30000"},
        column="acctsessiontime",
        quantile_ranges={"quantiles": [0.95], "value_ranges": [[None, 30000]]},
    )
)

# calledstationid null values < 10% -> non-null proportion >= 90%
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "contract:calledstationid:non_null_proportion"},
        column="calledstationid",
        min_value=0.90,
        max_value=1.0,
    )
)

# callingstationid null values < 10% -> non-null proportion >= 90%
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "contract:callingstationid:non_null_proportion"},
        column="callingstationid",
        min_value=0.90,
        max_value=1.0,
    )
)

# acctterminatecause valid values, invalid < 1% -> mostly in set
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:acctterminatecause:valid_values"},
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

# --- Freshness: Data no older than 25 hours based on acctstarttime ---
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "contract:acctstarttime:freshness_25h"},
        column="acctstarttime",
        min_value=(datetime.utcnow() - timedelta(hours=25)),
        max_value=datetime.utcnow(),
    )
)