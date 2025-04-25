import requests
import json
import argparse
from typing import List, Dict
from tabulate import tabulate

GRAFANA_URL = ""
DEBUG_MODE = False  # Set to True to enable detailed debug output


def debug_print(message):
    if DEBUG_MODE:
        print(message)


def get_headers(token: str) -> dict:
    """Create headers with authorization token"""
    return {"Authorization": f"Bearer {token}"}


def get_all_dashboards_search(headers: dict, prefix: str, limit: int) -> List[Dict]:
    """Get all dashboards using the search API with comprehensive parameters"""
    params = {
        "type": "dash-db",
        "sort": "name",
        # Debug 時可以限制數量
        "limit": limit,
        "query": prefix,
    }

    url = f"{GRAFANA_URL}/api/search"
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        dashboards = response.json()
        print(f"Found {len(dashboards)} dashboards via search API")
        return dashboards
    except requests.exceptions.RequestException as e:
        print(f"Error getting dashboards via search: {str(e)}")
        if hasattr(e.response, "text"):
            print(f"Response: {e.response.text}")
        return []


def get_all_dashboards(headers: dict, prefix: str, limit: int) -> List[Dict]:
    """Get all dashboards from Grafana"""
    dashboards = get_all_dashboards_search(headers, prefix, limit)
    return dashboards


def get_dashboard_details(headers: dict, uid: str) -> Dict:
    """Get detailed information for a specific dashboard"""
    try:
        response = requests.get(
            f"{GRAFANA_URL}/api/dashboards/uid/{uid}", headers=headers
        )
        response.raise_for_status()
        data = response.json()
        if not data:
            print(f"Warning: Empty response for dashboard {uid}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error getting dashboard details for {uid}: {str(e)}")
        if hasattr(e.response, "text"):
            print(f"Response: {e.response.text}")
        return {}


def check_plugins_usage(dashboard_data: Dict, plugins: List[str]) -> Dict[str, bool]:
    """
    Check if dashboard uses specified plugins.
    """
    dashboard = dashboard_data.get("dashboard", {})
    panels = dashboard.get("panels", [])

    debug_print(f"\nAnalyzing dashboard: {dashboard.get('title', 'Unknown')}")

    plugin_usage = {plugin: False for plugin in plugins}

    def check_panel_plugins(panel, plugin_usage):
        debug_print(f"\nChecking panel: {panel.get('title', 'Untitled')}")
        debug_print(f"Panel type: {panel.get('type', 'No type')}")

        # Check panel type
        panel_type = panel.get("type", "")
        if panel_type == "row":
            return
        if panel_type in plugins:
            plugin_usage[panel_type] = True
            debug_print(f"Found panel type: {panel_type}")

    def process_panels(panels_list):
        for panel in panels_list:
            check_panel_plugins(panel, plugin_usage)
            # Process nested panels (rows/groups)
            if "panels" in panel:
                nested_panels = panel["panels"]
                debug_print(
                    f"\nFound nested panels in {panel.get('title', 'Untitled')}, count: {len(nested_panels)}"
                )
                process_panels(nested_panels)

    # Start processing from top level
    debug_print(f"\nTotal top-level panels: {len(panels)}")
    process_panels(panels)
    return plugin_usage


def check_datasource_usage(
    dashboard_data: Dict, datasources: List[str]
) -> Dict[str, bool]:
    """
    Check if dashboard uses specified datasources.
    """
    dashboard = dashboard_data.get("dashboard", {})
    panels = dashboard.get("panels", [])

    debug_print(f"\nAnalyzing dashboard: {dashboard.get('title', 'Unknown')}")

    datasource_usage = {datasource: False for datasource in datasources}

    def check_panel_datasource(panel, datasource_usage):
        # Check datasource
        panel_type = panel.get("type", "")
        if panel_type == "row":
            return
        datasource = panel.get("datasource", {})
        debug_print(f"Datasource: {datasource}")

        if isinstance(datasource, str):
            debug_print(f"Datasource is string: {datasource}")
            if datasource in datasources:
                datasource_usage[datasource] = True
                debug_print(f"Found datasource: {datasource}")
        else:
            print(
                f"\nPanel: {panel.get('title')}'s datasource is not a string: {datasource}, type: {type(datasource)}"
            )
            print(f"Panel type: {panel.get('type', 'No type')}")
            return

    def process_panels(panels_list):
        for panel in panels_list:
            check_panel_datasource(panel, datasource_usage)
            # Process nested panels (rows/groups)
            if "panels" in panel:
                nested_panels = panel["panels"]
                debug_print(
                    f"\nFound nested panels in {panel.get('title', 'Untitled')}, count: {len(nested_panels)}"
                )
                process_panels(nested_panels)

    # Start processing from top level
    debug_print(f"\nTotal top-level panels: {len(panels)}")
    process_panels(panels)
    return datasource_usage


