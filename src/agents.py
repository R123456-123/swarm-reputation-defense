# src/agents.py

class Agent:
    def __init__(self, agent_id, is_malicious=False):
        self.agent_id = agent_id
        self.is_malicious = is_malicious
        self.reputation = 0

    def perform_task(self):
        # Honest agents generate a valid proof of work.
        # Malicious agents skip work to spam transactions.
        return "fake_transcript_no_work_done" if self.is_malicious else "real_transcript_task_completed"