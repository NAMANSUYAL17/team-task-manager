from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Project, ProjectMember, UserRole
from ..schemas import ProjectCreate, ProjectOut, MemberAdd
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("/")
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_project = Project(
        name=project.name,
        description=project.description,
        owner_id=current_user.id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    # Auto-add creator as admin member
    membership = ProjectMember(
        user_id=current_user.id,
        project_id=new_project.id,
        role=UserRole.admin
    )
    db.add(membership)
    db.commit()

    return new_project


@router.get("/")
def get_projects(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    memberships = db.query(ProjectMember).filter(
        ProjectMember.user_id == current_user.id
    ).all()
    project_ids = [m.project_id for m in memberships]
    projects = db.query(Project).filter(Project.id.in_(project_ids)).all()
    return projects


@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/{project_id}/members")
def add_member(project_id: int, member: MemberAdd, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Only admin can add members
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
        ProjectMember.role == UserRole.admin
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Only admins can add members")

    existing = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == member.user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already a member")

    new_member = ProjectMember(
        user_id=member.user_id,
        project_id=project_id,
        role=member.role
    )
    db.add(new_member)
    db.commit()
    return {"message": "Member added successfully"}


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not owner")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}