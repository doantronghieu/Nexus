"""
This module provides comprehensive coverage of `Evaluating` within LlamaIndex.

Refs:
- https://docs.llamaindex.ai/en/stable/module_guides/evaluating/
"""

from llama_index.core.evaluation import (
  FaithfulnessEvaluator, RelevancyEvaluator, BatchEvalRunner, 
  BaseRetrievalEvaluator, generate_question_context_pairs,
)

from llama_index.core.llama_dataset.generator import RagDatasetGenerator

try:
  from deepeval.integrations.llama_index import (
  DeepEvalAnswerRelevancyEvaluator, DeepEvalFaithfulnessEvaluator,
  DeepEvalContextualRelevancyEvaluator, DeepEvalSummarizationEvaluator,
  DeepEvalBiasEvaluator, DeepEvalToxicityEvaluator,
)
except: pass