import datetime
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# ==== Table-level expectations ====
suite.add_expectation(
    gx.expectations.ExpectTableColumnsToMatchSet(
        meta={"check_id": "table_columns_match_set"},
        column_set=[
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
        ]
    )
)

# ==== Column-level expectations ====

# radacctid: PK (not null, unique, integer-like)
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
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "radacctid_type_integer"},
        column="radacctid",
        type_="INTEGER"
    )
)

# Optional: radacctid operational range (kept but corrected to integers)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacctid_range"},
        column="radacctid",
        min_value=1000002,
        max_value=1000099
    )
)

# acctsessionid: required string, mostly not null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid",
        mostly=0.95
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctsessionid_type_string"},
        column="acctsessionid",
        type_="VARCHAR"
    )
)

# acctuniqueid: required, unique
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

# realm: required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "realm_not_null"},
        column="realm"
    )
)

# nasportid: pattern "Uniq-Sess-ID<id>" where <id> numerics
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_format"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID[0-9]+$",
        mostly=0.95
    )
)

# nasporttype: in allowed set
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.99
    )
)

# acctstarttime: timestamp + freshness (within last 25 hours)
now = datetime.datetime.now(datetime.UTC)
freshness_cutoff = now - datetime.timedelta(hours=25)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctstarttime_not_null"},
        column="acctstarttime"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctstarttime_freshness"},
        column="acctstarttime",
        min_value=freshness_cutoff.isoformat(),
        max_value=now.isoformat()
    )
)

# acctupdatetime: timestamp (optional)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctupdatetime_type_timestamp"},
        column="acctupdatetime",
        type_="DATETIME"
    )
)

# acctstoptime: timestamp + >= acctstarttime when not null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctstoptime_type_timestamp"},
        column="acctstoptime",
        type_="DATETIME"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_vs_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
        ignore_row_if="either_value_is_missing"
    )
)

# acctinterval: integer, non-negative
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctinterval_type_integer"},
        column="acctinterval",
        type_="INTEGER"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinterval_non_negative"},
        column="acctinterval",
        min_value=0,
        mostly=0.99
    )
)

# acctsessiontime: unsigned int, 95% < 30000
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctsessiontime_type_integer"},
        column="acctsessiontime",
        type_="INTEGER"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_range"},
        column="acctsessiontime",
        min_value=0,
        max_value=30000,
        mostly=0.95
    )
)

# acctauthentic: string (optional)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctauthentic_type_string"},
        column="acctauthentic",
        type_="VARCHAR"
    )
)

# connectinfo_start / connectinfo_stop: strings (optional)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "connectinfo_start_type_string"},
        column="connectinfo_start",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "connectinfo_stop_type_string"},
        column="connectinfo_stop",
        type_="VARCHAR"
    )
)

# acctinputoctets / acctoutputoctets: bigint, non-negative
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctinputoctets_type_bigint"},
        column="acctinputoctets",
        type_="BIGINT"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinputoctets_non_negative"},
        column="acctinputoctets",
        min_value=0,
        mostly=0.99
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctoutputoctets_type_bigint"},
        column="acctoutputoctets",
        type_="BIGINT"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctoutputoctets_non_negative"},
        column="acctoutputoctets",
        min_value=0,
        mostly=0.99
    )
)

# calledstationid: <10% null -> mostly=0.90
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "calledstationid_not_null"},
        column="calledstationid",
        mostly=0.90
    )
)

# callingstationid: <10% null -> mostly=0.90
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "callingstationid_not_null"},
        column="callingstationid",
        mostly=0.90
    )
)

# acctterminatecause: domain
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
        mostly=0.99
    )
)

# servicetype, framedprotocol: string (optional)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "servicetype_type_string"},
        column="servicetype",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "framedprotocol_type_string"},
        column="framedprotocol",
        type_="VARCHAR"
    )
)

# IPv6-related fields: strings with simple IPv6-like patterns (optional)
ipv6_like_regex = r"^[0-9A-Fa-f:./]+$"

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "framedipv6address_type_string"},
        column="framedipv6address",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "framedipv6address_format"},
        column="framedipv6address",
        regex=ipv6_like_regex,
        mostly=0.95
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "framedipv6prefix_type_string"},
        column="framedipv6prefix",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "framedipv6prefix_format"},
        column="framedipv6prefix",
        regex=ipv6_like_regex,
        mostly=0.95
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "framedinterfaceid_type_string"},
        column="framedinterfaceid",
        type_="VARCHAR"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "delegatedipv6prefix_type_string"},
        column="delegatedipv6prefix",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "delegatedipv6prefix_format"},
        column="delegatedipv6prefix",
        regex=ipv6_like_regex,
        mostly=0.95
    )
)

# Persist suite
context.suites.add_or_update(suite)