import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# -------------------------
# Column presence / schema
# -------------------------
required_columns = [
    "radacctid",
    "acctsessionid",
    "acctuniqueid",
    "created_at",
]

suite.add_expectation(
    gx.expectations.ExpectTableColumnsToMatchSet(
        meta={"check_id": "required_columns_present"},
        column_set=required_columns
    )
)

# -------------------------
# radacctid
# -------------------------
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

# -------------------------
# acctsessionid
# -------------------------
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

# -------------------------
# acctuniqueid
# -------------------------
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

# -------------------------
# realm
# -------------------------
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

# -------------------------
# nasportid
# -------------------------
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

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_domain"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID[0-9]+$"
    )
)

# -------------------------
# nasporttype
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "nasporttype_type"},
        column="nasporttype",
        type_="VARCHAR"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"]
    )
)

# -------------------------
# acctstarttime / acctupdatetime / acctstoptime
# -------------------------
for col, check_id_prefix in [
    ("acctstarttime", "acctstarttime"),
    ("acctupdatetime", "acctupdatetime"),
    ("acctstoptime", "acctstoptime"),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"{check_id_prefix}_type"},
            column=col,
            type_="DATETIME"
        )
    )

# acctstoptime >= acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_after_or_equal_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True
    )
)

# Freshness on created_at (per service level: youngest row <= 25h old)
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "created_at_freshness"},
        column="created_at",
        min_value=datetime.utcnow() - timedelta(hours=25),
        max_value=datetime.utcnow()
    )
)

# -------------------------
# acctinterval
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctinterval_type"},
        column="acctinterval",
        type_="INTEGER"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinterval_range"},
        column="acctinterval",
        min_value=0,
        max_value=86402
    )
)

# -------------------------
# acctsessiontime
# -------------------------
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
        min_value=0
    )
)

# Approximate: 95% of acctsessiontime < 30000
suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={"check_id": "acctsessiontime_p95_lt_30000"},
        column="acctsessiontime",
        quantile_ranges={
            "quantiles": [0.95],
            "value_ranges": [[0, 30000]]
        }
    )
)

# -------------------------
# acctauthentic
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctauthentic_type"},
        column="acctauthentic",
        type_="VARCHAR"
    )
)

# -------------------------
# connectinfo_start / connectinfo_stop
# -------------------------
for col, check_id_prefix, max_len in [
    ("connectinfo_start", "connectinfo_start", 50),
    ("connectinfo_stop", "connectinfo_stop", 50),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"{check_id_prefix}_type"},
            column=col,
            type_="VARCHAR"
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValueLengthsToBeBetween(
            meta={"check_id": f"{check_id_prefix}_length"},
            column=col,
            min_value=0,
            max_value=max_len
        )
    )

# -------------------------
# acctinputoctets / acctoutputoctets
# -------------------------
for col, check_id_prefix in [
    ("acctinputoctets", "acctinputoctets"),
    ("acctoutputoctets", "acctoutputoctets"),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"{check_id_prefix}_type"},
            column=col,
            type_="INTEGER"
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            meta={"check_id": f"{check_id_prefix}_non_negative"},
            column=col,
            min_value=0
        )
    )

# -------------------------
# calledstationid / callingstationid
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "calledstationid_not_null"},
        column="calledstationid",
        min_value=0.90,
        max_value=1.0
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "callingstationid_not_null"},
        column="callingstationid",
        min_value=0.90,
        max_value=1.0
    )
)

for col, check_id_prefix in [
    ("calledstationid", "calledstationid"),
    ("callingstationid", "callingstationid"),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"{check_id_prefix}_type"},
            column=col,
            type_="VARCHAR"
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValueLengthsToBeBetween(
            meta={"check_id": f"{check_id_prefix}_length"},
            column=col,
            min_value=0,
            max_value=50
        )
    )

# -------------------------
# acctterminatecause
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctterminatecause_type"},
        column="acctterminatecause",
        type_="VARCHAR"
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
            "Service-Unvaliable"
        ]
    )
)

# -------------------------
# servicetype / framedprotocol
# -------------------------
for col, check_id_prefix in [
    ("servicetype", "servicetype"),
    ("framedprotocol", "framedprotocol"),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"{check_id_prefix}_type"},
            column=col,
            type_="VARCHAR"
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValueLengthsToBeBetween(
            meta={"check_id": f"{check_id_prefix}_length"},
            column=col,
            min_value=0,
            max_value=32
        )
    )

# -------------------------
# IPv6-related fields
# -------------------------
for col, max_len in [
    ("framedipv6address", 45),
    ("framedipv6prefix", 45),
    ("framedinterfaceid", 44),
    ("delegatedipv6prefix", 45),
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"{col}_type"},
            column=col,
            type_="VARCHAR"
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValueLengthsToBeBetween(
            meta={"check_id": f"{col}_length"},
            column=col,
            min_value=0,
            max_value=max_len
        )
    )

# -------------------------
# created_at
# -------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "created_at_not_null"},
        column="created_at"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "created_at_type"},
        column="created_at",
        type_="TIMESTAMP"
    )
)