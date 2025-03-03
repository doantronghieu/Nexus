import packages
from configs import settings, const
from toolkit.llm.llama_index.data import storing, querying

#*==============================================================================

index_car_manual = storing.get_index(
	type_index="qdrant",
	# client=settings.qdrant_client,
	aclient=settings.qdrant_aclient,
	collection_name=settings.chosen_qdrant_collections["car_manual"],
)

query_toolkit_car_manual = querying.get_query_toolkit_from_vector_store_index(
	vector_store_index=index_car_manual, similarity_top_k=5
)

retriever_car_manual: querying.RetrieverQueryEngine = settings.error_handler_silent.execute(
  lambda: query_toolkit_car_manual["retriever"],
	error_msg="Error creating retriever `car_manual`",
)

#*------------------------------------------------------------------------------

index_car_info_field_paths = storing.get_index(
	type_index="qdrant",
	# client=settings.qdrant_client,
	aclient=settings.qdrant_aclient,
	collection_name=settings.chosen_qdrant_collections["car_info_field_paths"],
)

query_toolkit_car_info_field_paths = querying.get_query_toolkit_from_vector_store_index(
	vector_store_index=index_car_info_field_paths, similarity_top_k=15
)

retriever_car_info_field_paths: querying.RetrieverQueryEngine = settings.error_handler_silent.execute(
  lambda: query_toolkit_car_info_field_paths["retriever"],
	error_msg="Error creating retriever `car_info_field_paths`",
)

#*------------------------------------------------------------------------------

index_user_query_category = storing.get_index(
	type_index="qdrant",
	# client=settings.qdrant_client,
	aclient=settings.qdrant_aclient,
	collection_name=settings.chosen_qdrant_collections["user_query_category"],
)

query_toolkit_user_query_category = querying.get_query_toolkit_from_vector_store_index(
	vector_store_index=index_user_query_category, similarity_top_k=5
)

retriever_user_query_category: querying.RetrieverQueryEngine = settings.error_handler_silent.execute(
  lambda: query_toolkit_user_query_category["retriever"],
	error_msg="Error creating retriever `user_query_category`",
)

#*------------------------------------------------------------------------------