from ..covid19find.simulator import Simulator

simulator = Simulator()


class TestSimulator:

    def test_fetch_default_scenarios(self):
        assert simulator.default_scenarios() == [
            {
                "interventionType": "lockdown",
                "interventionTiming": ">50",
                "testSymptomaticOnly": True,
                "hospitalTestProportion": 0.0,
                "otherHighContactPopulationTestProportion": 0.0,
                "restOfPopulationTestProportion": 1.0
            },
            {
                "interventionType": "lockdown",
                "interventionTiming": ">50",
                "testSymptomaticOnly": True,
                "hospitalTestProportion": 0.5,
                "otherHighContactPopulationTestProportion": 0.5,
                "restOfPopulationTestProportion": 0.0
            },
            {
                "interventionType": "lockdown",
                "interventionTiming": ">50",
                "testSymptomaticOnly": True,
                "hospitalTestProportion": 1.0,
                "otherHighContactPopulationTestProportion": 0.0,
                "restOfPopulationTestProportion": 0.0
            }
        ]
