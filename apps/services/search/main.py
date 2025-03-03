import packages
import os
import asyncio
import logging
from loguru import logger
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Union, Any, TypedDict, Literal, Protocol
from dataclasses import dataclass, field
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table



# Configuration
@dataclass
class TavilyConfig:
    """Central configuration for Tavily operations"""
    MAX_RESULTS_LIMIT: int = 20
    MAX_DAYS_LIMIT: int = 30
    DEFAULT_MAX_TOKENS: int = 4000
    DEFAULT_TIMEOUT: float = 30.0
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2
    VALID_SEARCH_DEPTHS: List[str] = field(default_factory=lambda: ["basic", "advanced"])
    VALID_TOPICS: List[str] = field(default_factory=lambda: ["general", "news"])

# Exceptions
class TavilyError(Exception):
    """Base exception for Tavily-related errors"""
    pass

class TavilyAPIError(TavilyError):
    """Raised when the Tavily API returns an error"""
    pass

class TavilyRateLimitError(TavilyAPIError):
    """Raised when API rate limit is exceeded"""
    pass

class TavilyAuthenticationError(TavilyAPIError):
    """Raised when authentication fails"""
    pass

class TavilyValidationError(TavilyError):
    """Raised when input validation fails"""
    pass

class TavilyTimeoutError(TavilyError):
    """Raised when an operation times out"""
    pass

# Type definitions
class ImageResult(TypedDict, total=False):
    """Type for image search results"""
    url: str
    description: Optional[str]

class TavilyClientProtocol(Protocol):
    """Protocol defining the required interface for Tavily clients"""
    def search(self, **kwargs) -> Dict[str, Any]: ...
    def qna_search(self, **kwargs) -> str: ...
    def get_search_context(self, **kwargs) -> str: ...
    def extract(self, urls: List[str]) -> Dict[str, Any]: ...

# Result formatting
class ResultFormatter(ABC):
    """Abstract base class for result formatters"""
    @abstractmethod
    def format(self, result: 'TavilySearchResult') -> str:
        pass

class ConsoleFormatter(ResultFormatter):
    """Formats results for console output using Rich"""
    def __init__(self, console: Console):
        self.console = console

    def format(self, result: 'TavilySearchResult') -> str:
        # Print query and response time
        self.console.print("\n[bold cyan]🔍 Search Query:[/bold cyan]", 
                          Text(result.query, style="bright_white"))
        self.console.print("[bold cyan]⏱️ Response Time:[/bold cyan]", 
                          f"{result.response_time:.2f}s", style="bright_white")

        # Print answer if available
        if result.answer:
            self.console.print(Panel(
                Text(result.answer, style="bright_white"),
                title="[bold green]Answer[/bold green]",
                expand=False
            ))

        # Print sources
        if result.results:
            self.console.print("\n[bold yellow]📚 Sources:[/bold yellow]")
            for idx, item in enumerate(result.results, 1):
                self.console.print(f"[cyan]{idx}.[/cyan] [bright_white]{item['title']}[/bright_white]")
                self.console.print(f"   [bright_blue]{item['url']}[/bright_blue]\n")

        # Print images if available
        if result.images:
            self.console.print("\n[bold magenta]🖼️ Images:[/bold magenta]")
            for image in result.images:
                if isinstance(image, dict):
                    self.console.print(f"[bright_blue]{image['url']}[/bright_blue]")
                    if 'description' in image:
                        self.console.print(f"[bright_white]{image['description']}[/bright_white]\n")
                else:
                    self.console.print(f"[bright_blue]{image}[/bright_blue]\n")

        # Print follow-up questions
        if result.follow_up_questions:
            self.console.print("\n[bold green]❓ Follow-up Questions:[/bold green]")
            for idx, question in enumerate(result.follow_up_questions, 1):
                self.console.print(f"[cyan]{idx}.[/cyan] [bright_white]{question}[/bright_white]")

        self.console.print("\n" + "="*80 + "\n")
        return ""

