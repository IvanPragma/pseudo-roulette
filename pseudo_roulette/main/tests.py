from django.test import TestCase

from main.models import Player, Round, Scroll


class ScrollTestCase(TestCase):
    def setUp(self):
        self.player = Player.objects.create()
        self.roulette_round = Round.objects.create()

    def test_choose_random_slot(self):
        scroll = Scroll(
            round=self.roulette_round,
            player=self.player,
            result=-1,  # jackpot
        )
        scroll.save()
        self.assertIsNot(scroll.result, -1)

    def test_for_unique_slots(self):
        already_chosen_slots = []
        for i in range(11):
            scroll = Scroll.objects.create(round=self.roulette_round, player=self.player)
            self.assertNotIn(scroll.result, already_chosen_slots)
            already_chosen_slots.append(scroll.result)

    def test_scroll_request(self):
        response = self.client.post('/scroll/', {'user_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data['result'], int)
        self.assertIsNot(response.data['result'], -1)
        Scroll.objects.get(pk=1)

    def test_new_round_creation(self):
        for i in range(12):
            response = self.client.post('/scroll/', {'user_id': 1})
        self.assertEqual(Scroll.objects.count(), 12)
        self.assertIsNot(Scroll.objects.get(pk=11).round_id, Scroll.objects.get(pk=12).round_id)


class StatsTestCase(TestCase):
    def setUp(self):
        self.players = []
        for i in range(4):
            self.players.append(Player.objects.create())

        self.roulette_rounds = []
        for i in range(3):
            self.roulette_rounds.append(Round.objects.create())

        Scroll.objects.create(round=self.roulette_rounds[0], player=self.players[0])
        Scroll.objects.create(round=self.roulette_rounds[0], player=self.players[1])
        Scroll.objects.create(round=self.roulette_rounds[0], player=self.players[2])
        Scroll.objects.create(round=self.roulette_rounds[1], player=self.players[1])
        Scroll.objects.create(round=self.roulette_rounds[1], player=self.players[3])
        Scroll.objects.create(round=self.roulette_rounds[1], player=self.players[1])
        Scroll.objects.create(round=self.roulette_rounds[2], player=self.players[0])

    def test_round_statistic(self):
        self.assertEqual(Round.get_statistic(), [[1, 3], [2, 2], [3, 1]])

    def test_player_statistic(self):
        self.assertEqual(
            Player.get_statistic(),
            [
                {
                    'user_id': 1,
                    'rounds_count': 2,
                    'average_roulette_spins': 1.0,
                },
                {
                    'user_id': 2,
                    'rounds_count': 2,
                    'average_roulette_spins': 1.5,
                },
                {
                    'user_id': 3,
                    'rounds_count': 1,
                    'average_roulette_spins': 1.0,
                },
                {
                    'user_id': 4,
                    'rounds_count': 1,
                    'average_roulette_spins': 1.0,
                },
            ]
        )
