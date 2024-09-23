import unittest
import pandas as pd
from movies_stats import Movies
import os


class TestMovies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment before running tests
        """
        cls.test_file = "./movies_metadata.csv"
        cls.movies = Movies(cls.test_file)
        cls.movies.load_dataset()

    def test_unique_movies_count(self):
        """
        Test for unique movies count.
        Ensures it returns an integer.
        """
        unique_count = self.movies.get_unique_movies_count()  
        self.assertIsInstance(unique_count, int)

    def test_average_rating(self):
        """
        Test for average rating calculation.
        Ensures it returns a float.
        """
        average_rating = self.movies.get_average_rating()  
        self.assertIsInstance(average_rating, float)

    def test_top_5_movies(self):
        """
        Test for retrieval of top 5 highest rated movies.
        Ensures it returns 5 movies.
        """
        top_movies = self.movies.get_top_5_movies()  
        self.assertEqual(top_movies.shape[0], 5)  

    def test_movies_per_years(self):
        """
        Test for movies released per year.
        Ensures it returns a Pandas DataFrame.
        """
        movies_per_year = self.movies.get_movies_per_year()  
        self.assertIsInstance(movies_per_year, pd.DataFrame)  
        self.assertIn('release_year', movies_per_year.columns) 
        self.assertIn('Movie_Count', movies_per_year.columns)  


    def test_movies_per_genre(self):
        """
        Test for movies counted per genre.
        Ensures it returns a DataFrame and
        checks if 'Genre' column exists.
        """
        genre_counts = self.movies.get_movies_per_genre()
        self.assertIsInstance(genre_counts, pd.DataFrame)
        self.assertTrue('genres' in genre_counts.columns)
        
    def test_save_to_json(self):
        """
        Test for saving DataFrame to a JSON file.
        Checks if the file was created and cleans up after test
        """
        output_file = 'test_movies_stats.json'
        self.movies.save_to_json(output_file)  
        self.assertTrue(os.path.exists(output_file))
        os.remove(output_file)


if __name__ == '__main__':
    unittest.main()