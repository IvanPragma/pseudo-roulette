import random

from django.db import models


class Player(models.Model):
    """Model for all players.
    We will not use the default django User model in our project.
    """

    def __str__(self) -> str:
        return f'Player #{self.id} with {self.get_scrolls_count()} scrolls'

    def get_scrolls_count(self) -> int:
        return self.scrolls.count()

    @staticmethod
    def get_statistic() -> list[dict]:
        """Return list of top players, each player is dict,
        with keys: "user_id", "rounds_count", "average_roulette_spins".

        Sort by "rounds_count" field. So, whoever has the most rounds
        will be at the top of the list.
        """

        # FIXME: At the moment, statistics are being returned & sorted for all players.
        #  If there are too many players/rounds, then this process will be quite difficult,
        #  so it's better to limit it to fixed size of players top and add the model
        #  linking Player to Round in order to sort the top by it in the future.

        result = []

        for player in Player.objects.all():
            scroll_count = 0
            rounds = []
            for scroll in player.scrolls.all():
                if scroll.round_id not in rounds:
                    rounds.append(scroll.round_id)
                scroll_count += 1

            rounds_count = len(rounds)

            result.append({
                'user_id': player.id,
                'rounds_count': rounds_count,
                'average_roulette_spins': 0 if rounds_count <= 0 else scroll_count/rounds_count,
            })

        result.sort(key=lambda player: player['rounds_count'], reverse=True)

        return result


class Round(models.Model):
    """Roulette round.
    Consists of 11 roulette scrolls. Multiple players can play in one round.
    """

    is_finished = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Round #{self.id}'

    @staticmethod
    def get_statistic() -> list[list]:
        """Return list of rounds, each round is list,
        with round's id and players count.
        """

        result = []

        for roulette_round in Round.objects.all():
            roulette_round_players = []
            for scroll in roulette_round.scrolls.all():
                if scroll.player_id not in roulette_round_players:
                    roulette_round_players.append(scroll.player_id)

            result.append([roulette_round.id, len(roulette_round_players)])

        return result


class Scroll(models.Model):
    """Roulette scroll."""

    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='scrolls')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='scrolls')
    result_choices = [
        (-1, 'Jackpot'),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    ]
    result = models.IntegerField(choices=result_choices, blank=True, editable=False)

    def __str__(self) -> str:
        return f'Player #{self.player_id} got {self.get_result_display()} in Round #{self.round_id}'

    def save(self, *args, **kwargs) -> None:
        """Custom save method.
        Generate random Scroll.result for Round.
        """

        assert not self.round.is_finished

        self.result = self.generate_scroll_result()
        return super().save(*args, **kwargs)

    def generate_scroll_result(self) -> int:
        """Chooses random slot for Round.
        One Round cant consists of Scrolls with same results.
        """
        already_chosen_slots = []
        for scroll in self.round.scrolls.all():
            already_chosen_slots.append(scroll.result)

        if len(already_chosen_slots) == 10:
            # If all slots are chosen we must choose a jackpot slot.
            # After this moment our view will finish round.
            return -1

        while True:
            potential_result = random.randint(1, 10)
            if potential_result not in already_chosen_slots:
                break

        return potential_result
