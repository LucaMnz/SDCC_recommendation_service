from src.controller.RecommendationController import RecommendationController
import proto_pb2_grpc
import proto_pb2
import grpc


# Service class
class RecommendationService:
    recommendation_controller = 0
    n_neighbors = 4

    # Contructor: self.n_neighbors indicate the total nearest interest returned from model plus one
    def __init__(self):
        super()
        self.recommendation_controller = RecommendationController(self.n_neighbors)

    # Call user service to get favorite restaurant by ID
    def get_user_favorite(self, id):
        # remote call to user service
        channel = grpc.insecure_channel('localhost:50051')
        stub = proto_pb2_grpc.sdcc_user_serviceStub(channel)
        user = stub.findByID(proto_pb2.IDMessage(id=id))
        favorite = user.preferito.preferito
        return favorite

    # Ask k-nn for recommendation
    # Call to user service
    def get_recommendation_by_user_id(self, id):
        return self.recommendation_controller.get_recommendation(self.get_user_favorite(id))

    # Update recommendation model, not used yet
    def update_model(self, user_id, restourant_name, rating):
        self.recommendation_controller.learn_from_stream(user_id, restourant_name, rating)
