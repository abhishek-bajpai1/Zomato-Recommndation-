import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd
import os

def load_zomato_data_kaggle():
    """
    Fetches the Zomato dataset from Kaggle using kagglehub.
    Saves it as a CSV locally for Phase 2.
    """
    print("Fetching dataset from Kaggle: abhijitdahatonde/zomato-restaurants-dataset...")
    try:
        # Load the latest version
        df = kagglehub.load_dataset(
            KaggleDatasetAdapter.PANDAS,
            "abhijitdahatonde/zomato-restaurants-dataset",
            "zomato.csv",  # Specifically looking for the main csv file
        )
        
        # Save to current directory for consistency with previous phases
        output_path = os.path.join(os.getcwd(), "zomato_data.csv")
        df.to_csv(output_path, index=False)
        
        print(f"Dataset successfully saved to {output_path}")
        print(f"Total records loaded: {len(df)}")
        return df
    except Exception as e:
        print(f"Error loading Kaggle dataset: {e}")
        # Fallback to general load if filename is different
        try:
             df = kagglehub.load_dataset(
                KaggleDatasetAdapter.PANDAS,
                "abhijitdahatonde/zomato-restaurants-dataset",
                "",
            )
             output_path = os.path.join(os.getcwd(), "zomato_data.csv")
             df.to_csv(output_path, index=False)
             return df
        except:
            return None

if __name__ == "__main__":
    load_zomato_data_kaggle()
