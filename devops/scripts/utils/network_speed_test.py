# pip install speedtest-cli rich psutil
import speedtest
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    BarColumn,
    TaskProgressColumn,
)
from rich.table import Table
import psutil
import platform
import socket

def get_device_info():
    """
    Get system and network information
    """
    try:
        # Get network interfaces
        network_interfaces = []
        for interface, addresses in psutil.net_if_addrs().items():
            for addr in addresses:
                if addr.family == socket.AF_INET:  # IPv4
                    network_interfaces.append({
                        'interface': interface,
                        'ip': addr.address
                    })

        # Get system information
        info = {
            'system': platform.system(),
            'release': platform.release(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'hostname': socket.gethostname(),
            'interfaces': network_interfaces
        }
        return info
    except Exception as e:
        return str(e)

def test_network_speed():
    """
    Test network download and upload speeds using speedtest-cli.
    Returns download speed, upload speed, and ping in a formatted string.
    """
    console = Console()
    
    try:
        # Create speedtest object
        st = speedtest.Speedtest()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            # Get best server
            server_task = progress.add_task("[cyan]Finding best server...", total=1)
            server = st.get_best_server()
            progress.update(server_task, completed=1, description="[green]Found best server")
            
            # Test download speed
            download_task = progress.add_task("[cyan]Testing download speed...", total=1)
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            progress.update(download_task, completed=1, 
                          description=f"[green]Download completed: {round(download_speed, 2)} Mbps")
            
            # Test upload speed
            upload_task = progress.add_task("[cyan]Testing upload speed...", total=1)
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            progress.update(upload_task, completed=1, 
                          description=f"[green]Upload completed: {round(upload_speed, 2)} Mbps")
        
        # Get ping
        ping = st.results.ping
        
        return {
            'timestamp': timestamp,
            'download': round(download_speed, 2),
            'upload': round(upload_speed, 2),
            'ping': round(ping, 2),
            'server': server
        }
        
    except Exception as e:
        console.print(f"[red]An error occurred: {str(e)}[/red]")
        return None

def main():
    """
    Main function to run the speed test and display results.
    """
    console = Console()
    
    try:
        console.print("\n[bold cyan]Network Speed Test[/bold cyan]\n")
        
        # Get device information
        device_info = get_device_info()
        
        # Create device info table
        device_table = Table(show_header=True, header_style="bold magenta")
        device_table.add_column("Device Information", style="cyan", width=20)
        device_table.add_column("Value", style="green")
        
        device_table.add_row("OS", f"{device_info['system']} {device_info['release']}")
        device_table.add_row("Machine", device_info['machine'])
        device_table.add_row("Processor", device_info['processor'])
        device_table.add_row("Hostname", device_info['hostname'])
        
        # Add network interfaces
        for interface in device_info['interfaces']:
            device_table.add_row(
                "Network Interface", 
                f"{interface['interface']} ({interface['ip']})"
            )
        
        console.print(Panel(
            device_table,
            title="Device Information",
            border_style="blue",
            padding=(1, 2)
        ))
        
        # Run speed test
        results = test_network_speed()
        
        if results:
            # Create speed test results table
            speed_table = Table(show_header=True, header_style="bold magenta")
            speed_table.add_column("Metric", style="cyan", width=15)
            speed_table.add_column("Value", style="green")
            
            speed_table.add_row("Timestamp", results['timestamp'])
            speed_table.add_row("Download Speed", f"{results['download']} Mbps")
            speed_table.add_row("Upload Speed", f"{results['upload']} Mbps")
            speed_table.add_row("Ping", f"{results['ping']} ms")
            speed_table.add_row("Server Host", results['server']['host'])
            speed_table.add_row("Server Location", 
                              f"{results['server']['name']}, {results['server']['country']}")
            
            console.print(Panel(
                speed_table,
                title="Speed Test Results",
                border_style="blue",
                padding=(1, 2)
            ))
            
    except Exception as e:
        console.print(f"[red]An error occurred in main: {str(e)}[/red]")

if __name__ == "__main__":
    from datetime import datetime
    
    # Run the main program
    main()