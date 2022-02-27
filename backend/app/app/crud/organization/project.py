from sqlalchemy.orm import session
from app.crud.base import CRUDBase
from app.db_models.organization.project import OrganizationProject
from app.models.organization.project import OrganizationProjectCreate, OrganizationProjectUpdate, OrganizationProjectSummary

Organizationproject = CRUDBase[OrganizationProject,
                               OrganizationProjectCreate, OrganizationProjectUpdate](OrganizationProject)


class CRUDOrganizationproject(CRUDBase[OrganizationProject, OrganizationProjectCreate, OrganizationProjectUpdate]):

    def get(self, db: session, id: any) -> OrganizationProjectSummary:
        return db.query(OrganizationProject).filter(OrganizationProject.organization_project_id == id).first()


Organizationproject = CRUDOrganizationproject(OrganizationProject)
