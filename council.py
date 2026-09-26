# council.py
from brain import think
from tools import AVAILABLE_TOOLS
import re

class CouncilMember:
    def __init__(self, name, persona):
        self.name = name
        self.persona = persona

    def deliberate(self, problem, context=""):
        prompt = f"{self.persona}\n\nProblem: {problem}\nContext: {context}\n\nProvide your professional analysis and proposed solution."
        # We use the same 'think' function but we'll need to modify it or create a raw version for the council
        # For now, we'll use a specialized call to the brain
        return think(prompt)

class OlympusCouncil:
    def __init__(self):
        self.members = {
            "Analyst": CouncilMember("The Analyst", "You are the Analyst. You focus on hard data, efficiency, and objective facts. Be concise and precise."),
            "Creative": CouncilMember("The Creative", "You are the Creative. You focus on innovation, user experience, and 'outside-the-box' solutions. Be imaginative."),
            "Critic": CouncilMember("The Critic", "You are the Critic. Your only job is to find flaws, risks, and gaps in the logic of others. Be adversarial and skeptical.")
        }

    def convene(self, problem):
        print(f"[*] Zeus is convening the Council of Olympus to discuss: {problem}")

        # 1. Initial Proposals
        analyst_view = self.members["Analyst"].deliberate(problem)
        creative_view = self.members["Creative"].deliberate(problem)

        # 2. The Critique
        context = f"Analyst says: {analyst_view}\n\nCreative says: {creative_view}"
        critique = self.members["Critic"].deliberate(problem, context)

        # 3. Final Synthesis (delivered by Zeus)
        final_context = f"Analyst: {analyst_view}\n\nCreative: {creative_view}\n\nCritic: {critique}"
        synthesis_prompt = f"As ZEUS, synthesize the following council deliberation into one final, powerful verdict for the user.\n\nProblem: {problem}\n\nDeliberation:\n{final_context}"

        return think(synthesis_prompt)

# Singleton instance for easy access
council = OlympusCouncil()
