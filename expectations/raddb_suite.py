import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# ---------- Structural & key constraints ----------

# radacctid not null
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

# acctsessionid not null (<5% null allowed -> mostly >=0.95 non-null)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid",
        mostly=0.95,
    )
)

# acctuniqueid not null
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

# created_at not null (<5% null allowed -> mostly >=0.95 non-null)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "created_at_not_null"},
        column="created_at",
        mostly=0.95,
    )
)

# ---------- Domain / pattern constraints ----------

# nasportid format: "Uniq-Sess-ID<id>" where <id> are numerics
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_pattern"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID\d+$",
    )
)

# nasporttype domain (mustBeLessThan: 1 invalid -> mostly == 1.0 valid)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=1.0,
    )
)

# acctterminatecause domain (mustBeLessThan: 1 invalid -> mostly == 1.0 valid)
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

# ---------- Freshness (service level) ----------

# freshness: age of youngest row <= 25h based on created_at
now_utc = datetime.utcnow()
max_delay_hours = 25
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "created_at_freshness"},
        column="created_at",
        min_value=now_utc - timedelta(hours=max_delay_hours),
        max_value=now_utc,
    )
)

# ---------- Temporal consistency ----------

# acctstoptime must be later than or equal to acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_greater_or_equal_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
    )
)

# ---------- Distribution / range checks ----------

# acctsessiontime: 95% of values should be <= 30000 seconds
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_range"},
        column="acctsessiontime",
        min_value=0,
        max_value=30000,
        mostly=0.95,
    )
)

# ---------- Completeness checks ----------

# calledstationid should not be null (<10% null -> mostly >=0.90 non-null)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "calledstationid_not_null"},
        column="calledstationid",
        mostly=0.90,
    )
)

# callingstationid should not be null (<10% null -> mostly >=0.90 non-null)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "callingstationid_not_null"},
        column="callingstationid",
        mostly=0.90,
    )
)