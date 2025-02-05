import logging
from data_loader import DataLoader
from data_processor import DataProcessor
from excel_writer import ExcelWriter

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """Main ETL process"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize components
        loader = DataLoader()
        processor = DataProcessor()
        writer = ExcelWriter()
        
        # Load data
        logger.info("Loading input files...")
        pc_df = loader.load_csv('PC.csv')
        nb_df = loader.load_csv('NB.csv')
        
        # Process data
        logger.info("Processing data...")
        max_isn = processor.get_max_cost_isn(pc_df, nb_df)
        cost_stats = processor.calculate_cost_stats(pc_df, nb_df)
        battery_stats = processor.calculate_battery_stats(nb_df)
        
        # Write results
        logger.info("Writing results...")
        writer.write_results('result.xlsx', max_isn, cost_stats, battery_stats)
        
        logger.info("ETL process completed successfully")
        
    except Exception as e:
        logger.error(f"ETL process failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()