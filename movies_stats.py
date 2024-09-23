import pandas as pd
import logging
import ast
from collections import Counter

class Movies:

    def __init__(self, file_path):
        """
        Initializes the Movies object with the provided file path
        """
        self.file_path = file_path
        self.df = None
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_dataset(self):
        """
        Loads the CSV file into a Pandas Dataframe
        """
        try:
            logging.info(f"Loading data from {self.file_path}")
            self.df = pd.read_csv(self.file_path, low_memory=False)
            logging.info("Data loaded successfully")
        except FileNotFoundError:
            logging.error(f"The file {self.file_path} does not exist.")
            raise
        except pd.errors.ParserError as e:
            logging.error(f"Error parsing the file: {e}")
            raise

    def check_data(self):
        """
        Check the basic info of the loaded DataFrame.
        """
        if self.df is not None:
            logging.info("Dataset Info:")
            return self.df.info()
        else:
            logging.error("DataFrame is empty. Load the data first.")

    def get_unique_movies_count(self):
        """
        Returns the number of unique movies based on the 'original_title' column.
        """
        if self.df is not None:
            return self.df['original_title'].nunique()
        else:
            logging.error("Data is not loaded.")
            raise ValueError("Data is not loaded.")

    def get_average_rating(self):
        """
        Returns the average rating of all the movies rounded to 2 decimals
        """
        if self.df is not None:
            return round(self.df['vote_average'].mean(), 2)
        else:
            logging.error("Data is not loaded.")
            raise ValueError("Data is not loaded.")

    def get_top_5_movies(self):
        """
        Returns the top 5 highest-rated movies.
        For more accurate result and to avoid movies rated with 10 by 1 user,
        a threshold was set of at least 8000 votes and at least 8 average rating
        """
        if self.df is not None:
            return (
                self.df.loc[(self.df['vote_average'] > 8) & (self.df['vote_count'] > 8000)]
                .nlargest(5, 'vote_average')[['original_title', 'vote_average', 'vote_count']]
            )
        else:
            logging.error("Data is not loaded.")
            raise ValueError("Data is not loaded.")

    def get_movies_per_year(self):
        """
        Returns the number of movies released per year.
        """
        if self.df is not None:
            return (
                self.df.assign(release_year=pd.to_datetime(self.df['release_date'], errors='coerce').dt.year)  # Create a new column for release_year
                .groupby('release_year')
                .size()
                .reset_index(name='Movie_Count')  
                .sort_values('release_year')  
            )
        else:
            logging.error("Data is not loaded.")
            raise ValueError("Data is not loaded.")

    def extract_genres(self, genre_list_str):
        """
        Extracts a list of genres from the string representation of a list of dictionaries.
        This method is used for the next method (get_movies_per_genre)
        """
        try:
            genres = ast.literal_eval(genre_list_str)
            return [genre['name'] for genre in genres]
        except (ValueError, SyntaxError):
            return []

    def get_movies_per_genre(self):
        """
        Returns the number of movies in each genre.
        Apply the extract_genres function to 'genres' column, flatten the list,
        group by genre to count the occurrences 
        """
        if self.df is not None:
            return (
                self.df['genres']
                .apply(self.extract_genres)  
                .explode()                   
                .value_counts()              
                .reset_index(name='Count')   
                .rename(columns={'index': 'Genre'}) 
                .sort_values(by='Count', ascending=False)
            )    
        else:
            logging.error("Data is not loaded.")
            raise ValueError("Data is not loaded.")

    def save_to_json(self, output_file):
        """
        Saves the DataFrame to a JSON file.
        """
        if self.df is not None:
            logging.info(f"Saving data to {output_file}")
            try:
                self.df.to_json(output_file, orient='records', lines=True)
                logging.info(f"Data successfully saved to {output_file}")
            except Exception as e:
                logging.error(f"Error saving file to JSON: {e}")
                raise
        else:
            logging.error("Data is not loaded.")
            raise ValueError("Data is not loaded.")


def main():
    movies = Movies("./movies_metadata.csv")
    movies.load_dataset()
    movies.check_data()
    print("-------------------------------------------------")
    print("Number of unique movies released: ", movies.get_unique_movies_count())
    print("-------------------------------------------------")
    print("Average rating of all movies: ", movies.get_average_rating())
    print("-------------------------------------------------")
    print("Top 5 highest rated movies:\n ", movies.get_top_5_movies().to_string(justify='center',index=False))
    print("-------------------------------------------------")
    print("Number of movies released per year:\n", movies.get_movies_per_year().to_string(justify='center',index=False))
    print("-------------------------------------------------")
    print("Number of movies per genre:\n ", movies.get_movies_per_genre().to_string(justify='center',index=False))
    print("-------------------------------------------------")
    movies.save_to_json('movies_metadata.json')


if __name__ == '__main__':
    main()