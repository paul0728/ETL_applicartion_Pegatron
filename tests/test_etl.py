from typing import Dict, List, Any, Union, Optional
import unittest
import functools
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
import numpy as np
from src.data_loader import DataLoader
from src.data_processor import DataProcessor
from src.excel_writer import ExcelWriter
import os

def print_test_result(func: Any) -> Any:
    """Decorator to print test results"""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        test_name = func.__name__
        print(f"\nRunning {test_name}...", end=" ")
        try:
            func(*args, **kwargs)
            print("✅ PASS")
        except Exception as e:
            print(f"❌ FAIL - {str(e)}")
            raise
    return wrapper

class TestDataLoader(unittest.TestCase):
    def setUp(self) -> None:
        self.loader = DataLoader()
        
    @print_test_result
    def test_init_custom_directory(self) -> None:
        """Test custom input directory initialization"""
        custom_dir: str = "custom/input/dir"
        loader = DataLoader(input_dir=custom_dir)
        self.assertEqual(loader.input_dir, custom_dir)
        
    @print_test_result
    def test_init_default_directory(self) -> None:
        """Test default input directory initialization"""
        loader = DataLoader()
        self.assertEqual(loader.input_dir, 'data/input')
        
    @print_test_result
    def test_clean_column_names(self) -> None:
        df = pd.DataFrame({
            'Defective ': [True, False],
            'ISN': ['PC1', 'PC2']
        })
        cleaned_df = self.loader._clean_column_names(df)
        self.assertIn('Defective', cleaned_df.columns)
        
    @print_test_result
    @patch('pandas.read_csv')
    def test_load_csv_success(self, mock_read_csv: MagicMock) -> None:
        mock_df = pd.DataFrame({
            'Product Type': ['PC', 'PC'],
            'ISN': ['PC1', 'PC2'],
            'Defective': [True, False],
            'CPU Cost': [100, 200],
            'Network Card Cost': [50, 60],
            'Total Cost': [150, 260]
        })
        mock_read_csv.return_value = mock_df
        
        result = self.loader.load_csv('PC.csv')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), [
            'Product Type', 'ISN', 'Defective', 'CPU Cost', 
            'Network Card Cost', 'Total Cost'
        ])
        
    @print_test_result
    @patch('pandas.read_csv')
    def test_load_csv_missing_columns(self, mock_read_csv: MagicMock) -> None:
        mock_df = pd.DataFrame({
            'Product Type': ['PC'],
            'ISN': ['PC1']
        })
        mock_read_csv.return_value = mock_df
        
        with self.assertRaises(ValueError) as context:
            self.loader.load_csv('PC.csv')
        self.assertIn('Missing required columns', str(context.exception))
        
    @print_test_result
    def test_load_csv_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            self.loader.load_csv('nonexistent.csv')
            
