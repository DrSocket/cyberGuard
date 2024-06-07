from agency_swarm import Agency

from Agents.Browser import BrowsingAgent
from Agents.Developer import Devid
from Agents.Scanner import ScannerAgent
from Planners.PentestCEO import PlannerAgent

from dotenv import load_dotenv
load_dotenv()

planner = PlannerAgent()
devid = Devid()
browsingAgent = BrowsingAgent()
scanner = ScannerAgent()

agency = Agency([planner, devid, browsingAgent, scanner,
                
                [planner, devid],
                [planner, browsingAgent],
                [planner, scanner],

                [devid, planner],
                [devid, browsingAgent],

                [scanner, planner],
                [scanner, browsingAgent],

                [browsingAgent, planner],
                [browsingAgent, scanner],
                [browsingAgent, devid],
                ],
                shared_instructions='./agency_manifesto.md')

if __name__ == '__main__':
    agency.demo_gradio(server_name="0.0.0.0")