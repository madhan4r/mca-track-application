from fastapi.exceptions import HTTPException
from app.db_models.issue.audit import AuditIssue
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql.expression import label

from app.crud.base import CRUDBase
from app.crud.issue.audit import audit
from app.db_models.issue.issue import Issue
from app.db_models.project.project import Project
from app.db_models.issue.status import IssueStatus
from app.models.issue.issue import IssueCreate, IssueUpdate
from app.models.issue.audit import AuditIssueCreate


class CRUDIssue(CRUDBase[Issue, IssueCreate, IssueUpdate]):

    def get(self, db: Session, id: Any) -> Optional[Issue]:
        return db.query(Issue).filter(Issue.issue_id == id).first()

    def get_by_title(self, db: Session, *, title: str) -> Optional[Issue]:
        return db.query(Issue).filter(Issue.issue_title == title).first()

    def get_issue_count_project_id(self, db: Session, *, project_id: int) -> int:
        return db.query(Issue).filter(Issue.project_id == project_id).count()

    def get_open_issue_count_project_id(self, db: Session, *, project_id: int) -> int:
        return db.query(Issue).filter(Issue.project_id == project_id, Issue.status_id == 1).count()

    def create(self, db: Session, *, obj_in: IssueCreate, created_by: int) -> Issue:
        db_obj = Issue(**obj_in.dict(exclude_unset=True))
        db_obj.created_by = created_by
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Issue, obj_in: Union[IssueUpdate, Dict[str, Any]], created_by: int
    ) -> Issue:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        old_status_id = db_obj.status_id
        old_type_id = db_obj.type_id
        old_assignee_id = db_obj.assigned_to
        issue_data = super().update(db, db_obj=db_obj, obj_in=update_data)
        if update_data.get('status_id', None) and old_status_id != update_data.get('status_id'):
            new_audit = AuditIssueCreate(
                issue_id=update_data.get('issue_id'),
                audit_type='status_change',
                previous_status_id=old_status_id,
                updated_status_id=update_data.get('status_id')
            )
            audit.create(
                db=db,
                obj_in=new_audit,
                created_by=created_by
            )
        if update_data.get('type_id', None) and old_type_id != update_data.get('type_id'):
            new_audit = AuditIssueCreate(
                issue_id=update_data.get('issue_id'),
                audit_type='type_change',
                previous_type_id=old_type_id,
                updated_type_id=update_data.get('type_id')
            )
            audit.create(
                db=db,
                obj_in=new_audit,
                created_by=created_by
            )
        if update_data.get('assigned_to', None) and old_assignee_id != update_data.get('assigned_to'):
            new_audit = AuditIssueCreate(
                issue_id=update_data.get('issue_id'),
                audit_type='assignee_change',
                previous_assignee_id=old_assignee_id,
                updated_assignee_id=update_data.get('assigned_to')
            )
            audit.create(
                db=db,
                obj_in=new_audit,
                created_by=created_by
            )
        return issue_data

    def delete(self, db: Session, id: Any):
        audit_issue = db.query(AuditIssue).filter(AuditIssue.issue_id == id).first()

        if audit_issue is None:
            super().remove(db, id=id)
            return "Requested issue has been deleted"
        else:
            raise HTTPException(
                status_code=400,

                detail="Requested issue id exist in another table",
            )

    def get_issue_count_by_status(self, db: Session):
        return db.query(Issue.status_id,
                        IssueStatus.status,
                        label('count', func.count('*'))
                        ).join(IssueStatus).group_by(Issue.status_id,
                                                     IssueStatus.status).order_by(Issue.status_id).all()

    def get_issue_count_by_project(self, db: Session):
        return db.query(Issue.project_id,
                        Project.project_name,
                        label('count', func.count('*'))
                        ).join(Project).group_by(Issue.project_id,
                                                 Project.project_name,).order_by(Issue.project_id).all()

    def get_detailed_issues_count(self, db: Session):
        return db.query(Issue.project_id,
                        Project.project_name,
                        Issue.status_id,
                        IssueStatus.status,
                        label('count', func.count('*'))
                        ).join(IssueStatus,
                               Project).group_by(Issue.project_id,
                                                 Project.project_name,
                                                 Issue.status_id,
                                                 IssueStatus.status).order_by(Issue.project_id).all()

    def get_issue_with_title(self, db: Session):
        project = db.query(Issue.project_id, Project.project_name,
                           IssueStatus.status, Issue.issue_title,
                           Issue.issue_id).join(IssueStatus,
                                                Project).group_by(Issue.project_id, Project.project_name,
                                                                  IssueStatus.status, IssueStatus.issue_status_id,
                                                                  Issue.issue_id, Issue.issue_title).order_by(Issue.project_id).all()

        list = []
        for val in project:
            if val[2] == "Completed" or val[2] == 'Open' or val[2] == 'WIP':
                list.append(val)
        project_id_set, status_set = set(
            [list[0] for list in list]), set(list[2] for list in list)
        issue_list = []
        for value in sorted(project_id_set):
            for values in sorted(status_set):
                this_group = [value]
                title_list = []
                for lists in list:
                    if lists[0] == value and lists[2] == values:
                        string = str(lists[4])+" - "+lists[3]
                        title_list.append(string)
                        project_name = lists[1]
                this_group.append(values)
                if title_list == []:
                    this_group.append(0)
                else:
                    str1 = ', '.join(title_list)
                    this_group.append(str1)
                this_group.insert(1, project_name)
                issue_list.append(this_group)
        res = {}
        list2 = ["PROJECT ID", "PROJECT NAME", "STATUS", "ISSUE TITLE"]
        result = []
        for val in range(0, len(issue_list)):
            for key in list2:
                for value in issue_list[val]:
                    res[key] = value
                    issue_list[val].remove(value)
                    break
            result.append(res)
            res = {}

        return result


issue = CRUDIssue(Issue)
