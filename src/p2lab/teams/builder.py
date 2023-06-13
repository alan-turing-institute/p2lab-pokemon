"""
The team builder
"""

class Builder:
    """
    The team builder
    """

    def __init__(self):
        pass 

    def make_team(self):
        pass

    def make_N_teams(self, N):
        return [self.make_team() for _ in range(N)]