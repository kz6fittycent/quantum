from units.compat.mock import MagicMock
from quantum.utils.path import unfrackpath


mock_unfrackpath_noop = MagicMock(spec_set=unfrackpath, side_effect=lambda x, *args, **kwargs: x)
