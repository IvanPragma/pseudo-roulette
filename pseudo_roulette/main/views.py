from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Round, Player, Scroll
from main.serializers import DoScrollSerializer


class GetPlayersCountPerRounds(APIView):
    """Return JSON list of rounds, each round is list,
    with round's id and players count.

    Example: [[1, 8], [2, 3], [3, 11], [4, 6]]
    """

    def get(self, request) -> Response:
        """Main and only one method is GET"""
        result = Round.get_statistic()
        return Response(result)


class GeTopPlayers(APIView):
    """Return JSON list of players, each player is dict with keys: "user_id", "rounds_count", "average_roulette_spins"

    Example: [
        {
            "user_id": 0,
            "rounds_count": 16,
            "average_roulette_spins": 2.6875
        },
        {
            "user_id": 1,
            "rounds_count": 11,
            "average_roulette_spins": 2.54
        },
    ]
    """

    def get(self, request) -> Response:
        """Main and only one method is GET"""
        result = Player.get_statistic()
        return Response(result)


class DoScroll(APIView):
    """Do scroll roulette in current round."""

    def post(self, request) -> Response:
        """Main and only one method is POST.
        Must content JSON dict with key: "user_id". Return verbose chosen slot num/jackpot.
        """
        serializer = DoScrollSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        player = serializer.validated_data['user_id']

        last_round = Round.objects.last()
        if not last_round or last_round.is_finished:
            last_round = Round.objects.create()

        scroll = Scroll(round=last_round, player=player)
        scroll.save()

        if scroll.result == -1:
            last_round.is_finished = True
            last_round.save()

        return Response({
            'result': scroll.get_result_display(),
            'round_id': scroll.round_id,
            'scroll_id': scroll.id
        })
