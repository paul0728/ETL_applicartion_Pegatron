from typing import Dict, List
import pandas as pd
import logging
import os

class DataLoader:
    """Handles loading and initial processing of CSV files"""
    
    def __init__(self, input_dir: str = 'data/input'):
        self.logger = logging.getLogger(__name__)
        self.input_dir = input_dir
    
    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean column names by removing leading/trailing whitespace
        """
        return df.rename(columns=lambda x: x.strip())
    
    def load_csv(self, filename: str) -> pd.DataFrame:
        """
        Load CSV file into pandas DataFrame
        
        Args:
            filename: Name of CSV file
            
        Returns:
            DataFrame containing the CSV data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            pd.errors.EmptyDataError: If file is empty
        """
        filepath = os.path.join(self.input_dir, filename)
        try:
            self.logger.info(f"Loading {filepath}")
            df = pd.read_csv(filepath)
            
            if df.empty:
                raise pd.errors.EmptyDataError(f"File {filepath} is empty")
            
            # Clean column names by removing whitespace
            df = self._clean_column_names(df)
            
            # Validate expected columns
            expected_columns = ['Product Type', 'ISN', 'Defective', 'CPU Cost', 
                              'Network Card Cost', 'Total Cost']
            missing_columns = [col for col in expected_columns if col not in df.columns]
            
            if missing_columns:
                self.logger.error(f"Columns in file: {list(df.columns)}")
                self.logger.error(f"Missing columns: {missing_columns}")
                raise ValueError(f"Missing required columns in {filepath}: {', '.join(missing_columns)}")
                
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading {filepath}: {str(e)}")
            raise