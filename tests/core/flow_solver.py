from datetime import datetime

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from opennem.core.flow_solver import calculate_flow_for_interval, solve_flows_for_interval
from opennem.schema.network import NetworkNEM, NetworkSchema


# fixtures for this test adapted from Simons spreadsheet at
# https://docs.google.com/spreadsheets/d/12eAnLYSdXJ55I06m0sRfrJyVd-1gGsSr/edit#gid=1210585319
def load_energy_and_emissions_spreadsheet(interval: datetime, network: NetworkSchema = NetworkNEM) -> pd.DataFrame:
    """Load generation and emissions for an interval and the interval prior for each region of the network

    trading_interval network_id network_region  energy  emissions  emissions_intensity
          2023-01-01        NEM           QLD1     500        325                 0.65
          2023-01-01        NEM           NSW1     600        330                 0.55
          2023-01-01        NEM           VIC1     300        180                 0.60
          2023-01-01        NEM            SA1     100         15                 0.15
          2023-01-01        NEM           TAS1      80          4                 0.05
    """
    df = pd.DataFrame(
        {
            "trading_interval": [interval] * 5,
            "network_id": [network.code] * 5,
            "network_region": ["QLD1", "NSW1", "VIC1", "SA1", "TAS1"],
            "energy": [500, 600, 300, 100, 80],
            "emissions": [325, 330, 180, 15, 4],
        },
    )

    df["emissions_intensity"] = df["emissions"] / df["energy"]

    return df


def load_interconnector_interval_spreadsheet(interval: datetime, network: NetworkSchema = NetworkNEM) -> pd.DataFrame:
    """Load interval for each interconnector for a given interval


    trading_interval network_id interconnector_region_from interconnector_region_to  energy
          2023-01-01        NEM                       VIC1                      SA1    22.0
          2023-01-01        NEM                       NSW1                     QLD1   -55.0
          2023-01-01        NEM                       TAS1                     VIC1    11.0
          2023-01-01        NEM                       VIC1                     NSW1    27.5
    """

    df = pd.DataFrame(
        {
            "trading_interval": [interval] * 4,
            "network_id": [network.code] * 4,
            "interconnector_region_from": ["VIC1", "NSW1", "TAS1", "VIC1"],
            "interconnector_region_to": ["SA1", "QLD1", "VIC1", "NSW1"],
            "energy": [22, -55, 11, 27.5],
        },
    )

    return df


def flow_solver_test_output_spreadsheet() -> pd.DataFrame:
    """This is the test output to compare against

    network_region  energy_exported  emissions_exported  energy_imported emissions_imported
              TAS1             11.0                0.55              0.0                0.0
              VIC1             49.5               28.70             11.0                0.6
               SA1              0.0                0.00             22.0               12.8
              QLD1             55.0               35.75              0.0                0.0
              NSW1              0.0                0.00             82.5               51.7

    """
    df = pd.DataFrame(
        {
            "network_region": ["TAS1", "VIC1", "SA1", "QLD1", "NSW1"],
            "energy_exported": [11, 49.5, 0, 55, 0],
            "emissions_exported": [0.55, 28.7, 0, 35.75, 0],
            "energy_imported": [0, 11, 22, 0, 82.5],
            "emissions_imported": [0, 0.55, 12.8, 0, 51.7],
        },
    )

    return df


# Secondary test of raw values from dicts into solver function


@pytest.mark.parametrize(
    "emissions_dict, power_dict, demand_dict, expected_output",
    [
        (
            {
                "NSW1": 63576.32150005468,
                "QLD1": 72424.89831325083,
                "SA1": 1207.01427219245,
                "TAS1": 0,
                "VIC1": 55621.219853363276,
                ("QLD1", "NSW1"): 0.0002745705239764611,
                ("SA1", "VIC1"): 0.12867995814508557,
                ("TAS1", "VIC1"): 0,
            },
            {
                "NSW1": 99876.21579870833,
                "QLD1": 92799.05102995834,
                "SA1": 14571.279994583334,
                "TAS1": 9635.90418625,
                "VIC1": 68247.643680625,
                ("QLD1", "NSW1"): 1845378.0125,
                ("VIC1", "TAS1"): 9345725.368333332,
                ("NSW1", "VIC1"): 2928083.5116666667,
                ("SA1", "VIC1"): 2263190.0225,
                ("NSW1", "QLD1"): 1845378.0125,
                ("TAS1", "VIC1"): 9345725.368333332,
                ("VIC1", "NSW1"): 2928083.5116666667,
                ("VIC1", "SA1"): 2263190.0225,
            },
            {
                "NSW1": 99876.21579870884,
                "QLD1": 92799.0510299583,
                "SA1": 14571.279994583223,
                "TAS1": 9635.904186250642,
                "VIC1": 68247.6436806256,
            },
            pd.DataFrame(
                {
                    "region_flow": [
                        ("NSW1", "QLD1"),
                        ("VIC1", "NSW1"),
                        ("NSW1", "VIC1"),
                        ("VIC1", "SA1"),
                        ("VIC1", "TAS1"),
                        ("QLD1", "NSW1"),
                        ("TAS1", "NSW1"),
                        ("SA1", "VIC1"),
                    ],
                    "emissions": [
                        24074.331101,
                        18809.261834,
                        38199.031024,
                        14538.155604,
                        60034.556659,
                        0.000275,
                        0.000000,
                        0.128680,
                    ],
                }
            ),
        ),
    ],
)
def test_solve_flows_for_interval(
    emissions_dict: dict, power_dict: dict, demand_dict: dict, expected_output: pd.DataFrame
) -> None:
    """
    Unit test for the solve_flows_for_interval function.
    """
    subject_output = solve_flows_for_interval(region_emissions=emissions_dict, power=power_dict, demand=demand_dict)
    assert_frame_equal(subject_output, expected_output)


def test_calculate_flow_for_interval() -> None:
    """
    Unit test for the calculate_flow_for_interval function.

    This test checks that the function correctly calculates the flow of energy and emissions
    between network regions for a given interval. It compares the function's output against
    the expected output generated by the flow_solver_test_output function.

    The function does not accept any arguments and does not return any value. It will raise an
    AssertionError if the function's output does not match the expected output.
    """
    interval = datetime.fromisoformat("2023-04-09T10:15:00+10:00")

    df_energy_and_emissions = load_energy_and_emissions_spreadsheet(interval)
    df_interconnector = load_interconnector_interval_spreadsheet(interval)

    expected_output = flow_solver_test_output_spreadsheet()

    # Call the function with the test data
    actual_output = calculate_flow_for_interval(df_energy_and_emissions, df_interconnector)

    # Sort both dataframes by 'network_region' to ensure the same order
    expected_output.sort_values(by="network_region", inplace=True)
    actual_output.sort_values(by="network_region", inplace=True)

    # Reset index for both dataframes to ensure equal comparison
    expected_output.reset_index(drop=True, inplace=True)
    actual_output.reset_index(drop=True, inplace=True)

    # Check if the actual output matches the expected output between dataframes (deep compare)
    assert_frame_equal(actual_output, expected_output)
