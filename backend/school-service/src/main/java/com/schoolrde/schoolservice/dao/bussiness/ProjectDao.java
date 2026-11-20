package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;

import com.schoolrde.schoolservice.entity.ProjectEntity;

public interface ProjectDao{
	
    ProjectEntity saveProject(ProjectEntity project);

    List<ProjectEntity> findProjectByIssueId(Integer issueId);

    Optional<ProjectEntity> findProjectById(Integer id);

}
