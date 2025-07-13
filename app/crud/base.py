from typing import Any, Generic, List, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Define TypeVars for generic typing
# ModelType: The SQLAlchemy ORM model (e.g., Todo, User)
# CreateSchemaType: Pydantic schema for creating a new item (e.g., TodoCreate, UserCreate)
# UpdateSchemaType: Pydantic schema for updating an item (e.g., TodoUpdate, UserUpdate)
ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for CRUD operations.
    Provides generic methods for common database interactions.
    """
    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUDBase with the SQLAlchemy model.

        Args:
            model: The SQLAlchemy model class (e.g., models.Todo).
        """
        self.model = model

    def get(self, db: Session, model_id: Any) -> ModelType | None:
        """
        Retrieve a single record by its ID.

        Args:
            db: The SQLAlchemy database session.
            model_id: The ID of the record to retrieve.

        Returns:
            The SQLAlchemy model instance if found, otherwise None.
        """
        return db.query(self.model).filter(self.model.id == model_id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Retrieve multiple records with optional pagination.

        Args:
            db: The SQLAlchemy database session.
            skip: The number of records to skip (for pagination).
            limit: The maximum number of records to return (for pagination).

        Returns:
            A list of SQLAlchemy model instances.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record in the database.

        Args:
            db: The SQLAlchemy database session.
            obj_in: The Pydantic schema containing data for creation.

        Returns:
            The newly created SQLAlchemy model instance.
        """
        # Convert Pydantic model to a dictionary to pass to the SQLAlchemy model
        obj_data = obj_in.model_dump() # Use .model_dump() for Pydantic v2
        # obj_data = obj_in.dict() # Use .dict() for Pydantic v1

        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj) # Refresh to get any DB-generated values (like ID)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        """
        Update an existing record in the database.

        Args:
            db: The SQLAlchemy database session.
            db_obj: The SQLAlchemy model instance to update.
            obj_in: The Pydantic schema or dictionary containing update data.

        Returns:
            The updated SQLAlchemy model instance.
        """
        obj_data = db_obj.__dict__ # Get current data from DB object

        # Determine update data source
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True) # Exclude unset fields from Pydantic model

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, model_id: int) -> ModelType | None:
        """
        Delete a record from the database by its ID.

        Args:
            db: The SQLAlchemy database session.
            model_id: The ID of the record to delete.

        Returns:
            The deleted SQLAlchemy model instance if found, otherwise None.
        """
        obj = db.query(self.model).get(model_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj