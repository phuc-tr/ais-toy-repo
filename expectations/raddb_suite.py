import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# ------------------------
# Column-level expectations
# ------------------------

# radacctid: required, unique, primary key, non-negative integer
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
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacctid_non_negative"},
        column="radacctid",
        min_value=0,
    )
)

# acctsessionid: required (<=5% null)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid",
        min_value=0.95,
        max_value=1.0,
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

# realm: optional, but if present, not constrained further (keep non-null % check if desired)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "realm_not_null"},
        column="realm",
        min_value=0.0,
        max_value=1.0,
    )
)

# nasportid: format "Uniq-Sess-ID<id>" where <id> are numerics
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_format"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID\d+$",
    )
)

# nasporttype: domain (<1% invalid)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.99,
    )
)

# acctstarttime: timestamp (no freshness here; freshness is on created_at)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctstarttime_not_null"},
        column="acctstarttime",
    )
)

# acctupdatetime: optional timestamp
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctupdatetime_type"},
        column="acctupdatetime",
        type_="DATETIME",
    )
)

# acctstoptime: acctstoptime >= acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_gte_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
    )
)

# acctinterval: integer interval between updates, non-negative, reasonable upper bound
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinterval_range"},
        column="acctinterval",
        min_value=0,
        max_value=86402,
    )
)

# acctsessiontime: 95% of values < 30000 seconds
suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={"check_id": "acctsessiontime_p95_lt_30000"},
        column="acctsessiontime",
        quantile_ranges={
            "quantiles": [0.95],
            "value_ranges": [[None, 30000]],
        },
    )
)

# acctauthentic: domain (<1% invalid)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "acctauthentic_domain"},
        column="acctauthentic",
        value_set=["RADIUS", "Local"],
        mostly=0.99,
    )
)

# connectinfo_start: free text; keep only basic non-null proportion if needed
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "connectinfo_start_non_null"},
        column="connectinfo_start",
        min_value=0.0,
        max_value=1.0,
    )
)

# connectinfo_stop: free text; basic non-null proportion
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "connectinfo_stop_non_null"},
        column="connectinfo_stop",
        min_value=0.0,
        max_value=1.0,
    )
)

# acctinputoctets: non-negative, with 95% within observed range
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinputoctets_non_negative_p95_range"},
        column="acctinputoctets",
        min_value=0,
        max_value=4855973286.020002,
        mostly=0.95,
    )
)

# acctoutputoctets: non-negative, with 95% within observed range
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctoutputoctets_non_negative_p95_range"},
        column="acctoutputoctets",
        min_value=0,
        max_value=92194263696.25005,
        mostly=0.95,
    )
)

# calledstationid: nullValues < 10%  => non-null proportion >= 90%
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "calledstationid_not_null"},
        column="calledstationid",
        min_value=0.90,
        max_value=1.0,
    )
)

# callingstationid: nullValues < 10%  => non-null proportion >= 90%
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "callingstationid_not_null"},
        column="callingstationid",
        min_value=0.90,
        max_value=1.0,
    )
)

# acctterminatecause: domain (<1% invalid)
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
        mostly=0.99,
    )
)

# servicetype: nullValues < 5%  => non-null proportion >= 95%
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "servicetype_not_null"},
        column="servicetype",
        min_value=0.95,
        max_value=1.0,
    )
)

# framedprotocol: nullValues < 5%  => non-null proportion >= 95%
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "framedprotocol_not_null"},
        column="framedprotocol",
        min_value=0.95,
        max_value=1.0,
    )
)

# framedipv6address: nullValues < 5%  => non-null proportion >= 95%
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "framedipv6address_not_null"},
        column="framedipv6address",
        min_value=0.95,
        max_value=1.0,
    )
)

# framedipv6prefix: nullValues < 5%  => non-null proportion >= 95%
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "framedipv6prefix_not_null"},
        column="framedipv6prefix",
        min_value=0.95,
        max_value=1.0,
    )
)

# framedinterfaceid: nullValues < 5%  => non-null proportion >= 95%
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "framedinterfaceid_not_null"},
        column="framedinterfaceid",
        min_value=0.95,
        max_value=1.0,
    )
)

# delegatedipv6prefix: nullValues < 5%  => non-null proportion >= 95%
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "delegatedipv6prefix_not_null"},
        column="delegatedipv6prefix",
        min_value=0.95,
        max_value=1.0,
    )
)

# created_at: required, and freshness threshold 25h (youngest row <= 25h old)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "created_at_not_null"},
        column="created_at",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "created_at_freshness_25h"},
        column="created_at",
        min_value=(datetime.utcnow() - timedelta(hours=25)).isoformat(),
        max_value=datetime.utcnow().isoformat(),
    )
)