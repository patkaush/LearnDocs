
class Retriever:

    def __init__(self):

        pass

    @staticmethod
    def get_instance():
        if Retriever.retriever_obj is None:
            Retriever.retriever_obj = Retriever()
        return Retriever.retriever_obj
