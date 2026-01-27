import datetime
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# =========================
# Column-level Expectations
# =========================

# radacctid: required, unique, integer
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
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "radacctid_type_integer"},
        column="radacctid",
        type_="INTEGER",
    )
)

# acctsessionid: required, string, <5% nulls
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null_strict"},
        column="acctsessionid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid",
        min_value=0.95,
        max_value=1.0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctsessionid_type_string"},
        column="acctsessionid",
        type_="VARCHAR",
    )
)

# acctuniqueid: required, unique, string
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
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctuniqueid_type_string"},
        column="acctuniqueid",
        type_="VARCHAR",
    )
)

# realm: optional, string
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "realm_type_string"},
        column="realm",
        type_="VARCHAR",
    )
)

# nasportid: optional, string with pattern "Uniq-Sess-ID<id>" where <id> are numerics
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "nasportid_type_string"},
        column="nasportid",
        type_="VARCHAR",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_format"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID[0-9]+$",
        mostly=0.97,
    )
)

# nasporttype: string, domain constraint ["Virtual", "ISDN"], mustBeLessThan: 1 invalid => mostly=1.0
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "nasporttype_type_string"},
        column="nasporttype",
        type_="VARCHAR",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=1.0,
    )
)

# acctstarttime: timestamp, used for freshness
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctstarttime_type_timestamp"},
        column="acctstarttime",
        type_="DATETIME",
    )
)

# acctupdatetime: timestamp
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctupdatetime_type_timestamp"},
        column="acctupdatetime",
        type_="DATETIME",
    )
)

# acctstoptime: timestamp, must be >= acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctstoptime_type_timestamp"},
        column="acctstoptime",
        type_="DATETIME",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_ge_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
        mostly=0.99,
    )
)

# acctinterval: integer, range [0, 86581] for >97% of rows
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctinterval_type_integer"},
        column="acctinterval",
        type_="INTEGER",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinterval_range"},
        column="acctinterval",
        min_value=0,
        max_value=86581,
        mostly=0.97,
    )
)

# acctsessiontime: integer unsigned, 95% < 30000 seconds
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctsessiontime_type_integer"},
        column="acctsessiontime",
        type_="INTEGER",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_range"},
        column="acctsessiontime",
        min_value=0,
        max_value=30000,
        mostly=0.95,
    )
)

# acctauthentic: string
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctauthentic_type_string"},
        column="acctauthentic",
        type_="VARCHAR",
    )
)

# connectinfo_start: string
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "connectinfo_start_type_string"},
        column="connectinfo_start",
        type_="VARCHAR",
    )
)

# connectinfo_stop: string
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "connectinfo_stop_type_string"},
        column="connectinfo_stop",
        type_="VARCHAR",
    )
)

# acctinputoctets: integer
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctinputoctets_type_integer"},
        column="acctinputoctets",
        type_="INTEGER",
    )
)

# acctoutputoctets: integer
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctoutputoctets_type_integer"},
        column="acctoutputoctets",
        type_="INTEGER",
    )
)

# calledstationid: string, <10% nulls
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "calledstationid_type_string"},
        column="calledstationid",
        type_="VARCHAR",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "calledstationid_not_null"},
        column="calledstationid",
        min_value=0.90,
        max_value=1.0,
    )
)

# callingstationid: string, <10% nulls, restricted classification (same technical expectation)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "callingstationid_type_string"},
        column="callingstationid",
        type_="VARCHAR",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "callingstationid_not_null"},
        column="callingstationid",
        min_value=0.90,
        max_value=1.0,
    )
)

# acctterminatecause: string, domain constraint with allowed set
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctterminatecause_type_string"},
        column="acctterminatecause",
        type_="VARCHAR",
    )
)
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

# servicetype: string
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "servicetype_type_string"},
        column="servicetype",
        type_="VARCHAR",
    )
)

# framedprotocol: string
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "framedprotocol_type_string"},
        column="framedprotocol",
        type_="VARCHAR",
    )
)

# framedipv6address: string
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "framedipv6address_type_string"},
        column="framedipv6address",
        type_="VARCHAR",
    )
)

# framedipv6prefix: string
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "framedipv6prefix_type_string"},
        column="framedipv6prefix",
        type_="VARCHAR",
    )
)

# framedinterfaceid: string
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "framedinterfaceid_type_string"},
        column="framedinterfaceid",
        type_="VARCHAR",
    )
)

# delegatedipv6prefix: string
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "delegatedipv6prefix_type_string"},
        column="delegatedipv6prefix",
        type_="VARCHAR",
    )
)

# =========================
# Freshness Expectation
# =========================

# acctstarttime freshness: data no older than 25h
now_utc = datetime.datetime.utcnow()
min_time = (now_utc - datetime.timedelta(hours=25)).isoformat()
max_time = now_utc.isoformat()

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctstarttime_freshness"},
        column="acctstarttime",
        min_value=min_time,
        max_value=max_time,
        mostly=0.99,
    )
)

# Optional: acctupdatetime freshness aligned with contract (if desired)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctupdatetime_freshness"},
        column="acctupdatetime",
        min_value=min_time,
        max_value=max_time,
        mostly=0.99,
    )
)

context.suites.add_or_update(suite)