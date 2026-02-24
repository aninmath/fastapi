
from pydantic import BaseModel, Field
from typing import Annotated, Literal

class InsuranceInput(BaseModel):
    age: Annotated[
        int, 
        Field(
            ge=0, le=120,
            description="Age of the individual in years. Must be between 0 and 120."
        )
    ]

    sex: Annotated[
        Literal["male", "female"],
        Field(
            description="Biological sex: 'male' or 'female'."
        )
    ]

    bmi: Annotated[
        float,
        Field(
            ge=10, le=60,
            description="Body Mass Index. Typical values range from 10 to 60."
        )
    ]

    children: Annotated[
        int,
        Field(
            ge=0, le=10,
            description="Number of dependent children. Must be 0–10."
        )
    ]

    smoker: Annotated[
        Literal["yes", "no"],
        Field(
            description="Smoking status: 'yes' or 'no'."
        )
    ]

    region: Annotated[
        Literal["southeast", "southwest", "northeast", "northwest"],
        Field(
            description="Residential region in the US. Must be one of: southeast, southwest, northeast, northwest."
        )
    ]