def parse_key_value(arg):
    if "=" in arg:
        key, value = arg.split("=", 1)
        return key, value
    else:
        raise argparse.ArgumentTypeError(f"Invalid key=value format: {arg}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Search Grafana dashboards for specific plugins"
    )
    parser.add_argument(
        "--params",
        nargs="+",
        type=parse_key_value,
        help="""
Key-value pairs in the format key=value
Valid key=value pairs:
- url=Grafana URL (e.g., https://grafana.example.com)
- token=Grafana service account token
- dashboard_prefix=Prefix for the dashboards to fetch. Default is empty string
- limit=Limit for the number of dashboards to fetch. Default is 1000
- plugins=List of plugin names to search for (e.g., grafana-piechart-panel,grafana-polystat-panel)
- datasources=List of datasource names to search for (e.g., doitintl-bigquery-datasource,grafana-googlesheets-datasource)
- debug=Enable debug mode (true/false). Default is false
""",
    )
    args = parser.parse_args()
    # Grafana service account token
    args = dict(args.params)
    global GRAFANA_URL
    GRAFANA_URL = args.get("url")
    if not GRAFANA_URL:
        print("Error: Grafana URL is required")
        return
    token = args.get("token")
    if not token:
        print("Error: Token is required")
        return
    # Prefix for the dashboards to fetch
    dashboard_prefix = args.get("dashboard_prefix", "")
    # Limit for the number of dashboards to fetch
    limit = args.get("limit", 1000)
    # List of plugin names to search for (e.g., grafana-piechart-panel,grafana-polystat-panel)
    plugins = args.get("plugins", "").split(",")
    # List of datasource names to search for (e.g., doitintl-bigquery-datasource,grafana-googlesheets-datasource)
    datasources = args.get("datasources", "").split(",")
    if not plugins and not datasources:
        print("Error: At least one plugin or datasource is required")
        return
    # Enable debug mode
    debug = args.get("debug", "False")
    global DEBUG_MODE
    DEBUG_MODE = debug.lower() == "true"

    # Create headers with the provided token
    headers = get_headers(token)

    print("Searching for dashboards using specific plugins...")
    print(f"Grafana URL: {GRAFANA_URL}")

    # Get all dashboards
    dashboards = get_all_dashboards(headers, prefix=dashboard_prefix, limit=limit)

    # Store results
    results = []

    # Get plugins from arguments
    print(f"Searching for dashboards using plugins: {', '.join(plugins)}")
    print(f"Searching for dashboards using datasources: {', '.join(datasources)}")

    # Check each dashboard
    for dashboard in dashboards:
        try:
            title = dashboard.get("title", "Unknown")
            uid = dashboard.get("uid", "")
            if not uid:
                print(f"Warning: Dashboard '{title}' has no UID")
                continue

            details = get_dashboard_details(headers, uid)
            if not details:
                continue

            plugin_usage = check_plugins_usage(details, plugins)
            datasource_usage = check_datasource_usage(details, datasources)

            if any(plugin_usage.values()) or any(datasource_usage.values()):
                dashboard_url = f"{GRAFANA_URL}/d/{uid}"
                folder = dashboard.get("folderTitle", "Root")
                used_plugins = [plugin for plugin, used in plugin_usage.items() if used]
                used_datasources = [
                    datasource for datasource, used in datasource_usage.items() if used
                ]

                results.append(
                    [
                        title,
                        folder,
                        dashboard_url,
                        ", ".join(used_plugins),
                        ", ".join(used_datasources),
                    ]
                )
        except Exception as e:
            print(f"Error processing dashboard {dashboard['title']}: {str(e)}")

    # Display results
    if results:
        print("\nDashboards using specified plugins:")
        headers = ["Dashboard", "Folder", "URL", "Plugins Used", "Datasources Used"]
        print(tabulate(results, headers=headers, tablefmt="grid"))
    else:
        print("\nNo dashboards found using the specified plugins.")


if __name__ == "__main__":
    main()
