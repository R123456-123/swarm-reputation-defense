import pandas as pd
import random
import os
from agents import Agent  # Add this line to link your files

class Marketplace:
    def __init__(self, use_defense=False):
        self.agents = []
        self.history = []
        self.use_defense = use_defense

    def add_agent(self, agent):
        self.agents.append(agent)

    def verify_transcript_at_gateway(self, transcript):
        # THE FIX: External Reference Monitor (Track 3 Innovation)
        if not self.use_defense:
            return True # Vulnerable: blindly accepts all ratings
        
        # Defense: cryptographically/programmatically verify the transcript
        if "real_transcript" in transcript:
            return True
        return False

    def submit_rating(self, target_id, score, transcript):
        # Rating ONLY counts if it passes the gateway
        if self.verify_transcript_at_gateway(transcript):
            for agent in self.agents:
                if agent.agent_id == target_id:
                    agent.reputation += score
                
    def run_round(self, round_num):
        malicious_agents = [a for a in self.agents if a.is_malicious]
        
        for agent in self.agents:
            transcript = agent.perform_task()
            
            if agent.is_malicious:
                # SYBIL ATTACK: Malicious agents collude and spam 5 transactions with each other per round
                reviewers = random.choices(malicious_agents, k=5) 
                for reviewer in reviewers:
                    self.submit_rating(agent.agent_id, 5, transcript)
            else:
                # Honest agents do 1 normal transaction with a random peer
                reviewer = random.choice([a for a in self.agents if a.agent_id != agent.agent_id])
                score = random.choice([3, 4, 5]) if "real_transcript" in transcript else 1
                self.submit_rating(agent.agent_id, score, transcript)
                
        # Log standings
        for agent in self.agents:
            self.history.append({
                "round": round_num,
                "agent_id": agent.agent_id,
                "is_malicious": agent.is_malicious,
                "reputation": agent.reputation
            })

def run_simulation(scenario_name, use_defense):
    market = Marketplace(use_defense=use_defense)
    
    for i in range(1, 11):
        market.add_agent(Agent(f"Honest_{i}", is_malicious=False))
    for i in range(1, 4):
        market.add_agent(Agent(f"Malicious_{i}", is_malicious=True))
        
    for r in range(1, 51):
        market.run_round(r)
        
    df = pd.DataFrame(market.history)
    os.makedirs("data", exist_ok=True)
    df.to_csv(f"data/{scenario_name}.csv", index=False)
    
    print(f"\n--- Top 5 Leaderboard ({scenario_name}) ---")
    final_standings = df[df["round"] == 50].sort_values(by="reputation", ascending=False)
    print(final_standings[["agent_id", "reputation", "is_malicious"]].head(5).to_string(index=False))

if __name__ == "__main__":
    print("PHASE 1: Sybil Attack (No Defense)")
    run_simulation("attack_results", use_defense=False)
    
    print("\nPHASE 2: Gateway Verification (With Defense)")
    run_simulation("defense_results", use_defense=True)