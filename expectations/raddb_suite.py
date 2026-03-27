import great_expectations as gx
from datetime import datetime, timedelta, UTC

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# Primary key & uniqueness
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "radacctid_unique"},
        column="radacctid",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacctid_not_null"},
        column="radacctid",
    )
)

# Required identifiers
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctsessionid_not_null"},
        column="acctsessionid",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "acctuniqueid_unique"},
        column="acctuniqueid",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctuniqueid_not_null"},
        column="acctuniqueid",
    )
)

# Optional but present realm (contract does not require, so only soft completeness if desired)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "realm_mostly_not_null"},
        column="realm",
        min_value=0.9,
        max_value=1.0,
    )
)

# nasportid format rule
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "nasportid_text"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID[0-9]+$",
    )
)

# nasporttype domain rule
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "nasporttype_domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
    )
)

# Timestamps: not null & logical relationships
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctstarttime_not_null"},
        column="acctstarttime",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctupdatetime_not_null"},
        column="acctupdatetime",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "acctstoptime_greater_or_equal_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
    )
)

# acctinterval non-negative (integer)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinterval_non_negative"},
        column="acctinterval",
        min_value=0,
        max_value=None,
    )
)

# acctsessiontime distribution rule: 95% < 30000
suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={
            "check_id": "acctsessiontime_p95_less_than_30000",
            "description": "95% of acctsessiontime should be less than 30000 seconds.",
            "source_query": "SELECT quantile(acctsessiontime, 0.95) AS session_time_90th_percentile FROM radacct",
        },
        column="acctsessiontime",
        quantile_ranges={
            "quantiles": [0.95],
            "value_ranges": [[None, 30000]],
        },
        allow_relative_error=False,
    )
)

# acctsessiontime basic range: must be non-negative
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctsessiontime_non_negative"},
        column="acctsessiontime",
        min_value=0,
        max_value=None,
    )
)

# Authentication and connection info
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctauthentic_not_null"},
        column="acctauthentic",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "connectinfo_start_not_null"},
        column="connectinfo_start",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "connectinfo_stop_not_null"},
        column="connectinfo_stop",
    )
)

# Octet counters non-null & non-negative
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctinputoctets_not_null"},
        column="acctinputoctets",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctinputoctets_non_negative"},
        column="acctinputoctets",
        min_value=0,
        max_value=None,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "acctoutputoctets_not_null"},
        column="acctoutputoctets",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "acctoutputoctets_non_negative"},
        column="acctoutputoctets",
        min_value=0,
        max_value=None,
    )
)

# calledstationid & callingstationid null thresholds (<=10% null)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "calledstationid_not_null"},
        column="calledstationid",
        min_value=0.9,
        max_value=1.0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "callingstationid_not_null"},
        column="callingstationid",
        min_value=0.9,
        max_value=1.0,
    )
)

# acctterminatecause domain rule (no invalid values allowed)
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
    )
)

# Service and protocol-related fields: mostly not null (contract does not mark as required)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "servicetype_mostly_not_null"},
        column="servicetype",
        min_value=0.9,
        max_value=1.0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "framedprotocol_mostly_not_null"},
        column="framedprotocol",
        min_value=0.9,
        max_value=1.0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "framedipv6address_mostly_not_null"},
        column="framedipv6address",
        min_value=0.9,
        max_value=1.0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "framedipv6prefix_mostly_not_null"},
        column="framedipv6prefix",
        min_value=0.9,
        max_value=1.0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "framedinterfaceid_mostly_not_null"},
        column="framedinterfaceid",
        min_value=0.9,
        max_value=1.0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "delegatedipv6prefix_mostly_not_null"},
        column="delegatedipv6prefix",
        min_value=0.9,
        max_value=1.0,
    )
)

# Freshness SLA: data should be no older than 25 hours based on acctstarttime
# This uses Batch-level expectation; assumes a run_time parameter "run_time" is passed.
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={
            "check_id": "freshness_acctstarttime_within_25h",
            "description": "Data should be no older than 25 hours based on acctstarttime.",
        },
        column="acctstarttime",
        min_value=None,
        max_value=(datetime.now(UTC) - timedelta(hours=25)),
    )
)

context.suites.add_or_update(suite)