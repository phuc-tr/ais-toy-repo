import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# 1) radacctid: primary key, non-null, unique, non-negative
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

# 2) acctsessionid required → not_null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid",
    )
)

# 3) acctuniqueid required & unique
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

# 4) realm optional: allow nulls, but if present limit length to 64
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "realm_length_le_64"},
        column="realm",
        min_value=0,
        max_value=64,
        mostly=1.0,
    )
)

# 5) nasportid format: "Uniq-Sess-ID<id>" where <id> are numerics
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_format"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID\d+$",
        mostly=1.0,
    )
)

# 6) nasporttype domain: ['Virtual', 'ISDN'], invalidValues mustBeLessThan:1 → mostly=1.0
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=1.0,
    )
)

# 7) acctstarttime: timestamp & freshness: data should be no older than 25h
now = datetime.utcnow()
freshness_cutoff = now - timedelta(hours=25)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctstarttime_freshness"},
        column="acctstarttime",
        min_value=freshness_cutoff.isoformat(),
        max_value=now.isoformat(),
    )
)

# 8) acctupdatetime: optional, but if present should be >= acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctupdatetime_ge_acctstarttime"},
        column_A="acctupdatetime",
        column_B="acctstarttime",
        or_equal=True,
        mostly=0.95,
    )
)

# 9) acctstoptime: must be later than or equal to acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_ge_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
        mostly=1.0,
    )
)

# 10) acctinterval: non-negative integer
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinterval_non_negative"},
        column="acctinterval",
        min_value=0,
        mostly=0.95,
    )
)

# 11) acctsessiontime: per SQL quality rule 95% < 30000 seconds
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_95pct_lt_30000"},
        column="acctsessiontime",
        min_value=0,
        max_value=30000,
        mostly=0.95,
    )
)

# 12) acctauthentic: optional string, constrain length
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "acctauthentic_length_le_32"},
        column="acctauthentic",
        min_value=0,
        max_value=32,
        mostly=1.0,
    )
)

# 13) connectinfo_start: optional string, length ≤ 50
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "connectinfo_start_length_le_50"},
        column="connectinfo_start",
        min_value=0,
        max_value=50,
        mostly=1.0,
    )
)

# 14) connectinfo_stop: optional string, length ≤ 50
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "connectinfo_stop_length_le_50"},
        column="connectinfo_stop",
        min_value=0,
        max_value=50,
        mostly=1.0,
    )
)

# 15) acctinputoctets: non-negative
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinputoctets_non_negative"},
        column="acctinputoctets",
        min_value=0,
        mostly=0.95,
    )
)

# 16) acctoutputoctets: non-negative
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctoutputoctets_non_negative"},
        column="acctoutputoctets",
        min_value=0,
        mostly=0.95,
    )
)

# 17) calledstationid should not be null, mustBeLessThan 10% nulls → mostly >= 0.90
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "calledstationid_not_null"},
        column="calledstationid",
        mostly=0.90,
    )
)

# 18) callingstationid should not be null, mustBeLessThan 10% nulls → mostly >= 0.90
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "callingstationid_not_null"},
        column="callingstationid",
        mostly=0.90,
    )
)

# 19) acctterminatecause domain, invalidValues mustBeLessThan 1 → mostly=1.0
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
        mostly=1.0,
    )
)

# 20) servicetype: optional string, length ≤ 32
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "servicetype_length_le_32"},
        column="servicetype",
        min_value=0,
        max_value=32,
        mostly=1.0,
    )
)

# 21) framedprotocol: optional string, length ≤ 32
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "framedprotocol_length_le_32"},
        column="framedprotocol",
        min_value=0,
        max_value=32,
        mostly=1.0,
    )
)

# 22) framedipv6address: optional, length ≤ 45
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "framedipv6address_length_le_45"},
        column="framedipv6address",
        min_value=0,
        max_value=45,
        mostly=1.0,
    )
)

# 23) framedipv6prefix: optional, length ≤ 45
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "framedipv6prefix_length_le_45"},
        column="framedipv6prefix",
        min_value=0,
        max_value=45,
        mostly=1.0,
    )
)

# 24) framedinterfaceid: optional, length ≤ 44
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "framedinterfaceid_length_le_44"},
        column="framedinterfaceid",
        min_value=0,
        max_value=44,
        mostly=1.0,
    )
)

# 25) delegatedipv6prefix: optional, length ≤ 45
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "delegatedipv6prefix_length_le_45"},
        column="delegatedipv6prefix",
        min_value=0,
        max_value=45,
        mostly=1.0,
    )
)