import datetime
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# --- Column presence and types (basic schema checks) ---

for col in [
    "radacctid",
    "acctsessionid",
    "acctuniqueid",
    "realm",
    "nasportid",
    "nasporttype",
    "acctstarttime",
    "acctupdatetime",
    "acctstoptime",
    "acctinterval",
    "acctsessiontime",
    "acctauthentic",
    "connectinfo_start",
    "connectinfo_stop",
    "acctinputoctets",
    "acctoutputoctets",
    "calledstationid",
    "callingstationid",
    "acctterminatecause",
    "servicetype",
    "framedprotocol",
    "framedipv6address",
    "framedipv6prefix",
    "framedinterfaceid",
    "delegatedipv6prefix",
    "created_at",
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(
            meta={"check_id": f"{col}_exists"},
            column=col,
        )
    )

# radacctid: required, unique (primary key)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacctid_not_null"},
        column="radacctid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "radacctid_unique"},
        column="radacctid",
    )
)

# acctsessionid: required (not null)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid",
    )
)

# acctuniqueid: required, unique
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctuniqueid_not_null"},
        column="acctuniqueid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "acctuniqueid_unique"},
        column="acctuniqueid",
    )
)

# nasportid: quality text rule -> must follow "Uniq-Sess-ID<id>"
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_format"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID[0-9]+$",
    )
)

# nasporttype: quality library invalidValues < 1 with validValues [Virtual, ISDN]
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
    )
)

# acctstoptime must be >= acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_ge_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
    )
)

# acctinterval: integer, non-negative (no upper bound given, but reasonable sanity)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinterval_non_negative"},
        column="acctinterval",
        min_value=0,
        max_value=None,
    )
)

# acctsessiontime: integer >= 0; additional percentile-based quality rule
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_non_negative"},
        column="acctsessiontime",
        min_value=0,
        max_value=None,
    )
)

# Approximate the SQL quality rule:
# "95% of acctsessiontime should be less than 30000 seconds."
suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={"check_id": "acctsessiontime_p95_lt_30000"},
        column="acctsessiontime",
        quantile_ranges={
            "quantiles": [0.95],
            "value_ranges": [[None, 30000]],
        },
        allow_relative_error=True,
    )
)

# acctinputoctets, acctoutputoctets: non-negative
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinputoctets_non_negative"},
        column="acctinputoctets",
        min_value=0,
        max_value=None,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctoutputoctets_non_negative"},
        column="acctoutputoctets",
        min_value=0,
        max_value=None,
    )
)

# calledstationid: quality metric nullValues < 10% -> at least 90% non-null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "calledstationid_not_too_many_nulls"},
        column="calledstationid",
        mostly=0.9,
    )
)

# callingstationid: quality metric nullValues < 10% -> at least 90% non-null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "callingstationid_not_too_many_nulls"},
        column="callingstationid",
        mostly=0.9,
    )
)

# acctterminatecause: restricted set of values
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
            "Service-Unvaliable",
        ],
    )
)

# created_at: required (not null)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "created_at_not_null"},
        column="created_at",
    )
)

# Freshness service level: age of youngest row in table <= 25h
# Implemented as: max(created_at) between now-25h and now
now_utc = datetime.datetime.utcnow()
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "created_at_freshness_25h"},
        column="created_at",
        min_value=now_utc - datetime.timedelta(hours=25),
        max_value=now_utc,
    )
)