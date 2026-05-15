{
  "name": "expectation_suite",
  "expectations": [
    {
      "type": "expect_column_values_to_not_be_null",
      "kwargs": {
        "column": "realm"
      },
      "meta": {
        "check_id": "realm__not_null"
      }
    },
    {
      "type": "expect_column_values_to_be_in_set",
      "kwargs": {
        "column": "nasporttype",
        "value_set": [
          "Virtual",
          "ISDN"
        ]
      },
      "meta": {
        "check_id": "nasporttype__domain"
      }
    },
    {
      "type": "expect_column_pair_values_a_to_be_greater_than_b",
      "kwargs": {
        "column_A": "acctstoptime",
        "column_B": "acctstarttime",
        "or_equal": true
      },
      "meta": {
        "check_id": "acctstoptime__domain"
      }
    },
    {
      "type": "expect_column_values_to_be_between",
      "kwargs": {
        "column": "acctsessiontime",
        "min_value": 0,
        "max_value": 30000
      },
      "meta": {
        "check_id": "acctsessiontime__range"
      }
    },
    {
      "type": "expect_column_values_to_not_be_null",
      "kwargs": {
        "column": "calledstationid"
      },
      "meta": {
        "check_id": "calledstationid__not_null"
      }
    },
    {
      "type": "expect_column_values_to_not_be_null",
      "kwargs": {
        "column": "callingstationid"
      },
      "meta": {
        "check_id": "callingstationid__not_null"
      }
    },
    {
      "type": "expect_column_values_to_be_in_set",
      "kwargs": {
        "column": "acctterminatecause",
        "value_set": [
          "User-Request",
          "Admin-Reset",
          "Host-Request",
          "NAS-Error",
          "Port-Error",
          "Service-Unvaliable"
        ]
      },
      "meta": {
        "check_id": "acctterminatecause__domain"
      }
    }
  ],
  "meta": {}
}