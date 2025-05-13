from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )
    
    def to_dict(self, ) -> dict:
        return self.model_dump()
    