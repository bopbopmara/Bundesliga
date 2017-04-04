class Team(object):
    def __init__(self, name, image=None):
        self.name = name
        self.image = image

    def __str__(self):
        return self.name


class Match(object):
    def __init__(self, host, guest, start_time, host_score=None, guest_score=None):
        self.host = host
        self.guest = guest

        self.start_time = start_time

        self.host_score = host_score
        self.guest_score = guest_score

    def __str__(self):
        return '{host} - {guest}'.format(
            host=self.host,
            guest=self.guest,
        )


class TeamStanding(object):
    def __init__(self, name, wins=0, draws=0, losses=0, points=0, difference=0):
        self.name = name
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.points = points
        self.difference = difference

    def __str__(self):
        return self.name
