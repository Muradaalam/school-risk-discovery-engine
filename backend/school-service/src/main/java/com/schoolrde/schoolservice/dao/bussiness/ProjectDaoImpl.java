package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Repository;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.schoolrde.schoolservice.dao.repository.ProjectRepository;
import com.schoolrde.schoolservice.entity.ProjectEntity;
import com.schoolrde.schoolservice.util.JsonUtility;

@Repository
public class ProjectDaoImpl implements ProjectDao{

    private static final Logger LOGGER = LoggerFactory.getLogger(ProjectDaoImpl.class);

    private final ProjectRepository projectRepository;

    public ProjectDaoImpl(ProjectRepository projectRepository){
        this.projectRepository=projectRepository;
    }

    @Override
    public List<ProjectEntity> findProjectByIssueId(Integer issueId){
        LOGGER.info("Quering project from database with issueId : {}", issueId);
        return projectRepository.findByIssueId(issueId);
    }

    @Override
    public Optional<ProjectEntity> findProjectById(Integer id){
        LOGGER.info("Quering project from database with id : {}", id);
        return projectRepository.findById(id);
    }

    @Override
    public ProjectEntity saveProject(ProjectEntity projectEntity){
        LOGGER.info("project to be saved into DB : {}", JsonUtility.toJson(projectEntity));
        ProjectEntity savedProjectEntity=projectRepository.save(projectEntity);
        LOGGER.info("project saved successfully : {}", JsonUtility.toJson(savedProjectEntity));
        return savedProjectEntity;
    }

}