class TestDataProcessor(unittest.TestCase):
    def setUp(self) -> None:
        self.processor = DataProcessor()
        
        # 準備測試資料
        self.pc_data: pd.DataFrame = pd.DataFrame({
            'Product Type': ['PC', 'PC', 'PC'],
            'ISN': ['PC1', 'PC2', 'PC3'],
            'Defective': [False, True, False],
            'CPU Cost': [200, 300, 400],
            'Network Card Cost': [50, 60, 70],
            'Total Cost': [250, 360, 470]
        })
        
        self.nb_data: pd.DataFrame = pd.DataFrame({
            'Product Type': ['NB', 'NB', 'NB'],
            'ISN': ['NB1', 'NB2', 'NB3'],
            'Defective': [False, False, True],
            'CPU Cost': [300, 400, 500],
            'Network Card Cost': [60, 70, 80],
            'Battery Cost': [100, 120, 140],
            'Total Cost': [460, 590, 720]
        })
        
    @print_test_result
    def test_get_max_cost_isn(self) -> None:
        result = self.processor.get_max_cost_isn(self.pc_data, self.nb_data)
        self.assertEqual(result, 'NB2')
        
    @print_test_result
    def test_get_max_cost_isn_all_defective(self) -> None:
        pc_all_defective = self.pc_data.copy()
        pc_all_defective['Defective'] = True
        nb_all_defective = self.nb_data.copy()
        nb_all_defective['Defective'] = True
        
        with self.assertRaises(ValueError) as context:
            self.processor.get_max_cost_isn(pc_all_defective, nb_all_defective)
        self.assertIn('No valid (non-defective) items found', str(context.exception))
        
    @print_test_result
    def test_calculate_cost_stats(self) -> None:
        stats = self.processor.calculate_cost_stats(self.pc_data, self.nb_data)
        
        self.assertIsInstance(stats, dict)
        self.assertIn('max_cost', stats)
        self.assertIn('min_cost', stats)
        self.assertIn('avg_cost', stats)
        
        self.assertEqual(stats['max_cost'], 590.0)  # NB2
        self.assertEqual(stats['min_cost'], 250.0)  # PC1
        
    @print_test_result
    def test_calculate_cost_stats_empty_data(self) -> None:
        """Test cost statistics calculation with empty data"""
        # 創建一個有正確欄位和型別的空 DataFrame
        empty_df = pd.DataFrame({
            'Product Type': pd.Series(dtype='str'),
            'ISN': pd.Series(dtype='str'),
            'Defective': pd.Series(dtype='bool'),
            'CPU Cost': pd.Series(dtype='float64'),
            'Network Card Cost': pd.Series(dtype='float64'),
            'Total Cost': pd.Series(dtype='float64')
        })
        with self.assertRaises(ValueError) as context:
            self.processor.calculate_cost_stats(empty_df, empty_df)
        self.assertIn('No valid', str(context.exception))
            
    @print_test_result
    def test_calculate_cost_stats_exception_handling(self) -> None:
        """Test exception handling in cost statistics calculation"""
        invalid_df = pd.DataFrame({'invalid': [1, 2, 3]})
        with self.assertRaises(Exception):
            self.processor.calculate_cost_stats(invalid_df, invalid_df)
        
    @print_test_result
    def test_calculate_battery_stats(self) -> None:
        stats = self.processor.calculate_battery_stats(self.nb_data)
        
        self.assertIsInstance(stats, dict)
        self.assertIn('max_battery', stats)
        self.assertIn('min_battery', stats)
        self.assertIn('avg_battery', stats)
        
        self.assertEqual(stats['max_battery'], 120.0)  # NB2
        self.assertEqual(stats['min_battery'], 100.0)  # NB1
        
    @print_test_result
    def test_calculate_battery_stats_missing_column(self) -> None:
        """Test battery statistics calculation with missing Battery Cost column"""
        invalid_df = pd.DataFrame({'invalid': [1, 2, 3]})
        with self.assertRaises(ValueError) as context:
            self.processor.calculate_battery_stats(invalid_df)
        self.assertIn('Battery Cost column not found', str(context.exception))
        
    @print_test_result
    def test_calculate_battery_stats_empty_data(self) -> None:
        """Test battery statistics calculation with empty data"""
        # 創建一個有正確欄位和型別的空 DataFrame
        empty_df = pd.DataFrame({
            'Product Type': pd.Series(dtype='str'),
            'ISN': pd.Series(dtype='str'),
            'Defective': pd.Series(dtype='bool'),
            'CPU Cost': pd.Series(dtype='float64'),
            'Network Card Cost': pd.Series(dtype='float64'),
            'Battery Cost': pd.Series(dtype='float64'),
            'Total Cost': pd.Series(dtype='float64')
        })
        with self.assertRaises(ValueError) as context:
            self.processor.calculate_battery_stats(empty_df)
        self.assertIn('No valid', str(context.exception))
        
class TestExcelWriter(unittest.TestCase):
    def setUp(self) -> None:
        self.writer = ExcelWriter()
        self.test_data: Dict[str, Union[str, Dict[str, float]]] = {
            'max_isn': 'PC1',
            'cost_stats': {
                'max_cost': 1000.0,
                'min_cost': 500.0,
                'avg_cost': 750.0
            },
            'battery_stats': {
                'max_battery': 200.0,
                'min_battery': 100.0,
                'avg_battery': 150.0
            }
        }
        
    @print_test_result
    def test_init_custom_directory(self) -> None:
        """Test custom input directory initialization"""
        custom_dir = "custom/input/dir"
        loader = DataLoader(input_dir=custom_dir)
        self.assertEqual(loader.input_dir, custom_dir)

    @print_test_result
    def test_init_default_directory(self) -> None:
        """Test default input directory initialization"""
        loader = DataLoader()
        self.assertEqual(loader.input_dir, 'data/input')

    @print_test_result
    def test_write_results(self) -> None:
        filename = 'test_result.xlsx'
        filepath = os.path.join(self.writer.output_dir, filename)

        m = mock_open()
        with patch('builtins.open', m), \
             patch('pandas.ExcelWriter') as mock_excel_writer, \
             patch('pandas.DataFrame.to_excel') as mock_to_excel:
            
            self.writer.write_results(
                filename,
                self.test_data['max_isn'],
                self.test_data['cost_stats'],
                self.test_data['battery_stats']
            )

            mock_excel_writer.assert_called_once_with(
                filepath,
                engine='openpyxl'
            )

            self.assertEqual(mock_to_excel.call_count, 3)
            
            calls = mock_to_excel.call_args_list
            self.assertEqual(calls[0][1]['sheet_name'], 'Results')
            self.assertEqual(calls[0][1]['startrow'], 0)
            self.assertEqual(calls[1][1]['startrow'], 3)
            self.assertEqual(calls[2][1]['startrow'], 8)

if __name__ == '__main__':
    print("Starting ETL Unit Tests...")
    unittest.main(verbosity=2)