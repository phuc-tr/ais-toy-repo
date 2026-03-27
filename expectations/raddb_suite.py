import great_expectations as gx
from datetime import datetime, timedelta, UTC

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# ------------------------------------------------------------------------------
# radacctid
# ------------------------------------------------------------------------------

# radacctid must be non-null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacctid_not_null"},
        column="radacctid",
    )
)

# radacctid unique
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "radacctid_unique"},
        column="radacctid",
    )
)

# ------------------------------------------------------------------------------
# acctsessionid
# ------------------------------------------------------------------------------

# acctsessionid required -> no nulls
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid",
    )
)

# ------------------------------------------------------------------------------
# acctuniqueid
# ------------------------------------------------------------------------------

# acctuniqueid required -> no nulls
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctuniqueid_not_null"},
        column="acctuniqueid",
    )
)

# acctuniqueid unique
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "acctuniqueid_unique"},
        column="acctuniqueid",
    )
)

# ------------------------------------------------------------------------------
# realm
# ------------------------------------------------------------------------------

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "realm_type"},
        column="realm",
        type_="VARCHAR",
    )
)

# ------------------------------------------------------------------------------
# nasportid
# ------------------------------------------------------------------------------

# nasportid text pattern: "Uniq-Sess-ID<id>" where <id> are numerics
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_pattern"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID[0-9]+$",
    )
)

# ------------------------------------------------------------------------------
# nasporttype
# ------------------------------------------------------------------------------

# nasporttype domain restriction; mustBeLessThan:1 invalid -> mostly=1.0
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=1.0,
    )
)

# ------------------------------------------------------------------------------
# acctstarttime / acctupdatetime / acctstoptime
# ------------------------------------------------------------------------------

# Types
for col in ["acctstarttime", "acctupdatetime", "acctstoptime"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"{col}_type"},
            column=col,
            type_="DATETIME",
        )
    )

# acctstoptime >= acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_ge_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
    )
)

# Freshness based on created_at (youngest row age <= 25h)
now_utc = datetime.now(UTC)
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "created_at_freshness_25h"},
        column="created_at",
        min_value=(now_utc - timedelta(hours=25)).isoformat(),
        max_value=now_utc.isoformat(),
    )
)

# ------------------------------------------------------------------------------
# acctinterval
# ------------------------------------------------------------------------------

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctinterval_type"},
        column="acctinterval",
        type_="INTEGER",
    )
)

# ------------------------------------------------------------------------------
# acctsessiontime
# ------------------------------------------------------------------------------

# Basic type & non-negative
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "acctsessiontime_type"},
        column="acctsessiontime",
        type_="INTEGER",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_non_negative"},
        column="acctsessiontime",
        min_value=0,
        max_value=None,
    )
)

# 95% of acctsessiontime should be < 30000 seconds
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_p95_lt_30000"},
        column="acctsessiontime",
        min_value=0,
        max_value=30000,
        mostly=0.95,
    )
)

# ------------------------------------------------------------------------------
# calledstationid / callingstationid
# ------------------------------------------------------------------------------

# calledstationid not_null with <10% nulls -> proportion_nonnull >= 0.9
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "calledstationid_non_null_rate"},
        column="calledstationid",
        min_value=0.9,
        max_value=1.0,
    )
)

# callingstationid not_null with <10% nulls -> proportion_nonnull >= 0.9
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "callingstationid_non_null_rate"},
        column="callingstationid",
        min_value=0.9,
        max_value=1.0,
    )
)

# ------------------------------------------------------------------------------
# acctterminatecause
# ------------------------------------------------------------------------------

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

# ------------------------------------------------------------------------------
# created_at
# ------------------------------------------------------------------------------

# created_at required -> no nulls
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "created_at_not_null"},
        column="created_at",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "created_at_type"},
        column="created_at",
        type_="TIMESTAMP",
    )
)