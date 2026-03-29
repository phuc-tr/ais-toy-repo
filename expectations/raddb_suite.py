import great_expectations as gx
from datetime import datetime, timedelta
import re

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# radacctid: unique, non-null, integer
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
        meta={"check_id": "radacctid_type"},
        column="radacctid",
        type_="INTEGER"
    )
)

# acctsessionid: required (mostly 100%), string, length <= 64
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid",
        mostly=0.999
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

# acctuniqueid: required, unique, string, length <= 32
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctuniqueid_not_null"},
        column="acctuniqueid",
        mostly=0.999
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "acctuniqueid_unique"},
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

# realm: optional in contract, but enforce low nulls (<5%)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "realm_not_null"},
        column="realm",
        mostly=0.95
    )
)
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

# nasportid: pattern "Uniq-Sess-ID<id>" with numeric suffix
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_pattern"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID\d+$",
        mostly=0.99
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "nasportid_type"},
        column="nasportid",
        type_="VARCHAR"
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

# nasporttype: valid set ['Virtual', 'ISDN'], invalid values <1% -> mostly=0.99
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.99
    )
)

# acctstarttime: datetime, freshness within last 25h
now = datetime.utcnow()
max_delay_hours = 25
freshness_cutoff = now - timedelta(hours=max_delay_hours)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctstarttime_type"},
        column="acctstarttime",
        type_="DATETIME"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctstarttime_freshness"},
        column="acctstarttime",
        min_value=freshness_cutoff.isoformat(sep=" "),
        max_value=now.isoformat(sep=" ")
    )
)

# acctupdatetime: datetime, mostly non-null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctupdatetime_type"},
        column="acctupdatetime",
        type_="DATETIME"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctupdatetime_not_null"},
        column="acctupdatetime",
        mostly=0.95
    )
)

# acctstoptime: datetime, >= acctstarttime when not null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctstoptime_type"},
        column="acctstoptime",
        type_="DATETIME"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_gte_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
        mostly=0.99
    )
)

# acctinterval: integer, >=0
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

# acctsessiontime: unsigned int, >=0; 95% < 30000 seconds
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctsessiontime_type"},
        column="acctsessiontime",
        type_="INTEGER"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_non_negative"},
        column="acctsessiontime",
        min_value=0,
        max_value=None
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_95pct_below_30000"},
        column="acctsessiontime",
        min_value=0,
        max_value=30000,
        mostly=0.95
    )
)

# acctauthentic: optional, categorical
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "acctauthentic_domain"},
        column="acctauthentic",
        value_set=["RADIUS", "Local"],
        mostly=0.95
    )
)

# connectinfo_start: optional, but mostly non-null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "connectinfo_start_not_null"},
        column="connectinfo_start",
        mostly=0.95
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

# connectinfo_stop: optional, but mostly non-null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "connectinfo_stop_not_null"},
        column="connectinfo_stop",
        mostly=0.95
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

# acctinputoctets: bigint, >=0; 99% below large upper bound
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctinputoctets_type"},
        column="acctinputoctets",
        type_="BIGINT"
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
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinputoctets_99pct_range"},
        column="acctinputoctets",
        min_value=0,
        max_value=41782664281.47005,
        mostly=0.99
    )
)

# acctoutputoctets: bigint, >=0; 99% below large upper bound
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctoutputoctets_type"},
        column="acctoutputoctets",
        type_="BIGINT"
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
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctoutputoctets_99pct_range"},
        column="acctoutputoctets",
        min_value=0,
        max_value=41782664281.47005,
        mostly=0.99
    )
)

# calledstationid: not null <10% -> mostly 0.90, length <= 50
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "calledstationid_not_null"},
        column="calledstationid",
        mostly=0.90
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

# callingstationid: restricted; not null <10% -> mostly 0.90, length <= 50
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "callingstationid_not_null"},
        column="callingstationid",
        mostly=0.90
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

# acctterminatecause: valid RADIUS codes, invalid <1% -> mostly 0.99
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

# servicetype: varchar(32)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "servicetype_length"},
        column="servicetype",
        min_value=0,
        max_value=32
    )
)

# framedprotocol: varchar(32)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "framedprotocol_length"},
        column="framedprotocol",
        min_value=0,
        max_value=32
    )
)

# framedipv6address: varchar(45)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "framedipv6address_length"},
        column="framedipv6address",
        min_value=0,
        max_value=45
    )
)

# framedipv6prefix: varchar(45)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "framedipv6prefix_length"},
        column="framedipv6prefix",
        min_value=0,
        max_value=45
    )
)

# framedinterfaceid: varchar(44)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "framedinterfaceid_length"},
        column="framedinterfaceid",
        min_value=0,
        max_value=44
    )
)

# delegatedipv6prefix: varchar(45)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "delegatedipv6prefix_length"},
        column="delegatedipv6prefix",
        min_value=0,
        max_value=45
    )
)

context.suites.add_or_update(suite)