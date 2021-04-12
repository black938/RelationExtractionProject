from concurrent import futures
import grpc
import relationExtractService_pb2
import relationExtractService_pb2_grpc
import tools
class relationExtractService(relationExtractService_pb2_grpc.relationExtractServiceServicer):
    def ExtractTriple(self,request,context):
        sentence = request.sentence
        triples = tools.extract_items(sentence)
        response = relationExtractService_pb2.relationExtractResponse()
        for triple in triples:
            data = response.triples.add()
            data.sub=triple[0]
            data.pred=triple[1]
            data.obj=triple[2]
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    relationExtractService_pb2_grpc.add_relationExtractServiceServicer_to_server(relationExtractService(),server)
    server.add_insecure_port("[::]:4232")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
