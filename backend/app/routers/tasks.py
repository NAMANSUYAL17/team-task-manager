from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import Task, ProjectMember, TaskStatus
from ..schemas import TaskCreate, TaskUpdate, TaskOut
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("/")
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == task.project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not a project member")

    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/")
def get_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    memberships = db.query(ProjectMember).filter(
        ProjectMember.user_id == current_user.id
    ).all()
    project_ids = [m.project_id for m in memberships]
    tasks = db.query(Task).filter(Task.project_id.in_(project_ids)).all()
    return tasks


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    memberships = db.query(ProjectMember).filter(
        ProjectMember.user_id == current_user.id
    ).all()
    project_ids = [m.project_id for m in memberships]
    all_tasks = db.query(Task).filter(Task.project_id.in_(project_ids)).all()
    now = datetime.utcnow()

    return {
        "total": len(all_tasks),
        "todo": len([t for t in all_tasks if t.status == TaskStatus.todo]),
        "in_progress": len([t for t in all_tasks if t.status == TaskStatus.in_progress]),
        "done": len([t for t in all_tasks if t.status == TaskStatus.done]),
        "overdue": len([t for t in all_tasks if t.due_date and t.due_date < now and t.status != TaskStatus.done])
    }


@router.patch("/{task_id}/status")
def update_status(task_id: int, status: TaskStatus, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = status
    db.commit()
    db.refresh(task)
    return task


@router.patch("/{task_id}")
def update_task(task_id: int, updates: TaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}