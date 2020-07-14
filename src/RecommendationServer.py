from concurrent import futures
import logging

import proto_pb2
import proto_pb2_grpc
import grpc

from src.service.RecommendationService import RecommendationService


class RecommendationServer(proto_pb2_grpc.recommendationServiceServicer):
    rec_service = 0

    def __init__(self):
        super()
        self.rec_service = RecommendationService()

    def getRecommendations(self, request, context):
        rec_array = self.rec_service.get_recommendation_by_user_id(request.userID)
        return proto_pb2.getRecommendationsResponse(recommendationList=rec_array)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    proto_pb2_grpc.add_recommendationServiceServicer_to_server(RecommendationServer(), server)
    server.add_insecure_port('[::]:50051')
    print("Starting GRPC Server..")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
