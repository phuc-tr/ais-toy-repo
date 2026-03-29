import datetime
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# radacctid
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "radacctid_unique"},
        column="radacctid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacctid_not_null"},
        column="radacctid"
    )
)

# acctsessionid
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid"
    )
)

# acctuniqueid
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "acctuniqueid_unique"},
        column="acctuniqueid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctuniqueid_not_null"},
        column="acctuniqueid"
    )
)

# realm (optional in contract, so no not-null expectation)

# nasportid (quality: text format "Uniq-Sess-ID<id>" where <id> numerics)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "nasportid_mostly_not_null"},
        column="nasportid",
        min_value=0.95,
        max_value=1.0
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_format"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID\d+$",
        mostly=0.95,
    )
)

# nasporttype (contract: invalidValues < 1 with valid set)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.99,
    )
)

# acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctstarttime_not_null"},
        column="acctstarttime"
    )
)

# acctupdatetime
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctupdatetime_not_null"},
        column="acctupdatetime"
    )
)

# acctstoptime (must be >= acctstarttime)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_ge_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True
    )
)

# acctinterval
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctinterval_not_null"},
        column="acctinterval"
    )
)

# acctsessiontime (95% < 30000, non-negative)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_non_negative"},
        column="acctsessiontime",
        min_value=0,
        mostly=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={"check_id": "acctsessiontime_p95_lt_30000"},
        column="acctsessiontime",
        quantile_ranges={
            "quantiles": [0.95],
            "value_ranges": [[0, 30000]],
        }
    )
)

# acctauthentic
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctauthentic_not_null"},
        column="acctauthentic"
    )
)

# connectinfo_start
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "connectinfo_start_not_null"},
        column="connectinfo_start"
    )
)

# connectinfo_stop
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "connectinfo_stop_not_null"},
        column="connectinfo_stop"
    )
)

# acctinputoctets
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctinputoctets_not_null"},
        column="acctinputoctets"
    )
)

# acctoutputoctets
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctoutputoctets_not_null"},
        column="acctoutputoctets"
    )
)

# calledstationid (nullValues < 10%)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "calledstationid_not_null_90pct"},
        column="calledstationid",
        min_value=0.90,
        max_value=1.0
    )
)

# callingstationid (nullValues < 10%)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "callingstationid_not_null_90pct"},
        column="callingstationid",
        min_value=0.90,
        max_value=1.0
    )
)

# acctterminatecause (invalidValues < 1 with valid set)
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

# servicetype
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "servicetype_not_null"},
        column="servicetype"
    )
)

# framedprotocol
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "framedprotocol_not_null"},
        column="framedprotocol"
    )
)

# framedipv6address
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "framedipv6address_not_null_95pct"},
        column="framedipv6address",
        min_value=0.95,
        max_value=1.0
    )
)

# framedipv6prefix
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "framedipv6prefix_not_null_95pct"},
        column="framedipv6prefix",
        min_value=0.95,
        max_value=1.0
    )
)

# framedinterfaceid
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "framedinterfaceid_not_null_95pct"},
        column="framedinterfaceid",
        min_value=0.95,
        max_value=1.0
    )
)

# delegatedipv6prefix
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "delegatedipv6prefix_not_null_95pct"},
        column="delegatedipv6prefix",
        min_value=0.95,
        max_value=1.0
    )
)

# created_at (required + freshness)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "created_at_not_null"},
        column="created_at"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "created_at_freshness_25h"},
        column="created_at",
        min_value=datetime.datetime.utcnow() - datetime.timedelta(hours=25),
        max_value=datetime.datetime.utcnow()
    )
)

# Data-level freshness using acctstarttime (service level)
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "acctstarttime_freshness_25h"},
        column="acctstarttime",
        min_value=datetime.datetime.utcnow() - datetime.timedelta(hours=25),
        max_value=datetime.datetime.utcnow(),
    )
)