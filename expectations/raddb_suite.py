import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# ---------- Primary key and uniqueness ----------

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

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid"
    )
)

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

# ---------- Realm ----------

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "realm_not_null"},
        column="realm"
    )
)

# ---------- nasportid pattern ----------

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_pattern"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID[0-9]+$"
    )
)

# ---------- nasporttype domain ----------

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.99
    )
)

# ---------- Time fields consistency ----------

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctstarttime_not_null"},
        column="acctstarttime"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_after_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True
    )
)

# ---------- acctsessiontime quantile constraint (~95% < 30000) ----------

suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={"check_id": "acctsessiontime_95th_lt_30000"},
        column="acctsessiontime",
        quantile_ranges={
            "quantiles": [0.95],
            "value_ranges": [[0, 30000]]
        },
        allow_relative_error=False
    )
)

# Also enforce non-negative session times
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_non_negative"},
        column="acctsessiontime",
        min_value=0
    )
)

# ---------- calledstationid / callingstationid null thresholds ----------

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "calledstationid_not_null_mostly"},
        column="calledstationid",
        mostly=0.90
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "callingstationid_not_null_mostly"},
        column="callingstationid",
        mostly=0.90
    )
)

# ---------- acctterminatecause domain ----------

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

# ---------- IPv6 fields (not required by contract but kept as quality checks) ----------

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "framedipv6address_not_null_mostly"},
        column="framedipv6address",
        mostly=0.90
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "framedipv6prefix_not_null_mostly"},
        column="framedipv6prefix",
        mostly=0.90
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "framedinterfaceid_not_null_mostly"},
        column="framedinterfaceid",
        mostly=0.90
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "delegatedipv6prefix_not_null_mostly"},
        column="delegatedipv6prefix",
        mostly=0.90
    )
)