from typing_extensions import override
import re
from agency_swarm.agents import Agent
from agency_swarm.tools import Retrieval
from instructor import llm_validator

class ScannerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Scanner",
            description="Scanner is an AI agent specialized in scanning and reporting comprehensive data about targets. It performs detailed assessments to gather actionable intelligence.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[Retrieval],
            tools_folder="./tools",
            validation_attempts=1,
        )

    @override
    def response_validator(self, message):
        pattern = r'(```)((.*\n){5,})(```)'

        if re.search(pattern, message):
            # take only first 100 characters
            raise ValueError(
                "You returned a data snippet. Please never return raw data snippets to me. "
                "Use the FileWriter tool to save the data locally. Then, analyze it if applicable. Continue."
            )

        llm_validator(statement="Verify whether the update from the Scanner Agent confirms the task's "
                                "successful completion. If the task remains unfinished, provide guidance "
                                "within the 'reason' argument on the next steps the agent should take. "
                                "For instance, if the agent identified issues during data collection, "
                                "advise on refining the scanning parameters for another attempt. Should "
                                "the agent outline potential solutions or further actions, direct the agent "
                                "to execute those plans. Message does not have to contain data snippets. "
                                "Just confirmation.",
                      openai_client=self.client)(message)

        return message