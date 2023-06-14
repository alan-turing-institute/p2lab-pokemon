from pathlib import Path


class TeamRecorder():
    def __init__(self) -> None:
        pass
    
    def create_folder(self, f):
        Path(f"outputs/{f}").mkdir(parents=True, exist_ok=True)

    def record(self, team, generation, uid):
        team.to_df().to_csv(f"outputs/{generation}/{uid}.csv", index=False)

    def record_teams(self, teams, generation):
        self.create_folder(generation)
        for idx, team in enumerate(teams):
            self.record(team, generation, idx)