class ReadTest():
    @staticmethod
    def read_batch(keys, cluster_client):
        for key in keys:
            resp = cluster_client.readHashSingle(key)
            if cluster_client.pipeline:
                return cluster_client.pipeline.execute()
            else:
                return resp