import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# radacctid
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:radacctid:exists"},
        column="radacctid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:radacctid:not_null"},
        column="radacctid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:radacctid:type"},
        column="radacctid",
        type_="INTEGER"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:radacctid:unique"},
        column="radacctid"
    )
)

# acctsessionid
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:acctsessionid:exists"},
        column="acctsessionid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:acctsessionid:not_null"},
        column="acctsessionid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:acctsessionid:type"},
        column="acctsessionid",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:acctsessionid:length"},
        column="acctsessionid",
        min_value=0,
        max_value=64
    )
)

# acctuniqueid
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:acctuniqueid:exists"},
        column="acctuniqueid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:acctuniqueid:not_null"},
        column="acctuniqueid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:acctuniqueid:type"},
        column="acctuniqueid",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "contract:acctuniqueid:unique"},
        column="acctuniqueid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:acctuniqueid:length"},
        column="acctuniqueid",
        min_value=0,
        max_value=32
    )
)

# realm
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:realm:exists"},
        column="realm"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:realm:type"},
        column="realm",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:realm:length"},
        column="realm",
        min_value=0,
        max_value=64
    )
)

# nasportid
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:nasportid:exists"},
        column="nasportid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:nasportid:type"},
        column="nasportid",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:nasportid:length"},
        column="nasportid",
        min_value=0,
        max_value=15
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "contract:nasportid:format"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID[0-9]+$"
    )
)

# nasporttype
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:nasporttype:exists"},
        column="nasporttype"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:nasporttype:type"},
        column="nasporttype",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "contract:nasporttype:length"},
        column="nasporttype",
        min_value=0,
        max_value=32
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:nasporttype:valid_values"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.99
    )
)

# acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:acctstarttime:exists"},
        column="acctstarttime"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:acctstarttime:type"},
        column="acctstarttime",
        type_="DATETIME"
    )
)

# acctupdatetime
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:acctupdatetime:exists"},
        column="acctupdatetime"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:acctupdatetime:type"},
        column="acctupdatetime",
        type_="DATETIME"
    )
)

# acctstoptime
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:acctstoptime:exists"},
        column="acctstoptime"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:acctstoptime:type"},
        column="acctstoptime",
        type_="DATETIME"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "contract:acctstoptime:gte_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True
    )
)

# acctinterval
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:acctinterval:exists"},
        column="acctinterval"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:acctinterval:type"},
        column="acctinterval",
        type_="INTEGER"
    )
)

# acctsessiontime
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:acctsessiontime:exists"},
        column="acctsessiontime"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:acctsessiontime:type"},
        column="acctsessiontime",
        type_="INTEGER"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:acctsessiontime:non_negative"},
        column="acctsessiontime",
        min_value=0,
        max_value=None
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={"check_id": "contract:acctsessiontime:q95_lt_30000"},
        column="acctsessiontime",
        quantile_ranges={
            "quantiles": [0.95],
            "value_ranges": [[None, 30000]]
        },
        allow_relative_error=False
    )
)

# acctauthentic
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:acctauthentic:exists"},
        column="acctauthentic"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:acctauthentic:type"},
        column="acctauthentic",
        type_="VARCHAR"
    )
)

# connectinfo_start
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:connectinfo_start:exists"},
        column="connectinfo_start"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:connectinfo_start:type"},
        column="connectinfo_start",
        type_="VARCHAR"
    )
)

# connectinfo_stop
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:connectinfo_stop:exists"},
        column="connectinfo_stop"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:connectinfo_stop:type"},
        column="connectinfo_stop",
        type_="VARCHAR"
    )
)

# acctinputoctets
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:acctinputoctets:exists"},
        column="acctinputoctets"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:acctinputoctets:type"},
        column="acctinputoctets",
        type_="INTEGER"
    )
)

# acctoutputoctets
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:acctoutputoctets:exists"},
        column="acctoutputoctets"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:acctoutputoctets:type"},
        column="acctoutputoctets",
        type_="INTEGER"
    )
)

# calledstationid
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:calledstationid:exists"},
        column="calledstationid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:calledstationid:type"},
        column="calledstationid",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:calledstationid:not_null_mostly"},
        column="calledstationid",
        mostly=0.9
    )
)

# callingstationid
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:callingstationid:exists"},
        column="callingstationid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:callingstationid:type"},
        column="callingstationid",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "contract:callingstationid:not_null_mostly"},
        column="callingstationid",
        mostly=0.9
    )
)

# acctterminatecause
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:acctterminatecause:exists"},
        column="acctterminatecause"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:acctterminatecause:type"},
        column="acctterminatecause",
        type_="VARCHAR"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "contract:acctterminatecause:valid_values"},
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

# servicetype
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:servicetype:exists"},
        column="servicetype"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:servicetype:type"},
        column="servicetype",
        type_="VARCHAR"
    )
)

# framedprotocol
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:framedprotocol:exists"},
        column="framedprotocol"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:framedprotocol:type"},
        column="framedprotocol",
        type_="VARCHAR"
    )
)

# framedipv6address
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:framedipv6address:exists"},
        column="framedipv6address"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:framedipv6address:type"},
        column="framedipv6address",
        type_="VARCHAR"
    )
)

# framedipv6prefix
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:framedipv6prefix:exists"},
        column="framedipv6prefix"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:framedipv6prefix:type"},
        column="framedipv6prefix",
        type_="VARCHAR"
    )
)

# framedinterfaceid
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:framedinterfaceid:exists"},
        column="framedinterfaceid"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:framedinterfaceid:type"},
        column="framedinterfaceid",
        type_="VARCHAR"
    )
)

# delegatedipv6prefix
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(
        meta={"check_id": "contract:delegatedipv6prefix:exists"},
        column="delegatedipv6prefix"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "contract:delegatedipv6prefix:type"},
        column="delegatedipv6prefix",
        type_="VARCHAR"
    )
)

# Table-level: basic structure (from model definition)
suite.add_expectation(
    gx.expectations.ExpectTableColumnsToMatchSet(
        meta={"check_id": "contract:radacct:columns_set"},
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

# Freshness (acctstarttime within last 25 hours)
now = datetime.utcnow()
cutoff = now - timedelta(hours=25)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "contract:acctstarttime:freshness_25h"},
        column="acctstarttime",
        min_value=cutoff.isoformat(timespec="seconds"),
        max_value=now.isoformat(timespec="seconds")
    )
)