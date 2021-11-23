from unittest.mock import patch
from MigrationScheduling.utils import initialize_seeds


@patch("MigrationScheduling.utils.np.random.seed", side_effect=None)
@patch("MigrationScheduling.utils.random.seed", side_effect=None)
def test_initialize_seeds(mock_random_seed, mock_numpy_seed):
    initialize_seeds(13)
    mock_random_seed.assert_called_once_with(13)
    mock_numpy_seed.assert_called_once_with(13)
