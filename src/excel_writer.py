# excel_writer.py
from typing import Dict
import pandas as pd
import logging
import os

class ExcelWriter:
    """Handles writing results to Excel file"""
    
    def __init__(self, output_dir: str = 'data/output'):
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def write_results(self, filename: str, max_isn: str, 
                     cost_stats: Dict, battery_stats: Dict):
        """Write analysis results to Excel file"""
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            self.logger.info(f"Writing results to {filepath}")
            
            # Create DataFrames for each result
            result1_df = pd.DataFrame({
                'Result1 - Max Cost ISN': [max_isn]
            })
            
            result2_df = pd.DataFrame({
                'Result2 - Cost Statistics': ['Maximum Cost', 'Minimum Cost', 'Average Cost'],
                'Values': [cost_stats['max_cost'], cost_stats['min_cost'], cost_stats['avg_cost']]
            })
            
            result3_df = pd.DataFrame({
                'Result3 - Battery Statistics': ['Maximum Battery Cost', 'Minimum Battery Cost', 'Average Battery Cost'],
                'Values': [battery_stats['max_battery'], battery_stats['min_battery'], battery_stats['avg_battery']]
            })
            
            # Write all results to Excel using openpyxl
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Write Result1 at the top
                result1_df.to_excel(writer, sheet_name='Results', index=False, startrow=0)
                
                # Write Result2 below Result1 (leaving one row gap)
                result2_df.to_excel(writer, sheet_name='Results', index=False, startrow=3)
                
                # Write Result3 below Result2 (leaving one row gap)
                result3_df.to_excel(writer, sheet_name='Results', index=False, startrow=8)
            
            self.logger.info(f"Results successfully written to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error writing results to Excel: {str(e)}")
            raise