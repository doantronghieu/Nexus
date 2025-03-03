""" Setup
- Local LLM: apps/toolkit/tools/llm/README.md
"""
import packages
import os
import time
import nest_asyncio # To connect to the same event-loop,

from loguru import logger
from pprint import pprint

from toolkit.llm.llama_index import (
	agents, cores, evaluation, models, observability, workflows, messages,
)
from toolkit.llm.llama_index.data import loading, querying, storing

from toolkit.utils.llm import measure_performance
from configs import const

nest_asyncio.apply() # allows async events to run on notebook

cores.Settings.transformations = [
	loading.SentenceSplitter(
		chunk_size=1024, chunk_overlap=100
	)
]

use_local_model = True # <-- True, False
embed_batch_size = 1

chosen_local_model = const.Model.QWEN_2_5_0_5B.value
chosen_api_model = const.Model.GPT_3_5_TURBO.value
chosen_model = chosen_local_model if use_local_model else chosen_api_model

chosen_local_embed_model = const.EmbeddingsModel.BGE_SMALL_EN.value
chosen_api_embed_model = const.EmbeddingsModel.TEXT_EMBED_3_SMALL.value
chosen_embed_model = chosen_local_embed_model if use_local_model else chosen_api_embed_model

if not use_local_model:
	cores.Settings.llm = models.OpenAI(model=chosen_model, temperature=0.0)
	cores.Settings.embed_model = models.OpenAIEmbedding(
		model=chosen_embed_model, embed_batch_size=embed_batch_size,
	)
else:
	cores.Settings.llm = models.Ollama(model=chosen_model, request_timeout=360.0)
	cores.Settings.embed_model = models.HuggingFaceEmbedding(
		model_name=chosen_embed_model, embed_batch_size=embed_batch_size, 
		trust_remote_code=True,
  )

mode_debug = False
if mode_debug:
	import logging
	import sys
	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
	logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
 
logger.info(f"Using model: {chosen_model}")
logger.info(f"Using embeddings model: {cores.Settings.embed_model.model_name}")
#*------------------------------------------------------------------------------
file_path = f"{packages.APP_PATH}/data/org/test/manual_toyota_corolla_cross_2023.pdf"
reader = loading.MyReader(file_path)
documents = reader.load_data()

client = storing.QdrantClient(host="localhost", port=6333, timeout=15)
aclient = storing.AsyncQdrantClient(host="localhost", port=6333, prefer_grpc=True)
collection_name = "car_manual_HF" # car_manual_OpenAI, car_manual_HF

logger.info(f"Using collection: `{collection_name}`")

vector_store = storing.QdrantVectorStore(
	client=client,
	# aclient=aclient,
	collection_name=collection_name,
)
storage_context = storing.StorageContext.from_defaults(vector_store=vector_store)

if client.collection_exists(collection_name=collection_name):
	logger.info(f"Loading data from collection: `{collection_name}`")
	index = storing.VectorStoreIndex.from_vector_store(
		vector_store=vector_store,
		storage_context=storage_context,
	)
else:
	logger.info(f"Creating data from {collection_name}")
	index = storing.VectorStoreIndex.from_documents(
		documents=documents,
		storage_context=storage_context,
		show_progress=True,
	)

retriever = querying.VectorIndexRetriever(
	index=index, similarity_top_k=10,
)
node_postprocessors = [
	querying.SimilarityPostprocessor(similarity_cutoff=0.4),
]
response_synthesizer = querying.get_response_synthesizer(
	response_mode=querying.ResponseMode.COMPACT, streaming=True
)
query_engine = querying.RetrieverQueryEngine(
	retriever=retriever,
	node_postprocessors=node_postprocessors,
	response_synthesizer=response_synthesizer,
)
logger.info("Query engine created.")

query_tool = agents.QueryEngineTool.from_defaults(
	query_engine=query_engine,
	name="Query Engine",
	description=(
		"Useful for when you need to answer questions about the content. "
		"Input should be a fully formed question."
	),
)

# query_engine = index.as_query_engine()

# Add more doc: index.insert(doc)
#*------------------------------------------------------------------------------

def run_query_engine(
  query: str, 
  query_engine: querying.BaseQueryEngine, 
  print_in_streaming=True
):
    start_time = time.time()
    first_token_time = None
    total_response = ""

    if not query_engine._response_synthesizer._streaming:
        response = query_engine.query(query)
        total_time = time.time() - start_time
        pprint(response)
        logging.info(f"Total response time: {total_time:.4f} seconds")
        return response, None, total_time

    else:
        response = query_engine.query(query)
        
        for i, token in enumerate(response.response_gen):
            if i == 0:
                first_token_time = time.time() - start_time
            
            total_response += token
            if print_in_streaming:
                print(token, end="", flush=True)
        
        total_time = time.time() - start_time
        
        
        return total_response, first_token_time, total_time

# # Example usage:
# # query = "What did the author do growing up?"
# query = "What are some notes before driving the car?"
# # response, first_token_time, total_time = run_query_engine(query, query_engine, print_in_streaming=False)

# # print(f"Time to first token: {first_token_time:.4f} seconds")
# # print(f"Total response time: {total_time:.4f} seconds")

query = "What are some notes before driving the car?"

metadata = measure_performance.Metadata(
	dataset="car_manual",
	algorithm="basic",
	model=chosen_model,
	inference_server="API",
)

is_run_loop = True # <-- Set to True to run the loop

if is_run_loop:
	for i in range(0, 20):
		result = measure_performance.execute_query(query_engine, run_query_engine, query, metadata=metadata)
else:
	result = measure_performance.execute_query(query_engine, run_query_engine, query, metadata=metadata)

measure_performance.json_to_csv(
	json_file_path=f"{packages.APP_PATH}/data/logs/performance_logs.json",
	csv_file_path=f"{packages.APP_PATH}/data/logs/performance_logs.csv"
)