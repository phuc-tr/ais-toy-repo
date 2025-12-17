import datetime
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# 1) radacctid unique and not null (PK)
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

# 2) acctsessionid not_null (required)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid",
    )
)

# 3) acctuniqueid unique and not null (required + unique)
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

# 4) realm: optional -> no hard domain constraint from contract

# 5) nasportid format "Uniq-Sess-IDXX"
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_format"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID\d{2}$",
    )
)

# 6) nasporttype in allowed_set ['Virtual', 'ISDN']
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
    )
)

# 7) acctstoptime > acctstarttime (row-wise)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_gt_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=False,
    )
)

# 8) acctinterval >= 0
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinterval_non_negative"},
        column="acctinterval",
        min_value=0,
        max_value=None,
    )
)

# 9) acctsessiontime >= 0
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_non_negative"},
        column="acctsessiontime",
        min_value=0,
        max_value=None,
    )
)

# 10) acctsessiontime 95th percentile < 30000
suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={"check_id": "acctsessiontime_p95_lt_30000"},
        column="acctsessiontime",
        quantile_ranges={
            "quantiles": [0.95],
            "value_ranges": [[None, 30000]],
        },
        allow_relative_error=False,
    )
)

# 11) calledstationid nulls < 10%
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "calledstationid_not_null_90pct"},
        column="calledstationid",
        mostly=0.90,
    )
)

# 12) callingstationid nulls < 10%
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "callingstationid_not_null_90pct"},
        column="callingstationid",
        mostly=0.90,
    )
)

# 13) acctterminatecause in allowed_set
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

# 14) created_at required not null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "created_at_not_null"},
        column="created_at",
    )
)

# 15) table-level freshness using created_at: youngest row not older than 25h
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "created_at_freshness_25h"},
        column="created_at",
        max_value=(datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=25)),
    )
)