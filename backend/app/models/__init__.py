# Import all models so Alembic autogenerate can discover them
from app.models.codon_table import CodonTableCache  # noqa: F401
from app.models.construct import Construct  # noqa: F401
from app.models.construct_element import ConstructElement  # noqa: F401
from app.models.optimization_job import OptimizationJob  # noqa: F401
from app.models.organism import Organism  # noqa: F401
from app.models.project import Project  # noqa: F401
