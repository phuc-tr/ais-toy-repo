import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")
suite = context.suites.get("expectation_suite")

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:radacctid"},
        column="radacctid"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:acctsessionid"},
        column="acctsessionid"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:acctuniqueid"},
        column="acctuniqueid"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "raddb:format:nasportid"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID\d+$"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "raddb:domain:nasporttype"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "raddb:range:acctstoptime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={"check_id": "raddb:range:acctsessiontime"},
        column="acctsessiontime",
        quantile_ranges={"quantiles": [0.95], "value_ranges": [[0, 30000]]}
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:calledstationid"},
        column="calledstationid",
        mostly=0.9
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:callingstationid"},
        column="callingstationid",
        mostly=0.9
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "raddb:domain:acctterminatecause"},
        column="acctterminatecause",
        value_set=[
            "User-Request",
            "Admin-Reset",
            "Host-Request",
            "NAS-Error",
            "Port-Error",
            "Service-Unvaliable",
        ]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "raddb:freshness:acctstarttime"},
        column="acctstarttime",
        min_value=(datetime.utcnow() - timedelta(hours=25)).isoformat(),
        max_value=datetime.utcnow().isoformat()
    )
)