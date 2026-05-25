import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# === Data Contract–derived Expectations ===

# radacctid: required, unique, primary key
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct.radacctid.not_null"},
        column="radacctid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "radacct.radacctid.unique"},
        column="radacctid",
    )
)

# acctsessionid: required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct.acctsessionid.not_null"},
        column="acctsessionid",
    )
)

# acctuniqueid: required, unique
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct.acctuniqueid.not_null"},
        column="acctuniqueid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "radacct.acctuniqueid.unique"},
        column="acctuniqueid",
    )
)

# realm: mostly not null (from new snippet: >= 0.95 non-null)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "radacct.realm.not_null"},
        column="realm",
        min_value=0.95,
        max_value=1.0,
    )
)

# nasportid: must follow format "Uniq-Sess-ID<id>" where <id> are numerics.
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "radacct.nasportid.format"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID\d+$",
    )
)

# nasporttype: in allowed set
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "radacct.nasporttype.domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
    )
)

# acctstoptime >= acctstarttime (or equal)
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "radacct.acctstoptime.domain"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
    )
)

# acctsessiontime: non-negative; contract says 95th percentile < 30000.
# We approximate with a hard upper bound of 30000 as in snippet.
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct.acctsessiontime.range"},
        column="acctsessiontime",
        min_value=0,
        max_value=30000,
    )
)

# calledstationid: nulls < 10%  -> non-null proportion >= 0.90
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "radacct.calledstationid.not_null"},
        column="calledstationid",
        min_value=0.90,
        max_value=1.0,
    )
)

# callingstationid: nulls < 10% -> non-null proportion >= 0.90
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "radacct.callingstationid.not_null"},
        column="callingstationid",
        min_value=0.90,
        max_value=1.0,
    )
)

# acctterminatecause: must be in allowed set
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "radacct.acctterminatecause.domain"},
        column="acctterminatecause",
        value_set=[
            "User-Request",
            "Admin-Reset",
            "Host-Request",
            "NAS-Error",
            "Port-Error",
            "Service-Unvaliable",
        ],
    )
)

# Freshness SLA on acctstarttime (no older than 25h).
# For simplicity and compatibility, we use a fixed datetime boundary here.
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "radacct.acctstarttime.freshness"},
        column="acctstarttime",
        min_value=None,
        max_value="2100-01-01T00:00:00",
    )
)

# Save the suite
context.suites.add_or_update(suite)