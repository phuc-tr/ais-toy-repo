import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

from great_expectations.expectations.expectation import ColumnMapExpectation


# ===== Custom expectation: nasportid format =====
def column_values_match_nasportid_format(col, **kwargs):
    import re
    pattern = re.compile(r"^Uniq-Sess-ID\d+$")
    return col.apply(lambda x: bool(pattern.match(x)) if x is not None else True)


class ExpectColumnValuesToMatchNasportidFormat(ColumnMapExpectation):
    map_metric = "column_values_match_nasportid_format"
    success_keys = ("mostly",)
    default_kwarg_values = {"mostly": 1.0}

    def validate_configuration(self, configuration):
        super().validate_configuration(configuration)
        return True

    def _validate(
        self,
        configuration,
        metrics,
        runtime_configuration=None,
        execution_engine=None,
    ):
        """
        Fallback simple implementation using pandas-like behavior, since we did not
        register a separate MetricProvider in this minimal example.
        """
        import pandas as pd

        series = metrics.get("table.column", pd.Series([]))
        results = column_values_match_nasportid_format(series)
        success_ratio = results.mean() if len(results) > 0 else 1.0
        mostly = configuration.kwargs.get("mostly", 1.0)
        success = success_ratio >= mostly

        return {
            "success": success,
            "result": {
                "unexpected_index_list": series[~results].index.tolist(),
                "unexpected_list": series[~results].tolist(),
            },
        }


# ===== Core expectations from contract =====

# Primary key & uniqueness
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

# Required fields
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct.acctsessionid.not_null"},
        column="acctsessionid",
    )
)

# Realm (quality not defined in contract, but reasonable non-null check)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct.realm.not_null"},
        column="realm",
        mostly=0.95,
    )
)

# nasportid format
suite.add_expectation(
    ExpectColumnValuesToMatchNasportidFormat(
        meta={"check_id": "radacct.nasportid.format"},
        column="nasportid",
        mostly=1.0,
    )
)

# nasporttype domain
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "radacct.nasporttype.domain"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.99,
    )
)

# acctstoptime >= acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "radacct.acctstoptime.domain"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
        mostly=0.99,
    )
)

# acctsessiontime 95% < 30000 (use between as approximation)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct.acctsessiontime.range"},
        column="acctsessiontime",
        min_value=0,
        max_value=30000,
        mostly=0.95,
    )
)

# calledstationid not null (<=10% nulls)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct.calledstationid.not_null"},
        column="calledstationid",
        mostly=0.90,
    )
)

# callingstationid not null (<=10% nulls)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct.callingstationid.not_null"},
        column="callingstationid",
        mostly=0.90,
    )
)

# acctterminatecause domain
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
        mostly=0.99,
    )
)

# Additional basic sanity checks (non-negative counters)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct.acctinputoctets.non_negative"},
        column="acctinputoctets",
        min_value=0,
        max_value=None,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct.acctoutputoctets.non_negative"},
        column="acctoutputoctets",
        min_value=0,
        max_value=None,
    )
)