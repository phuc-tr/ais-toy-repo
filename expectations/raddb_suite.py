import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# Primary key / required / unique constraints from contract
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
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid",
    )
)
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

# Optional: enforce physical-type-inspired max lengths on key string fields
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "acctsessionid_length"},
        column="acctsessionid",
        min_value=1,
        max_value=64,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValueLengthsToBeBetween(
        meta={"check_id": "acctuniqueid_length"},
        column="acctuniqueid",
        min_value=1,
        max_value=32,
    )
)

# nasportid format: "Uniq-Sess-ID<id>" where <id> are numerics
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_format"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID\d+$",
    )
)

# nasporttype domain, mustBeLessThan: 1 (percent invalid)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.99,
    )
)

# acctstoptime must be later than or equal to acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_ge_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
        ignore_row_if="either_value_is_missing",
    )
)

# acctsessiontime: 95% should be < 30000
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_lt_30000_p95"},
        column="acctsessiontime",
        min_value=0,
        max_value=29999,
        mostly=0.95,
    )
)

# calledstationid/callingstationid: nullValues mustBeLessThan: 10 percent => mostly >= 0.90
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "calledstationid_not_null"},
        column="calledstationid",
        mostly=0.90,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "callingstationid_not_null"},
        column="callingstationid",
        mostly=0.90,
    )
)

# acctterminatecause domain, mustBeLessThan: 1 (percent invalid)
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
        mostly=0.99,
    )
)