from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.db.models import Task, User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
        task_in: TaskCreate,
        session: AsyncSession = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)
) -> Any:
    task = Task(
        title=task_in.title,
        description=task_in.description,
        completed=task_in.completed,
        owner_id=current_user.id
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@router.get("", response_model=List[TaskResponse])
async def read_tasks(
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)
) -> Any:
    stmt = select(Task).where(Task.owner_id == current_user.id).offset(skip).limit(limit)
    result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
        task_id: int,
        task_in: TaskUpdate,
        session: AsyncSession = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)
) -> Any:
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="This task does not belong to you.")

    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


from fastapi import Response


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_task(
        task_id: int,
        session: AsyncSession = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)
) -> None:
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="This task does not belong to you.")

    await session.delete(task)
    await session.commit()
    return None
