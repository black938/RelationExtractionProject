from concurrent import futures
import grpc
# from protoc import re_pb2
# from protoc import re_pb2_grpc
import protoc.re_pb2 as re_pb2
import protoc.re_pb2_grpc as re_pb2_grpc
import tools
class API(re_pb2_grpc.APIServicer):
    def re(self,request,context):
        sentence = request.sentence
        triples = tools.extract_items(sentence)
        response = re_pb2.reResponse()
        for triple in triples:
            data = response.results.add()
            data.subject=triple[0]
            data.predicate=triple[1]
            data.object=triple[2]
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    re_pb2_grpc.add_APIServicer_to_server(API(),server)
    server.add_insecure_port("[::]:4232")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
