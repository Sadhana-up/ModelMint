import pandas as pd
from google.adk.agents import Agent
from dotenv import load_dotenv
load_dotenv()

# TOOL 1: Read the CSV file
def read_csv_file(file_path: str) -> dict:
    """
    Reads a CSV file and returns a summary of its contents.
    Args:
        file_path: The full path to the CSV file.
    Returns:
        A dict with columns, row count, missing values, and duplicates found.
    """
    try:
        df = pd.read_csv(file_path)
        return {
            "status": "success",
            "columns": list(df.columns),
            "row_count": len(df),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 2nd tool which cleans the csv 
def clean_csv_file(file_path: str, output_path: str) -> dict:
    """
    Cleans a CSV file by removing duplicates, handling missing values,
    and stripping whitespace from string columns. Saves the result.
    Args:
        file_path: Path to the input CSV file.
        output_path: Path where the cleaned CSV will be saved.
    Returns:
        A dict with a summary of what was cleaned and where it was saved.
    """
    try:
        df = pd.read_csv(file_path)
        original_rows = len(df)

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Strip whitespace from string columns
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].str.strip()

        # Fill missing numeric values with column median
        for col in df.select_dtypes(include="number").columns:
            df[col] = df[col].fillna(df[col].median())

        # Drop rows where ALL values are missing
        df = df.dropna(how="all")

        df.to_csv(output_path, index=False)

        return {
            "status": "success",
            "original_rows": original_rows,
            "cleaned_rows": len(df),
            "rows_removed": original_rows - len(df),
            "output_file": output_path,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# agent that uses the above tools to read and clean csv files
root_agent = Agent(
    model="gemini-3-flash-preview",
    name="csv_cleaner_agent",
    description="An agent that reads, analyzes, and cleans CSV files.",
    instruction="""You are a data cleaning assistant. 
    When a user gives you a CSV file path, first use read_csv_file to inspect it, 
    then use clean_csv_file to clean it and report what was done.""",
    tools=[read_csv_file, clean_csv_file],
)

