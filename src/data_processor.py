from typing import Dict
import pandas as pd
import logging

class DataProcessor:
    """Implements business logic for data analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_max_cost_isn(self, pc_df: pd.DataFrame, nb_df: pd.DataFrame) -> str:
        """
        Find ISN with maximum total cost across both dataframes
        
        Args:
            pc_df: DataFrame with PC data
            nb_df: DataFrame with notebook data
            
        Returns:
            ISN string of item with highest total cost
        """
        try:
            # Filter out defective items
            pc_valid = pc_df[~pc_df['Defective']]
            nb_valid = nb_df[~nb_df['Defective']]

            print(pc_valid)
            print(nb_valid)
            
            # Combine and find max
            all_items = pd.concat([pc_valid, nb_valid])
            if all_items.empty:
                raise ValueError("No valid (non-defective) items found")
                
            max_cost_row = all_items.loc[all_items['Total Cost'].idxmax()]
            return max_cost_row['ISN']
            
        except Exception as e:
            self.logger.error(f"Error in get_max_cost_isn: {str(e)}")
            raise
            
    def calculate_cost_stats(self, pc_df: pd.DataFrame, nb_df: pd.DataFrame) -> Dict:
        """
        Calculate cost statistics across both dataframes
        
        Args:
            pc_df: DataFrame with PC data
            nb_df: DataFrame with notebook data
            
        Returns:
            Dictionary with max, min and average costs
        """
        try:
            # Filter out defective items
            pc_valid = pc_df[~pc_df['Defective']]
            nb_valid = nb_df[~nb_df['Defective']]
            
            # Combine costs
            all_costs = pd.concat([pc_valid['Total Cost'], nb_valid['Total Cost']])
            
            if all_costs.empty:
                raise ValueError("No valid (non-defective) items found")
                
            return {
                'max_cost': float(all_costs.max()),
                'min_cost': float(all_costs.min()),
                'avg_cost': round(float(all_costs.mean()), 2)
            }
            
        except Exception as e:
            self.logger.error(f"Error in calculate_cost_stats: {str(e)}")
            raise
            
    def calculate_battery_stats(self, nb_df: pd.DataFrame) -> Dict:
        """
        Calculate battery cost statistics for notebooks
        
        Args:
            nb_df: DataFrame with notebook data
            
        Returns:
            Dictionary with max, min and average battery costs
        """
        try:
            if 'Battery Cost' not in nb_df.columns:
                raise ValueError("Battery Cost column not found in notebook data")
                
            # Filter out defective items
            valid_items = nb_df[~nb_df['Defective']]
            battery_costs = valid_items['Battery Cost']
            
            if battery_costs.empty:
                raise ValueError("No valid (non-defective) items found")
                
            return {
                'max_battery': float(battery_costs.max()),
                'min_battery': float(battery_costs.min()),
                'avg_battery': round(float(battery_costs.mean()), 2)
            }
            
        except Exception as e:
            self.logger.error(f"Error in calculate_battery_stats: {str(e)}")
            raise