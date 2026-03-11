import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# radacctid unique, non-null, integer
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
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "radacctid_type"},
        column="radacctid",
        type_="INTEGER"
    )
)

# acctsessionid required, string
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctsessionid_type"},
        column="acctsessionid",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "acctsessionid_length"},
        column="acctsessionid",
        min_value=0,
        max_value=64
    )
)

# acctuniqueid required, unique, string
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
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctuniqueid_type"},
        column="acctuniqueid",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "acctuniqueid_length"},
        column="acctuniqueid",
        min_value=0,
        max_value=32
    )
)

# realm string length
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "realm_type"},
        column="realm",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "realm_length"},
        column="realm",
        min_value=0,
        max_value=64
    )
)

# nasportid pattern: "Uniq-Sess-ID<id>" where <id> are numerics
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_pattern"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID[0-9]+$"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "nasportid_length"},
        column="nasportid",
        min_value=0,
        max_value=15
    )
)

# nasporttype domain: ['Virtual', 'ISDN'], mustBeLessThan 1 invalid -> mostly=0.99
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.99
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "nasporttype_length"},
        column="nasporttype",
        min_value=0,
        max_value=32
    )
)

# acctstarttime type + freshness (no older than 25h)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctstarttime_type"},
        column="acctstarttime",
        type_="DATETIME"
    )
)

now = datetime.utcnow()
max_delay_hours = 25
freshness_cutoff = now - timedelta(hours=max_delay_hours)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctstarttime_freshness"},
        column="acctstarttime",
        min_value=freshness_cutoff,
        max_value=now
    )
)

# acctupdatetime type
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctupdatetime_type"},
        column="acctupdatetime",
        type_="DATETIME"
    )
)

# acctstoptime type + must be >= acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctstoptime_type"},
        column="acctstoptime",
        type_="DATETIME"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_after_start"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True
    )
)

# acctinterval integer, non-negative
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctinterval_type"},
        column="acctinterval",
        type_="INTEGER"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinterval_non_negative"},
        column="acctinterval",
        min_value=0,
        max_value=None
    )
)

# acctsessiontime integer, unsigned, 95% < 30000
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctsessiontime_type"},
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

# acctauthentic type/length
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctauthentic_type"},
        column="acctauthentic",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "acctauthentic_length"},
        column="acctauthentic",
        min_value=0,
        max_value=32
    )
)

# connectinfo_start type/length
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "connectinfo_start_type"},
        column="connectinfo_start",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "connectinfo_start_length"},
        column="connectinfo_start",
        min_value=0,
        max_value=50
    )
)

# connectinfo_stop type/length
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "connectinfo_stop_type"},
        column="connectinfo_stop",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "connectinfo_stop_length"},
        column="connectinfo_stop",
        min_value=0,
        max_value=50
    )
)

# acctinputoctets integer, non-negative
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctinputoctets_type"},
        column="acctinputoctets",
        type_="INTEGER"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinputoctets_non_negative"},
        column="acctinputoctets",
        min_value=0,
        max_value=None
    )
)

# acctoutputoctets integer, non-negative
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctoutputoctets_type"},
        column="acctoutputoctets",
        type_="INTEGER"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctoutputoctets_non_negative"},
        column="acctoutputoctets",
        min_value=0,
        max_value=None
    )
)

# calledstationid not null (<10% null -> mostly=0.90)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "calledstationid_type"},
        column="calledstationid",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "calledstationid_length"},
        column="calledstationid",
        min_value=0,
        max_value=50
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "calledstationid_not_null"},
        column="calledstationid",
        mostly=0.90
    )
)

# callingstationid not null (<10% null -> mostly=0.90)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "callingstationid_type"},
        column="callingstationid",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "callingstationid_length"},
        column="callingstationid",
        min_value=0,
        max_value=50
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "callingstationid_not_null"},
        column="callingstationid",
        mostly=0.90
    )
)

# acctterminatecause domain, mustBeLessThan 1 invalid -> mostly=0.99
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
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctterminatecause_type"},
        column="acctterminatecause",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "acctterminatecause_length"},
        column="acctterminatecause",
        min_value=0,
        max_value=32
    )
)

# servicetype type/length
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "servicetype_type"},
        column="servicetype",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "servicetype_length"},
        column="servicetype",
        min_value=0,
        max_value=32
    )
)

# framedprotocol type/length
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "framedprotocol_type"},
        column="framedprotocol",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "framedprotocol_length"},
        column="framedprotocol",
        min_value=0,
        max_value=32
    )
)

# framedipv6address type/length
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "framedipv6address_type"},
        column="framedipv6address",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "framedipv6address_length"},
        column="framedipv6address",
        min_value=0,
        max_value=45
    )
)

# framedipv6prefix type/length
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "framedipv6prefix_type"},
        column="framedipv6prefix",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "framedipv6prefix_length"},
        column="framedipv6prefix",
        min_value=0,
        max_value=45
    )
)

# framedinterfaceid type/length
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "framedinterfaceid_type"},
        column="framedinterfaceid",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "framedinterfaceid_length"},
        column="framedinterfaceid",
        min_value=0,
        max_value=44
    )
)

# delegatedipv6prefix type/length
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "delegatedipv6prefix_type"},
        column="delegatedipv6prefix",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "delegatedipv6prefix_length"},
        column="delegatedipv6prefix",
        min_value=0,
        max_value=45
    )
)

context.suites.add_or_update(suite)