@dataclass
class TavilySearchResult:
    """Class to store Tavily search results in a structured format."""
    query: str
    results: List[Dict[str, Any]]
    response_time: float
    answer: Optional[str] = None
    images: Optional[List[Union[str, ImageResult]]] = None
    follow_up_questions: Optional[List[str]] = None
    formatter: ResultFormatter = field(default_factory=lambda: ConsoleFormatter(Console()))

    def __post_init__(self):
        self.formatter.format(self)

    @classmethod
    def from_response(cls, response: Dict[str, Any], query: str, 
                     formatter: Optional[ResultFormatter] = None) -> 'TavilySearchResult':
        """Create TavilySearchResult from API response."""
        return cls(
            query=query,
            results=response.get('results', []),
            response_time=response.get('response_time', 0.0),
            answer=response.get('answer'),
            images=response.get('images', []),
            follow_up_questions=response.get('follow_up_questions'),
            formatter=formatter or ConsoleFormatter(Console())
        )

class TavilySearchUtils:
    """Utility class for handling Tavily API searches."""
    
    def __init__(
        self, 
        client: Optional[TavilyClientProtocol] = None,
        api_key: Optional[str] = None,
        config: Optional[TavilyConfig] = None
    ):
        """Initialize the TavilySearchUtils with client and configuration."""
        self.config = config or TavilyConfig()
        
        if client:
            self.client = client
        else:
            if not api_key:
                api_key = os.getenv("TAVILY_API_KEY")
                if not api_key:
                    raise TavilyValidationError(
                        "API key is required. Either pass it directly or set TAVILY_API_KEY environment variable."
                    )
            
            try:
                from tavily import TavilyClient
                self.client = TavilyClient(api_key=api_key)
            except ImportError:
                raise ImportError("Please install tavily-python: pip install tavily-python")
            except Exception as e:
                raise TavilyError(f"Failed to initialize Tavily client: {str(e)}")

    def _validate_search_params(self, **params) -> None:
        """Validate search parameters."""
        if 'search_depth' in params and params['search_depth'] not in self.config.VALID_SEARCH_DEPTHS:
            raise TavilyValidationError(
                f"Invalid search_depth. Must be one of {self.config.VALID_SEARCH_DEPTHS}"
            )
            
        if 'topic' in params and params['topic'] not in self.config.VALID_TOPICS:
            raise TavilyValidationError(
                f"Invalid topic. Must be one of {self.config.VALID_TOPICS}"
            )
            
        if 'max_results' in params and not (0 < params['max_results'] <= self.config.MAX_RESULTS_LIMIT):
            raise TavilyValidationError(
                f"max_results must be between 1 and {self.config.MAX_RESULTS_LIMIT}"
            )
            
        if 'days' in params and not (0 < params['days'] <= self.config.MAX_DAYS_LIMIT):
            raise TavilyValidationError(
                f"days must be between 1 and {self.config.MAX_DAYS_LIMIT}"
            )

    def _prepare_search_params(self, **kwargs) -> Dict[str, Any]:
        """Prepare and validate search parameters."""
        valid_params = {
            'query', 'search_depth', 'topic', 'max_results', 
            'include_domains', 'exclude_domains', 'include_answer',
            'include_images', 'include_image_descriptions',
            'include_raw_content', 'days', 'max_tokens'
        }
        params = {k: v for k, v in kwargs.items() if k in valid_params and v is not None}
        self._validate_search_params(**params)
        return params

    def _handle_api_error(self, e: Exception, context: str) -> None:
        """Centralized error handling for API calls."""
        error_msg = str(e).lower()
        
        if "rate limit" in error_msg:
            raise TavilyRateLimitError(f"Rate limit exceeded during {context}")
        elif "authentication" in error_msg or "unauthorized" in error_msg:
            raise TavilyAuthenticationError(f"Authentication failed during {context}")
        elif "422 Client Error" in str(e):
            raise TavilyValidationError(
                f"Invalid parameters for {context}. Please check your parameters: {str(e)}"
            )
        
        raise TavilyAPIError(f"{context} failed: {str(e)}")

    async def _execute_with_retry(
        self,
        func: Any,
        *args: Any,
        max_retries: Optional[int] = None,
        **kwargs: Any
    ) -> Any:
        """Execute a function with retry logic."""
        max_retries = max_retries or self.config.MAX_RETRIES
        
        for attempt in range(max_retries):
            try:
                return await asyncio.wait_for(
                    asyncio.to_thread(func, *args, **kwargs),
                    timeout=self.config.DEFAULT_TIMEOUT
                )
            except asyncio.TimeoutError:
                if attempt == max_retries - 1:
                    raise TavilyTimeoutError(f"Operation timed out after {max_retries} attempts")
                logger.warning(f"Attempt {attempt + 1} timed out, retrying...")
                await asyncio.sleep(self.config.RETRY_DELAY ** attempt)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                if isinstance(e, (TavilyValidationError, TavilyAuthenticationError)):
                    raise
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}, retrying...")
                await asyncio.sleep(self.config.RETRY_DELAY ** attempt)

    async def search_async(
        self,
        query: str,
        search_depth: Literal["basic", "advanced"] = "basic",
        topic: Literal["general", "news"] = "general",
        max_results: int = 5,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        include_answer: bool = False,
        include_images: bool = False,
        include_image_descriptions: bool = False,
        include_raw_content: bool = False,
        days: Optional[int] = None,
        formatter: Optional[ResultFormatter] = None
    ) -> TavilySearchResult:
        """
        Perform an asynchronous search using Tavily API with retry logic.
        """
        try:
            search_params = self._prepare_search_params(
                query=query,
                search_depth=search_depth,
                topic=topic,
                max_results=max_results,
                include_domains=include_domains,
                exclude_domains=exclude_domains,
                include_answer=include_answer,
                include_images=include_images,
                include_image_descriptions=include_image_descriptions,
                include_raw_content=include_raw_content,
                days=days if topic == "news" else None
            )
            
            response = await self._execute_with_retry(self.client.search, **search_params)
            return TavilySearchResult.from_response(response, query, formatter)
            
        except Exception as e:
            self._handle_api_error(e, f"Search for query '{query}'")

    def search(
        self,
        query: str,
        formatter: Optional[ResultFormatter] = None,
        **kwargs
    ) -> TavilySearchResult:
        """Synchronous version of search_async."""
        try:
            search_params = self._prepare_search_params(query=query, **kwargs)
            response = self.client.search(**search_params)
            return TavilySearchResult.from_response(response, query, formatter)
        except Exception as e:
            self._handle_api_error(e, f"Search for query '{query}'")

    async def qna_search_async(
        self,
        query: str,
        search_depth: Literal["basic", "advanced"] = "advanced",
        **kwargs
    ) -> str:
        """Perform a question-answering search asynchronously with retry logic."""
        try:
            search_params = self._prepare_search_params(
                query=query,
                search_depth=search_depth,
                **kwargs
            )
            
            response = await self._execute_with_retry(self.client.qna_search, **search_params)
            return response
            
        except Exception as e:
            self._handle_api_error(e, f"QnA search for query '{query}'")

    def qna_search(self, query: str, **kwargs) -> str:
        """Synchronous version of qna_search_async."""
        try:
            search_params = self._prepare_search_params(query=query, **kwargs)
            response = self.client.qna_search(**search_params)
            return response
        except Exception as e:
            self._handle_api_error(e, f"QnA search for query '{query}'")

    async def batch_search_async(
        self,
        queries: List[str],
        formatter: Optional[ResultFormatter] = None,
        **kwargs
    ) -> List[TavilySearchResult]:
        """Perform multiple searches concurrently with retry logic."""
        if not queries:
            raise TavilyValidationError("Queries list cannot be empty")
            
        tasks = [
            self.search_async(query, formatter=formatter, **kwargs) 
            for query in queries
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Re-raise the first error if any occurred
        for result in results:
            if isinstance(result, Exception):
                raise result
                
        return results

    def batch_search(
        self,
        queries: List[str],
        formatter: Optional[ResultFormatter] = None,
        **kwargs
    ) -> List[TavilySearchResult]:
        """Synchronous version of batch_search_async."""
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(
            self.batch_search_async(queries, formatter=formatter, **kwargs)
        )

    async def get_context_async(
        self,
        query: str,
        max_tokens: int = TavilyConfig.DEFAULT_MAX_TOKENS,
        **kwargs
    ) -> str:
        """Get search context optimized for RAG applications with retry logic."""
        try:
            search_params = self._prepare_search_params(
                query=query,
                max_tokens=max_tokens,
                **kwargs
            )
            result = await self._execute_with_retry(
                self.client.get_search_context,
                **search_params
            )
            return result
        except Exception as e:
            self._handle_api_error(e, f"Context retrieval for query '{query}'")

    def get_context(self, query: str, max_tokens: int = TavilyConfig.DEFAULT_MAX_TOKENS, 
                   **kwargs) -> str:
        """Synchronous version of get_context_async."""
        try:
            search_params = self._prepare_search_params(
                query=query,
                max_tokens=max_tokens,
                **kwargs
            )
            result = self.client.get_search_context(**search_params)
            return result
        except Exception as e:
            self._handle_api_error(e, f"Context retrieval for query '{query}'")

    async def extract_url_async(
        self,
        urls: Union[str, List[str]]
    ) -> Dict[str, Any]:
        """Extract content from specific URLs asynchronously with retry logic."""
        try:
            if isinstance(urls, str):
                urls = [urls]
            
            if not urls:
                raise TavilyValidationError("URLs list cannot be empty")
                
            result = await self._execute_with_retry(self.client.extract, urls=urls)
            return result
            
        except Exception as e:
            self._handle_api_error(e, "URL extraction")

    def extract_url(self, urls: Union[str, List[str]]) -> Dict[str, Any]:
        """Synchronous version of extract_url_async."""
        try:
            if isinstance(urls, str):
                urls = [urls]
                
            if not urls:
                raise TavilyValidationError("URLs list cannot be empty")
                
            result = self.client.extract(urls=urls)
            return result
        except Exception as e:
            self._handle_api_error(e, "URL extraction")

# Command pattern for CLI actions
class Command(ABC):
    """Abstract base class for CLI commands"""
    def __init__(self, tavily: TavilySearchUtils, console: Console):
        self.tavily = tavily
        self.console = console

    @abstractmethod
    async def execute(self) -> None:
        pass

class BasicSearchCommand(Command):
    async def execute(self) -> None:
        query = Prompt.ask("\n[cyan]Enter your search query[/cyan]")
        max_results = IntPrompt.ask("[cyan]Enter maximum number of results[/cyan]", default=5)
        include_answer = Confirm.ask("[cyan]Include AI-generated answer?[/cyan]", default=True)
        
        await self.tavily.search_async(
            query=query,
            max_results=max_results,
            include_answer=include_answer
        )

class NewsSearchCommand(Command):
    async def execute(self) -> None:
        query = Prompt.ask("\n[cyan]Enter news search query[/cyan]")
        days = IntPrompt.ask("[cyan]How many days back? (1-30)[/cyan]", default=7)
        include_answer = Confirm.ask("[cyan]Include AI-generated answer?[/cyan]", default=True)
        
        await self.tavily.search_async(
            query=query,
            topic="news",
            days=days,
            include_answer=include_answer
        )

class QnASearchCommand(Command):
    async def execute(self) -> None:
        query = Prompt.ask("\n[cyan]Enter your question[/cyan]")
        result = await self.tavily.qna_search_async(query=query)
        self.console.print(Panel(
            Text(result, style="bright_white"),
            title="[bold green]QnA Answer[/bold green]",
            expand=False
        ))

class ImageSearchCommand(Command):
    async def execute(self) -> None:
        query = Prompt.ask("\n[cyan]Enter image search query[/cyan]")
        include_descriptions = Confirm.ask(
            "[cyan]Include image descriptions?[/cyan]",
            default=True
        )
        
        await self.tavily.search_async(
            query=query,
            include_images=True,
            include_image_descriptions=include_descriptions
        )

class RAGContextCommand(Command):
    async def execute(self) -> None:
        query = Prompt.ask("\n[cyan]Enter query for RAG context[/cyan]")
        max_tokens = IntPrompt.ask(
            "[cyan]Maximum tokens (default: 4000)[/cyan]",
            default=4000
        )
        
        result = await self.tavily.get_context_async(
            query=query,
            max_tokens=max_tokens
        )
        self.console.print(Panel(
            Text(result[:200] + "..." if len(result) > 200 else result,
                 style="bright_white"),
            title="[bold green]RAG Context[/bold green]",
            expand=False
        ))

class URLExtractionCommand(Command):
    async def execute(self) -> None:
        urls = []
        while True:
            url = Prompt.ask(
                "\n[cyan]Enter URL to extract (or press Enter to finish)[/cyan]"
            )
            if not url:
                break
            urls.append(url)
            
        if urls:
            result = await self.tavily.extract_url_async(urls=urls)
            self.console.print("\n[bold magenta]📄 Extracted Content:[/bold magenta]")
            for url, content in result.items():
                self.console.print(f"\n[cyan]URL:[/cyan] [bright_blue]{url}[/bright_blue]")
                if content:
                    preview = content[:200] + "..." if len(content) > 200 else content
                    self.console.print(Panel(
                        Text(preview, style="bright_white"),
                        title="[bold green]Content Preview[/bold green]",
                        expand=False
                    ))
                else:
                    self.console.print("[yellow]No content available[/yellow]")
        else:
            self.console.print("[yellow]No URLs provided[/yellow]")

class BatchSearchCommand(Command):
    async def execute(self) -> None:
        queries = []
        while True:
            query = Prompt.ask(
                "\n[cyan]Enter search query (or press Enter to finish)[/cyan]"
            )
            if not query:
                break
            queries.append(query)
            
        if queries:
            max_results = IntPrompt.ask(
                "[cyan]Maximum results per query[/cyan]",
                default=3
            )
            include_answer = Confirm.ask(
                "[cyan]Include AI-generated answers?[/cyan]",
                default=True
            )
            
            await self.tavily.batch_search_async(
                queries=queries,
                max_results=max_results,
                include_answer=include_answer
            )
        else:
            self.console.print("[yellow]No queries provided[/yellow]")

class TavilyInteractiveCLI:
    """Interactive CLI for Tavily search operations"""
    
    def __init__(self):
        self.console = Console()
        try:
            self.tavily = TavilySearchUtils()
        except Exception as e:
            self.console.print(f"[bold red]Failed to initialize Tavily: {str(e)}[/bold red]")
            exit(1)

        self.commands = {
            "1": BasicSearchCommand(self.tavily, self.console),
            "2": NewsSearchCommand(self.tavily, self.console),
            "3": QnASearchCommand(self.tavily, self.console),
            "4": ImageSearchCommand(self.tavily, self.console),
            "5": RAGContextCommand(self.tavily, self.console),
            "6": URLExtractionCommand(self.tavily, self.console),
            "7": BatchSearchCommand(self.tavily, self.console)
        }

    async def display_menu(self) -> None:
        while True:
            self.console.clear()
            self.console.print("\n[bold cyan]🔍 Tavily Search CLI[/bold cyan]")
            
            menu = Table(show_header=False, box=None)
            menu.add_row("[1]", "Basic Search")
            menu.add_row("[2]", "News Search")
            menu.add_row("[3]", "QnA Search")
            menu.add_row("[4]", "Image Search")
            menu.add_row("[5]", "RAG Context")
            menu.add_row("[6]", "URL Content Extraction")
            menu.add_row("[7]", "Batch Search")
            menu.add_row("[q]", "Quit")
            
            self.console.print(menu)
            
            choice = Prompt.ask(
                "\n[yellow]Choose an option[/yellow]",
                choices=["1", "2", "3", "4", "5", "6", "7", "q"]
            )
            
            if choice == "q":
                break
                
            await self.handle_choice(choice)
            Prompt.ask("\n[yellow]Press Enter to continue[/yellow]")

    async def handle_choice(self, choice: str) -> None:
        """Handle menu choice using Command pattern."""
        try:
            if choice in self.commands:
                await self.commands[choice].execute()
        except Exception as e:
            self.console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
            logger.error(f"Error executing command: {str(e)}", exc_info=True)

async def main():
    try:
        cli = TavilyInteractiveCLI()
        await cli.display_menu()
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[yellow]Exiting...[/yellow]")
    except Exception as e:
        console = Console()
        console.print(f"\n[bold red]Fatal error: {str(e)}[/bold red]")
        logger.critical(f"Fatal error: {str(e)}", exc_info=True)
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())