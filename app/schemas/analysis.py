from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field, root_validator, validator

FROM_ANALYSIS_ERROR = 'From date must be before to date.'
TO_ANALYSIS_ERROR = 'To date must be after from analysis.'

FROM_ANALYSIS = (
    datetime.now() - timedelta(minutes=10)
).isoformat(' ', timespec='minutes')
TO_ANALYSIS = (datetime.now().isoformat(' ', timespec='minutes'))


class AnalysisPeriod(BaseModel):
    from_analysis: datetime = Field(..., example=FROM_ANALYSIS)
    to_analysis: datetime = Field(..., example=TO_ANALYSIS)

    @validator('from_analysis')
    def check_from_analysis_lower_than_now(cls, value: datetime):
        if value > datetime.now():
            raise ValueError(FROM_ANALYSIS_ERROR)
        return value

    @root_validator(skip_on_failure=True)
    def check_to_analysis_after_from_analysis(cls, values: dict):
        if values['to_analysis'] <= values['from_analysis']:
            raise ValueError(TO_ANALYSIS_ERROR)
        return values


class AnalysisFilter(BaseModel):
    device_id: Optional[int] = None
    period: Optional[AnalysisPeriod] = None
    user_id: Optional[int] = None


class AnalysisDb(BaseModel):
    min_x: float | None
    min_y: float | None
    min_z: float | None
    max_x: float | None
    max_y: float | None
    max_z: float | None
    count: int | None
    sum_x: float | None
    sum_y: float | None
    sum_z: float | None
    median_x: float | None
    median_y: float | None
    median_z: float | None
